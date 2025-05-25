from sqlalchemy.orm import Session
import base64
import json
from pathlib import Path
from typing import Any

from src.db.session import SessionLocal, engine
from src.db.models.base import Base
from src.db.models.password import Password
from src.db.models.meta import Meta
from src.crypto import CryptoHandler

class PassKeyException(Exception):
    pass

class PasswordDatabase:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.db: Session = SessionLocal()
        self.crypto: CryptoHandler = None

    def is_initialized(self) -> bool:
        return self.db.query(Meta).count() > 0

    def start(self, master_key: str) -> None:
        if self.is_initialized():
            meta: Meta = self.db.query(Meta).first()
            self.crypto = CryptoHandler.from_existing(master_key, meta.salt, meta.kdf_iter)

            try:
                if self.crypto.decrypt(meta.verify_token) != "VERIFY":
                    raise PassKeyException("Invalid password")
            except Exception as e:
                raise PassKeyException("Invalid password or corrupted data")
        else:
            self.crypto, salt, iter, verify_token = CryptoHandler.create_new(master_key)
        
            meta: Meta = Meta(
                salt=salt,
                kdf_iter=iter,
                verify_token=verify_token
            )

            self.db.add(meta)
            self.db.commit()
            self.db.refresh(meta)

    def end(self) -> None:
        self.crypto.key = None
        self.crypto = None

    def write_meta(self, salt: bytes, kdf_iter: int, verify_token: bytes) -> None:
        self.db.add(Meta(
            salt=salt,
            kdf_iter=kdf_iter,
            verify_token=verify_token
        ))
        self.db.commit()

    def load_meta(self) -> tuple[bytes, int, bytes]:
        meta: Meta = self.db.query(Meta).first()
        return meta.salt, meta.kdf_iter, meta.verify_token

    def add_password(self, name: str, login: str, password: str) -> int:
        new_password = Password(
            name=name,
            login=login,
            password=self.crypto.encrypt(password)
        )
        
        self.db.add(new_password)
        self.db.commit()
        self.db.refresh(new_password)

        return new_password.id

    def get_all_record_names(self) -> list[dict]:
        result: list[dict] = []
        
        for password_record in self.db.query(Password).all():
            result.append(
                {"id": password_record.id, "name": password_record.name}
            )

        return result
    
    def show_record(self, record_id: int) -> tuple[str, str]:
        record: Password = self.db.query(Password).filter(Password.id == record_id).first()

        return record.login, self.crypto.decrypt(record.password)

    def delete_password(self, record_id: int) -> None:
        record: Password = self.db.query(Password).filter(Password.id == record_id).first()

        self.db.delete(record)
        self.db.commit()

    def record_exists(self, name: str, login: str) -> bool:
        return self.db.query(Password).filter(Password.name == name, Password.login == login).count() > 0

    def update_password(self, record_id: int, login: str, password: str):
        record: Password = self.db.query(Password).filter(Password.id == record_id).first()

        record.login = login
        record.password = self.crypto.encrypt(password)

        self.db.commit()
        self.db.refresh(record)

    def find_by_name(self, name: str) -> list[str]:
        records = self.db.query(Password).filter(Password.name.ilike(f"%{name}%")).all()
        
        return [
            {
                "id": r.id,
                "name": r.name
            }
            for r in records
        ]
    
    def import_db(self, path: Path, key: str) -> int:
        with open(path, "rb") as f:
            magic = f.read(3)
            if magic != b"PW!":
                raise ValueError("Not valid .pwddb")
            raw_json = f.read()

        try:
            data = json.loads(raw_json)
        except Exception:
            raise ValueError("Invalid or corrupted .pwddb file")

        try:
            salt = base64.b64decode(data["meta"]["salt"])
            kdf_iter = data["meta"]["kdf_iter"]
            verify_token = base64.b64decode(data["meta"]["verify_token"])
            encrypted_data = base64.b64decode(data["entries"])

            imported_crypto: CryptoHandler = CryptoHandler.from_existing(
                key, salt, kdf_iter
            )

            if imported_crypto.decrypt(verify_token) != "VERIFY":
                raise ValueError("Wrong key")

            json_str = imported_crypto.decrypt(encrypted_data)
            entries = json.loads(json_str)

            records_added = 0
            for entry in entries:
                name = entry["name"]
                login = entry["login"]
                password = base64.b64decode(entry["password"])
                password = imported_crypto.decrypt(password)

                if not self.record_exists(name, login):
                    self.add_password(name, login, password)
                    records_added += 1

            return records_added

        except Exception as e:
            raise ValueError(f"Import failed: {e}")
    
    def export_db(self, path: Path, filename: str):
        path = Path(path)
        if not path.exists() or not path.is_dir():
            raise RuntimeError("Export path is empty")
        
        filename = filename if len(filename) > 0 else "export"

        filename += ".pwddb"
        path = path / filename

        salt, kdf_iter, verify_token = self.load_meta()
        entries = self.db.query(Password).all()

        serialized_entries = [
            {
                "name": e.name,
                "login": e.login,
                "password": base64.b64encode(e.password).decode()
            }
            for e in entries
        ]

        entries_json = json.dumps(serialized_entries)
        encrypted_entries = self.crypto.encrypt(entries_json)

        payload = {
            "meta": {
                "salt": base64.b64encode(salt).decode(),
                "kdf_iter": kdf_iter,
                "verify_token": base64.b64encode(verify_token).decode()
            },
            "entries": base64.b64encode(encrypted_entries).decode()
        }

        json_str = json.dumps(payload)

        with open(path, "wb") as f:
            f.write(b"PW!")
            f.write(json_str.encode())
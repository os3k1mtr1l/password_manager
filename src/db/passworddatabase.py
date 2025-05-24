from sqlalchemy.orm import Session

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
            except Exception:
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

    def add_password(self, name: str, login: str, password: str):
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

    def record_exists(self, record_id: int) -> bool:
        return self.db.query(Password).filter(Password.id == record_id).count() > 0

    def update_password(self, record_id: int, name: str, login: str, password: str):
        record: Password = self.db.query(Password).filter(Password.id == record_id).first()

        record.login = login
        record.password = self.crypto.encrypt(password)

        self.db.refresh(record)
        self.db.commit()

    def find_by_name(self, name: str) -> list[str]:
        result: list[str] = []
        
        for password_record in self.db.query(Password).filter(Password.name.ilike(f"{name}%")).all():
            result.append(
                password_record.name
            )

        return result
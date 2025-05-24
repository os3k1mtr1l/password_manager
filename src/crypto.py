import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from src.constants import ITERATIONS

class CryptoHandler:
    def __init__(self, master_key: str, salt: bytes | None):
        self.backend = default_backend()
        self.key = master_key
        self.salt = salt
        
    @classmethod
    def create_new(cls, password: str, iterations: int = ITERATIONS):
        salt = os.urandom(16)
        key = cls._derive_key(password.encode(), salt, iterations)
        instance = cls(key, salt)
        verify_token = instance.encrypt("VERIFY")
        return instance, salt, iterations, verify_token

    @classmethod
    def from_existing(cls, password: str, salt: bytes, iterations: int):
        key = cls._derive_key(password.encode(), salt, iterations)
        return cls(key, salt)

    @staticmethod
    def _derive_key(password: bytes, salt: bytes, iterations: int) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return kdf.derive(password)
    
    def encrypt(self, plain_text: str) -> bytes:
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)
        cipher_text = aesgcm.encrypt(nonce, plain_text.encode(), None)
        return nonce + cipher_text

    def decrypt(self, cipher_data: bytes) -> str:
        aesgcm = AESGCM(self.key)
        nonce = cipher_data[:12]
        cipher_text = cipher_data[12:]
        return aesgcm.decrypt(nonce, cipher_text, None).decode()
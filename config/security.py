import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# Securely pull system master keys
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "7afc93e4d9b6261f9d50a256a482ee123b53b81180b953d6aef88e7d8c1c4f55")
ENCON_MASTER_KEY = AESGCM.generate_key(bit_length=256) # In production, lock this down via AWS KMS or HashiCorp Vault
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityEngine:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def encrypt_sensitive_data(data: str) -> bytes:
        """Applies AES-256-GCM Military Grade Authenticated Encryption."""
        aesgcm = AESGCM(ENCON_MASTER_KEY)
        nonce = os.urandom(12)
        encrypted_data = aesgcm.encrypt(nonce, data.encode(), None)
        return nonce + encrypted_data

    @staticmethod
    def decrypt_sensitive_data(encrypted_blob: bytes) -> str:
        """Decrypts and verifies authentication tags on the payload."""
        aesgcm = AESGCM(ENCON_MASTER_KEY)
        nonce = encrypted_blob[:12]
        ciphertext = encrypted_blob[12:]
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_bytes.decode()

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

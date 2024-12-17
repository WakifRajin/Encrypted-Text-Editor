from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a secure key from the password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def generate_salt() -> bytes:
    """Generates a random salt."""
    return os.urandom(16)

def encrypt_message(message: str, password: str) -> tuple:
    """Encrypts a message using a password."""
    salt = generate_salt()
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return salt, encrypted_message

def decrypt_message(encrypted_message: bytes, password: str, salt: bytes) -> str:
    """Decrypts a message using a password and salt."""
    key = derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

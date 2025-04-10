import json
import base64
from cryptography.fernet import Fernet

def generate_key(master_password: str) -> bytes:
    return base64.urlsafe_b64encode(master_password.encode().ljust(32)[:32])

def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(ciphertext: bytes, key: bytes) -> dict:
    f = Fernet(key)
    return json.loads(f.decrypt(ciphertext).decode())
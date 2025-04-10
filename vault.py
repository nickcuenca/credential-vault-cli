import json
import base64
import string
from cryptography.fernet import Fernet

def generate_key(master_password: str) -> bytes:
    return base64.urlsafe_b64encode(master_password.encode().ljust(32)[:32])

def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(ciphertext: bytes, key: bytes) -> dict:
    f = Fernet(key)
    return json.loads(f.decrypt(ciphertext).decode())

def check_password_strength(password):
    """
    Evaluates password strength based on character types and length.
    Returns one of: 'Weak', 'Medium', 'Strong'
    """
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = sum([has_lower, has_upper, has_digit, has_special])

    if length >= 12 and score == 4:
        return '🟢 Strong'
    elif length >= 8 and score >= 3:
        return '🟡 Medium'
    else:
        return '🔴 Weak'
import json
import base64
import string
import time
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants
LOCK_TIMEOUT = 300  # 5 minutes
LOCK_FILE = ".last_access"
SALT_FILE = "salt.bin"
ITERATIONS = 100_000

# ---------------------
# Key Derivation
# ---------------------

def generate_salt():
    return os.urandom(16)

def load_or_create_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = generate_salt()
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt

def generate_key(master_password: str) -> bytes:
    """
    Derives a strong encryption key from the master password using PBKDF2-HMAC-SHA256 and salt.
    """
    salt = load_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

# ---------------------
# Encryption Functions
# ---------------------

def encrypt_data(data: dict, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(ciphertext: bytes, key: bytes) -> dict:
    f = Fernet(key)
    return json.loads(f.decrypt(ciphertext).decode())

# ---------------------
# Password Strength Check
# ---------------------

def check_password_strength(password):
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

# ---------------------
# Vault Locking
# ---------------------

def update_last_access():
    with open(LOCK_FILE, "w") as f:
        f.write(str(int(time.time())))

def is_vault_locked():
    if not os.path.exists(LOCK_FILE):
        return False
    with open(LOCK_FILE, "r") as f:
        last = int(f.read().strip())
    return (time.time() - last) > LOCK_TIMEOUT

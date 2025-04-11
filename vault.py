from datetime import datetime
import os
import base64
import json
import string
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants
LOCK_TIMEOUT = 300  # 5 minutes
LOCK_FILE = ".last_access"
SALT_FILE = "salt.bin"
ITERATIONS = 100_000
AUDIT_LOG_FILE = "vault_audit.log"

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

# ---------------------
# Vault Audit
# ---------------------

def log_action(action: str, site: str = None, status: str = "SUCCESS", note: str = ""):
    """
    Logs actions performed on the vault with timestamps.

    Args:
        action (str): Action performed (e.g., ADD, GET, DELETE)
        site (str): Site related to the action
        status (str): Status of the action (e.g., SUCCESS, FAILURE)
        note (str): Optional message for context
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    site_part = f" | SITE: {site}" if site else ""
    note_part = f" ({note})" if note else ""
    line = f"{timestamp} ACTION: {action}{site_part} | STATUS: {status}{note_part}\n"

    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
            log.write(line)
    except Exception as e:
        print(f"⚠️ Failed to write to audit log: {e}")

def read_audit_log():
    if not os.path.exists(AUDIT_LOG_FILE):
        return "No audit log entries found."
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as log_file:
            return log_file.read()
    except Exception as e:
        return f"Failed to read audit log: {e}"
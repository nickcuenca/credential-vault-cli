import os
import pyotp

TOTP_FILE = "totp_secret.txt"

def get_or_create_totp_secret():
    if os.path.exists(TOTP_FILE):
        with open(TOTP_FILE, "r") as f:
            return f.read().strip()
    else:
        secret = pyotp.random_base32()
        with open(TOTP_FILE, "w") as f:
            f.write(secret)
        return secret

def verify_totp_code(code, secret):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def get_provisioning_uri(account_name="VaultApp", issuer="Credential Vault CLI"):
    secret = get_or_create_totp_secret()
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=account_name, issuer_name=issuer)
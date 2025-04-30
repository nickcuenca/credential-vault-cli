import os
import pyotp

def get_or_create_totp_secret():
    # Use environment variable instead of file-based secret
    return os.environ["TOTP_SECRET"]

def verify_totp_code(code, secret=None):
    secret = secret or os.environ["TOTP_SECRET"]
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

def get_provisioning_uri(account_name="VaultApp", issuer="Credential Vault CLI", secret=None):
    if not secret:
        secret = get_or_create_totp_secret()
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=account_name, issuer_name=issuer)
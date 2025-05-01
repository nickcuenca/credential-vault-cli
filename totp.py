import os
import pyotp

# File to persist the secret; in CI/tests you can override via TOTP_SECRET_FILE
SECRET_FILE = os.environ.get("TOTP_SECRET_FILE", "totp_secret.txt")

def get_or_create_totp_secret() -> str:
    # 1) env‐override
    env = os.environ.get("TOTP_SECRET")
    if env:
        # make sure the file exists for file-based tests
        if not os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "w") as f:
                f.write(env)
        return env

    # 2) existing on disk?
    if os.path.exists(SECRET_FILE):
        return open(SECRET_FILE, "r").read().strip()

    # 3) generate & persist
    secret = pyotp.random_base32()
    with open(SECRET_FILE, "w") as f:
        f.write(secret)
    return secret

def verify_totp_code(code: str, secret: str = None) -> bool:
    if secret is None:
        secret = get_or_create_totp_secret()
    return pyotp.TOTP(secret).verify(code)

def get_provisioning_uri(account_name: str, issuer_name: str, secret: str = None) -> str:
    if secret is None:
        secret = get_or_create_totp_secret()
    return pyotp.TOTP(secret).provisioning_uri(
        name=account_name,
        issuer_name=issuer_name
    )
from flask import Flask, request, session, send_file
from vault import generate_key, decrypt_data, encrypt_data, update_last_access, is_vault_locked, read_audit_log
from functools import wraps
from totp import verify_totp_code, get_provisioning_uri, get_or_create_totp_secret
import os
import io
import qrcode
import base64
import bcrypt
from datetime import timedelta
from flask import current_app as logger
from flask_cors import CORS


FRONT_ORIGIN = "https://credential-vault-cli.netlify.app"

import time, pyotp          # add to the imports at top

print("[BOOT]  TOTP_SECRET =", os.getenv("TOTP_SECRET", "<missing>"))

app = Flask(__name__)
CORS(
    app,
    origins=[FRONT_ORIGIN],   # 👈 Netlify URL
    supports_credentials=True
)
app.permanent_session_lifetime = timedelta(minutes=10)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
app.config.update(
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_SAMESITE = 'None',
    SESSION_COOKIE_SECURE   = True,   #  ← must be True in production
)

VAULT_FILE = 'vault.json.enc'
MASTER_HASH_FILE = "master.hash"

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'master' not in session or not session.get('2fa_passed'):
            session.clear()
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/qrcode")
def show_qr():
    secret = get_or_create_totp_secret()
    # 3-arg call: account_name, issuer_name, secret
    uri = get_provisioning_uri("VaultUser", "Credential-Vault", secret)

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")



def load_vault_data():
    key = generate_key(session['master'])
    if not os.path.exists(VAULT_FILE):        
        return {}                             

    try:
        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()
        data = decrypt_data(encrypted, key)
    except Exception as exc:
        app.logger.warning("vault decrypt failed: %s", exc)
        raise                                     
    update_last_access()
    return data


@app.route("/", methods=["HEAD", "GET"])
def health():
    return "", 200     # bare-bones OK response

@app.route('/', methods=['POST'])
def login():
    master = request.json.get('master') if request.is_json else request.form.get('master')

    session['2fa_passed'] = False

    if not os.path.exists(MASTER_HASH_FILE):
        # First time setup — hash and save password
        hashed = bcrypt.hashpw(master.encode(), bcrypt.gensalt())
        with open(MASTER_HASH_FILE, 'wb') as f:
            f.write(hashed)
        session.permanent = True        
        session['master'] = master
        return {"status": "2fa_required"}, 200

    with open(MASTER_HASH_FILE, 'rb') as f:
        stored_hash = f.read()

    if not bcrypt.checkpw(master.encode(), stored_hash):
        return {"error": "Incorrect master password"}, 401

    session['master'] = master
    return {"status": "2fa_required"}, 200


@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    if 'master' not in session:
        return {"error": "Unauthorized"}, 401

    code = (request.form.get('code') or request.json.get('code') or '').strip()

    secret   = os.environ["TOTP_SECRET"]
    expected = pyotp.TOTP(secret).now()

    app.logger.info(      # <── Gunicorn will forward this line
        "TOTP-DEBUG | entered=%s expected=%s secret=%s",
        code, expected, secret[:6] + "…",
    )

    if verify_totp_code(code, secret):
        session['2fa_passed'] = True
        return {"status": "ok"}, 200

    return {"error": "Invalid 2FA code"}, 401



@app.route('/reset-vault', methods=['POST'])
@login_required
def reset_vault():
    for file in ['vault.json.enc', 'vault_audit.log', 'salt.bin']:
        if os.path.exists(file):
            os.remove(file)
    return {"status": "authenticated"}, 200


@app.route('/force-reset', methods=['POST'])
def force_reset():
    print("🔥 /force-reset endpoint hit")
    try:
        for file in ['vault.json.enc', 'vault_audit.log', 'salt.bin']:
            if os.path.exists(file):
                os.remove(file)
        try:
            session.clear()  # Optional, wrap to avoid session errors
        except Exception as e:
            print(f"⚠️ Warning: session.clear() failed: {e}")
        return {"message": "Vault reset successfully."}, 200
    except Exception as e:
        print(f"❌ Vault reset failed: {e}")
        return {"error": f"Failed to reset vault: {str(e)}"}, 500



@app.route('/api/credentials', methods=['GET'])
@login_required
def api_credentials():
    data = load_vault_data()
    if data is None:
        return {"error": "Vault locked or corrupted."}, 403

    return {"credentials": [
        {"site": site, "username": creds["username"], "password": creds["password"]}
        for site, creds in data.items()
    ]}, 200


@app.route('/add-credential', methods=['POST'])
@login_required
def add_credential():
    data = request.get_json()
    site = data.get("site")
    username = data.get("username")
    password = data.get("password")

    if not site or not username or not password:
        return {"error": "Missing required fields."}, 400

    vault_data = load_vault_data()
    if vault_data is None:
        return {"error": "Vault is locked or invalid."}, 403

    vault_data[site] = {"username": username, "password": password}
    key = generate_key(session['master'])

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypt_data(vault_data, key))

    update_last_access()
    return {"message": f"Credential for '{site}' added."}, 200


@app.route('/delete/<site>', methods=['POST'])
@login_required
def delete_site(site):
    try:
        key = generate_key(session['master'])

        # Load current vault data
        with open(VAULT_FILE, "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        # Remove the entry if it exists
        if site in data:
            del data[site]

            # Save updated vault
            with open(VAULT_FILE, "wb") as f:
                f.write(encrypt_data(data, key))

            return {"message": f"Deleted credentials for {site}"}, 200
        else:
            return {"error": "Site not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/edit/<site>', methods=['POST'])
@login_required
def edit_site(site):
    try:
        key = generate_key(session['master'])
        new_data = request.json  # expects {"username": "...", "password": "..."}

        # Load existing vault
        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()
        data = decrypt_data(encrypted, key)

        # Update the credential
        if site in data:
            data[site] = {
                "username": new_data.get("username", data[site]["username"]),
                "password": new_data.get("password", data[site]["password"]),
            }

            # Save vault
            with open(VAULT_FILE, "wb") as f:
                f.write(encrypt_data(data, key))

            return {"message": f"Updated {site}"}, 200
        else:
            return {"error": "Site not found"}, 404

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/export', methods=['GET'])
@login_required
def export():
    data = load_vault_data()
    if data is None:
        return {"error": "Vault locked"}, 403

    content = "".join([f"Site: {site}\nUsername: {creds['username']}\nPassword: {creds['password']}\n\n"
                       for site, creds in data.items()])
    return send_file(io.BytesIO(content.encode()), as_attachment=True, download_name='vault_export.txt', mimetype='text/plain')


@app.route('/logout')
def logout():
    session.clear()
    return {"message": "Logged out"}, 200


@app.errorhandler(404)
def not_found(e):
    return {"error": "Not found"}, 404


@app.errorhandler(403)
def forbidden(e):
    return {"error": "Forbidden"}, 403


@app.errorhandler(500)
def internal_error(e):
    return {"error": "Internal server error"}, 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
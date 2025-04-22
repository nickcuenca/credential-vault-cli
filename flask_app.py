from flask import Flask, render_template, request, redirect, session, url_for, flash, Response, send_file
from vault import generate_key, decrypt_data, encrypt_data, update_last_access, is_vault_locked, read_audit_log
from functools import wraps
from totp import verify_totp_code, get_provisioning_uri, get_or_create_totp_secret
import os
import qrcode
import base64
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace in production

VAULT_FILE = 'vault.json.enc'
TOTP_SECRET = get_or_create_totp_secret()

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'master' not in session or not session.get('2fa_passed'):
            flash("Please log in and verify 2FA.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
    
def load_vault_data():
    try:
        key = generate_key(session['master'])
        with open(VAULT_FILE, "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            flash("Vault session expired. Please log in again.", "warning")
            return None

        update_last_access()
        return data

    except ValueError:
        flash("❌ Incorrect master password or corrupted vault.", "danger")
        session.clear()
        return None
    except Exception as e:
        flash(f"Unexpected error: {e}", "danger")
        session.clear()
        return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        master = request.form['master']
        session['master'] = master

        # Validate password right away
        try:
            key = generate_key(master)
            with open(VAULT_FILE, "rb") as f:
                encrypted_data = f.read()
            decrypt_data(encrypted_data, key)
        except Exception:
            flash("Incorrect master password.", "danger")
            return render_template('login.html')

        update_last_access()
        return redirect(url_for('verify_2fa'))  # 🔐 go to TOTP
    return render_template('login.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/reset-vault', methods=['POST'])
@login_required
def reset_vault():
    try:
        for file in ['vault.json.enc', 'vault_audit.log', 'salt.bin']:
            if os.path.exists(file):
                os.remove(file)
        flash("✅ Vault and logs deleted successfully.", "success")
    except Exception as e:
        flash(f"❌ Error resetting vault: {e}", "danger")
    return redirect(url_for('dashboard'))


@app.route('/rotate-key', methods=['POST'])
@login_required
def rotate_key():
    current = request.form['current']
    new = request.form['new']

    try:
        old_key = generate_key(current)
        with open(VAULT_FILE, "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, old_key)

        # Overwrite salt and re-derive key from new password
        if os.path.exists("salt.bin"):
            os.remove("salt.bin")
        new_key = generate_key(new)

        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, new_key))

        session['master'] = new
        flash("🔐 Master password and key updated successfully.", "success")
    except Exception as e:
        flash(f"❌ Key rotation failed: {e}", "danger")

    return redirect(url_for('settings'))

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'master' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form['code']
        if verify_totp_code(code, TOTP_SECRET):
            session['2fa_passed'] = True
            flash("✅ 2FA Verified!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid 2FA code.", "danger")

    return render_template('verify_2fa.html')

@app.route('/qrcode')
def show_qr():
    import qrcode
    import base64
    from io import BytesIO

    uri = get_provisioning_uri("VaultUser", TOTP_SECRET)
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template('qrcode.html', qr=qr_b64)


@app.route('/dashboard')
@login_required
def dashboard():
    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))
    return render_template("dashboard.html", credentials=data)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = request.form['password']

        data = load_vault_data()
        if data is None:
            return redirect(url_for('logout'))

        key = generate_key(session['master'])
        data[site] = {"username": username, "password": password}
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, key))

        flash(f"Credentials for '{site}' added!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add.html')

@app.route('/edit/<site>', methods=['GET', 'POST'])
@login_required
def edit(site):
    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    key = generate_key(session['master'])

    if request.method == 'POST':
        data[site] = {
            "username": request.form['username'],
            "password": request.form['password']
        }
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, key))
        flash(f"Updated credentials for {site}.", "success")
        return redirect(url_for('dashboard'))

    creds = data.get(site)
    if not creds:
        flash(f"No credentials found for {site}", "danger")
        return redirect(url_for('dashboard'))

    return render_template('edit.html', site=site, creds=creds)

@app.route('/delete/<site>', methods=['POST'])
@login_required
def delete(site):
    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    key = generate_key(session['master'])

    if site in data:
        del data[site]
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, key))
        flash(f"Deleted {site}.", "info")
    else:
        flash(f"{site} not found.", "warning")
    return redirect(url_for('dashboard'))

@app.route('/export')
@login_required
def export():
    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    export_content = ""
    for site, creds in data.items():
        export_content += f"Site: {site}\nUsername: {creds['username']}\nPassword: {creds['password']}\n\n"

    return send_file(
        io.BytesIO(export_content.encode('utf-8')),
        as_attachment=True,
        download_name='vault_export.txt',
        mimetype='text/plain'
    )

@app.route('/audit')
@login_required
def audit():
    try:
        log = read_audit_log()
        return render_template('audit.html', log=log)
    except Exception as e:
        flash(f"Error reading audit log: {e}", "danger")
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(500)
def internal_error(e):
    flash("An internal error occurred.", "danger")
    return render_template("errors/500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)

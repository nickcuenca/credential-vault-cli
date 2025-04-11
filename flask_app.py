from flask import Flask, render_template, request, redirect, session, url_for, flash, Response, send_file
from vault import generate_key, decrypt_data, encrypt_data, update_last_access, is_vault_locked
from functools import wraps
import os
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key in production

VAULT_FILE = 'vault.json.enc'

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
        session.pop('master', None)
        return None

    except Exception as e:
        flash(f"Unexpected error: {e}", "danger")
        session.pop('master', None)
        return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        master = request.form['master']
        session['master'] = master
        update_last_access()
        return redirect(url_for('dashboard'))
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'master' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/dashboard')
@login_required
def dashboard():
    if 'master' not in session:
        return redirect(url_for('login'))

    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    return render_template("dashboard.html", credentials=data)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if 'master' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = request.form['password']

        data = load_vault_data()
        if data is None:
            return redirect(url_for('logout'))

        key = generate_key(session['master'])
        data[site] = {
            "username": username,
            "password": password
        }

        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, key))

        flash(f"Credentials for '{site}' added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add.html')

@app.route('/edit/<site>', methods=['GET', 'POST'])
@login_required
def edit(site):
    if 'master' not in session:
        return redirect(url_for('login'))

    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    key = generate_key(session['master'])

    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        data[site] = {
            "username": new_username,
            "password": new_password
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
    if 'master' not in session:
        return redirect(url_for('login'))

    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    key = generate_key(session['master'])

    if site in data:
        del data[site]
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypt_data(data, key))
        flash(f"Deleted credentials for {site}.", "info")
    else:
        flash(f"Site '{site}' not found in vault.", "warning")

    return redirect(url_for('dashboard'))

@app.route('/export')
@login_required
def export():
    if 'master' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    data = load_vault_data()
    if data is None:
        return redirect(url_for('logout'))

    export_content = ""
    for site, creds in data.items():
        export_content += f"Site: {site}\n"
        export_content += f"  Username: {creds['username']}\n"
        export_content += f"  Password: {creds['password']}\n\n"

    return send_file(
        io.BytesIO(export_content.encode('utf-8')),
        as_attachment=True,
        download_name='vault_export.txt',
        mimetype='text/plain'
    )

@app.route('/logout')
def logout():
    session.pop('master', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/audit')
@login_required
def audit():
    if 'master' not in session:
        return redirect(url_for('login'))

    try:
        from vault import read_audit_log
        log = read_audit_log()
        return render_template('audit.html', log=log)
    except Exception as e:
        flash(f"Error reading audit log: {e}", "danger")
        return redirect(url_for('dashboard'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(500)
def internal_error(e):
    flash("An internal error occurred. Please try again.", "danger")
    return render_template("errors/500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)

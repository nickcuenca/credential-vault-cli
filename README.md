# 🔐 Credential Vault CLI + Flask GUI

![Python Tests](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/python-tests.yml/badge.svg)

A secure, offline password manager built with Python.  
Features a robust **command-line interface** (CLI) and a sleek **Flask-powered web GUI**.

---

## 💪 Features

- 🔑 **Master Password Protected** – Never stored, derived using PBKDF2-HMAC-SHA256
- 🧊 **AES-256 Encryption** – All credentials stored securely in `vault.json.enc`
- ⏲️ **Session Timeout** – Auto-locks after 5 minutes of inactivity
- 🧠 **Password Strength Meter** – Real-time feedback (Strong / Medium / Weak)
- 📋 **Clipboard Copying** – One-click password copy (GUI)
- 🔎 **Search Bar** – Fuzzy search for credentials by site name
- 🗂️ **Add / Edit / Delete** – Fully supported in both CLI and GUI
- 📤 **Export** – Download credentials to plaintext file (manual backup)
- 📜 **Audit Logging** – All sensitive operations are tracked
- 🧪 **Unit Tested** – Secure and reliable core logic with Python's `unittest`
- 🌐 **Web GUI** – User-friendly interface built with Flask + JavaScript

---

## 🚀 Getting Started

### 🔧 Setup

```bash
git clone https://github.com/nickcuenca/credential-vault-cli.git
cd credential-vault-cli

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🖥️ CLI Usage

```bash
python cli.py init        # Initialize your vault
python cli.py add         # Add new credentials
python cli.py list        # List all saved sites
python cli.py get         # View credentials for a site
python cli.py delete      # Delete credentials
python cli.py edit        # Edit credentials
python cli.py search      # Search by site
python cli.py export      # Export to plaintext
python cli.py generate    # Generate a random secure password
python cli.py audit       # View the audit log
```

---

## 🌐 GUI Usage

```bash
python flask_app.py
```

Then visit `http://127.0.0.1:5000` in your browser.

**Web Features:**

- 🔐 Login with master password
- ✅ Add/Edit/Delete credentials
- 🧠 Password strength feedback
- 📋 Copy passwords with 1 click
- 🔎 Live search filtering
- 📄 Export to text
- 📜 View audit log

---

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

Tests include:
- Key derivation consistency
- Encryption/decryption correctness
- Invalid password rejection
- Password strength scoring

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `cli.py` | Command-line interface logic |
| `vault.py` | Core crypto + vault handling |
| `flask_app.py` | Web app using Flask |
| `templates/` | HTML templates for GUI |
| `tests/` | Unit tests |
| `vault.json.enc` | Encrypted credentials vault |
| `salt.bin` | PBKDF2 salt (keep secret!) |
| `.last_access` | Session timeout tracking |
| `vault_audit.log` | Logs all sensitive operations |
| `.gitignore` | Excludes vault/salt/log files from Git |
| `requirements.txt` | Python dependencies |

---

## 🔐 Security Notes

- Your **master password is never stored** — it only derives the encryption key.
- All data stays **offline on your machine**
- If you forget your master password, there is **no recovery**
- All vault contents are **AES-256 encrypted** and audit-logged

---

## ✨ Author

Made with ❤️ by [Nicolas Cuenca](https://github.com/nickcuenca)

---

## 📌 Disclaimer

This tool is for **educational and personal use only**.  
Do not use it to manage credentials for other individuals or companies.
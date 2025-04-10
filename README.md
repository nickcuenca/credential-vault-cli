# 🔐 Credential Vault CLI Tool

A secure, command-line password manager built in Python.  
Encrypts your credentials with AES-256 using a master password.  
Everything is stored offline — no plaintext, no leaks.

---

## 💪 Features

- **Master Password Encryption** – Your vault is protected using AES-256
- **Add Credentials** – Store site, username, and password securely
- **Retrieve Credentials** – Get your saved credentials using the `get` command
- **Edit Credentials** – Update username or password for an existing entry
- **Password Strength Checker** – Provides feedback on whether a password is 🔴 Weak, 🟡 Medium, or 🟢 Strong
- **Generate Secure Passwords** – Quickly create strong, random passwords
- **Copy to Clipboard** – Instantly copy any password for quick access
- **Export Vault** – Save all credentials into a plaintext file if needed
- **Unit Tested** – Includes tests for encryption logic and password strength
- **Lock Timeout** – Auto-locks the vault after 5 minutes of inactivity
- **Command Line Interface** – Built with `Click` for clean prompts and options

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/nickcuenca/credential-vault-cli.git
cd credential-vault-cli
```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
.
env\Scripts ctivate
pip install -r requirements.txt
```

---

## 📦 Usage

### Initialize the Vault
```bash
python cli.py init
```

### Add Credentials
```bash
python cli.py add
```

### Retrieve Credentials
```bash
python cli.py get
```

### Edit Existing Credentials
```bash
python cli.py edit
```

### List Stored Sites
```bash
python cli.py list
```

### Delete Credentials
```bash
python cli.py delete
```

### Copy Password to Clipboard
```bash
python cli.py copy
```

### Export Vault to TXT (not encrypted)
```bash
python cli.py export
```

### Generate Password
```bash
python cli.py generate
python cli.py generate --length 24 --copy
```

---

## 🧠 Example

```bash
python cli.py add
Master: **************
Site: github.com
Username: nickcuenca
Password: **************
✅ Credentials for 'github.com' added to vault!
🧠 Password Strength: 🟢 Strong
```

```bash
python cli.py get
Master: **************
Site: github.com

🔍 Credentials found:
  👤 Username: nickcuenca
  🔑 Password: SuperSecret123!
```

```bash
python cli.py edit
Master: **************
Site: github.com
New Username [Leave blank to keep existing]: nick_c_updated
New Password [Leave blank to keep existing]: **************
✅ Credentials for 'github.com' updated!
```

---

## 🧪 Unit Testing

This tool includes basic unit tests to ensure cryptographic reliability and password scoring logic.

### Run All Tests

```bash
python -m unittest discover tests
```

### Folder Structure

```
tests/
├── test_password_strength.py   # Checks weak, medium, strong ratings
├── test_vault.py               # Verifies encryption/decryption integrity
├── __init__.py                 # Enables Python test discovery
```

---

## 🔐 Security Notes

- Your master password is **never stored**
- The vault is encrypted using a key derived from your master password
- If you lose the password, **there is no way to recover the data**

---

## 📁 Files

| File | Description |
|------|-------------|
| `cli.py` | Main command-line tool |
| `vault.py` | Handles encryption/decryption, password strength, lock session |
| `vault.json.enc` | Encrypted credentials (auto-generated) |
| `.last_access` | Tracks session lock timeout (ignored in `.gitignore`) |
| `requirements.txt` | Python dependencies |
| `tests/` | Contains unit tests for password logic and encryption |
| `.gitignore` | Prevents vault + virtual env from being committed |

---

## ✨ Credits

Made with 💻 by [Nicolas Cuenca](https://github.com/nickcuenca)

---

## 📌 Disclaimer

This tool is for **personal use or educational purposes only**. Do not use to store or manage other people's data.
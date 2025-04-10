
# 🔐 Credential Vault CLI Tool

A secure, command-line password manager built in Python.  
Encrypts your credentials with AES-256 using a master password.  
Everything is stored offline — no plaintext, no leaks.

---

## 💪 Features

- **Master Password Encryption** – Your vault is protected using AES-256
- **Add Credentials** – Store site, username, and password securely
- **Retrieve Credentials** – Get your saved credentials using the `get` command
- **List Stored Sites** – View a list of saved sites with `list`
- **Delete Credentials** – Remove credentials with `delete`
- **Copy to Clipboard** – Copy password directly to clipboard with `copy`
- **Export Vault** – Decrypt and save your vault as plaintext with `export`
- **Generate Passwords** – Create strong random passwords with `generate`
- **Command Line Interface** – Clean interface powered by `Click`
- **Encrypted Vault File** – Data is saved in `vault.json.enc`, fully encrypted

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

### List All Sites
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

### Export Vault to Plaintext
```bash
python cli.py export
```

### Generate a Secure Password
```bash
python cli.py generate
```

### Custom Length & Clipboard Copy
```bash
python cli.py generate --length 24 --copy
```

```
🔐 Generated Password: A!uF9#k@7T3q)Y$g2LwVz8Bd
📋 Password copied to clipboard!
```

---

## 🧠 Example

```bash
python cli.py add
Master: **************
Site: github.com
Username: nickcuenca
Password: **************
```

```bash
python cli.py get
Master: **************
Site: github.com

🔍 Credentials found:
  👤 Username: nickcuenca
  🔑 Password: SuperSecret123!
```

---

## 🔐 Security Notes

- Your master password is **never stored**
- The vault is encrypted using a key derived from your master password
- If you lose the password, **there is no way to recover the data**
- Use `export` responsibly — the file is **not encrypted**

---

## 📁 Files

| File              | Description                                     |
|-------------------|-------------------------------------------------|
| `cli.py`          | Main command-line interface                     |
| `vault.py`        | Handles encryption/decryption logic             |
| `vault.json.enc`  | Encrypted vault (auto-generated)                |
| `vault_export.txt`| Plaintext export (manually generated)           |
| `test_vault.py`   | Unit tests for core encryption functions        |
| `requirements.txt`| Python dependencies                             |
| `.gitignore`      | Prevents vault and virtualenv from being tracked|

---

## ✨ Credits

Made with 💻 by [Nicolas Cuenca](https://github.com/nickcuenca)

---

## 📌 Disclaimer

This tool is for **personal use or educational purposes only**.  
Do not use to store or manage other people's data.

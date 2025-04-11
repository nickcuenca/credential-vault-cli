# 🔐 Credential Vault CLI Tool

A secure, offline command-line password manager built in Python.  
Encrypts your credentials using PBKDF2-HMAC-SHA256 with AES-256.  
Includes full audit logging, clipboard support, and password strength feedback.

---

## 💪 Features

- **PBKDF2 Key Derivation** – Strong encryption keys derived from your master password + salt
- **AES-256 Encryption** – Vault data is securely encrypted and stored as a single file
- **Session Timeout** – Auto-locks after 5 minutes of inactivity
- **Audit Logging** – Tracks `INIT`, `ADD`, `GET`, `LIST`, `DELETE`, `AUDIT_VIEW`, and failure events
- **Password Strength Indicator** – 🟢 Strong, 🟡 Medium, 🔴 Weak
- **Generate Strong Passwords** – Create random secure passwords instantly
- **Copy to Clipboard** – Quickly copy passwords without displaying them
- **Export Vault** – Save your vault to plaintext if needed (manual backup)
- **Search Functionality** – Fuzzy site search for credentials
- **Command-Line Interface** – Powered by Click for intuitive usage

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/nickcuenca/credential-vault-cli.git
cd credential-vault-cli
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

## 📦 Usage

### Initialize Vault
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

### List Stored Sites
```bash
python cli.py list
```

### Delete Credentials
```bash
python cli.py delete
```

### Edit Credentials
```bash
python cli.py edit
```

### Search Credentials
```bash
python cli.py search
```

### Export Vault
```bash
python cli.py export
```

### Generate Password
```bash
python cli.py generate --length 24 --copy
```

### View Audit Log
```bash
python cli.py audit
```

---

## 🧪 Unit Testing

```bash
python -m unittest discover tests
```

---

## 🔐 Security Notes

- Your **master password is never stored**
- If you lose your master password, there is **no recovery**
- Vault is encrypted using a **key derived from PBKDF2 with salt**
- Everything is stored **offline**, no data ever leaves your machine

---

## 📁 Files

| File | Description |
|------|-------------|
| `cli.py` | Main command-line tool |
| `vault.py` | Handles encryption, decryption, strength scoring, and auditing |
| `audit.log` | Timestamped action log |
| `vault.json.enc` | Encrypted vault |
| `salt.bin` | Cryptographic salt (never share this!) |
| `.last_access` | Session lock timer |
| `tests/` | Unit tests for core features |
| `.gitignore` | Ensures vault + virtual env + salt are not committed |
| `requirements.txt` | Python dependencies (Click, cryptography, pyperclip) |

---

## ✨ Credits

Made with 💻 by [Nicolas Cuenca](https://github.com/nickcuenca)

---

## 📌 Disclaimer

This tool is for **personal or educational use only**.  
Do not use it to manage others' sensitive data.
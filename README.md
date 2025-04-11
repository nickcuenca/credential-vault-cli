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
- **Search by Site** – Find credentials with partial site matches
- **Password Strength Checker** – Feedback on whether a password is 🔴 Weak, 🟡 Medium, or 🟢 Strong
- **Generate Secure Passwords** – Quickly create strong, random passwords
- **Copy to Clipboard** – Instantly copy any password for quick access
- **Export Vault** – Save all credentials into a plaintext file if needed
- **Lock Timeout** – Auto-locks the vault after 5 minutes of inactivity
- **Session-Aware Authentication** – Vault remains unlocked temporarily after successful use
- **Unit Tested** – Includes tests for encryption logic and password strength
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

### Search Sites by Keyword

```bash
python cli.py search
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
python cli.py search
Master: **************
Search query: git

🔍 Matching Results:
  🌐 Site: github.com
     👤 Username: nickcuenca
     🔑 Password: SuperSecret123!
```

---

## 🧪 Unit Testing

```bash
python -m unittest discover tests
```

---

## 🔐 Security Notes

- Your master password is **never stored**
- If you lose the password, **there is no way to recover the data**

---

## 📁 Files

| File | Description |
|------|-------------|
| `cli.py` | Command-line interface |
| `vault.py` | Core encryption + logic |
| `.last_access` | Tracks session access time |
| `vault.json.enc` | Encrypted vault |
| `tests/` | Unit tests |
| `.gitignore` | Ensures vault and session files are not committed |

---

## ✨ Credits

Made with 💻 by [Nicolas Cuenca](https://github.com/nickcuenca)
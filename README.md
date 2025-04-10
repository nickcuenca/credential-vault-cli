# 🔐 Credential Vault CLI Tool

A secure, command-line password manager built in Python.  
Encrypts your credentials with AES-256 using a master password.  
Everything is stored offline — no plaintext, no leaks.

---

## 💪 Features

- **Master Password Encryption** – Your vault is protected using AES-256
- **Add Credentials** – Store site, username, and password securely
- **Retrieve Credentials** – Get your saved credentials using the `get` command
- **Command Line Interface** – Built with `Click` for clean prompts and options
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
.\venv\Scripts\activate
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

---

## 📁 Files

| File | Description |
|------|-------------|
| `cli.py` | Main command-line tool |
| `vault.py` | Handles encryption/decryption logic |
| `vault.json.enc` | Encrypted credentials (auto-generated) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Prevents vault + virtual env from being committed |

---

## ✨ Credits

Made with 💻 by [Nicolas Cuenca](https://github.com/nickcuenca)

---

## 📌 Disclaimer

This tool is for **personal use or educational purposes only**. Do not use to store or manage other people's data.
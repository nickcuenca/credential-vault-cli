# 🔐 Credential Vault CLI + Flask GUI
![Python Tests](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/python-tests.yml/badge.svg)
![Build](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/python-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/nickcuenca/credential-vault-cli)
![Framework](https://img.shields.io/badge/Flask-Web_App_Framework-red)
![Offline](https://img.shields.io/badge/Secure-Offline-brightgreen)
[![codecov](https://codecov.io/gh/nickcuenca/credential-vault-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/nickcuenca/credential-vault-cli)

A secure, offline password manager with a sleek Bootstrap-powered web interface.  
Supports AES-256 encryption, audit logging, clipboard copy, password strength scoring, and more.

---

## 💻 Features

- **Modern Flask + Bootstrap UI**
- **AES-256 Encrypted Vault** (PBKDF2-HMAC-SHA256)
- **Password Strength Meter** (Live scoring via JavaScript)
- **Clipboard Copy**
- **Audit Log Viewer**
- **Search, Add, Edit, Delete Credentials**
- **Dark/Light Mode Toggle**
- **Session Timeout Auto-lock**
- **Export Vault as TXT**
- **404 Error Handling + Clean Routing**

---

## 🚀 Getting Started

```bash
git clone https://github.com/nickcuenca/credential-vault-cli.git
cd credential-vault-cli
python -m venv venv
venv\Scripts\activate    # or source venv/bin/activate
pip install -r requirements.txt
python flask_app.py
```

---

## 🧪 Unit Testing

```bash
python -m unittest discover tests
```

---

## 📁 Project Structure

| File/Folder         | Purpose                                      |
|---------------------|----------------------------------------------|
| `vault.py`          | Encryption logic, audit logging, vault ops   |
| `cli.py`            | CLI entry point (optional)                   |
| `flask_app.py`      | Web GUI app                                  |
| `templates/`        | Bootstrap HTML views                         |
| `tests/`            | Unit tests                                   |
| `vault.json.enc`    | Encrypted vault (autogenerated)              |
| `salt.bin`          | Salt for PBKDF2-HMAC                         |
| `vault_audit.log`   | Secure action logging                        |

---

## 🔐 Security

- Your **master password is never stored**
- Vault uses **PBKDF2-HMAC-SHA256** with **AES-256**
- Session timeout: 5 min inactivity = auto-lock
- Everything stored **offline**, nothing leaves your machine

---

## ✨ Credits

Created by **Nicolas Cuenca**  
Made for SWE / IT / Cyber / Air Force 17X prep 🌍

---

## 📌 Disclaimer

This tool is for **educational and personal use only.**  
Do not use for managing sensitive real-world passwords.
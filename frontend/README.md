# 🔐 Credential Vault CLI

[![CI](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/ci.yml)
[![Frontend Tests](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/nickcuenca/credential-vault-cli/actions/workflows/frontend-ci.yml)
[![Codecov](https://codecov.io/gh/nickcuenca/credential-vault-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/nickcuenca/credential-vault-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://github.com/nickcuenca/credential-vault-cli/blob/main/LICENSE)

A full‐stack password manager built with **Flask + React**.  
Users can securely **store, edit, delete, and export credentials**, protected by a **master password** and **TOTP‑based 2‑Factor Authentication**.

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Auth** | 🔑 First‑time master‑password setup <br> 🔐 TOTP 2FA via Google Authenticator/Authy |
| **Vault** | AES‑256 encrypted `vault.json.enc` <br> Add / edit / delete credentials <br> Export vault as plaintext backup |
| **UI** | React 18 SPA (Vite) <br> Dark / light mode <br> Password strength meter + generator |
| **Security** | PBKDF2‐SHA256 ✕ 200 000 iterations <br> Session cookies: HttpOnly, Secure, SameSite=None |
| **Maintenance** | 🔄 Force‑reset endpoint <br> Audit trail logging |

---

## 🗂️ Tech Stack

* **Backend** – Flask 3, Gunicorn, Flask‑CORS, pyotp, cryptography  
* **Frontend** – React 18, Axios, zxcvbn, Vite  
* **Deployment** – Render (Flask) ∙ Netlify (React)  
* **Testing & CI** – pytest, unittest, Jest, GitHub Actions, Codecov

---

## 🚀 Quick Start (Local)

```bash
# Clone & enter project
git clone https://github.com/nickcuenca/credential-vault-cli.git
cd credential-vault-cli

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
export TOTP_SECRET=$(python - <<'PY'
import pyotp;print(pyotp.random_base32())
PY)
python flask_app.py

# In a second terminal, run Frontend
cd ../frontend
npm install
npm run dev  # http://localhost:5173
```

> 📱 Scan the QR code with an authenticator after login; first password becomes master password.

---

## 🔧 Environment Variables

| Service | Variable             | Description                             |
|---------|----------------------|-----------------------------------------|
| Backend | `FLASK_SECRET_KEY`   | Flask session secret key               |
| Backend | `TOTP_SECRET`        | Base32 TOTP secret for 2FA             |
| Frontend| `REACT_APP_API`      | URL of backend API (e.g. Render URL)   |

---

## 🏗️ Deployment

### Back‑end on Render

1. Create new Python service, point to `backend/flask_app.py`.  
2. Build & start command:
   ```bash
   pip install -r requirements.txt
   gunicorn --log-level info --capture-output flask_app:app
   ```
3. Set env vars and deploy.

### Front‑end on Netlify

1. Connect repo, set build command: `npm run build`, publish dir: `frontend/dist`.  
2. Set `REACT_APP_API` env var to backend URL.  
3. Deploy.

---

## 🛡️ Security Notes

* Encryption key derived via PBKDF2 from master password + salt.
* TOTP allows ±30 s drift (`valid_window=1`).
* Cookies set as `HttpOnly`, `Secure`, `SameSite=None`.

---

## 📜 License

MIT © 2025 Nicolas Cuenca
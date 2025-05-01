# 🔐 Credential Vault CLI

A full‑stack password manager built with **Flask + React**.  
Users can securely **store, edit, delete, and export credentials**, protected by a **master password** and **TOTP‑based 2‑Factor Authentication**.

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Auth** | 🔑 First‑time master‑password setup <br> 🔐 TOTP 2‑factor using Google Authenticator/Authy |
| **Vault** | AES‑256 encrypted `vault.json.enc` on the server <br> Add / edit / delete credentials <br> Export vault as plaintext backup |
| **UI** | React (Vite) SPA <br> Dark / light mode <br> Password strength meter + generator |
| **Security** | PBKDF2‑derived key, per‑user salt <br> Session cookies set **HttpOnly + Secure + SameSite=None** |
| **Maintenance** | 🔄 Force‑reset endpoint <br> Audit trail (optional) |

---

## 🗂️ Tech Stack

* **Frontend** – React 18, Axios, zxcvbn, Vite  
* **Backend**  – Flask 3, Gunicorn, Flask‑CORS, pyotp, cryptography  
* **Deployment** – **Render** (Flask)   |   **Netlify** (React)

---

## 🚀 Quick Start (local)

```bash
# 1. Clone & enter project
git clone https://github.com/<your‑user>/credential-vault-cli.git
cd credential-vault-cli

# 2. Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY=$(python -c "import secrets,base64;print(secrets.token_urlsafe(32))")
export TOTP_SECRET=$(python - <<'PY'
import pyotp,os;print(pyotp.random_base32())
PY)
python flask_app.py
```

In a **second terminal**:

```bash
# 3. Frontend
cd frontend
npm install
npm run dev          # http://localhost:5173
```

> 📱 Scan the QR code shown after login with Google Authenticator.  
> The first password you enter becomes the master password.

---

## 🔧 Environment Variables (production)

| Service  | Key              | Example value                            |
|----------|------------------|------------------------------------------|
| Render   | `FLASK_SECRET_KEY` | *generate a 32‑byte url‑safe secret* |
| Render   | `TOTP_SECRET`    | *pyotp.random_base32()*                 |
| Netlify  | `REACT_APP_API`  | `https://credential-vault-cli.onrender.com` |

---

## 🏗️ Deployment

### Back‑end (Render)

1. **New › Web Service** → **Python 3**.
2. Point to repo & `flask_app.py`; set **Start Command**:

   ```sh
   gunicorn --log-level info --capture-output flask_app:app
   ```

3. Add env vars above → Deploy.

### Front‑end (Netlify)

1. **New Site from Git** → repo root, **build command**: `npm run build`, **publish directory**: `frontend/dist`.
2. Add `REACT_APP_API` env var → Deploy.

---

## 🛡️ Security Notes

* The encryption key is never stored – it’s derived from the master password + salt (PBKDF2‑SHA256 ✕ 200 000).
* TOTP codes allow ±30 s drift (`valid_window=1`).
* All cookies are `HttpOnly`, `Secure`, `SameSite=None` – required for cross‑origin front‑end ⇔ back‑end.

---

## 📸 Screenshots

| Login → 2FA | Vault |
|-------------|-------|
| ![Login](docs/login.png) | ![Vault](docs/vault.png) |

---

## 📜 License

MIT © 2025 Nicolas Cuenca

# 🔐 Credential Vault

A full-stack password manager web app built with **Flask** (Python) and **React**. Users can securely store, edit, delete, and export credentials—protected by master password authentication and 2FA using TOTP (e.g., Google Authenticator).

---

## 🚀 Features

- ✅ Master password login with TOTP-based 2FA
- 🔐 AES-encrypted vault file (`vault.json.enc`)
- 🌐 React frontend with:
  - Add, edit, and delete credentials
  - Password strength meter (zxcvbn)
  - Password generator with customizable rules
  - Light/Dark mode toggle
  - Export plaintext credentials (backup)
  - Session-based authentication and logout
- 📋 Copy credentials to clipboard
- 🧨 Reset and force-reset vault buttons
- 🧪 Toast-based UI notifications

---

## 🛠 Tech Stack

- **Frontend:** React (Vite), Axios, zxcvbn
- **Backend:** Flask, Flask-CORS, pyotp, qrcode, cryptography
- **Deployment:** Render (Flask backend) + Netlify (React frontend)

---

## 🧑‍💻 Local Setup

### 1. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

> Requires Python 3.8+ and `pip`.

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

> Open `http://localhost:5173` in your browser.

---

## ⚙️ Environment Notes

- First login sets your master password.
- QR code for 2FA setup is available at `/qrcode`.
- Vault is encrypted and stored locally as `vault.json.enc`.

---

## 🔐 Security Design

- AES encryption using a key derived from the master password
- TOTP-based 2FA with QR provisioning (e.g., Google Authenticator)
- Flask session authentication for protecting backend routes

---

## 📁 File Structure

```
├── backend/
│   ├── app.py              # Flask app and API routes
│   ├── vault.py            # AES encryption/decryption logic
│   ├── totp.py             # TOTP QR generation + verification
│   ├── vault.json.enc      # Encrypted vault (generated at runtime)
│   ├── salt.bin            # Salt used for key derivation
│   ├── vault_audit.log     # Audit logging (optional)
│
├── frontend/
│   ├── src/
│   │   ├── App.css
│   │   ├── Vault.jsx
│   │   ├── AddCredential.jsx
│   │   ├── Login.jsx
│   │   └── main.jsx
│   └── index.html
│
├── README.md
```

---

## 🌐 Deployment

- **Backend (Flask)**: Deployed to [Render](https://render.com)
- **Frontend (React)**: Deployed to [Netlify](https://netlify.com)

---

## 🧑‍🎓 Author

Made with ❤️ by **Nicolas Cuenca**
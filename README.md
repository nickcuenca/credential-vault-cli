# 🔐 Credential Vault

A full-stack password manager web app built with Flask (Python) and React. Users can securely store, edit, delete, and export credentials, protected by master password authentication and 2FA using TOTP (Google Authenticator).

## 🚀 Features

- ✅ Master password login with 2FA (Time-based One-Time Password)
- 🔐 AES-encrypted vault stored locally (`vault.json.enc`)
- 🌐 React frontend with:
  - Add, edit, and delete credentials
  - Password strength meter using `zxcvbn`
  - Password generator with custom options (length, symbols, uppercase, numbers)
  - Light/Dark mode toggle
  - Export credentials as plaintext (for backup)
  - Logout + session management
- 📋 Clipboard copy for generated passwords
- 🧨 Reset and force-reset vault functionality
- 🧪 Toast notifications for clipboard copy and error feedback
- 🎨 Fully responsive UI with theming support

## 🛠 Tech Stack

- **Frontend:** React (Vite), Axios, zxcvbn
- **Backend:** Flask, Flask-CORS, qrcode, base64, cryptography
- **Deployment:** Flask via Render | React via Netlify

## 🧑‍💻 Local Setup

### 1. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

> Ensure you have Python 3.8+ and `pip` installed.

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

> Visit `http://localhost:5173` (or your dev server port).

### 3. Environment Notes

- First login sets the master password.
- After login, visit `/qrcode` to scan with Google Authenticator.
- All data is stored locally encrypted under `vault.json.enc`.

## 🛡 Security Considerations

- All credential data is AES-encrypted using a key derived from the master password.
- TOTP 2FA ensures MFA-level protection using QR and authenticator apps.
- Backend endpoints are protected with Flask session-based auth.

## 📂 File Structure

```
├── backend
│   ├── app.py               # Flask backend app
│   ├── vault.py             # Encryption utilities
│   ├── totp.py              # TOTP QR and verification
│   ├── vault.json.enc       # Encrypted vault data
│   ├── salt.bin             # Salt for key derivation
│   ├── vault_audit.log      # Optional audit trail
│
├── frontend
│   ├── src
│   │   ├── App.css
│   │   ├── Vault.jsx
│   │   ├── AddCredential.jsx
│   │   ├── Login.jsx
│   │   └── main.jsx
│   └── index.html
│
├── README.md
```

## 📦 Deployment

- Flask backend is hosted on [Render](https://render.com).
- React frontend is hosted on [Netlify](https://netlify.com).

---

Made with ❤️ by Nicolas Cuenca
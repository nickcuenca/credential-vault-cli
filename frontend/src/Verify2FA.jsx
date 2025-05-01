// src/Verify2FA.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Verify2FA({ onSuccess }) {
  const [code, setCode]   = useState('');
  const [qr, setQR]       = useState('');   // PNG URL
  const [error, setError] = useState('');

  /* ---------------- Load QR once ---------------- */
  useEffect(() => {
    // Give <img> a direct URL; ?ts=… prevents old-cache hits
    setQR(`${process.env.REACT_APP_API}/qrcode?ts=${Date.now()}`);
  }, []);

  /* ---------------- Verify code ----------------- */
  const handleVerify = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        `${process.env.REACT_APP_API}/verify-2fa`,
        new URLSearchParams({ code }),
        { withCredentials: true }
      );
      setError('');
      onSuccess();          // go to Vault page
    } catch {
      setError('❌ Invalid 2FA code.');
    }
  };

  /* ------------------ UI ------------------------ */
  return (
    <div className="login-container">
      <h2>🔐 2FA Verification</h2>
      <p>Scan this QR code with Google Authenticator or Authy:</p>

      {qr ? (
        <img src={qr} alt="QR Code" style={{ marginBottom: '1rem' }} />
      ) : (
        <p>Loading QR code…</p>
      )}

      <form onSubmit={handleVerify}>
        <input
          type="text"
          placeholder="Enter 6-digit 2FA code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          required
        />
        <button type="submit">Verify</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default Verify2FA;
// src/Verify2FA.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Verify2FA({ onSuccess }) {
  const [code, setCode] = useState('');
  const [qr, setQR] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (!qr) {  // don't refetch if already fetched
      axios.get(`${process.env.REACT_APP_API}/qrcode`, { withCredentials: true })
        .then(res => {
          const match = res.data.match(/src="data:image\/png;base64,([^"]+)"/);
          if (match) {
            setQR(`data:image/png;base64,${match[1]}`);
          }
        })
        .catch(err => console.error('Failed to load QR code:', err));
    }
  }, [qr]);
  

  const handleVerify = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${process.env.REACT_APP_API}/verify-2fa`,
        new URLSearchParams({ code }),
        { withCredentials: true }
      );
      setError('');
      onSuccess(); // moves to Vault page
    } catch (err) {
      setError('❌ Invalid 2FA code.');
    }
  };

  return (
    <div className="login-container">
      <h2>🔐 2FA Verification</h2>
      <p>Scan this QR code with Google Authenticator or Authy:</p>
      {qr ? <img src={qr} alt="QR Code" style={{ marginBottom: '1rem' }} /> : <p>Loading QR code...</p>}

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
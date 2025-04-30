import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Login.css';

function Login({ onLogin }) {
  const [password, setPassword] = useState('');
  const [step, setStep] = useState('login');
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [qrCode, setQrCode] = useState('');

  useEffect(() => {
    if (step === '2fa') {
      axios.get('http://localhost:5000/qrcode', { withCredentials: true })
        .then((res) => {
          const match = res.data.match(/src="data:image\/png;base64,([^"]+)"/);
          if (match) {
            setQrCode(`data:image/png;base64,${match[1]}`);
          }
        })
        .catch(() => {
          setQrCode('');
        });
    }
  }, [step]);

  const handleMasterSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/', 
        new URLSearchParams({ master: password }), 
        { withCredentials: true }
      );
      if (response.data.status === '2fa_required') {
        setStep('2fa');
        setError('');
      } else {
        throw new Error('Unexpected response from server.');
      }
    } catch (err) {
      setError('❌ Incorrect master password.');
    }
  };

  const handle2FASubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/verify-2fa', 
        new URLSearchParams({ code }), 
        { withCredentials: true }
      );
      setError('');
      onLogin();
    } catch (err) {
      setError('❌ Invalid 2FA code.');
    }
  };

  const handleResetVault = () => {
    if (window.confirm("Are you sure you want to reset the vault? This will delete all data.")) {
      axios.post('http://localhost:5000/force-reset', {}, { withCredentials: true })
        .then(() => {
          alert("✅ Vault reset successfully.");
          window.location.reload();
        })
        .catch(() => {
          alert("❌ Failed to reset the vault.");
        });
    }
  };

  return (
    <div className="login-container">
      <h2>🔐 Welcome to Vault</h2>

      {step === 'login' && (
        <>
          <p style={{ fontSize: '14px', marginBottom: '10px', color: '#555' }}>
            New user? First time setup requires scanning the QR code to register 2FA.<br />
            You'll see it after entering a new password.
          </p>
          <form onSubmit={handleMasterSubmit}>
            <input
              type="password"
              placeholder="Master Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
        </>
      )}

      {step === '2fa' && (
        <>
          <p>Scan this QR code with Google Authenticator or Authy if you're a new user:</p>
          {qrCode ? (
            <img src={qrCode} alt="QR Code" style={{ marginBottom: '1rem' }} />
          ) : (
            <p>Loading QR code...</p>
          )}
          <form onSubmit={handle2FASubmit}>
            <input
              type="text"
              placeholder="2FA Code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />
            <button type="submit">Verify</button>
          </form>
        </>
      )}

      <button 
        onClick={handleResetVault} 
        style={{ marginTop: '12px', backgroundColor: '#dc3545', color: 'white' }}
      >
        🧨 Reset Vault
      </button>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
}

export default Login;
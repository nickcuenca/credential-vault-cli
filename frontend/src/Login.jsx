import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

function Login({ onLogin }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleMasterSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${process.env.REACT_APP_API}/`, 
        new URLSearchParams({ master: password }), 
        { withCredentials: true }
      );
      if (response.data.status === '2fa_required') {
        onLogin(); // move to <Verify2FA /> via App.jsx
        setError('');
      } else {
        throw new Error('Unexpected response from server.');
      }
    } catch (err) {
      setError('❌ Incorrect master password.');
    }
  };

  const handleForceReset = async () => {
    if (!window.confirm("Are you sure you want to reset the vault? This will delete all data.")) return;

    try {
      const res = await axios.post(`${process.env.REACT_APP_API}/force-reset`, {}, { withCredentials: true });
      if (res.status === 200) {
        alert("✅ Vault reset successfully.");
        sessionStorage.removeItem('authenticated');
        window.location.reload();
      } else {
        alert("❌ Failed to reset the vault.");
      }
    } catch (err) {
      alert("❌ Failed to reset the vault.");
    }
  };

  return (
    <div className="login-container">
      <h2>🔐 Welcome to Vault</h2>
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

      <button onClick={handleForceReset} className="danger-btn">
        🧨 Reset Vault
      </button>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
}

export default Login;
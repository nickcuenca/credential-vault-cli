import React, { useState } from 'react';
import axios from 'axios';
import zxcvbn from 'zxcvbn';

function AddCredential({ onAdd }) {
  const [site, setSite] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [strength, setStrength] = useState(null);
  const [length, setLength] = useState(12);
  const [includeSymbols, setIncludeSymbols] = useState(true);
  const [includeNumbers, setIncludeNumbers] = useState(true);
  const [includeUppercase, setIncludeUppercase] = useState(true);
  const [toastMessage, setToastMessage] = useState('');


  const handlePasswordChange = (e) => {
    const val = e.target.value;
    setPassword(val);
    setStrength(zxcvbn(val));
  };

  const generatePassword = () => {
    const lower = "abcdefghijklmnopqrstuvwxyz";
    const upper = includeUppercase ? "ABCDEFGHIJKLMNOPQRSTUVWXYZ" : "";
    const numbers = includeNumbers ? "0123456789" : "";
    const symbols = includeSymbols ? "!@#$%^&*()_+-=[]{}|;:,.<>?" : "";
    const charset = lower + upper + numbers + symbols;

    let generated = "";
    for (let i = 0; i < length; i++) {
      generated += charset.charAt(Math.floor(Math.random() * charset.length));
    }

    setPassword(generated);
    setStrength(zxcvbn(generated));
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(password).then(() => {
      setToastMessage("📋 Password copied!");
      setTimeout(() => setToastMessage(''), 2500);
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${process.env.REACT_APP_API}/add-credential`,
        { site, username, password },
        { withCredentials: true }
      );
      setSite('');
      setUsername('');
      setPassword('');
      setStrength(null);
      if (onAdd) onAdd();
    } catch {
      alert('❌ Failed to add credential.');
    }
  };

  const strengthLabel = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"];
  const strengthColor = ["#dc3545", "#f66", "#ffc107", "#28a745", "#007bff"];

  return (
    <div className="add-credential-container">
      <h3>Add New Credential</h3>
      {toastMessage && (
        <div className="toast">
        {toastMessage}
        </div>
      )}  
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Site" value={site} onChange={e => setSite(e.target.value)} required />
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />

        <input type="password" placeholder="Password" value={password} onChange={handlePasswordChange} required />

        {strength && (
        <div style={{
            fontSize: '0.9rem',
            marginBottom: '10px',
            color: strengthColor[strength.score],
            textAlign: 'center',
            fontWeight: '500'
        }}>
            Strength: {strengthLabel[strength.score]}
        </div>
        )}

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center', marginBottom: '10px' }}>
          <button type="button" onClick={generatePassword}>🔒 Generate</button>
          <button type="button" onClick={copyToClipboard}>📋 Copy</button>
        </div>

        <div className="password-options">
          <label><input type="checkbox" checked={includeUppercase} onChange={() => setIncludeUppercase(!includeUppercase)} /> Uppercase</label>
          <label><input type="checkbox" checked={includeNumbers} onChange={() => setIncludeNumbers(!includeNumbers)} /> Numbers</label>
          <label><input type="checkbox" checked={includeSymbols} onChange={() => setIncludeSymbols(!includeSymbols)} /> Symbols</label>
          <label>Password Length: {length}</label>
          <input type="range" min="6" max="30" value={length} onChange={e => setLength(parseInt(e.target.value))} />
        </div>

        <button type="submit">Add</button>
      </form>
    </div>
  );
}

export default AddCredential;
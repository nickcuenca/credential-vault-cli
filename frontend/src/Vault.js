import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import AddCredential from './AddCredential';

function Vault({ onDelete }) {
  const [credentials, setCredentials] = useState([]);
  const [showPasswords, setShowPasswords] = useState(false);
  const [editingSite, setEditingSite] = useState(null);
  const [editData, setEditData] = useState({ username: '', password: '' });
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('darkMode') === 'true');

  const fetchCredentials = () => {
    axios
      .get(`${process.env.REACT_APP_API}/api/credentials`, { withCredentials: true })
      .then((res) => {
        setCredentials(res.data.credentials || []);
      })
      .catch((err) => {
        console.error('Error fetching data:', err);
      });
  };

  const handleLogout = () => {
    axios
      .get(`${process.env.REACT_APP_API}/logout`, { withCredentials: true })
      .then(() => {
        window.location.reload();
      });
  };

  const handleExport = () => {
    window.open(`${process.env.REACT_APP_API}/export`, '_blank');
  };

  const handleResetVault = () => {
    if (window.confirm('Are you sure you want to reset the vault? This will delete all data.')) {
      axios
        .post(`${process.env.REACT_APP_API}/reset-vault`, {}, { withCredentials: true })
        .then(() => {
          alert('✅ Vault reset successfully.');
          setCredentials([]);
        })
        .catch((err) => {
          console.error('Reset failed:', err);
          alert('❌ Failed to reset vault.');
        });
    }
  };

  const handleDelete = (site) => {
    if (window.confirm(`Delete credentials for ${site}?`)) {
      if (onDelete) {
        onDelete(site); // ← use mock handler for tests
      } else {
        axios
          .post(`${process.env.REACT_APP_API}/delete/${encodeURIComponent(site)}`, {}, { withCredentials: true })
          .then(() => fetchCredentials())
          .catch((err) => console.error('Delete failed:', err));
      }
    }
  };  

  useEffect(() => {
    fetchCredentials();
    const interval = setInterval(fetchCredentials, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    document.body.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  return (
    <div className="App">
      <h1>🔐 Credential Vault</h1>

      <div style={{ marginBottom: '12px' }}>
        <button onClick={() => setShowPasswords((prev) => !prev)}>
          {showPasswords ? 'Hide Passwords' : 'Show Passwords'}
        </button>
        <button onClick={fetchCredentials} style={{ marginLeft: '10px' }}>
          🔄 Refresh
        </button>
        <button onClick={handleLogout} style={{ marginLeft: '10px', backgroundColor: '#666', color: 'white' }}>
          🚪 Logout
        </button>
        <button onClick={handleExport} style={{ marginLeft: '10px' }}>
          📄 Export
        </button>
        <button onClick={() => setDarkMode((prev) => !prev)} style={{ marginLeft: '10px' }}>
          🌓 Toggle Dark Mode
        </button>
        <button
          onClick={handleResetVault}
          style={{ marginLeft: '10px', backgroundColor: '#dc3545', color: 'white' }}
        >
          🧨 Reset Vault
        </button>
      </div>

      <AddCredential onAdd={fetchCredentials} />

      <table>
        <thead>
          <tr>
            <th>Site</th>
            <th>Username</th>
            <th>Password</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {credentials.length === 0 ? (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center', padding: '1rem', color: '#666' }}>
                No credentials found.
              </td>
            </tr>
          ) : (
            credentials.map((cred, index) => (
              <tr key={index}>
                <td>{cred.site}</td>
                <td>
                  {editingSite === cred.site ? (
                    <input
                      value={editData.username}
                      onChange={(e) => setEditData({ ...editData, username: e.target.value })}
                    />
                  ) : (
                    cred.username
                  )}
                </td>
                <td>
                  {editingSite === cred.site ? (
                    <input
                      value={editData.password}
                      onChange={(e) => setEditData({ ...editData, password: e.target.value })}
                    />
                  ) : showPasswords ? (
                    cred.password
                  ) : (
                    '••••••••'
                  )}
                </td>
                <td>
                  {editingSite === cred.site ? (
                    <>
                      <button
                        onClick={() => {
                          axios
                            .post(`${process.env.REACT_APP_API}/edit/${encodeURIComponent(cred.site)}`, editData, {
                              withCredentials: true,
                            })
                            .then(() => {
                              setEditingSite(null);
                              fetchCredentials();
                            });
                        }}
                      >
                        ✅ Save
                      </button>
                      <button onClick={() => setEditingSite(null)}>❌ Cancel</button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => {
                          setEditingSite(cred.site);
                          setEditData({
                            username: cred.username,
                            password: cred.password,
                          });
                        }}
                      >
                        ✏️ Edit
                      </button>
                      <button
                        onClick={() => handleDelete(cred.site)}
                        style={{ backgroundColor: '#f44336', color: 'white', marginLeft: '5px' }}
                      >
                        🗑️ Delete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Vault;
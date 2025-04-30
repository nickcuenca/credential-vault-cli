import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import AddCredential from './AddCredential';

function Vault() {
  const [credentials, setCredentials] = useState([]); // State for storing credentials
  const [showPasswords, setShowPasswords] = useState(false); // State for showing/hiding passwords
  const [editingSite, setEditingSite] = useState(null); // State for editing site
  const [editData, setEditData] = useState({ username: '', password: '' }); // State for edit form data

  const [darkMode, setDarkMode] = useState(() => {
    // Retrieve dark mode setting from localStorage
    return localStorage.getItem('darkMode') === 'true';
  });

  const generatePassword = (length = 12) => {
    // Function to generate a random password
    const charset =
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?";
    let newPassword = "";
    for (let i = 0; i < length; i++) {
      const randomChar = charset[Math.floor(Math.random() * charset.length)];
      newPassword += randomChar;
    }
    return newPassword;
  };

  const fetchCredentials = () => {
    // Fetch credentials from the backend
    axios
      .get('http://localhost:5000/api/credentials', { withCredentials: true })
      .then((res) => {
        setCredentials(res.data.credentials || []);
      })
      .catch((err) => {
        console.error('Error fetching data:', err);
      });
  };

  const handleLogout = () => {
    // Handle user logout
    axios
      .get('http://localhost:5000/logout', { withCredentials: true })
      .then(() => {
        window.location.reload(); // Reset app state
      });
  };

  const handleExport = () => {
    // Handle exporting the credentials
    window.open('http://localhost:5000/export', '_blank');
  };

  const handleResetVault = () => {
    // Handle vault reset
    if (window.confirm('Are you sure you want to reset the vault? This will delete all data.')) {
      axios
        .post('http://localhost:5000/reset-vault', {}, { withCredentials: true })
        .then(() => {
          alert('✅ Vault reset successfully.');
          setCredentials([]); // Clear credentials state
        })
        .catch((err) => {
          console.error('Reset failed:', err);
          alert('❌ Failed to reset vault.');
        });
    }
  };

  const handleDelete = (site) => {
    // Handle deleting a credential
    if (window.confirm(`Delete credentials for ${site}?`)) {
      axios
        .post(`http://localhost:5000/delete/${encodeURIComponent(site)}`, {}, { withCredentials: true })
        .then(() => fetchCredentials())
        .catch((err) => console.error('Delete failed:', err));
    }
  };

  useEffect(() => {
    fetchCredentials(); // Fetch credentials when component mounts
    const interval = setInterval(fetchCredentials, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval); // Clean up interval on component unmount
  }, []);

  useEffect(() => {
    // Handle dark mode toggle
    document.body.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', darkMode); // Store dark mode setting in localStorage
  }, [darkMode]);

  return (
    <div className="App">
      <h1>🔐 Credential Vault</h1>

      <div style={{ marginBottom: '12px' }}>
        {/* Toggle show/hide passwords */}
        <button onClick={() => setShowPasswords((prev) => !prev)}>
          {showPasswords ? 'Hide Passwords' : 'Show Passwords'}
        </button>
        {/* Refresh credentials */}
        <button onClick={fetchCredentials} style={{ marginLeft: '10px' }}>
          🔄 Refresh
        </button>
        {/* Logout */}
        <button onClick={handleLogout} style={{ marginLeft: '10px', backgroundColor: '#666', color: 'white' }}>
          🚪 Logout
        </button>
        {/* Export credentials */}
        <button onClick={handleExport} style={{ marginLeft: '10px' }}>
          📄 Export
        </button>
        {/* Toggle dark mode */}
        <button onClick={() => setDarkMode((prev) => !prev)} style={{ marginLeft: '10px' }}>
          🌓 Toggle Dark Mode
        </button>
        {/* Reset vault */}
        <button
          onClick={handleResetVault}
          style={{ marginLeft: '10px', backgroundColor: '#dc3545', color: 'white' }}
        >
          🧨 Reset Vault
        </button>
      </div>

      {/* Add new credential */}
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
                      {/* Save or cancel editing */}
                      <button
                        onClick={() => {
                          axios
                            .post(`http://localhost:5000/edit/${encodeURIComponent(cred.site)}`, editData, {
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
                      {/* Edit or delete credentials */}
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
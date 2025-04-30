import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login'; // Your component paths
import Vault from './Vault'; // Your component paths

function App() {
  return (
    <Router>
      <div className="App">
        <Routes> {/* Replaced Switch with Routes */}
          <Route path="/" element={<Login />} /> {/* Use element prop */}
          <Route path="/vault" element={<Vault />} /> {/* Use element prop */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;

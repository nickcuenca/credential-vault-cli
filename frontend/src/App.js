import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Update import
import Login from './Login'; // Replace with your component paths
import Vault from './Vault'; // Replace with your component paths

function App() {
  return (
    <Router>
      <div className="App">
        <Routes> {/* Use Routes instead of Switch */}
          <Route path="/" element={<Login />} /> {/* Use element prop instead of component */}
          <Route path="/vault" element={<Vault />} /> {/* Use element prop instead of component */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
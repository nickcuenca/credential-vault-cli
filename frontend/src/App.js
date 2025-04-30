import React, { useState } from 'react';
import Vault from './Vault';  // the page that shows credentials
import Login from './Login';  // login page

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return loggedIn ? <Vault /> : <Login onLogin={() => setLoggedIn(true)} />;
}

export default App;
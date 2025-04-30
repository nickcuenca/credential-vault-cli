import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './Login'; // Replace with your component paths
import Vault from './Vault'; // Replace with your component paths

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route exact path="/" component={Login} />
          <Route path="/vault" component={Vault} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
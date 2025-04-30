import React, { useState } from 'react';
import Vault from './Vault';
import Login from './Login';
import Verify2FA from './Verify2FA';

function App() {
  const [step, setStep] = useState('login'); // 'login' → '2fa' → 'vault'

  return (
    <>
      {step === 'login' && <Login onLogin={() => setStep('2fa')} />}
      {step === '2fa' && <Verify2FA onSuccess={() => setStep('vault')} />}
      {step === 'vault' && <Vault />}
    </>
  );
}

export default App;
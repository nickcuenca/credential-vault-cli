import { render, screen } from '@testing-library/react';
import Login from './Login';

describe('Login Component', () => {
  test('renders master password field and buttons', () => {
    render(<Login onLogin={() => {}} onReset={() => {}} />);
    expect(screen.getByPlaceholderText(/Master Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Reset Vault/i })).toBeInTheDocument();
  });
});
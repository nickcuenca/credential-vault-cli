import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renders the welcome heading', () => {
    render(<App />);
    // Look for the welcome message in the login screen
    const heading = screen.getByText(/Welcome to Vault/i);
    expect(heading).toBeInTheDocument();
  });

  test('renders master password input field', () => {
    render(<App />);
    // Check that the Master Password input is present
    const input = screen.getByPlaceholderText(/Master Password/i);
    expect(input).toBeInTheDocument();
  });
});
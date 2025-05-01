import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';

jest.mock('axios'); // 🔧 Mock axios globally

beforeEach(() => {
  axios.post.mockReset();
  axios.get.mockReset();
});

describe('App Component', () => {
  test('renders the welcome heading', () => {
    render(<App />);
    expect(screen.getByText(/Welcome to Vault/i)).toBeInTheDocument();
  });

  test('renders master password input field', () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/Master Password/i)).toBeInTheDocument();
  });

  test('transitions to 2FA after successful login', async () => {
    axios.post.mockResolvedValueOnce({ data: { status: '2fa_required' } }); // mock login success
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText(/Master Password/i), {
      target: { value: 'correct-password' },
    });
    fireEvent.click(screen.getByText(/Login/i));

    await screen.findByPlaceholderText(/Enter 6-digit 2FA code/i);
  });

  test('transitions to Vault after successful 2FA', async () => {
    axios.post.mockResolvedValueOnce({ data: { status: '2fa_required' } }); // Login
    axios.post.mockResolvedValueOnce({ status: 200 }); // 2FA verify
    axios.get.mockResolvedValueOnce({ data: { credentials: [] } }); // Vault fetch
  
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText(/Master Password/i), {
      target: { value: 'correct-password' },
    });
    fireEvent.click(screen.getByText(/Login/i));
  
    const input2FA = await screen.findByPlaceholderText(/Enter 6-digit 2FA code/i);
    fireEvent.change(input2FA, { target: { value: '123456' } });
    fireEvent.click(screen.getByText(/Verify/i));
  
    await screen.findByText(/Credential Vault/i); // confirms Vault loaded
  });  
});
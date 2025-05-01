import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from './Login';
import axios from 'axios';

// Mocks
jest.mock('axios');

beforeEach(() => {
  window.alert = jest.fn();
  window.confirm = jest.fn(() => true);
  Object.defineProperty(window, 'location', {
    writable: true,
    value: { reload: jest.fn() },
  });
});

describe('Login Component', () => {
  test('renders password field and buttons', () => {
    render(<Login onLogin={() => {}} />);
    expect(screen.getByPlaceholderText(/Master Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Reset Vault/i })).toBeInTheDocument();
  });

  test('calls onLogin when 2FA is required', async () => {
    const mockLogin = jest.fn();
    axios.post.mockResolvedValueOnce({ data: { status: '2fa_required' } });

    render(<Login onLogin={mockLogin} />);

    fireEvent.change(screen.getByPlaceholderText(/Master Password/i), {
      target: { value: 'correct-password' },
    });
    fireEvent.click(screen.getByText(/Login/i));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalled();
    });
  });

  test('shows error on invalid password', async () => {
    axios.post.mockRejectedValueOnce(new Error('Invalid'));

    render(<Login onLogin={() => {}} />);

    fireEvent.change(screen.getByPlaceholderText(/Master Password/i), {
      target: { value: 'wrong-password' },
    });
    fireEvent.click(screen.getByText(/Login/i));

    await waitFor(() => {
      expect(screen.getByText(/❌ Incorrect master password/i)).toBeInTheDocument();
    });
  });

  test('shows alert and reloads on successful reset', async () => {
    axios.post.mockResolvedValueOnce({ status: 200 });

    render(<Login onLogin={() => {}} />);
    fireEvent.click(screen.getByText(/Reset Vault/i));

    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('✅ Vault reset successfully.');
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  test('shows error on unexpected server response during login', async () => {
    axios.post.mockResolvedValueOnce({ data: { status: 'unknown' } });
  
    render(<Login onLogin={() => {}} />);
    fireEvent.change(screen.getByPlaceholderText(/Master Password/i), {
      target: { value: 'some-password' },
    });
    fireEvent.click(screen.getByText(/Login/i));
  
    await waitFor(() => {
      expect(screen.getByText('❌ Incorrect master password.')).toBeInTheDocument();
    });
  });

  test('shows alert on failed reset', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network error'));
  
    render(<Login onLogin={() => {}} />);
    fireEvent.click(screen.getByText(/Reset Vault/i));
  
    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('❌ Failed to reset the vault.');
    });
  });
  
});
import { render, screen, act, fireEvent } from '@testing-library/react';
import Vault from './Vault';
import axios from 'axios';

jest.mock('axios');

beforeEach(() => {
  axios.get.mockResolvedValue({ data: { credentials: [] } });
  window.confirm = jest.fn(() => false);
  window.alert = jest.fn();
  localStorage.setItem('darkMode', 'false');
  document.body.classList.remove('dark');
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  console.error.mockRestore();
});

describe('Vault component', () => {
  test('renders "No credentials found" message', async () => {
    await act(async () => render(<Vault />));
    expect(await screen.findByText(/No credentials found/i)).toBeInTheDocument();
  });

  test('renders action buttons', async () => {
    await act(async () => render(<Vault />));
    expect(await screen.findByText(/Show Passwords/i)).toBeInTheDocument();
    expect(screen.getByText(/Refresh/i)).toBeInTheDocument();
    expect(screen.getByText(/Logout/i)).toBeInTheDocument();
    expect(screen.getByText(/Export/i)).toBeInTheDocument();
    expect(screen.getByText(/Toggle Dark Mode/i)).toBeInTheDocument();
    expect(screen.getByText(/Reset Vault/i)).toBeInTheDocument();
  });

  test('renders table headers', async () => {
    await act(async () => render(<Vault />));
    expect(await screen.findByText(/Site/i)).toBeInTheDocument();
    expect(screen.getByText(/Username/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Password/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Actions/i)).toBeInTheDocument();
  });

  test('handles error during fetchCredentials', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'));
    await act(async () => render(<Vault />));
    expect(console.error).toHaveBeenCalledWith('Error fetching data:', expect.any(Error));
  });

  test('clicking reset triggers confirm', async () => {
    await act(async () => render(<Vault />));
    const resetBtn = await screen.findByText(/Reset Vault/i);
    await act(async () => fireEvent.click(resetBtn));
    expect(window.confirm).toHaveBeenCalled();
  });

  test('handles error during reset', async () => {
    window.confirm = jest.fn(() => true);
    axios.post.mockRejectedValueOnce(new Error('fail'));
    await act(async () => render(<Vault />));
  
    const resetBtn = screen.getByText(/Reset Vault/i);
    await act(async () => fireEvent.click(resetBtn));
  
    expect(window.alert).toHaveBeenCalledWith('❌ Failed to reset vault.');
  });
  

  test('clicking delete calls API', async () => {
    axios.get.mockResolvedValueOnce({
      data: { credentials: [{ site: 'TestSite', username: 'user', password: 'pass' }] }
    });
    axios.post = jest.fn().mockResolvedValue({});
    window.confirm = jest.fn(() => true);

    await act(async () => render(<Vault />));
    fireEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/delete/TestSite'),
      {},
      { withCredentials: true }
    );
  });

  test('calls onDelete prop if provided', async () => {
    const mockDelete = jest.fn();
    axios.get.mockResolvedValueOnce({
      data: { credentials: [{ site: 'Zoom', username: 'x', password: 'y' }] }
    });
    window.confirm = jest.fn(() => true);

    await act(async () => render(<Vault onDelete={mockDelete} />));
    fireEvent.click(screen.getByRole('button', { name: /delete/i }));
    expect(mockDelete).toHaveBeenCalledWith('Zoom');
  });

  test('toggles password visibility', async () => {
    axios.get.mockResolvedValueOnce({
      data: { credentials: [{ site: 'GitHub', username: 'octo', password: 'secret' }] }
    });

    await act(async () => render(<Vault />));
    fireEvent.click(screen.getByText(/Show Passwords/i));
    expect(await screen.findByText('secret')).toBeInTheDocument();
  });

  test('toggles dark mode', async () => {
    await act(async () => render(<Vault />));
    fireEvent.click(screen.getByText(/Toggle Dark Mode/i));
    expect(document.body.classList.contains('dark')).toBe(true);
  });

  test('edits a credential and saves it', async () => {
    axios.get.mockResolvedValueOnce({
      data: { credentials: [{ site: 'Reddit', username: 'user', password: 'pass' }] }
    });
    axios.post = jest.fn().mockResolvedValue({});

    await act(async () => render(<Vault />));
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));

    const usernameInput = screen.getByDisplayValue('user');
    const passwordInput = screen.getByDisplayValue('pass');
    fireEvent.change(usernameInput, { target: { value: 'newUser' } });
    fireEvent.change(passwordInput, { target: { value: 'newPass' } });

    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/edit/Reddit'),
      { username: 'newUser', password: 'newPass' },
      { withCredentials: true }
    );
  });

  test('cancels editing a credential', async () => {
    axios.get.mockResolvedValueOnce({
      data: { credentials: [{ site: 'Facebook', username: 'mark', password: 'zuck' }] }
    });

    await act(async () => render(<Vault />));
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));

    expect(screen.queryByDisplayValue('mark')).not.toBeInTheDocument();
  });
});
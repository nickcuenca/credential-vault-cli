import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AddCredential from './AddCredential';
import axios from 'axios';

jest.mock('axios');

beforeAll(() => {
  window.alert = jest.fn(); // prevent jsdom crash on alert()
});

describe('AddCredential Component', () => {
  test('renders input fields and submit button', () => {
    render(<AddCredential onAdd={() => {}} />);
    expect(screen.getByPlaceholderText(/Site/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Add$/i })).toBeInTheDocument();
  });

  test('allows typing in all fields', () => {
    render(<AddCredential onAdd={() => {}} />);
    fireEvent.change(screen.getByPlaceholderText(/Site/i), { target: { value: 'example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'user123' } });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'pass123' } });

    expect(screen.getByDisplayValue('example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('user123')).toBeInTheDocument();
    expect(screen.getByDisplayValue('pass123')).toBeInTheDocument();
  });

  test('toggles checkboxes and updates slider', () => {
    render(<AddCredential onAdd={() => {}} />);
    const uppercase = screen.getByLabelText(/Uppercase/i);
    const numbers = screen.getByLabelText(/Numbers/i);
    const symbols = screen.getByLabelText(/Symbols/i);
    const range = screen.getByRole('slider');

    fireEvent.click(uppercase);
    fireEvent.click(numbers);
    fireEvent.click(symbols);
    fireEvent.change(range, { target: { value: 18 } });

    expect(range.value).toBe('18');
  });

  test('submits form and calls onAdd (sync)', async () => {
    const mockAdd = jest.fn();
    axios.post.mockResolvedValue({}); // simulate successful API response

    render(<AddCredential onAdd={mockAdd} />);

    fireEvent.change(screen.getByPlaceholderText(/Site/i), { target: { value: 'example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'testpass' } });

    fireEvent.click(screen.getByText(/^Add$/i));

    await waitFor(() => {
      expect(mockAdd).toHaveBeenCalled();
    });
  });

  test('submits form and calls onAdd (async fetch)', async () => {
    const mockAdd = jest.fn();
    axios.post.mockResolvedValue({}); // simulate successful API response

    render(<AddCredential onAdd={mockAdd} />);

    fireEvent.change(screen.getByPlaceholderText(/Site/i), {
      target: { value: 'example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), {
      target: { value: 'testpass' },
    });

    fireEvent.click(screen.getByText(/^Add$/i));

    await waitFor(() => {
      expect(mockAdd).toHaveBeenCalled();
    });
  });

  test('generates password when "Generate" is clicked', () => {
    render(<AddCredential onAdd={() => {}} />);
    const passwordInput = screen.getByPlaceholderText(/Password/i);
    const generateBtn = screen.getByText(/Generate/i);

    fireEvent.click(generateBtn);

    expect(passwordInput.value.length).toBeGreaterThan(0);
  });
});
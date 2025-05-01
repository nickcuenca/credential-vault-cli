import { render, screen } from '@testing-library/react';
import AddCredential from './AddCredential';

describe('AddCredential Component', () => {
  test('renders input fields and submit button', () => {
    render(<AddCredential onAdd={() => {}} />);
    expect(screen.getByPlaceholderText(/Site/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Add$/i })).toBeInTheDocument();
  });
});
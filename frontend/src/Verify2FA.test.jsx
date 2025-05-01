import { render, screen } from '@testing-library/react';
import Verify2FA from './Verify2FA';

describe('Verify2FA Component', () => {
  // silence axios error logs in tests
  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  test('renders code input and verify button', () => {
    render(<Verify2FA onVerify={() => {}} />);
    expect(screen.getByPlaceholderText(/Enter 6-digit 2FA code/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Verify/i })).toBeInTheDocument();
  });
});
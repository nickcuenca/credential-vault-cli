import unittest
from vault import (
    generate_key,
    encrypt_data,
    decrypt_data,
    check_password_strength
)

class TestVaultFunctions(unittest.TestCase):
    """
    Unit tests for vault.py to verify encryption, decryption,
    key generation, and password strength logic.
    """

    def test_key_generation_consistency(self):
        """
        Test that the same master password always generates the same encryption key.
        """
        password = "TestMasterPassword"
        key1 = generate_key(password)
        key2 = generate_key(password)
        self.assertEqual(key1, key2)

    def test_encryption_and_decryption(self):
        """
        Ensure that encrypted data can be decrypted correctly with the right key.
        """
        master = "Test123!"
        data = {
            "github.com": {
                "username": "nickcuenca",
                "password": "SuperSecret!"
            }
        }
        key = generate_key(master)
        encrypted = encrypt_data(data, key)
        decrypted = decrypt_data(encrypted, key)
        self.assertEqual(decrypted, data)

    def test_decryption_with_wrong_password_fails(self):
        """
        Ensure decryption fails with an incorrect master password.
        """
        key_correct = generate_key("correct_password")
        key_wrong = generate_key("wrong_password")
        encrypted = encrypt_data({"test": "data"}, key_correct)

        with self.assertRaises(ValueError):
            decrypt_data(encrypted, key_wrong)

    def test_password_strength_levels(self):
        """
        Validate that password strength evaluation returns expected values.
        """
        self.assertEqual(check_password_strength("abc"), '🔴 Weak')
        self.assertEqual(check_password_strength("Abcdef12"), '🟡 Medium')
        self.assertEqual(check_password_strength("Abcdef12!@"), '🟡 Medium')
        self.assertEqual(check_password_strength("Abcdef12!@XY"), '🟢 Strong')


if __name__ == '__main__':
    unittest.main()

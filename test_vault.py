import unittest
from vault import generate_key, encrypt_data, decrypt_data

class TestVaultFunctions(unittest.TestCase):
    """
    Unit tests for vault.py to verify encryption, decryption, and key generation.
    These tests help ensure cryptographic consistency and functional reliability.
    """

    def test_key_generation_consistency(self):
        """
        Test that the same master password always generates the same encryption key.
        This is critical for decrypting the vault reliably across sessions.
        """
        password = "TestMasterPassword"
        key1 = generate_key(password)
        key2 = generate_key(password)
        self.assertEqual(key1, key2)

    def test_encryption_and_decryption(self):
        """
        Test that data encrypted with a derived key can be correctly decrypted.
        Ensures encryption pipeline is lossless and secure.
        """
        master = "Test123!"
        data = {
            "github.com": {
                "username": "nickcuenca",
                "password": "SuperSecret!"
            }
        }
        key = generate_key(master)             # Derive encryption key
        encrypted = encrypt_data(data, key)    # Encrypt the data
        decrypted = decrypt_data(encrypted, key)  # Decrypt the data
        self.assertEqual(decrypted, data)      # Confirm round-trip is accurate

# Entry point for the test runner
if __name__ == '__main__':
    unittest.main()

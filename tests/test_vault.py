import unittest
import os
from vault import (
    generate_key,
    encrypt_data,
    decrypt_data,
    check_password_strength,
    log_action,
    read_audit_log
)

class TestVaultFunctions(unittest.TestCase):
    """
    Unit tests for vault.py to verify encryption, decryption,
    key generation, and password strength logic.
    """

    def test_key_generation_consistency(self):
        password = "TestMasterPassword"
        key1 = generate_key(password)
        key2 = generate_key(password)
        self.assertEqual(key1, key2)

    def test_encryption_and_decryption(self):
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
        key_correct = generate_key("correct_password")
        key_wrong = generate_key("wrong_password")
        encrypted = encrypt_data({"test": "data"}, key_correct)
        with self.assertRaises(ValueError):
            decrypt_data(encrypted, key_wrong)

    def test_password_strength_levels(self):
        self.assertEqual(check_password_strength("abc"), '🔴 Weak')
        self.assertEqual(check_password_strength("Abcdef12"), '🟡 Medium')
        self.assertEqual(check_password_strength("Abcdef12!@"), '🟡 Medium')
        self.assertEqual(check_password_strength("Abcdef12!@XY"), '🟢 Strong')

class TestVault(unittest.TestCase):

    def setUp(self):
        self.test_password = "test123"
        self.test_key = generate_key(self.test_password)
        self.test_data = {"site": {"username": "user", "password": "pass"}}
        self.test_file = "test_vault.enc"
        self.log_file = "vault_audit.log"

        # Clear audit log for clean test runs
        if os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.truncate(0)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_encrypt_and_decrypt_data(self):
        encrypted = encrypt_data(self.test_data, self.test_key)
        decrypted = decrypt_data(encrypted, self.test_key)
        self.assertEqual(decrypted, self.test_data)

    def test_decrypt_with_wrong_key(self):
        wrong_key = generate_key("wrongpass")
        encrypted = encrypt_data(self.test_data, self.test_key)
        with self.assertRaises(ValueError):
            decrypt_data(encrypted, wrong_key)

    def test_log_action_creates_entry(self):
        action = "TEST ACTION"
        log_action(action)
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            lines = f.readlines()
            self.assertTrue(any(action in line for line in lines))

    def test_read_audit_log_returns_string(self):
        log_action("TEST READ LOG")
        logs = read_audit_log()
        self.assertIsInstance(logs, str)
        self.assertIn("TEST READ LOG", logs)

    def test_generate_key_consistency(self):
        key1 = generate_key(self.test_password)
        key2 = generate_key(self.test_password)
        self.assertEqual(key1, key2)

    def test_generate_key_difference(self):
        key1 = generate_key("onepass")
        key2 = generate_key("differentpass")
        self.assertNotEqual(key1, key2)


if __name__ == '__main__':
    unittest.main()
import unittest
import os
from totp import get_or_create_totp_secret, verify_totp_code, get_provisioning_uri
import pyotp

class TestTOTP(unittest.TestCase):

    def setUp(self):
        self.secret_file = "totp_secret.txt"
        if os.path.exists(self.secret_file):
            os.remove(self.secret_file)

    def test_generate_and_store_secret(self):
        secret1 = get_or_create_totp_secret()
        self.assertTrue(os.path.exists(self.secret_file))
        secret2 = get_or_create_totp_secret()
        self.assertEqual(secret1, secret2)  # Should be same on 2nd call

    def test_verify_valid_code(self):
        secret = get_or_create_totp_secret()
        totp = pyotp.TOTP(secret)
        current_code = totp.now()
        self.assertTrue(verify_totp_code(current_code, secret))

    def test_verify_invalid_code(self):
        secret = get_or_create_totp_secret()
        self.assertFalse(verify_totp_code("000000", secret))

    def test_provisioning_uri_format(self):
        secret = get_or_create_totp_secret()
        uri = get_provisioning_uri("VaultTestUser", "MySecureApp")
        self.assertTrue(uri.startswith("otpauth://totp/"))
        self.assertIn("VaultTestUser", uri)
        self.assertIn("MySecureApp", uri)

    def tearDown(self):
        if os.path.exists(self.secret_file):
            os.remove(self.secret_file)

if __name__ == "__main__":
    unittest.main()
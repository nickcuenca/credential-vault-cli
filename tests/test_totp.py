import unittest
import os
import pyotp
from totp import get_or_create_totp_secret, verify_totp_code, get_provisioning_uri

class TestTOTP(unittest.TestCase):
    def setUp(self):
        # Where the file lives by default
        self.secret_file = "totp_secret.txt"
        # Ensure no leftover env-override or file
        os.environ.pop("TOTP_SECRET", None)
        if os.path.exists(self.secret_file):
            os.remove(self.secret_file)

    def test_env_override_persists_file(self):
        # Simulate production override, but persist to disk for tests
        os.environ["TOTP_SECRET"] = "OVERRIDE_SECRET"
        # File shouldn't exist yet
        if os.path.exists(self.secret_file):
            os.remove(self.secret_file)

        secret = get_or_create_totp_secret()
        self.assertEqual(secret, "OVERRIDE_SECRET")
        # Now the file must exist
        self.assertTrue(os.path.exists(self.secret_file))

        # A second call still returns the same override
        secret2 = get_or_create_totp_secret()
        self.assertEqual(secret2, "OVERRIDE_SECRET")

        # Clean up
        os.environ.pop("TOTP_SECRET", None)

    def test_generate_and_store_secret(self):
        # No env-override → file-based secret
        secret1 = get_or_create_totp_secret()
        self.assertTrue(os.path.exists(self.secret_file))
        secret2 = get_or_create_totp_secret()
        self.assertEqual(secret1, secret2)

    def test_verify_valid_code(self):
        secret = get_or_create_totp_secret()
        totp = pyotp.TOTP(secret)
        code = totp.now()
        self.assertTrue(verify_totp_code(code, secret))

    def test_verify_invalid_code(self):
        secret = get_or_create_totp_secret()
        self.assertFalse(verify_totp_code("000000", secret))

    def test_provisioning_uri_format(self):
        secret = get_or_create_totp_secret()
        uri = get_provisioning_uri("VaultTestUser", "MySecureApp")
        self.assertTrue(uri.startswith("otpauth://totp/"))
        self.assertIn("VaultTestUser", uri)
        self.assertIn("MySecureApp", uri)

    def test_provisioning_uri_with_explicit_secret(self):
        # Cover the branch where secret is passed directly
        uri = get_provisioning_uri("ExplicitUser", "ExplicitApp", secret="EXPLSEED123")
        self.assertTrue(uri.startswith("otpauth://totp/"))
        self.assertIn("ExplicitUser", uri)
        self.assertIn("ExplicitApp", uri)
        self.assertIn("EXPLSEED123", uri)

    def tearDown(self):
        if os.path.exists(self.secret_file):
            os.remove(self.secret_file)

if __name__ == "__main__":
    unittest.main()
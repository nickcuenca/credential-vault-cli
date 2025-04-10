import unittest
from vault import check_password_strength

class TestPasswordStrength(unittest.TestCase):

    def test_weak_passwords(self):
        self.assertEqual(check_password_strength("123"), "🔴 Weak")
        self.assertEqual(check_password_strength("password"), "🔴 Weak")
        self.assertEqual(check_password_strength("abc"), "🔴 Weak")

    def test_medium_passwords(self):
        self.assertEqual(check_password_strength("Password1"), "🟡 Medium")
        self.assertEqual(check_password_strength("abcABC123"), "🟡 Medium")

    def test_strong_passwords(self):
        self.assertEqual(check_password_strength("My$tr0ngP@ss"), "🟢 Strong")
        self.assertEqual(check_password_strength("Th!sIs$ecureVault99"), "🟢 Strong")

if __name__ == '__main__':
    unittest.main()
import string
import unittest

from password_functions import make_password, get_strength, make_hash, check_hash


class PasswordTests(unittest.TestCase):
    def test_password_length(self):
        password = make_password(16)
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_random_length(self):
        password = make_password(None)
        self.assertTrue(8 <= len(password) <= 64)

    def test_password_options(self):
        password = make_password(12, True, False, False, False)
        self.assertTrue(password.islower())

    def test_invalid_password_settings(self):
        with self.assertRaises(ValueError):
            make_password(5)
        with self.assertRaises(ValueError):
            make_password(16, False, False, False, False)

    def test_strength(self):
        self.assertEqual(get_strength("123456")[0], "Weak")
        self.assertEqual(get_strength("ComplexExample!987654")[0], "Strong")

    def test_hash_and_salt(self):
        first = make_hash("ExamplePassword123!")
        second = make_hash("ExamplePassword123!")
        self.assertNotEqual(first, second)
        self.assertNotEqual(first.split("$")[2], second.split("$")[2])
        self.assertTrue(check_hash("ExamplePassword123!", first))
        self.assertFalse(check_hash("wrong", first))

    def test_invalid_hash(self):
        self.assertFalse(check_hash("hello", "not a hash"))
        with self.assertRaises(ValueError):
            make_hash("")


if __name__ == "__main__":
    unittest.main()

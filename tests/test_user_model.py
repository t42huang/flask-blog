import unittest

from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'topsecret')
        self.assertTrue(u.password_hash is not None)
    
    def test_no_password_getter(self):
        u = User(password = 'topsecret')
        with self.assertRaises(AttributeError):
            u.password
        
    def test_password_verification(self):
        u = User(password='topsecret')
        self.assertTrue(u.verify_password('topsecret'))
        self.assertFalse(u.verify_password('topsecret-'))

    def test_password_salts_are_random(self):
        u1 = User(password='topsecret')
        u2 = User(password='topsecret')
        self.assertTrue(u1.password_hash != u2.password_hash)
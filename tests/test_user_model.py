import unittest

from app.models import User, db

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

    def test_valid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()

        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_reset_password_with_corrupted_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()

        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token+'a', 'dog'))
        self.assertTrue(u.verify_password('cat'))
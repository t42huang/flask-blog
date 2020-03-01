import unittest

from datetime import datetime

from app import create_app, db

from app.models import User, Permission, AnonymousUser, Role, Follow

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_user_role(self):
        u = User(email='john@gmail.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
    
    def test_follows(self):
        u1 = User(email='john@example.com', password='cat')
        u2 = User(email='susan@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        
        timestamp_before = datetime.utcnow()
        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        timestamp_after = datetime.utcnow()
        
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        
        f = u1.followed.all()[-1]
        self.assertTrue(f.followed == u2)
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)
        f = u2.followers.all()[-1]
        self.assertTrue(f.follower == u1)
        
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 0)
        self.assertTrue(u2.followers.count() == 0)
        self.assertTrue(Follow.query.count() == 0)
        
        u2.follow(u1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(Follow.query.count() == 0)

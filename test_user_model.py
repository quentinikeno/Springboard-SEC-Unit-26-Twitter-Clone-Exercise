"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
        
        user = User(
            email="test@email.com",
            username="Jane Doe",
            password="GreatPassword123"
        )
        
        user_2 = User(
            email="test2@email.com",
            username="John Smit",
            password="GreatPassword1234"
        )

        db.session.add_all([user, user_2])
        db.session.commit()
        
        self.user = user
        self.user_2 = user_2

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    def test_repr(self):
        """Test the string representation of the User instance."""  
        self.assertEqual(f"{self.user}", f"<User #{self.user.id}: {self.user.username}, {self.user.email}>")
        
    def test_is_following(self):
        """Test if is_following successfully detects when user1 is following user2."""
        self.user.following.append(self.user_2)
        self.assertTrue(self.user.is_following(self.user_2))
        
    def test_is_not_following(self):
        """Test if is_following successfully detects when user1 not is following user2."""
        self.assertFalse(self.user.is_following(self.user_2))
        
    def test_is_followed_by(self):
        """Test if is_followed_by successfully detects when user1 is followed by user2."""
        self.user_2.following.append(self.user)
        self.assertTrue(self.user.is_followed_by(self.user_2))
        
    def test_is_followed_by(self):
        """Test if is_followed_by successfully detects when user1 is not followed by user2."""
        self.assertFalse(self.user.is_followed_by(self.user_2))
        
    def test_user_signup(self):
        """Test if User.signup successfully creats a new user given valid credentials."""
        new_u = User.signup("newUser", "user@email.com", "Unhackable", "testurl.com")
        self.assertEqual(f"{new_u}", f"<User #{new_u.id}: {new_u.username}, {new_u.email}>")
"""Message model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows

from sqlalchemy.exc import IntegrityError
from datetime import datetime

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
        
        user = User.signup(
            "JaneDoe",
            "test@email.com",            
            "GreatPassword123",
            None
        )
        
        user_2 = User.signup(
            "JohnSmith",
            "test2@email.com",            
            "GreatPassword1234",
            None
        )
        
        db.session.commit()
        
        self.user = user
        self.user_2 = user_2
        
    def tearDown(self):
        """Rollback any failed transactions."""
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text="Test Message", timestamp=datetime.utcnow(), user_id=self.user.id)

        db.session.add(m)
        db.session.commit()

        self.assertIsInstance(m, Message)
        
    def test_user_relationship(self):
        """Does the user relationship for Message work?"""
        m = Message(text="Test Message", timestamp=datetime.utcnow(), user_id=self.user.id)

        db.session.add(m)
        db.session.commit()
        
        self.assertEqual(m.user, self.user)
        self.assertNotEqual(m.user, self.user_2)
        
    def test_message_relationship(self):
        """Does the messages relationship for Users work?"""
        m = Message(text="Test Message", timestamp=datetime.utcnow(), user_id=self.user.id)

        db.session.add(m)
        db.session.commit()
        
        self.assertEqual(len(self.user.messages), 1)
        self.assertEqual(self.user.messages[0], m)
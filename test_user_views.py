"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


from cgi import test
import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app
from flask import session
from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        test_user = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None
        )
        
        test_user_2 = User.signup(
            "JohnSmith",
            "test2@email.com",            
            "GreatPassword1234",
            None
        )

        db.session.commit()
        
        self.test_user = test_user
        self.test_user_id = test_user.id
        self.test_user_2 = test_user_2
        self.test_user_id_2 = test_user_2.id
        
    def tearDown(self):
        """Rollback any failed transactions."""
        db.session.rollback()
        
    def test_view_following(self):
        """When you’re logged in, can you see the following pages for any user?"""
        with self.client as c:            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
        
            resp = c.get(f"/users/{self.test_user_id_2}/following")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            
    def test_view_follower(self):
        """When you’re logged in, can you see the follower pages for any user?"""
        with self.client as c:            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user.id
        
            resp = c.get(f"/users/{self.test_user_id_2}/followers")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
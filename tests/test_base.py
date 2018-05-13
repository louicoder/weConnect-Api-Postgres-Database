import unittest
import json
import jwt
import datetime
from manage import db
from flask import request, url_for
from config import Config
from run import app


class BaseTestCase(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app=app
        
        # initialize the test client
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            # This is the user test json data with a predefined username, password and email
            self.user = {
                'username': 'louis',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_no_username = {
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_no_email = {
                'username': 'louis',
                'password': 'password'
            }

            self.user_no_password = {
                'username': 'louis',
                'email': 'louis.michael@gmail.com'
            }

            self.user_login_success = {
                'username': 'louis',
                'password': 'password'
            }

            self.user_not_registered = {
                'username': 'xxxxx',
                'password': 'password'
            }

            self.username_missing_login = {
                'password': 'password'
            }

            self.password_missing_login = {
                'username': 'password'
            }

            self.user_login_failed = {
                'username': 'louis',
                'password': 'pass'
            }

            self.user_with_special_characters = {
                'username': 'louis!',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_short_username = {
                'username': 'loui',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_long_username = {
                'username': 'justalongusername',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_email_dot_missing = {
                'username': 'louis',
                'password': 'password',
                'email': 'michael@gmailcom'
            }

            self.user_email_at_missing = {
                'username': 'louis',
                'password': 'password',
                'email': 'louis.michaelgmail.com'
            }

            self.business_without_data={}

        
            db.session.close()
            db.drop_all()
            db.create_all()

        
    

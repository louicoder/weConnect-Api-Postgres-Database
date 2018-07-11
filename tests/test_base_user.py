import unittest
import json
import jwt
import datetime
from manage import db
from flask import request, url_for
from config import Config
from run import app


class BaseTestUser(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app=app
        
        # initialize the test client
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.client.post('api/')
            email = 'louis.michael@andela.com'
            self.user = {
                'username': 'louis',
                'password': 'password',
                'email': email
                }
            
            self.user1 = {
                'username': 'xxxxx',
                'password': 'password',
                'email': email
                }

            # db.session.close()
            # db.drop_all()
            # db.create_all()

        
    

import unittest
import json
import jwt
import datetime
from manage import db
from flask import request, url_for
from config import Config
from run import app


class BaseTestReviews(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app=app
        
        # initialize the test client
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.user = {
                'username': 'louis',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_login = {
                'username': 'louis',
                'password': 'password',
            }

            self.business={
                'name':'business',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.client.post('/api/auth/logout', content_type='application/json')

            self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

            res = self.client.post('/api/auth/login', data=json.dumps(self.user_login), content_type='application/json')
            data  = json.loads(res.data.decode())
            self.token = data['token']

            self.client.post('/api/businesses', data=json.dumps(self.business), headers={'x-access-token': self.token})

            self.review= {
                'review': 'test review for a business'
            }
            # db.session.close()
import unittest
import json
import jwt
import datetime
from manage import db
from flask import request, url_for
from config import Config
from run import app


class BaseTestBusiness(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app=app
        
        # initialize the test client
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            email = 'louis.michael@andela.com'

            self.user = {
                'username': 'louis',
                'password': 'password',
                'email': email
            }

            self.user1 = {
                'username': 'user1',
                'password': 'password',
                'email': email
            }

            self.client.post('/api/auth/logout', content_type='application/json')

            self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
            self.user.pop('email')
            res = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
            data  = json.loads(res.data.decode())
            self.token = data['token']

            self.business={
                'name':'business',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business1={
                'name':'business1',
                'location':'mukono',
                'category':'bio-tech',
                'description':'service providers of bio-tech chemicals'
            }

            # db.session.close()
            # db.drop_all()
            # db.create_all()
    

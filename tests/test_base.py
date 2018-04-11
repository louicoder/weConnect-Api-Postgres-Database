import unittest
import json
import jwt
import datetime
from manage import db
from flask import request, url_for
from config import Config
from run import app
from main.user.userViews import userBlueprint
from main.business.businessViews import businessBlueprint
from main.reviews.reviewViews import reviewBlueprint

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.testing = True
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()        

        #register user, login the user in and create token for them
        self.client.post(url_for('userBluePrint.create_user'), data=json.dumps(self.user))
        test_user_login = self.client.post(url_for('userBlueprint.login'), data=json.dumps(self.login_user))
        test_user_login_data = json.loads(test_user_login.data.decode())
        self.token = test_user_login_data['message']['token']

        # register new business
        self.client.post(url_for('businessBluePrint.create_business'), data=json.dumps(self.business), headers={'x-access-token': self.token})
        #create the review
        self.client.post(url_for('reviewBlueprint.post_review', id=1), data=json.dumps(self.review), headers={'x-access-token': self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    login_user = {'password': 'password', 'username': 'testuser'}

    user = {
    'username': 'testuser',
    'password': 'password',
    'email': 'testuser@email.com'
    }

    business = {
        'name': 'business 1',
        'location': 'location 1',
        'category': 'category 1',
        'description': 'business description 1'
    }

    review = {'review': 'review 1 for the business'}


    

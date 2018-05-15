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
            
            self.user = {
                'username': 'xuser',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user1 = {
                'username': 'user1',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user_login1 = {
                'username': 'user1',
                'password': 'password',
            }

            self.user_login2 = {
                'username': 'user1',
                'password': 'password',
            }

            self.user_login = {
                'username': 'xuser',
                'password': 'password',
            }

            self.user2 = {
                'username': 'user2',
                'password': 'password',
                'email': 'louis.michael@gmail.com'
            }

            self.user2_login = {
                'username': 'user2',
                'password': 'password',
            }

            

            self.client.post('/api/auth/logout', content_type='application/json')

            self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

            res = self.client.post('/api/auth/login', data=json.dumps(self.user_login), content_type='application/json')
            data  = json.loads(res.data.decode())
            self.token = data['token']

            self.business_without_data={}

            self.business={
                'name':'business',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_update={
                'name':'newbiz',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business1={
                'name':'business1',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business2={
                'name':'business2',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_name_missing={
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_location_missing={
                'name':'business',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_category_missing={
                'name':'business',
                'location':'kampala',
                'description':'service providers for repair of computers'
            }

            self.business_description_missing={
                'name':'business',
                'location':'kampala',
                'category':'technology'
            }

            self.short_business_name={
                'name':'biz',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.long_business_name={
                'name':'longbusinessname',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_update_long_name={
                'name':'updatebusinesslongname',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_update_short_name={
                'name':'name',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            self.business_with_special_characters={
                'name':'name',
                'location':'kampala',
                'category':'technology',
                'description':'service providers for repair of computers'
            }

            # db.session.close()
            # db.drop_all()
            # db.create_all()
            

        
    

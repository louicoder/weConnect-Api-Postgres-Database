import unittest
from .test_base_reviews import BaseTestReviews
from flask import request, url_for, json
from manage import db
from run import app
from main.user.user_views import logged_in_user

class TestReviews(BaseTestReviews):

    def test_no_business_to_review(self):
        self.client.delete('/api/businesses/1', headers={'x-access-token':self.token})
        
        response= self.client.post('/api/businesses/1/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        data = json.loads(response.data.decode())
        self.assertEqual(404, response.status_code)
        self.assertEqual('no businesses exist', data['message'])

    def test_review_non_existing_business(self):
        response= self.client.post('/api/businesses/2/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('no business with that id exists', data['message'])

    def test_review_field_missing(self):
        self.review.pop('review')
        response= self.client.post('/api/businesses/1/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('review field missing', data['message'])

    def test_review_created_successfully(self):
        response= self.client.post('/api/businesses/1/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        data = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual('review has been successfully created', data['message'])

    # def test_business_has_reviews(self):
    #     self.client.post('/api/businesses/1/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual('reviews', data['message'])
    
    # def test_business_not_existing(self):
    #     # self.business['name']= 'business1'
    #     # self.client.delete('/api/businesses/1', headers={'x-access-token':self.token})
    #     self.user.pop('email')
    #     res = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
    #     data  = json.loads(res.data.decode())
    #     token1 = data['token']
    #     res = self.client.post('/api/businesses', data=json.dumps(self.business), headers={'x-access-token': token1})
    #     # data = json.loads(res.data.decode())
    #     # token1 = data['token']
    #     response= self.client.get('/api/businesses/1/reviews', headers={'x-access-token':token1})
    #     data = json.loads(response.data.decode())

    #     self.assertEqual(400, response.status_code)
    #     self.assertEqual('no business with that id exists', data['message'])

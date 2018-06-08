import unittest
from .test_base_reviews import BaseTestReviews
from flask import request, url_for, json
from manage import db
from run import app
from main.user.userViews import logged_in_user

class TestReviews(BaseTestReviews):

    def test_no_business_to_review(self):
        # x = self.client.delete('/api/businesses/1', headers={'x-access-token':self.token})

        response= self.client.post('/api/businesses/1/reviews', data=json.dumps(self.review), headers={'x-access-token':self.token})
        data = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual('review has been successfully created', data['message'])

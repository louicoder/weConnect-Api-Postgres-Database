import unittest
from .test_base import BaseTestCase
from main.user.userViews import userBlueprint
from flask import request, url_for, json
from manage import db
from run import app


class TestBusiness(BaseTestCase):

    def test_no_data_passed(self):
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

        res = self.client.post('/api/auth/login', data=json.dumps(self.user_login_success), content_type='application/json')

        data  = json.loads(res.data.decode())
        token = data['token']

        response = self.client.post('/api/businesses', data=json.dumps(self.business_without_data), content_type='application/json', headers={'x-access-token': token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('fill in all the fields that is name, location, category and description', result['message'])

    def test_length_of_data_keys(self):
        pass

    def test_business_name_missing(self):
        pass

    def test_business_category_missing(self):
        pass

    def test_business_location_missing(self):
        pass

    def test_business_description_missing(self):
        pass

    def test__short_business_name(self):
        pass

    def test_long_business_name(self):
        pass

    def test_business_creation_failed(self):
        pass

    def test_business_already_exists(self):
        pass

    def test_business_creation_successful(self):
        pass

    def test_retrieve_single_business_failed(self):
        pass

    def test_retrieve_single_business_success(self):
        pass

    def test_retrieve_all_businesses_failed(self):
        pass

    def test_retrieve_all_businesses_success(self):
        pass
    
    def test_update_business_without_login(self):
        pass

    def test_update_business_failed(self):
        pass

    def test_update_business_success(self):
        pass

    def test_delete_business_without_login(self):
        pass

    def test_delete_business_not_owned(self):
        pass

    def test_delete_business_failed_bad_id(self):
        pass

    def test_delete_business_success(self):
        pass

    def test_search_business_without_filter_type(self):
        pass

    def test_search_business_without_filter_value(self):
        pass

    def test_unknown_search_filter(self):
        pass



if __name__ == 'main':
    unittest.main()

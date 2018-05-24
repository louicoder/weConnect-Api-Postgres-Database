import unittest
from .test_base_business import BaseTestBusiness
from flask import request, url_for, json
from manage import db
from run import app
from main.user.userViews import logged_in_user


class TestBusiness(BaseTestBusiness):

    def test_no_data_passed(self):
        
        response = self.client.post('/api/businesses', data=json.dumps(self.business_without_data), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('fill in all the fields that is name, location, category and description', result['message'])

    def test_business_name_missing(self):

        response = self.client.post('/api/businesses', data=json.dumps(self.business_name_missing), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business name is missing', result['message'])

    def test_business_location_missing(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.business_location_missing), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business location is missing', result['message'])

    def test_business_category_missing(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.business_category_missing), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business category is missing', result['message'])

    def test_business_description_missing(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.business_description_missing), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business description is missing', result['message'])

    def test_short_business_name(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.short_business_name), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too short, should between five and ten characters', result['message'])

    def test_long_business_name(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.long_business_name), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too long, should between five and ten characters', result['message'])

    def test_special_characters_in_business_name(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.long_business_name), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too long, should between five and ten characters', result['message'])

    def test_business_creation_success(self):
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(201, response.status_code)
        self.assertEqual('business has been successfully created', result['message'])

    def test_business_already_exists(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business already exists, please try again', result['message'])

    def test_retrieve_single_business_failed(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.get('/api/businesses/2', content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(404, response.status_code)
        self.assertEqual('no business with that id exists', result['message'])

    def test_retrieve_single_business_success(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.get('/api/businesses/1', content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertIn('businesses', result.keys())
        self.assertEqual(type(result), dict)

    def test_retrieve_all_businesses_failed(self):
        response = self.client.get('/api/businesses', content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(result['businesses'], [])

    def test_retrieve_all_businesses_success(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        self.client.post('/api/businesses', data=json.dumps(self.business1), content_type='application/json', headers={'x-access-token': self.token})

        self.client.post('/api/businesses', data=json.dumps(self.business2), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.get('/api/businesses', content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())        
        self.assertIsNotNone(result)
        self.assertEqual(200, response.status_code)

    def test_update_business_long_name(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.put('/api/businesses/1', data=json.dumps(self.business_update_long_name), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too long, should between five and ten characters', data['message'])

    def test_update_business_short_name(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.put('/api/businesses/1', data=json.dumps(self.business_update_short_name), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too short, should between five and ten characters', data['message'])

    def test_update_business_special_characters(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.put('/api/businesses/1', data=json.dumps(self.business_with_special_characters), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too short, should between five and ten characters', data['message'])

    def test_delete_business_without_login(self):
        self.client.post('/api/auth/logout', content_type='application/json', headers={'x-access-token': self.token}) 

        response = self.client.delete('/api/businesses/1', data=json.dumps(self.business_with_special_characters), content_type='application/json')
        data  = json.loads(response.data.decode())

        self.assertEqual(401, response.status_code)
        self.assertEqual('Token not valid', data['message'])

    def test_delete_business_not_owned(self):
        pass

    def test_delete_business_failed_bad_id(self):
        response = self.client.delete('/api/businesses/12', data=json.dumps(self.business_with_special_characters), content_type='application/json', headers={'x-access-token': self.token})
        data  = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual('no business with that id exists', data['message'])

    def test_delete_business_success(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        response = self.client.delete('/api/businesses/1', data=json.dumps(self.business_with_special_characters), content_type='application/json', headers={'x-access-token': self.token})
        data  = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        self.assertEqual('business was deleted successfully', data['message'])

    def test_search_business_without_filter_type(self):
        response = self.client.get('/api/businesses/search?q=business&&filter_value=kampala', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        data  = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('invalid or unknown filter type passed in query url', data['message'])


    def test_search_business_without_filter_value(self):
        response = self.client.get('/api/businesses/search?q=business&&filter_type=location', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        data  = json.loads(response.data.decode())
        self.assertEqual(404, response.status_code)
        self.assertEqual('no businesses match your search', data['message'])

    # def test_unknown_search_filter(self):
    #     pass

    # def test_update_business_without_login(self):
    #     self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

    #     self.client.post('/api/auth/logout', content_type='application/json')

    #     response = self.client.put('/api/businesses/1', data=json.dumps(self.business_update), content_type='application/json', headers={'x-access-token': self.token})
        
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(400, response.status_code)
    #     self.assertEqual('please login', data['message'])


if __name__ == 'main':
    unittest.main()

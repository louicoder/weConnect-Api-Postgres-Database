import unittest
from .test_base_business import BaseTestBusiness
from flask import request, url_for, json
from manage import db
from run import app
from main.user.user_views import logged_in_user


class TestBusiness(BaseTestBusiness):

    def test_no_data_passed(self):
        self.business.clear()
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('fill in all the fields that is name, location, category and description', result['message'])

    def test_business_name_missing(self):
        self.business.pop('name')
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business name is missing', result['message'])

    def test_business_location_missing(self):
        self.business.pop('location')
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business location is missing', result['message'])

    def test_business_category_missing(self):
        self.business.pop('category')
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business category is missing', result['message'])

    def test_business_description_missing(self):
        self.business.pop('description')
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
    #     self.assertEqual('business description is missing', result['message'])

    def test_short_business_name(self):
        self.business['name'] = 'name'
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too short, should between five and ten characters', result['message'])

    def test_long_business_name(self):
        self.business['name'] = 'thisisthelongestbusinessnameihaveeverseenintheentireuniverseicannotbelieveit'
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too long, should between five and ten characters', result['message'])

    def test_special_characters_in_business_name(self):
        self.business['name'] = 'business!'
        response = self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business name contains special characters', result['message'])

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
        response = self.client.get('/api/businesses', content_type='application/json', headers={'x-access-token': self.token})

        result = json.loads(response.data.decode())        
        self.assertIsNotNone(result)
        self.assertEqual(200, response.status_code)

    def test_update_business_long_name(self):
        
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        self.business['name']= "averylongnameforthebusinesswhichcannotbeallowedinthesystem"
        response = self.client.put('/api/businesses/1', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too long, should between five and fifty characters', data['message'])

    def test_update_business_short_name(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        self.business['name']= 'name'
        response = self.client.put('/api/businesses/1', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('name of business is too short, should between five and fifty characters', data['message'])

    def test_update_business_special_characters(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        self.business['name']='business!'
        response = self.client.put('/api/businesses/1', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        
        data = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('business name contains special characters', data['message'])

    def test_delete_business_without_login(self):
        self.client.post('/api/auth/logout', content_type='application/json', headers={'x-access-token': self.token}) 

        response = self.client.delete('/api/businesses/1', content_type='application/json')
        data  = json.loads(response.data.decode())

        self.assertEqual(401, response.status_code)
        self.assertEqual('Token not valid', data['message'])

    # def test_delete_business_not_owned(self):
    #     self.client.post('/api/auth/register', data=json.dumps(self.user1), content_type='application/json')
    #     self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
    #     self.client.post('/api/auth/logout', content_type='application/json')
    #     res = self.client.post('/api/auth/login', data=json.dumps(self.user1), content_type='application/json')
    #     data  = json.loads(res.data.decode())
    #     token1 = data['token']
    #     response = self.client.delete('/api/businesses/1', content_type='application/json', headers={'x-access-token': token1})

        # data  = json.loads(response.data.decode())
        # self.assertEqual(400, response.status_code)
        # self.assertEqual('business was not deleted because you are not the owner', data['message'])

    def test_delete_business_failed_bad_id(self):
        response = self.client.delete('/api/businesses/12', content_type='application/json', headers={'x-access-token': self.token})
        data  = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual('no business with that id exists', data['message'])

    def test_delete_business_success(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        response = self.client.delete('/api/businesses/1', content_type='application/json', headers={'x-access-token': self.token})

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

    def test_unknown_search_filter(self):
        response = self.client.get('/api/businesses/search?q=business', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})

        data  = json.loads(response.data.decode())
        self.assertEqual(400, response.status_code)
        self.assertEqual('invalid or unknown filter type passed in query url', data['message'])

    def test_update_business_without_login(self):
        self.client.post('/api/businesses', data=json.dumps(self.business), content_type='application/json', headers={'x-access-token': self.token})
        self.client.post('/api/auth/logout', content_type='application/json')
        response = self.client.put('/api/businesses/1', data=json.dumps(self.business), content_type='application/json')
        
        data = json.loads(response.data.decode())
        self.assertEqual(401, response.status_code)
        self.assertEqual('Token not valid', data['message'])


if __name__ == 'main':
    unittest.main()

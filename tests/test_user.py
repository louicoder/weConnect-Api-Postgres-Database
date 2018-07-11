import unittest
from .test_base_user import BaseTestUser
from flask import request, url_for, json
from manage import db
from run import app

class Testuser(BaseTestUser):

    def test_username_missing_registration(self):
        self.user.pop('username')
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "username is missing")
        self.assertEqual(400, response.status_code)

    def test_username_special_characters_registration(self):
        self.user['username'] = 'louis!'
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "username contains special characters")
        self.assertEqual(400, response.status_code)

    def test_short_username_registration(self):
        self.user['username'] = 'loui'
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "username too short, should be between five and ten characters")
        self.assertEqual(400, response.status_code)

    def test_short_passwors_registration(self):
        self.user['password'] = 'loui'
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "password too short, should be between five and ten characters")
        self.assertEqual(400, response.status_code)

    def test_long_username_registration(self):
        self.user['username'] = 'lougusername'
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "username too long, should be between five and ten characters")
        self.assertEqual(400, response.status_code)

    def test_email_missing_registration(self):
        self.user.pop('email')
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "email is missing")
        self.assertEqual(400, response.status_code)

    def test_password_missing_registration(self):
        self.user.pop('password')
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "password is missing")
        self.assertEqual(400, response.status_code)

    def test_exists_registration(self):
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual("user already exists", result['message'])
        self.assertEqual(400, response.status_code)

    def test_invalid_email(self):
        self.user['email'] = 'louis@com'
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "email is not in valid format")
        self.assertEqual(400, response.status_code)

    def test_registration_successful(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual("user successfully registered", result['message'])
        self.assertEqual(201, response.status_code)

    def test_username_missing_login(self):
        self.user.pop('email')
        self.user.pop('username')
        self.client.post('/api/auth/logout', content_type='application/json')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())     
        self.assertEqual(result['message'], "username missing")
        self.assertEqual(400, response.status_code)

    def test_password_missing_login(self):
        self.user.pop('email')
        self.user.pop('password')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())     
        self.assertEqual(result['message'], "password missing")
        self.assertEqual(400, response.status_code)

    def test_non_registered_user_login(self):
        self.client.post('/api/auth/logout', content_type='application/json')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user1), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual("wrong username or password or user not registered", result['message'])
        self.assertEqual(400, response.status_code)

    # def test_xalready_logged_in(self):
    #     self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
    #     self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
    #     response = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(data['message'], "you are already logged in")
    #     self.assertEqual(400, response.status_code)

    def test_login_successful(self):
        
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        self.user.pop('email')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "successfully logged in")
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['token'])


if __name__ == 'main':
    unittest.main()
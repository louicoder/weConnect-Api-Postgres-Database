import unittest
from .test_base_user import BaseTestUser
from flask import request, url_for, json
from manage import db
from run import app


class Testuser(BaseTestUser):

    def test_username_missing_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_no_username), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "username is missing")
        self.assertEqual(400, response.status_code)

    def test_username_special_characters_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_with_special_characters), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "username contains special characters")
        self.assertEqual(400, response.status_code)

    def test_short_username_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_short_username), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "username too short, should be between five and ten characters")
        self.assertEqual(400, response.status_code)

    def test_long_username_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_long_username), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "username too long, should be between five and ten characters")
        self.assertEqual(400, response.status_code)

    def test_email_missing_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_no_email), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "email is missing")
        self.assertEqual(400, response.status_code)

    def test_password_missing_registration(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_no_password), content_type='application/json')

        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "password is missing")
        self.assertEqual(400, response.status_code)

    def test_user_exists_registration(self):
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "user already exists")
        self.assertEqual(400, response.status_code)

    def test_dot_mising_user_email(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_email_dot_missing), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "email is invalid, dot missing")
        self.assertEqual(400, response.status_code)

    def test_at_mising_user_email(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user_email_at_missing), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "email is invalid, @ symbol missing")
        self.assertEqual(400, response.status_code)

    def test_user_registration_successful(self):
        response = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "user successfully registered")
        self.assertEqual(201, response.status_code)

    def test_ausername_missing_login(self):
        response = self.client.post('/api/auth/login', data=json.dumps(self.username_missing_login), content_type='application/json')
        result = json.loads(response.data.decode())     
        # self.assertEqual(result['message'], "username missing")
        self.assertEqual(400, response.status_code)

    def test_password_missing_login(self):
        response = self.client.post('/api/auth/login', data=json.dumps(self.password_missing_login), content_type='application/json')
        result = json.loads(response.data.decode())     
        # self.assertEqual(result['message'], "password missing")
        self.assertEqual(400, response.status_code)

    def test_non_registered_user_login(self):
        response = self.client.post('/api/auth/login', data=json.dumps(self.user_not_registered), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['message'] == "wrong username or password or user not registered")
        self.assertEqual(400, response.status_code)

    def test_xuser_already_logged_in(self):
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "you are already logged in")
        self.assertEqual(400, response.status_code)

    def test_user_login_successful(self):
        self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        response = self.client.post('/api/auth/login', data=json.dumps(self.user_login_success), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "successfully logged in")
        self.assertEqual(200, response.status_code)
        self.assertTrue(data['token'])


if __name__ == 'main':
    unittest.main()
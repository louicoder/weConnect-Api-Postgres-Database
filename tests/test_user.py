import unittest
# from test_base import BaseTestCase
from main.user.userViews import userBlueprint
from flask import request, url_for, json
from manage import db
from run import app


class Testuser(unittest.TestCase):

    login_user = {'password': 'password', 'username': 'louis'}

    user1 = {
    'username': 'yyyy',
    'password': 'password',
    'email': 'testuser@email.com'
    }

    user = {
    'username': 'xxxxx',
    'password': 'password',
    'email': 'louis@email.com'
    }

    token = None

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.testing = True
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()

        # self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        # res = request.get
        # login = self.client.post('/api/auth/login', data=json.dumps({'password': 'person', 'username': 'louis'}), with self.client:
        
    
    def test_user_registration_success(self):
        print('here')
        x = self.client.post('/api/auth/register', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post('/api/auth/login', data=json.dumps(self.user))
        # print(res)
        # print(x)
        # test_user_login_data = json.loads(x.data.decode())
        # print(test_user_login_data)
        # self.token = test_user_login_data['message']['token']
        # response = self.client.post('api/auth/register', data = json.dumps(self.user))
        self.assertEqual(200, res.status_code)
        self.assertEqual(201, x.status_code)

    # def test_user_login(self):
    #     print('here')
    #     response = self.client.post(
    #         '/api/auth/login',
    #         data=json.dumps(dict(
    #             username='xxxxx',
    #             password='password'
    #         )),
    #         content_type='application/json'
    #     )

    #     data = json.loads(response.data.decode())
    #     self.assertTrue(data['message'] == 'successfully logged in')

    # def test_user_login(self):
    #     response = self.client.post('/api/auth/login', data=json.dumps(self.user1))

    #     self.assertEqual(200, response.status_code)


    def tearDown(self):        
        # db.drop_all()
        # db.create_all()
        # db.session.close()
        pass
        

if __name__ == 'main':
    unittest.main()
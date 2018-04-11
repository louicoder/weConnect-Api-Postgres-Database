import unittest
from test_base import BaseTestCase
from flask import request, url_for

class Testuser(BaseTestCase):
    
    def test_user_registration(self):
        response = self.client.post(
            url_for('api.create_user'), data = json.dumps(self.user)
        )

        self.assertEqual(201, response.status_code)


if __name__ == 'main':
    unittest.main()
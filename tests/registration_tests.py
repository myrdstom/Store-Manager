import unittest
import json
from tests.base import BaseTestCase

user_data = {

    'username': 'myrdstom',
    'password': 'password'
}


class FlaskTestCase(BaseTestCase):
    """Users tests"""

    def test_email_poorly_added(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="test",
                                                        password="password",
                                                        email="bgpetergmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Error: invalid email: Please check email', response.data)

    def test_existing_username(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 409)
            self.assertIn(b'A user with that username already exists', response.data)

    # def test_existing_email(self):
    #     with self.app.test_client() as client:
    #         response = client.post("v1/auth/signup", content_type='application/json',
    #                                data=json.dumps(dict(username="myrdstom",
    #                                                     password="password",
    #                                                     email="nserekopaul@gmail.com")))
    #         self.assertEqual(response.status_code, 201)
    #         response = client.post("v1/auth/signup", content_type='application/json',
    #                                data=json.dumps(dict(username="testa",
    #                                                     password="password",
    #                                                     email="nserekopaul@gmail.com")))
    #         self.assertEqual(response.status_code, 409)
    #         self.assertIn(b'A user with that email already exists', response.data)
    #
    def test_create_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User successfully registered', response.data)
    #
    # def test_missing_values(self):
    #     with self.app.test_client() as client:
    #         response = client.post("v1/auth/signup", content_type='application/json',
    #                                data=json.dumps(dict(username="  ",
    #                                                     password="password",
    #                                                     email="Angela@gmail.com")))
    #         self.assertEqual(response.status_code, 400)
    #         self.assertIn(b'please fill all fields', response.data)


if __name__ == '__main__':
    unittest.main()
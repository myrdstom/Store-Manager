import unittest
import json
from tests.base import BaseTestCase

user_data = {

    'username': 'myrdstom',
    'password': 'password'
}


class FlaskTestCase(BaseTestCase):
    """Users tests"""

    """Testing Sign Up endpoint"""

    """Testing a poorly added email"""

    def test_email_poorly_added(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="test",
                                                        password="password",
                                                        email="bgpetergmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Error: invalid email: Please check email', response.data)

    """Testing for an existing username"""

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

    """Testing for an existing email"""

    def test_existing_email(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response = client.post("api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="testa",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 409)
            self.assertIn(b'A user with that email already exists', response.data)

    """Testing successfully creating a user"""

    def test_create_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User successfully registered', response.data)

    """Testing for missing values when signing up"""

    def test_missing_values(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", content_type='application/json',
                                   data=json.dumps(dict(username="  ",
                                                        password="password",
                                                        email="Angela@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'please fill all fields', response.data)

    """Implement tests for the login endpoint"""

    """Testing missing values for the login endpoint"""
    def test_missing_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="  ",
                                                        password="password",
                                                        email="Angela@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'please fill all fields', response.data)


    """Testing incorrect values for the log in endpoint"""
    def test_incorrect_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username=123,
                                                        password="password",
                                                        email="Angela@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Testing username not in database for the log in endpoint"""

    def test_non_existent_username(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="Kayongo",
                                                        password="password",
                                                        email="Angela@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'The user does not exist, please register', response.data)


if __name__ == '__main__':
    unittest.main()

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

    """Testing for an existing username"""

    def test_existing_username(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", headers={'Content-Type': 'application/json',
                                                             'Authorization': 'Bearer ' +
                                                                              self.admin_login()[
                                                                                  'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password")))
            self.assertEqual(response.status_code, 201)
            response = client.post("api/v1/signup", headers={'Content-Type': 'application/json',
                                                             'Authorization': 'Bearer ' +
                                                                              self.admin_login()[
                                                                                  'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password")))
            self.assertEqual(response.status_code, 409)
            self.assertIn(b'A user with that username already exists', response.data)

    #

    """Testing successfully creating a user"""

    def test_create_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password")))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User successfully registered', response.data)


    """Test authority to signup a user"""

    def test_missing_values(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.login_user()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="  ",
                                                        password="password")))
            self.assertEqual(response.status_code, 409)
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    """Testing for missing values when signing up"""

    def test_missing_values(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="  ",
                                                        password="password")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Implement tests for the login endpoint"""

    """Testing missing values for the login endpoint"""

    def test_missing_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="  ",
                                                        password="password")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Testing incorrect values for the log in endpoint"""

    def test_incorrect_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username=123,
                                                        password="password")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Testing username not in database for the log in endpoint"""

    def test_non_existent_username(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="Kayongo",
                                                        password="password")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'The user does not exist, please register', response.data)


if __name__ == '__main__':
    unittest.main()

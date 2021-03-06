import unittest
import json
from tests.base import BaseTestCase


class FlaskTestCase(BaseTestCase):
    """Users tests"""

    """Testing Sign Up endpoint"""

    """Testing for an existing username"""

    def test_existing_username(self):
        with self.app.test_client() as client:
            response = client.post("api/v1/signup", headers={'Content-Type': 'application/json',
                                                             'Authorization': 'Bearer ' +
                                                                              self.admin_login()[
                                                                                  'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response = client.post("api/v1/signup", headers={'Content-Type': 'application/json',
                                                             'Authorization': 'Bearer ' +
                                                                              self.admin_login()[
                                                                                  'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 409)
            self.assertIn(b'A user with those credentials already exists', response.data)

    #

    """Testing successfully creating a user"""

    def test_create_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User successfully registered', response.data)

    """Test authority to signup a user"""

    def test_authority_to_access_user_registration(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User successfully registered', response.data)
            response2 = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                               'Authorization': 'Bearer ' +
                                                                                self.login_user()[
                                                                                    'access_token']},
                                    data=json.dumps(dict(username="myrdstom",
                                                         password="password",
                                                         email="bgpeter@gmail.com")))
            self.assertEqual(response2.status_code, 401)
            responseJson = json.loads(response2.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    """Testing for missing values when signing up"""

    def test_missing_values(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="  ",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Testing promoting a user"""

    def test_promote_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response1 = client.put("/api/v1/signup/2", headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(dict(role="store-owner")))
            self.assertEqual(response1.status_code, 200)
            self.assertIn(b'User has been promoted', response1.data)

    """Testing invalid user role"""

    def test_invalid_user_role(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response1 = client.put("/api/v1/signup/2", headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(dict(role="store-ownerrr")))
            self.assertEqual(response1.status_code, 400)
            self.assertIn(b'Invalid role, please try again', response1.data)

    """Testing promoting a non-existent user"""

    def test_promote_non_existent_user(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/signup", headers={'Content-Type': 'application/json',
                                                              'Authorization': 'Bearer ' +
                                                                               self.admin_login()[
                                                                                   'access_token']},
                                   data=json.dumps(dict(username="myrdstom",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 201)
            response1 = client.put("/api/v1/signup/2000", headers={'Content-Type': 'application/json',
                                                                   'Authorization': 'Bearer ' +
                                                                                    self.admin_login()[
                                                                                        'access_token']},
                                   data=json.dumps(dict(role="store-owner")))
            self.assertEqual(response1.status_code, 400)
            self.assertIn(b'User does not exist', response1.data)

    """Test right to access endpoint"""

    def test_authority_to_access_endpoint(self):
        with self.app.test_client() as client:
            response1 = client.put("/api/v1/signup/200", headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.login_user()[
                                                                                       'access_token']},
                                   data=json.dumps(dict(role="store-owner")))
            self.assertEqual(response1.status_code, 401)
            self.assertIn(b'you are not authorized to view this resource', response1.data)

    """Implement tests for the login endpoint"""

    """Testing missing values for the login endpoint"""

    def test_missing_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="  ",
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Please review the values added', response.data)

    """Testing incorrect values for the log in endpoint"""

    def test_incorrect_values_when_logging_in(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username=123,
                                                        password="password",
                                                        email="nserekopaul@gmail.com")))
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

    """Testing incorrect password"""

    def test_invalid_password(self):
        with self.app.test_client() as client:
            response = client.post("/api/v1/login", content_type='application/json',
                                   data=json.dumps(dict(username="admin",
                                                        password="password2",
                                                        email="admin@gmail.com")))
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Error: wrong password', response.data)


if __name__ == '__main__':
    unittest.main()

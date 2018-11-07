import unittest
import json
from tests.base import BaseTestCase

empty_product_data = {}

category_data = dict(category_name="laptop")


class FlaskTestCase(BaseTestCase):
    """Category tests"""

    """POST endpoint"""

    """Test authority to access various category endpoints"""

    def test_authority_to_post(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.login_user()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 409)
            responseJson = json.loads(response.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    """Test add a new category"""

    def test_add_new_category_item(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('category created', responseJson['message'])

    """Test posting a duplicate category"""

    def test_add_duplicate_category_item(self):
        with self.app.test_client() as client:
            response1 = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                   'Authorization': 'Bearer ' +
                                                                                    self.admin_login()[
                                                                                        'access_token']},
                                    data=json.dumps(category_data))
            self.assertEqual(response1.status_code, 201)
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 409)
            responseJson = json.loads(response.data.decode())
            self.assertIn('A category with that product name already exists', responseJson['message'])

    """Test invalid category data"""

    def test_invalid_category_data(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(dict(category_name=8876)))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please review the values added', responseJson['message'])

    """PUT endpoint"""

    """Test succesfully editing a category"""

    def test_edit_category_item(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.put('/api/v1/categories/1', headers={'Content-Type': 'application/json',
                                                                    'Authorization': 'Bearer ' +
                                                                                     self.admin_login()[
                                                                                         'access_token']},
                                   data=json.dumps(dict(category_name="accessories")))
            self.assertEqual(response1.status_code, 201)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('accessories', responseJson['category_name'])

    """Test editing non-existent category"""

    def test_edit_non_existent_category_item(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.put('/api/v1/categories/100', headers={'Content-Type': 'application/json',
                                                                      'Authorization': 'Bearer ' +
                                                                                       self.admin_login()[
                                                                                           'access_token']},
                                   data=json.dumps(dict(category_name="accessories")))
            self.assertEqual(response1.status_code, 400)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('no such entry found', responseJson['message'])

    """Test editing a category with wrong values"""

    def test_edit_a_category_with_wrong_values(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.put('/api/v1/categories/1', headers={'Content-Type': 'application/json',
                                                                      'Authorization': 'Bearer ' +
                                                                                       self.admin_login()[
                                                                                           'access_token']},
                                   data=json.dumps(dict(category_name=888)))
            self.assertEqual(response1.status_code, 400)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('Please review the values added', responseJson['message'])

    """Test authority to edit a category"""

    def test_authority_to_edit(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.put('/api/v1/categories/1', headers={'Content-Type': 'application/json',
                                                                    'Authorization': 'Bearer ' +
                                                                                     self.login_user()[
                                                                                         'access_token']},
                                   data=json.dumps(dict(category_name="accessories")))
            self.assertEqual(response1.status_code, 409)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    """GET endpoint"""

    """Test view all categories"""

    def test_view_all_categories(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.get('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(dict(category_data)))
            self.assertEqual(response1.status_code, 200)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('laptop', responseJson[0]['category_name'])

    """Test empty database"""

    def test_view_empty_categories(self):
        with self.app.test_client() as client:
            response1 = client.get('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(dict(category_data)))
            self.assertEqual(response1.status_code, 200)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('There are no values in the database', responseJson['message'])

    """Test authority to access endpoint"""

    def test_authority_to_view_categories(self):
        with self.app.test_client() as client:
            response1 = client.get('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.login_user()[
                                                                                       'access_token']},
                                   data=json.dumps(dict(category_data)))
            self.assertEqual(response1.status_code, 409)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    """DELETE endpoint"""
    """Test delete a category"""

    def test_delete_a_category(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response2 = client.delete('/api/v1/categories/1', headers={'Content-Type': 'application/json',
                                                                       'Authorization': 'Bearer ' +
                                                                                        self.admin_login()[
                                                                                            'access_token']},
                                      data=json.dumps(category_data))
            self.assertEqual(response2.status_code, 200)
            responseJson = json.loads(response2.data.decode())
            self.assertIn('Record successfully deleted', responseJson['message'])

    """Delete a non-existent category"""
    def test_delete_a_non_existent_category(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response2 = client.delete('/api/v1/categories/100', headers={'Content-Type': 'application/json',
                                                                       'Authorization': 'Bearer ' +
                                                                                        self.admin_login()[
                                                                                            'access_token']},
                                      data=json.dumps(category_data))
            self.assertEqual(response2.status_code, 200)
            responseJson = json.loads(response2.data.decode())
            self.assertIn('Category does not exist', responseJson['message'])


    """Test authority to access endpoint"""
    def test_authority_to_delete_category(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response2 = client.delete('/api/v1/categories/100', headers={'Content-Type': 'application/json',
                                                                       'Authorization': 'Bearer ' +
                                                                                        self.login_user()[
                                                                                            'access_token']},
                                      data=json.dumps(category_data))
            self.assertEqual(response2.status_code, 409)
            responseJson = json.loads(response2.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    if __name__ == '__main__':
        unittest.main()

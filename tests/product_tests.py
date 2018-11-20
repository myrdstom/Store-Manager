import unittest
import json
from tests.base import BaseTestCase

product_data = dict(product_name="acer",
                    unit_price=19000000,
                    stock=100,
                    category_name="laptop")

sale_data = dict(product_name="acer",
                 quantity=32)

empty_product_data = {}

category_data = dict(category_name="laptop")


class FlaskTestCase(BaseTestCase):
    """Products tests"""

    def test_invalid_url(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1//products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                   data=json.dumps(product_data))
            self.assertEqual(response.status_code, 404)
            responseJson = json.loads(response.data.decode())
            self.assertIn('The requested Resource does not exist; Please review the URL', responseJson['message'])

    """POST endpoints"""

    """Test adding a new item to the inventory"""
    """Testing for missing POST column"""

    def test_missing_POST_column(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' +
                                                             self.admin_login()[
                                                                 'access_token']},
                                   data=json.dumps(dict(unit_price=19000000,
                                                        stock=100)))
            self.assertEqual(response.status_code, 409)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Something went wrong with your inputs: Please review them', responseJson['message'])

    def test_add_new_inventory_item(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(response.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('product created', responseJson['message'])

        """Test duplicate product"""

    def test_adding_duplicate_data(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(product_data))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('product created', responseJson['message'])
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 409)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('A product with that product name already exists', responseJson['message'])

        """Test the product does not exist"""

    def test_product_does_not_exist(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.get("/api/v1/products/100",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(product_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('the product does not exist', response_json['message'])

    """Test authority to create a product"""

    def test_authority_to_create_a_product(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.login_user()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 401)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

        """testing  GET all items in the inventory"""

    def test_get_all_inventory_items(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.get("/api/v1/products",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(product_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("acer", response_json[0]['product_name'])

    """Testing for empty space"""

    def test_empty_space(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' +
                                                             self.admin_login()[
                                                                 'access_token']},
                                   data=json.dumps(dict(product_name=" ",
                                                        unit_price=19000000,
                                                        stock=100,
                                                        category_name="laptop")))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please review the values added', responseJson['message'])

    """Testing non-exsiting category when creating a POST"""
    def test_non_existent_POST_category(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' +
                                                             self.admin_login()[
                                                                 'access_token']},
                                   data=json.dumps(dict(product_name="acer",
                                                        unit_price=19000000,
                                                        stock=100,
                                                        category_name="laptops")))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('category does not exist', responseJson['message'])

    """GET endpoint"""

    """test empty product data"""

    def test_no_product_in_inventory(self):
        with self.app.test_client() as client:
            response = client.get("/api/v1/products",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(empty_product_data))
            response_json = json.loads(response.data.decode())
            self.assertIn('There are no values in the database', response_json['message'])

        """testing  GET a single item in the inventory"""

    def test_get_one_item_in_inventory(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.get("/api/v1/products/1",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(product_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    """testing  GET a single item in the inventory"""

    def test_inventory_item_does_not_exist(self):
        with self.app.test_client() as client:
            response = client.get("/api/v1/products/20",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(product_data))
            responseJson = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)



        """Testing the edit product endpoint"""

    def test_edit_a_product(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/1',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(dict(product_name="water",
                                                       unit_price=2000,
                                                       stock=100,
                                                       category_name="laptop")))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn("water", responseJson['product_name'])

    """Test Category does not exist"""
    def test_edit_non_existent_category(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/1',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(dict(product_name="water",
                                                       unit_price=2000,
                                                       stock=100,
                                                       category_name="laptops")))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn("Category does not exist", responseJson['message'])

    """Test authority to access this endpoint"""
    def test_authority_to_edit(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/1',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.login_user()[
                                                                'access_token']},
                                  data=json.dumps(dict(product_name="water",
                                                       unit_price=2000,
                                                       stock=100)))
            self.assertEqual(response.status_code, 401)
            responseJson = json.loads(response.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

        """Test missing PUT columns"""

    def test_invalid_edit_column(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/1',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(dict(unit_price=2000,
                                                       stock=100)))
            self.assertEqual(response.status_code, 409)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Something went wrong with your inputs: Please review them', responseJson['message'])

    """Testing editing a non-existent product"""
    def test_edit_a_non_existent_product(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/10',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(dict(product_name="water",
                                                       unit_price=2000,
                                                       stock=100,
                                                       category_name="laptop")))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('no such entry found', responseJson['message'])

    """Testing invalid data in PUT columns"""

    def test_invalid_data_in_put_columns(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.put('/api/v1/products/10',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(dict(product_name="water",
                                                       unit_price="water",
                                                       stock=100,
                                                       category_name="laptop")))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please review the values added', responseJson['message'])

    """DELETE Endpoint"""

    """Test deleting non-existing record"""
    def test_delete_a_non_existent_product(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(product_data))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('product created', responseJson['message'])
            response = client.delete('/api/v1/products/10',
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': 'Bearer ' +
                                                               self.admin_login()[
                                                                   'access_token']})
            self.assertEqual(response.status_code, 200)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Product does not exist', responseJson['message'])


    """Test deleting a record"""

    def test_delete_a_product(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(product_data))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('product created', responseJson['message'])
            response = client.delete('/api/v1/products/1',
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': 'Bearer ' +
                                                               self.admin_login()[
                                                                   'access_token']})
            self.assertEqual(response.status_code, 200)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Record successfully deleted', responseJson['message'])

    """Test the authority to delete an item"""
    def test_authority_to_delete(self):
        with self.app.test_client() as client:
            category = client.post('/api/v1/categories', headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer ' +
                                                                                   self.admin_login()[
                                                                                       'access_token']},
                                   data=json.dumps(category_data))
            self.assertEqual(category.status_code, 201)
            response = client.delete('/api/v1/products/10',
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': 'Bearer ' +
                                                               self.login_user()[
                                                                   'access_token']})
            self.assertEqual(response.status_code, 401)
            responseJson = json.loads(response.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])


    if __name__ == '__main__':
        unittest.main()

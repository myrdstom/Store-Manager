import unittest
import json
from tests.base import BaseTestCase

product_data = dict(product_name="Acer",
                    unit_price=19000000,
                    stock=100)

sale_data = dict(product_name="Acer",
                 quantity=32)

empty_product_data = {}


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

    """Test adding a new item to the inventory"""
    def test_add_new_inventory_item(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                'Authorization': 'Bearer ' +
                                                                                 self.admin_login()[
                                                                                     'access_token']},
                                   data=json.dumps(product_data))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn('product created', responseJson['message'])

    """Test duplicate product"""
    def test_add_new_inventory_item(self):
        with self.app.test_client() as client:
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
            response1 = client.post('/api/v1/products', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.login_user()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 409)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])


    """testing  GET all items in the inventory"""

    def test_get_all_inventory_items(self):
        with self.app.test_client() as client:
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
            self.assertIn("Acer", response_json[0]['product_name'])

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

    """Testing for empty space"""

    def test_empty_space(self):
        with self.app.test_client() as client:
            response = client.post('/api/v1/products',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' +
                                                             self.admin_login()[
                                                                 'access_token']},
                                   data=json.dumps(dict(product_name=" ",
                                                        unit_price=19000000,
                                                        stock=100)))
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Please review the values added', responseJson['message'])

    """Testing the edit product endpoint"""

    def test_edit_a_product(self):
        with self.app.test_client() as client:
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
                                                       stock=100)))
            self.assertEqual(response.status_code, 201)
            responseJson = json.loads(response.data.decode())
            self.assertIn("water", responseJson['product_name'])

    def test_delete_a_product(self):
        with self.app.test_client() as client:
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
            self.assertEqual(response.status_code, 400)
            responseJson = json.loads(response.data.decode())
            self.assertIn('Product does not exist', responseJson['message'])



    def test_get_all_items_sold(self):
        with self.app.test_client() as client:
            response1 = client.post('/api/v1/products',
                                    headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.post("/api/v1/sales",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.login_user()[
                                                                'access_token']},
                                  data=json.dumps(sale_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = client.get("/api/v1/sales",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                 data=json.dumps(sale_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Acer", response_json[0]['product_name'])

    """testing  GET a single sale"""

    def test_get_one_sale(self):
        with self.app.test_client() as client:
            response1 = client.post('/api/v1/products',
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' +
                                                              self.admin_login()[
                                                                  'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.post("/api/v1/sales",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' +
                                                             self.login_user()[
                                                                 'access_token']},
                                   data=json.dumps(sale_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            response = client.get("/api/v1/sales/1",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.admin_login()[
                                                                'access_token']},
                                  data=json.dumps(sale_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Acer", response_json['product_name'])
#     #
    """testing adding a sale"""

    def test_add_a_sale(self):
        with self.app.test_client() as client:
            response1 = client.post('/api/v1/products',
                                    headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 201)
            response = client.post("/api/v1/sales",
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' +
                                                            self.login_user()[
                                                                'access_token']},
                                  data=json.dumps(sale_data))
            response_json = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    """Test authority to post a sale"""

    def test_authority_to_create_a_sale(self):
        with self.app.test_client() as client:
            response1 = client.post('/api/v1/sales', headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(product_data))
            self.assertEqual(response1.status_code, 409)
            responseJson = json.loads(response1.data.decode())
            self.assertIn('you are not authorized to view this resource', responseJson['message'])

    #     #
#     # """Testing for wrong column name"""
#     #
#     # def test_wrong_sale_column_name(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/sales', content_type='application/json',
#     #                                data=json.dumps(dict(product_idd=1,
#     #                                                     quantity=32)))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('Please review the columns', responseJson['message'])
#     #
#     # """Testing for wrong data type in post sale"""
#     #
#     # def test_wrong_sale_data_type(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/sales', content_type='application/json',
#     #                                data=json.dumps(dict(product_id="1",
#     #                                                     quantity=32)))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('Error:Invalid value added, please review', responseJson['message'])
#     #

    if __name__ == '__main__':
        unittest.main()

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
    """Sales tests"""
#
#     def test_get_all_items_sold(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             response = client.get("/api/v1/sales",
#                                   headers={'Content-Type': 'application/json',
#                                            'Authorization': 'Bearer ' +
#                                                             self.admin_login()[
#                                                                 'access_token']},
#                                   data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("acer", response_json[0]['product_name'])
#
#     """testing  GET a single sale"""
#
#     def test_get_one_sale(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             response = client.get("/api/v1/sales/1",
#                                   headers={'Content-Type': 'application/json',
#                                            'Authorization': 'Bearer ' +
#                                                             self.admin_login()[
#                                                                 'access_token']},
#                                   data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("acer", response_json['product_name'])
#
#     """Test sale does not exist"""
#
#     def test_sale_does_not_exist(self):
#         with self.app.test_client() as client:
#             response = client.get("/api/v1/sales/100",
#                                   headers={'Content-Type': 'application/json',
#                                            'Authorization': 'Bearer ' +
#                                                             self.admin_login()[
#                                                                 'access_token']},
#                                   data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('Sale does not exist', response_json['message'])
#
#     """Test empty database"""
#
#     def test_empty_database(self):
#         with self.app.test_client() as client:
#             response = client.get("/api/v1/sales",
#                                   headers={'Content-Type': 'application/json',
#                                            'Authorization': 'Bearer ' +
#                                                             self.admin_login()[
#                                                                 'access_token']},
#                                   data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('There are no values in the database', response_json['message'])
#
#     """testing adding a sale"""
#
#     def test_add_a_sale(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(sale_data))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#
#     """Test authority to post a sale"""
#
#     def test_authority_to_create_a_sale(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/sales', headers={'Content-Type': 'application/json',
#                                                               'Authorization': 'Bearer ' +
#                                                                                self.admin_login()[
#                                                                                    'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 409)
#             responseJson = json.loads(response1.data.decode())
#             self.assertIn('you are not authorized to view this resource', responseJson['message'])
#
#     """Testing for wrong column name"""
#
#     def test_wrong_sale_column_name(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post('/api/v1/sales', headers={'Content-Type': 'application/json',
#                                                              'Authorization': 'Bearer ' +
#                                                                               self.login_user()[
#                                                                                   'access_token']},
#                                    data=json.dumps(dict(quantity=32)))
#             self.assertEqual(response.status_code, 409)
#             responseJson = json.loads(response.data.decode())
#             self.assertIn('Something went wrong with your inputs: Please review them', responseJson['message'])
#
#     """Test wrong data type for sale endpoint"""
#
#     def test_wrong_data_type_for_sale(self):
#         with self.app.test_client() as client:
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(dict(product_name="acer",
#                                                         quantity=32)))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 400)
#             self.assertIn('Product does not exist', response_json['message'])
#
#
#     """Test limited stock"""
#     def test_not_enough_stock(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(dict(product_name="acer",
#                                                         quantity=320)))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 400)
#             self.assertIn('not enough in stock for you to purchase that amount', response_json['message'])
#
#
#     """Test limited stock"""
#     def test_invalid_stock_data_types(self):
#         with self.app.test_client() as client:
#             response1 = client.post('/api/v1/products',
#                                     headers={'Content-Type': 'application/json',
#                                              'Authorization': 'Bearer ' +
#                                                               self.admin_login()[
#                                                                   'access_token']},
#                                     data=json.dumps(product_data))
#             self.assertEqual(response1.status_code, 201)
#             response = client.post("/api/v1/sales",
#                                    headers={'Content-Type': 'application/json',
#                                             'Authorization': 'Bearer ' +
#                                                              self.login_user()[
#                                                                  'access_token']},
#                                    data=json.dumps(dict(product_name="acer",
#                                                         quantity="340")))
#             response_json = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 400)
#             self.assertIn('Error:Invalid value added, please review', response_json['message'])
#
#
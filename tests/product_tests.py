# # import unittest
# # import json
# # from tests.base import BaseTestCase
# #
# # product_data = dict(product_name="Acer",
# #                     unit_price=19000000,
# #                     stock=100)
# #
# # sale_data = dict(product_id=1,
# #                  quantity=32)
# #
# # empty_product_data = {}
# #
# #
# # class FlaskTestCase(BaseTestCase):
# #     def setUp(self):
# #         self.app = create_app()
#
#     """Products tests"""
#     #
#     # """testing  GET all items in the inventory"""
#     #
#     # def test_get_all_inventory_items(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/products",
#     #                               content_type="application/json",
#     #                               data=json.dumps(product_data))
#     #         response_json = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn("Acer", response_json[0]['product_name'])
#
#     # """test empty product data"""
#     #
#     # def test_no_product_in_inventory(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/products/20",
#     #                               content_type="application/json",
#     #                               data=json.dumps(empty_product_data))
#     #         response_json = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn('product not in inventory', response_json['message'])
#     #
#     # """testing  GET a single item in the inventory"""
#     #
#     # def test_get_one_item_in_inventory(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/products/1",
#     #                               content_type="application/json",
#     #                               data=json.dumps(product_data))
#     #         response_json = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn("Acer", response_json[0]['product_name'])
#     #
#     # """testing  GET a single item in the inventory"""
#     #
#     # def test_inventory_item_does_not_exist(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/products/2",
#     #                               content_type="application/json",
#     #                               data=json.dumps(product_data))
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn('product not in inventory', responseJson['message'])
#     #
#     # """testing adding an item to inventory"""
#
#     # def test_add_new_inventory_item(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/products', content_type='application/json',
#     #                                data=json.dumps(product_data))
#     #         self.assertEqual(response.status_code, 201)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('product created', responseJson['message'])
#
#     # """testing adding an item to inventory"""
#     #
#     # def test_duplicate_data(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/products', content_type='application/json',
#     #                                data=json.dumps(product_data))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('you have already registered this product', responseJson['message'])
#     #
#     # """Testing for wrong data type inserted"""
#     #
#     # def test_wrong_data_type(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/products', content_type='application/json',
#     #                                data=json.dumps(dict(product_name="Acer",
#     #                                                     unit_price="19000000",
#     #                                                     stock=100)))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('Error:Invalid value please review product inputs', responseJson['message'])
#     #
#     # """Testing for empty space"""
#     #
#     # def test_empty_space(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/products', content_type='application/json',
#     #                                data=json.dumps(dict(product_name=" ",
#     #                                                     unit_price=19000000,
#     #                                                     stock=100)))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('Empty values are not allowed', responseJson['message'])
#     #
#     # """Testing for wrong column name"""
#     #
#     # def test_wrong_column_name(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/products', content_type='application/json',
#     #                                data=json.dumps(dict(product_namee="lenovo",
#     #                                                     unit_price=19000000,
#     #                                                     stock=100)))
#     #         self.assertEqual(response.status_code, 400)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('Please review the columns', responseJson['message'])
#     #
#     # """Sales tests"""
#     #
#     # """testing  GET all sales"""
#     #
#     # def test_get_all_items_sold(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/sales",
#     #                               content_type="application/json",
#     #                               data=json.dumps(sale_data))
#     #         response_json = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn("Acer", response_json[0]['product_name'])
#     #
#     # """testing  GET a single sale"""
#     #
#     # def test_get_one_sale(self):
#     #     with self.app.test_client() as client:
#     #         response = client.get("/api/v1/sales/1",
#     #                               content_type="application/json",
#     #                               data=json.dumps(sale_data))
#     #         response_json = json.loads(response.data.decode())
#     #         self.assertEqual(response.status_code, 200)
#     #         self.assertIn("Acer", response_json[0]['product_name'])
#     #
#     # """testing adding a sale"""
#     #
#     # def test_add_new_sale(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/sales', content_type='application/json',
#     #                                data=json.dumps(sale_data))
#     #         self.assertEqual(response.status_code, 201)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('sale made', responseJson['message'])
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
#     #
#     # """Registration tests"""
#     #
#     # """Test user registration"""
#     #
#     # def test_register_user(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/signup', content_type='application/json',
#     #                                data=json.dumps(dict(username="myrdstom",
#     #                                                     password="password",
#     #                                                     is_owner=bool('false'))))
#     #         self.assertEqual(response.status_code, 201)
#     #         responseJson = json.loads(response.data.decode())
#     #         self.assertIn('User registered', responseJson['message'])
#     #
#     # """Test Login User"""
#     #
#     # def test_login_user(self):
#     #     with self.app.test_client() as client:
#     #         response = client.post('/api/v1/login', content_type='application/json',
#     #                                data=json.dumps(dict(username="myrdstom",
#     #                                                     password="password",
#     #                                                     is_owner=bool('false'))))
#     #         self.assertEqual(response.status_code, 201)
#     #
#     # if __name__ == '__main__':
#     #     unittest.main()

import unittest
import json
from tests.base import BaseTestCase

empty_product_data = {}

category_data = dict(category_name="laptop")


class FlaskTestCase(BaseTestCase):
    """Category tests"""

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


    if __name__ == '__main__':
        unittest.main()

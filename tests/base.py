import unittest
import json
from flask_jwt_extended import JWTManager
from Instance.config import TestingConfig
from database.db import DBHandler
from flask import current_app as app
from app import create_app


class BaseTestCase(unittest.TestCase):

    def new_app(self):
        app = create_app()
        app.config.from_object(TestingConfig)

        return app

    def setUp(self):
        self.app = self.new_app()
        self.app.app_context().push()
        self.client = self.app.test_client()
        handler = DBHandler(app.config['DATABASE_URL'])
        handler.create_user_table()
        handler.create_products_table()
        handler.create_sales_table()

        self.user_data = {

            'username': 'myrdstom',
            'password': 'password'
        }
        self.user_data2 = {

            'username': 'bgpeter',
            'password': 'password'
        }

    def create_user(self):
        response = self.client.post("api/v1/signup", content_type='application/json',
                                    data=json.dumps(dict(username="myrdstom",
                                                         password="password",
                                                         email="nserekopaul@gmail.com",
                                                         is_admin=bool('true'))))
        return response

    def create_second_user(self):
        response = self.client.post("api/v1/signup", content_type='application/json',
                                    data=json.dumps(dict(username="bgpeter",
                                                         password="password",
                                                         email="bgpeter@gmail.com",
                                                         is_admin=bool('true'))))
        return response

    def login_user(self):
        login_response = self.client.post('api/v1/login', content_type='application/json',
                                          data=json.dumps(self.user_data))
        login_result = json.loads(login_response.data.decode())
        return login_result

    def login_user2(self):
        login_response = self.client.post('api/v1/login', content_type='application/json',
                                          data=json.dumps(self.user_data2))
        login_result = json.loads(login_response.data.decode())
        return login_result

    def tearDown(self):
        handler = DBHandler(app.config['DATABASE_URL'])
        handler.trancate_table()

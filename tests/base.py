import unittest
import json
from modules.Instance.config import TestingConfig
from database.db import DBHandler
from flask import current_app as app
from modules.app import create_app


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
        handler.create_tables()

        self.admin_user = {
            'username': 'admin',
            'password': 'password'
        }

        self.user_data = {

            'username': 'myrdstom',
            'password': 'password'
        }
        self.user_data2 = {

            'username': 'bgpeter',
            'password': 'password'
        }

    def create_user(self):
        response = self.client.post("api/v1/signup",
                                    headers={'Content-Type': 'application/json',
                                                                 'Authorization': 'Bearer ' +
                                                                                  self.admin_login()[
                                                                                      'access_token']},
                                    data=json.dumps(dict(username="myrdstom",
                                                         password="password")))
        return response


    def create_second_user(self):
        response = self.client.post("api/v1/signup", content_type='application/json',
                                    data=json.dumps(dict(username="bgpeter",
                                                         password="password")))
        return response

    def admin_login(self):
        login_response = self.client.post('api/v1/login', content_type='application/json',
                                          data=json.dumps(self.admin_user))
        login_result = json.loads(login_response.data.decode())
        return login_result

    def login_user(self):
        self.client.post("api/v1/signup",
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' +
                                                   self.admin_login()[
                                                       'access_token']},
                         data=json.dumps(dict(username="myrdstom",
                                              password="password")))
        login_response = self.client.post('api/v1/login', content_type='application/json',
                                          data=json.dumps(self.user_data))
        login_result = json.loads(login_response.data.decode())
        return login_result


    def tearDown(self):
        handler = DBHandler(app.config['DATABASE_URL'])
        handler.trancate_table()

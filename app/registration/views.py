from app.registration import auth_v1
from app_utils import empty_string_catcher, email_validator, is_string, is_Bool
from flask import request
from app.models import User
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (create_access_token)

API = Api(auth_v1)

'''This class handles user registration'''


class Registration(Resource):

    def post(self):
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')
        if not is_string(username) or not is_string(password):
            return {"message": "Please review the values added"}, 400

        if not empty_string_catcher(username) or not empty_string_catcher(password):
            return {'message': 'please fill all fields'}, 400

        if not email_validator(email):
            return {'message': 'Error: invalid email: Please check email'}, 400
        if User.query_username(username):
            return {'message': 'A user with that username already exists'}, 409
        if User.query_email(email):
            return {'message': 'A user with that email already exists'}, 409
        else:
            user = User(email, username, password)
            user.insert_user()
            return {'message': 'User successfully registered'}, 201
9

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not is_string(username) or not is_string(password):
            return {"message": "Please review the values added"}, 400

        if not empty_string_catcher(username) or not empty_string_catcher(password):
            return {'message': 'please fill all fields'}, 400

        query = User.query_username(username)
        if not query:
            return {'message': 'The user does not exist, please register'}, 400
        pswd = list(query)[3]
        if not check_password_hash(pswd, password):
            return {'message': 'Error: wrong password'}, 400

        access_token = create_access_token(identity=query)
        return {'access_token': access_token}, 200


API.add_resource(Registration, '/signup')
API.add_resource(Login, '/login')

from app.registration import auth_v1
from app_utils import empty_string_catcher, email_validator, is_string
from flask import request
from database.models import User
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

API = Api(auth_v1)

'''This class handles user registration'''


class Registration(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        is_admin = current_user['is_admin']
        if is_admin:
            data = request.get_json()
            username = data['username']
            password = generate_password_hash(data['password'], method='sha256')
            if not is_string(username) or not is_string(password):
                return {"message": "Please review the values added"}, 400

            if not empty_string_catcher(username) or not empty_string_catcher(password):
                return {'message': 'please fill all fields'}, 400

            if User.query_username(username):
                return {'message': 'A user with that username already exists'}, 409
            else:
                user = User(username, password)
                user.insert_user()
                return {'message': 'User successfully registered'}, 201
        else:
            return {'message':'you are not authorized to view this resource'}, 409
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
        pswd = list(query)[2]
        if not check_password_hash(pswd, password):
            return {'message': 'Error: wrong password'}, 400

        user = {"user_id": query[0], "username": query[1], "password": query[2], "is_admin": query[3]}


        access_token = create_access_token(identity=user)
        return {'access_token': access_token}, 200


API.add_resource(Registration, '/signup')
API.add_resource(Login, '/login')

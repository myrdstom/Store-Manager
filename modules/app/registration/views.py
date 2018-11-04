from modules.app.registration import auth_v1
from modules.app_utils import ValidateUserData
from flask import request
from database.models import User
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

API = Api(auth_v1)

'''This class handles user registration'''


class Registration(Resource):
    @jwt_required
    @swag_from("../docs/signup.yml")
    def post(self):
        role = get_jwt_identity()['role']
        if role == "store-owner":
            data = request.get_json()
            username = data['username']
            password = generate_password_hash(data['password'], method='sha256')
            user_data = ValidateUserData(username, password)
            if user_data.validate_user():
                return {"message": "Please review the values added"}, 400
            if User.get_by_username(username):
                return {'message': 'A user with that username already exists'}, 409
            else:
                user = User(username, password, role)
                user.insert_user()
                return {'message': 'User successfully registered', "username": username}, 201
        else:
            return {'message': 'you are not authorized to view this resource'}, 409


class Login(Resource):
    @swag_from("../docs/login.yml")
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        check_for_user = User.get_by_username(username)
        user_data = ValidateUserData(username, password)
        if user_data.validate_user():
            return {"message": "Please review the values added"}, 400
        if not check_for_user:
            return {'message': 'The user does not exist, please register'}, 400
        if not check_password_hash(check_for_user['password'], password):
            return {'message': 'Error: wrong password'}, 400

        access_token = create_access_token(identity=check_for_user)
        return {'access_token': access_token}, 200


API.add_resource(Registration, '/signup')
API.add_resource(Login, '/login')
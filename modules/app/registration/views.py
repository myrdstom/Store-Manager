from modules.app.registration import auth_v1
from modules.app_utils import ValidateUserData, is_string, empty_string_catcher
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
        if role != "store-owner":
            return {'message': 'you are not authorized to view this resource'}, 401
        data = request.get_json()
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')
        email = data['email']
        user_data = ValidateUserData(username, password, email)
        if user_data.validate_user():
            return {"message": "Please review the values added"}, 400
        if User.get_by_username(username) or User.get_by_email(email):
            return {'message': 'A user with those credentials already exists'}, 409
        else:
            user = User(username, password, email, role)
            user.insert_user()
            return {'message': 'User successfully registered', "username": username}, 201


    @jwt_required
    def put(self, userId):
        current_user = get_jwt_identity()['role']
        if current_user != "store-owner":
            return {'message': 'you are not authorized to view this resource'}, 401
        data = request.get_json()
        new_role = data['role']
        role = new_role.lower()
        user = User.update_user_role(role, userId)
        if len(user) == 0:
            return {'message': 'User does not exist'}, 400
        if role == 'store-owner' or role == 'shop-attendant':
            return {'message': 'User has been promoted'}, 200
        else:
            return {'message': 'Invalid role, please try again'}, 400



class Login(Resource):
    @swag_from("../docs/login.yml")
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        check_for_user = User.get_by_username(username)
        if not is_string(username) or not is_string(password) \
                or not empty_string_catcher(username) or not empty_string_catcher(password) \
                or not username.isalpha():
            return {"message": "Please review the values added"}, 400
        if not check_for_user:
            return {'message': 'The user does not exist, please register'}, 400
        if not check_password_hash(check_for_user['password'], password):
            return {'message': 'Error: wrong password'}, 400

        access_token = create_access_token(identity=check_for_user)
        return {'access_token': access_token}, 200


API.add_resource(Registration, '/signup', '/signup/<int:userId>')
API.add_resource(Login, '/login')

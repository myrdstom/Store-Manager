from modules.app.categories import apca_v1
from flask import request
from database.models import Category
from flask_restful import Resource, Api
from modules.app_utils import ValidateCategoryData
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

API = Api(apca_v1)


class Categories(Resource):
    @jwt_required
    def get(self):
        role = get_jwt_identity()['role']
        if role == "store-owner":
            category = Category.view_categories()
            if len(category) == 0:
                return {'message': 'There are no values in the database'}, 200
            return category
        else:
            return {'message': 'you are not authorized to view this resource'}, 409

    @jwt_required
    def post(self):
        role = get_jwt_identity()['role']
        if role == "store-owner":
            data = request.get_json()
            categoryname = data['category_name']

            category_data = ValidateCategoryData(categoryname)
            if category_data.validate_category_data():
                return {"message": "Please review the values added"}, 400
            category_name = categoryname.lower()
            if Category.find_category_by_name(category_name):
                return {'message': 'A category with that product name already exists'}, 409
            category = Category(category_name)
            category.insert_category()
            return {'message': 'category created', 'category_name': category_name}, 201
        else:
            return {'message': 'you are not authorized to view this resource'}, 409

    @jwt_required
    def put(self, category_id):
        role = get_jwt_identity()['role']
        if role == "store-owner":
            data = request.get_json()
            categoryname = data['category_name']
            category_name = categoryname.lower()
            category_data = ValidateCategoryData(category_name)
            if category_data.validate_category_data():
                return {"message": "Please review the values added"}, 400
            category = Category.update_category(category_name, category_id)
            if len(category) == 0:
                return {'message': 'no such entry found'}, 400
            return category, 201
        else:
            return {'message': 'you are not authorized to view this resource'}, 409

    @jwt_required
    def delete(self, category_id):
        role = get_jwt_identity()['role']
        if role == "store-owner":
            if Category.delete_single_category(category_id):
                return {'message': 'Record successfully deleted'}, 200
            return {'message': 'Product does not exist'}, 200
        else:
            return {'message': 'you are not authorized to view this resource'}, 409


API.add_resource(Categories, '/categories', '/categories/<int:category_id>')

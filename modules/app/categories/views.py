from modules.app.categories import apca_v1
from flask import request
from database.models import Category
from flask_restful import Resource, Api
from modules.app_utils import ValidateCategoryData
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

API = Api(apca_v1)


class Categories(Resource):
    def get(self):
        category = Category.view_categories()
        if len(category) == 0:
            return {'message': 'There are no values in the database'}, 200
        return category

    def post(self):
        data = request.get_json()
        categoryname = data['category_name']
        category_name = categoryname.lower()
        category_data = ValidateCategoryData(category_name)
        if category_data.validate_category_data():
            return {"message": "Please review the values added"}, 400
        if Category.find_category_by_name(category_name):
            return {'message': 'A product with that product name already exists'}, 409
        category = Category(category_name)
        category.insert_category()
        return {'message': 'category created', 'category_name': category_name}, 201

    def put(self):
        pass

    def delete(self, category_id):
        if Category.delete_single_category(category_id):
            return {'message': 'Record successfully deleted'}, 200
        return {'message': 'Product does not exist'}, 200


API.add_resource(Categories, '/categories', '/categories/<int:category_id>')

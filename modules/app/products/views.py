from modules.app.products import apcn_v1
from modules.app_utils import ValidateProductData
from flask import request
from database.models import Product, Category
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

API = Api(apcn_v1)


class Products(Resource):
    @jwt_required
    @swag_from("../docs/get_all_products.yml")
    def get(self, product_id=0):
        """This function returns a list of all products in the inventory or a single product"""
        if (product_id):
            product_identity = Product.view_single_product(product_id)
            if not product_identity:
                return {'message': 'the product does not exist'}, 200
            return product_identity
        else:
            product = Product.view_products()
            if len(product) == 0:
                return {'message': 'There are no values in the database'}, 200
            return product

    @jwt_required
    def post(self):
        """This function lets the administrator add a new product to the inventory"""
        try:
            role = get_jwt_identity()['role']
            if role == "store-owner":
                data = request.get_json()
                productname = data['product_name']
                unit_price = data['unit_price']
                stock = data['stock']
                categoryname = data['category_name']
                product_name = productname.lower()
                category_name = categoryname.lower()
                product_data = ValidateProductData(product_name, unit_price, stock)
                if product_data.validate_product_data():
                    return {"message": "Please review the values added"}, 400
                if Product.find_product_by_name(product_name):
                    return {'message': 'A product with that product name already exists'}, 409
                category_identity = Category.find_category_by_name(category_name)
                if category_identity:
                    product = Product(product_name, unit_price, stock, category_name)
                    product.insert_product()
                    return {'message': 'product created', 'product_name': product_name,
                            'unit_price': unit_price, 'stock': stock}, 201
                else:
                    return {'message':'category does not exist'}, 400
            else:
                return {'message': 'you are not authorized to view this resource'}, 409
        except Exception:
            return {'message': 'Something went wrong with your inputs: Please review them'}, 409

    @jwt_required
    def put(self, product_id):
        """This function lets the administrator edit a product"""
        try:
            role = get_jwt_identity()['role']
            if role == "store-owner":
                data = request.get_json()
                productname = data['product_name']
                unit_price = data['unit_price']
                stock = data['stock']
                categoryname = data['category_name']
                category_name= categoryname.lower()
                product_name = productname.lower()
                product_data = ValidateProductData(product_name, unit_price, stock)
                if product_data.validate_product_data():
                    return {"message": "Please review the values added"}, 400
                category_identity = Category.find_category_by_name(category_name)
                if category_identity:
                    product = Product.update_product(product_name, unit_price, stock, category_name, product_id)
                    if len(product) == 0:
                        return {'message': 'no such entry found'}, 400
                    return product, 201
            else:
                return {'message': 'you are not authorized to view this resource'}, 409
        except:
            return {'message': 'Something went wrong with your inputs: Please review them'}, 409

    @jwt_required
    def delete(self, product_id):
        """This function lets the administrator delete a product"""
        role = get_jwt_identity()['role']
        if role == "store-owner":
            if Product.delete_single_product(product_id):
                return {'message': 'Record successfully deleted'}, 200
            return {'message': 'Product does not exist'}, 200
        else:
            return {'message': 'you are not authorized to view this resource'}, 409


API.add_resource(Products, '/products', '/products/<int:product_id>')

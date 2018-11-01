from app.products import apcn_v1
from app_utils import empty_string_catcher, is_string, is_integer, check_for_letters
from flask import request
from database.models import Product
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

API = Api(apcn_v1)


class Products(Resource):
    @jwt_required
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
                product_name = productname.lower()
                if not is_string(product_name) or not is_integer(unit_price) or not is_integer(stock) \
                        or not empty_string_catcher(product_name) \
                        or check_for_letters(product_name):
                    return {"message": "Please review the values added"}, 400
                if Product.find_product_by_name(product_name):
                    return {'message': 'A product with that product name already exists'}, 409
                product = Product(product_name, unit_price, stock)
                product.insert_product()
                return {'message': 'product created', 'product_name': product_name, 'unit_price':unit_price, 'stock':stock}, 201
            else:
                return {'message':'you are not authorized to view this resource'}, 409
        except Exception:
            return {'message': 'Something went wrong with your inputs: Please review them'}, 400

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
                product_name = productname.lower()
                if not is_string(product_name) or not is_integer(unit_price) or not is_integer(stock) \
                        or not empty_string_catcher(product_name) \
                        or check_for_letters(product_name):
                    return {"message": "Please review the values added"}, 400
                product = Product.update_product(product_name, unit_price, stock, product_id)
                if product is False:
                    return {'message': 'no such entry found'}, 400
                return product, 201
            else:
                return {'message':'you are not authorized to view this resource'}, 409
        except:
            return {'message': 'Something went wrong with your inputs: Please review them'}, 400

    @jwt_required
    def delete(self, product_id):
        """This function lets the administrator delete a product"""
        role = get_jwt_identity()['role']
        if role == "store-owner":
            if Product.delete_single_product(product_id):
                return {'message': 'Record successfully deleted'}, 200
            return {'message': 'Product does not exist'}, 400
        else:
            return {'message':'you are not authorized to view this resource'}, 409


API.add_resource(Products, '/products', '/products/<int:product_id>')

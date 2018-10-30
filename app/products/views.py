from app.products import apcn_v1
from app_utils import empty_string_catcher, is_string, is_integer
from flask import request
from database.models import Product
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)

API = Api(apcn_v1)


class Products(Resource):
    def get(self, product_id=0):
        """This function returns a list of all products in the inventory or a single product"""
        if (product_id):
            prod_id = Product.view_single_product(product_id)
            if prod_id is False:
                return {'message': 'the product does not exist'}, 200
            return prod_id
        else:
            prod = Product.view_products()
            if len(prod) == 0:
                return {'message': 'There are no values in the database'}, 200
            return prod

    def post(self):
        """This function lets the administrator add a new product to the inventory"""
        data = request.get_json()
        product_name = data['product_name']
        unit_price = data['unit_price']
        stock = data['stock']
        if not is_string(product_name) or not is_integer(unit_price) or not is_integer(stock):
            return {"message": "Please review the values added"}, 400
        if not empty_string_catcher(product_name):
            return {'message': 'Empty values are not allowed'}, 400
        if Product.query_product_name(product_name):
            return {'message': 'A product with that product name already exists'}, 409
        prod = Product(product_name, unit_price, stock)
        prod.insert_product()
        return {'message': 'product created'}, 201

    def put(self, product_id):
        """This function lets the administrator edit a product"""
        data = request.get_json()
        product_name = data['product_name']
        unit_price = data['unit_price']
        stock = data['stock']
        if not is_string(product_name) or not is_integer(unit_price) or not is_integer(stock):
            return {"message": "Please review the values added"}, 400
        if not empty_string_catcher(product_name):
            return {'message': 'Empty values are not allowed'}, 400
        prod = Product.update_product(product_name, unit_price, stock, product_id)
        if prod is None:
            return {'message': 'no such entry found'}, 400
        return prod, 200

    def delete(self, product_id):
        """This function lets the administrator delete a product"""
        Product.delete_single_product(product_id)
        return {'message': 'Record successfully deleted'}, 200


API.add_resource(Products, '/products', '/products/<int:product_id>')

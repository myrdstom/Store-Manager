from app.products import apcn_v1
from app_utils import empty_string_catcher, email_validator
from flask import request, current_app as app, jsonify
from app.models import Product
from database.db import DBHandler
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)

API = Api(apcn_v1)


class Products(Resource):
    def get(self, product_id=0):
        """This function returns a list of all products in the inventory or a single product"""
        if (product_id):
            prod_id = Product.view_single_product(product_id)
            return prod_id
        else:
            prod = Product.view_products()
            return prod

    def post(self):
        """This function lets the administrator add a new product to the inventory"""
        data = request.get_json()
        username = data['username']
        product_name = data['product_name']
        unit_price = data['unit_price']
        stock = data['stock']
        if not isinstance(product_name, str) or not isinstance(unit_price, int) or not isinstance(stock, int):
            return {'message': 'Error:Invalid value please review product inputs'}, 400
        if not empty_string_catcher(product_name):
            return {'message': 'Empty values are not allowed'}, 400
        prod = Product(username, product_name, unit_price, stock)
        prod.insert_product()
        return {'message': 'product created'}, 201

    def delete(self, product_id):
        prod_id = Product.delete_single_product(product_id)
        return {'message': 'Record successfully deleted'}, 200



API.add_resource(Products, '/products', '/products/<int:product_id>')

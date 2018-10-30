from app.sales import apsn_v1
from app_utils import empty_string_catcher, is_integer
from flask import request, current_app as app, jsonify
from database.models import Sale,Product
from database.db import DBHandler
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)


API = Api(apsn_v1)


class Sales(Resource):
    """This function returns a list of all products in the inventory"""

    def get(self, sale_id=0):
        if (sale_id):
            sal_id = Sale.view_single_sale(sale_id)
            return sal_id
        else:
            sal = Sale.view_sales()
            return sal

    def post(self):
        """This function lets the administrator add a new product to the inventory"""

        data = request.get_json()
        product_id = data['product_id']
        username = data['username']
        quantity = data['quantity']
        prod_id = Product.view_single_product(product_id)
        if not is_integer(quantity) or not is_integer(product_id):
            return {'message': 'Error:Invalid value added, please review'}, 400
        available_stock = prod_id['stock']
        unit_price = prod_id['unitprice']
        product_name = prod_id['product_name']
        total = data['quantity'] * unit_price
        stock = available_stock - quantity
        prod = Sale.update_stock(stock, product_id)

        sale_items = Sale(product_id, username, product_name, quantity, total)
        sale_items.insert_sale()
        return {'message': 'sale created'}, 201


API.add_resource(Sales, '/sales', '/sales/<int:sale_id>')

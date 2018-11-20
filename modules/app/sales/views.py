from modules.app.sales import apsn_v1
from modules.app_utils import empty_string_catcher, is_integer, is_string, check_for_letters
from flask import request
from database.models import Sale, Product
from flask_restful import Resource, Api
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

API = Api(apsn_v1)


class Sales(Resource):
    """This function returns a list of all products in the inventory"""

    @jwt_required
    @swag_from("../docs/get_all_sales.yml")
    def get(self, sale_id=0):
        if (sale_id):
            sal_id = Sale.view_single_sale(sale_id)
            if len(sal_id) == 0:
                return {'message': 'Sale does not exist'}
            return sal_id
        else:
            sal = Sale.view_sales()
            if len(sal) == 0:
                return {'message': 'There are no values in the database'}, 200
            return sal

    @jwt_required
    def post(self):
        """This function lets the administrator add a new product to the inventory"""
        try:
            current_user = get_jwt_identity()['username']
            role = get_jwt_identity()['role']
            if role != "shop-attendant":
                return {'message': 'you are not authorized to view this resource'}, 401
            data = request.get_json()
            productname = data['product_name']
            username = current_user
            quantity = data['quantity']

            if not is_integer(quantity) or not is_string(productname) or not empty_string_catcher(productname) or \
                    check_for_letters(productname) or quantity < 0:
                return {'message': 'Error:Invalid value added, please review'}, 400
            product_name = productname.lower()
            product_identity = Product.view_single_product_by_name(product_name)
            if product_identity:
                available_stock = product_identity['stock']
                unit_price = product_identity['unitprice']
                product_name = product_identity['product_name']
                total = data['quantity'] * unit_price
                if available_stock < quantity:
                    return {'message': 'not enough in stock for you to purchase that amount'}, 400
                stock = available_stock - quantity
            else:
                return {'message': 'Product does not exist'}, 400
            Sale.update_stock(stock, product_name)
            sale_items = Sale(username=username, product_name=product_name, quantity=quantity,
                              total=total)
            sale_items.insert_sale()
            return {'message': 'sale created'}, 201

        except Exception:
            return {'message': 'Something went wrong with your inputs: Please review them'}, 409


API.add_resource(Sales, '/sales', '/sales/<int:sale_id>')

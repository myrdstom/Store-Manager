# from flask import request
# from flask_restful import Resource, Api
# from database.model import Salepoints
# from app.api import apsn_v1
# from .products import products_list
#
# sales_list = []
#
# API = Api(apsn_v1)


class Sales(Resource):
    """This function returns a list of all products in the inventory"""

    def get(self, sale_id=0):
        all_sales = []
        if (sale_id):
            single_sale = [sale_list.to_json_id() for sale_list in sales_list if sale_list.sale_id == sale_id]
            if not single_sale:
                return {'message': 'sale not in inventory'}, 200
            else:
                return single_sale, 200
        else:
            for sale_list in sales_list:
                all_sales.append(sale_list.to_json())
            return all_sales, 200

    def post(self):
        """This function lets the administrator add a new product to the inventory"""

        try:
            for product_list in products_list:
                data = request.get_json()
                sale_id = len(sales_list) + 1
                product_id = data['product_id']
                product_name = product_list.product_name
                unit_price = product_list.unit_price
                quantity = data['quantity']
                total = data['quantity'] * product_list.unit_price
                if not isinstance(product_id, int) or not isinstance(quantity, int):
                    return {'message': 'Error:Invalid value added, please review'}, 400
                if product_list.product_id == product_id:
                    sales_list.append(Salepoints(sale_id, product_id, product_name, unit_price, quantity, total))
            return {'message': 'sale made'}, 201
        except Exception as e:
            print(e)
            return {'message': "Please review the columns"}, 400


API.add_resource(Sales, '/sales', '/sales/<int:sale_id>')
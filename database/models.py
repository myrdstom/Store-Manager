from database.db import DBHandler
from flask import current_app as app
import re
from werkzeug.security import check_password_hash


class User:
    """Class handles user object operations"""

    def __init__(self,username, password, role):
        self.username = username
        self.password = password
        self.role = role


    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj

    def query_username(username):
        """Method to retrieve a username from the database"""
        user = User.database_url().fetch_by_param('users', 'username', username)

        if user is None:
            return False
        else:
            return {"user_id": user[0], "username": user[1], "password": user[2], "role": user[3]}


    def insert_user(self):
        user = User.database_url().create_user(self.username, self.password, self.role)

        if user is None:
            return False
        else:
            return user


class Product:
    def __init__(self, product_name, unit_price, stock):
        self.product_name = product_name
        self.unit_price = unit_price
        self.stock = stock

    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj

    def insert_product(self):
        response = Product.database_url().create_product(self.product_name, self.unit_price, self.stock)

        if response is None:
            return False
        else:
            return response

    @staticmethod
    def update_product(product_name, unit_price, stock, product_id):
        response = Product.database_url().modify_products(product_name, unit_price, stock, product_id)

        if response is None:
            return False
        else:
            return response

    def query_product_name(product_name):
        """Method to retrieve a username from the database"""
        response = Product.database_url().fetch_by_param('products', 'product_name', product_name)

        if response is None:
            return False
        else:
            return response

    def view_products():
        response = Product.database_url().view_all_products()
        return response

    def view_single_product(product_id):
        response = Product.database_url().fetch_by_param('products', 'product_id', product_id)

        if response is None:
            return {}
        else:
            return {
                'product_id': response[0],
                'product_name': response[1],
                'unitprice': response[2],
                'stock': response[3]
            }

    def delete_single_product(product_id):
        resp = Product.database_url().fetch_by_param('products', 'product_id', product_id)
        if resp:
            Product.database_url().delete_by_param('products', 'product_id', product_id)
            return True
        else:
            return False

class Sale:
    def __init__(self,  **kwargs):
        self.product_id = kwargs.get('product_id')
        self.username = kwargs.get('username')
        self.product_name = kwargs.get('product_name')
        self.quantity = kwargs.get('quantity')
        self.total = kwargs.get('total')

    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj

    def insert_sale(self):
        sale_response = Sale.database_url().create_sale(self.product_id,
                                                        self.username, self.product_name, self.quantity, self.total)

        if sale_response is None:
            return False
        else:
            return sale_response

    def view_sales():
        response = Sale.database_url().view_all_sales()
        return response

    def view_single_sale(sale_id):
        sale_response = Sale.database_url().fetch_by_param('sales', 'sale_id', sale_id)

        if sale_response is None:
            return False
        else:
            return {
                'sale_id': sale_response[0],
                'username': sale_response[2],
                'product_name': sale_response[3],
                'quantity': sale_response[4],
                'total': sale_response[5]
            }

    @staticmethod
    def update_stock(stock, product_id):
        response = Product.database_url().modify_stock(stock, product_id)

        if response is None:
            return False
        else:
            return response

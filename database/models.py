from database.db import DBHandler
from flask import current_app as app
import re
from werkzeug.security import check_password_hash


class DatabaseUrl:
    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj


class User:
    """Class handles user object operations"""

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def get_by_username(username):
        """Method to retrieve a username from the database"""
        user = DatabaseUrl.database_url().fetch_by_param('users', 'username', username)
        if user is None:
            return False
        else:
            return dict(user_id=user[0], username=user[1], password=user[2], role=user[3])

    def insert_user(self):
        user = DatabaseUrl.database_url().create_user(self.username, self.password, self.role)

        if user is None:
            return False
        else:
            return user


class Product:
    def __init__(self, product_name, unit_price, stock):
        self.product_name = product_name
        self.unit_price = unit_price
        self.stock = stock

    def insert_product(self):
        response = DatabaseUrl.database_url().create_product(self.product_name, self.unit_price, self.stock)

        if response is None:
            return False
        else:
            return response

    def view_single_product(product_id):
        product = DatabaseUrl.database_url().fetch_by_param('products', 'product_id', product_id)

        if product is None:
            return {}
        else:
            return dict(product_id=product[0], product_name=product[1], unitprice=product[2], stock=product[3])

    @staticmethod
    def update_product(product_name, unit_price, stock, product_id):
        response = DatabaseUrl.database_url().modify_products(product_name, unit_price, stock, product_id)

        if response is None:
            return False
        else:
            return response

    def find_product_by_name(product_name):
        """Method to retrieve a username from the database"""
        response = DatabaseUrl.database_url().fetch_by_param('products', 'product_name', product_name)

        if response is None:
            return False
        else:
            return response

    def view_products():
        response = DatabaseUrl.database_url().view_all_products()
        return response

    def view_single_product_by_name(product_name):
        product = DatabaseUrl.database_url().fetch_by_param('products', 'product_name', product_name)

        if product is None:
            return {}
        else:
            return dict(product_id=product[0], product_name=product[1], unitprice=product[2], stock=product[3])

    def delete_single_product(product_id):
        product = DatabaseUrl.database_url().fetch_by_param('products', 'product_id', product_id)
        if product:
            DatabaseUrl.database_url().delete_by_param('products', 'product_id', product_id)
            return True
        else:
            return False


class Sale:
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.product_name = kwargs.get('product_name')
        self.quantity = kwargs.get('quantity')
        self.total = kwargs.get('total')

    def insert_sale(self):
        sale_response = DatabaseUrl.database_url().create_sale(self.username, self.product_name, self.quantity,
                                                               self.total)

        if sale_response is None:
            return False
        else:
            return sale_response

    def view_sales():
        response = DatabaseUrl.database_url().view_all_sales()
        return response

    def view_single_sale(sale_id):
        response = DatabaseUrl.database_url().fetch_by_param('sales', 'sale_id', sale_id)
        sale = dict(sale_id=response[0], username=response[1], product_name=response[2], quantity=response[3],
                    total=response[4])

        if sale is None:
            return False
        else:
            return sale

    @staticmethod
    def update_stock(stock, product_id):
        product = DatabaseUrl.database_url().modify_stock(stock, product_id)

        if product is None:
            return False
        else:
            return product

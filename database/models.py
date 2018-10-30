from database.db import DBHandler
from flask import current_app as app
import re
from werkzeug.security import check_password_hash


class User:
    """Class handles user object operations"""

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj

    def query_username(username):
        """Method to retrieve a username from the database"""
        user = User.database_url().fetch_by_param('users', 'username', username)

        if user is None:
            return False
        else:
            return user

    def query_email(email):
        """Method to retrieve a username from the database"""

        user = User.database_url().fetch_by_param('users', 'email', email)

        if user is None:
            return False
        else:
            return user

    def query_password(password):
        """Method to retrieve a username from the database"""

        user = User.database_url().fetch_by_param('users', 'password', password)
        if not check_password_hash(user['password'], password):
            return False
        return True

    def insert_user(self):
        user = User.database_url().create_user(self.email, self.username, self.password)

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
            return False
        else:
            return {
                'product_name': response[1],
                'unitprice': response[2],
                'stock': response[3]
            }

    def delete_single_product(product_id):
        response = Product.database_url().delete_by_param('products', 'product_id', product_id)

        if response is None:
            return False
        else:
            return True


class Sale:
    def __init__(self, product_id, username, product_name, quantity, total):
        self.product_id = product_id
        self.username = username
        self.product_name = product_name
        self.quantity = quantity
        self.total = total

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
                'username': sale_response[1],
                'product_name': sale_response[2],
                'quantity': sale_response[3],
                'total': sale_response[3]
            }

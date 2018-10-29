from database.db import DBHandler
from flask import current_app as app
import re
from werkzeug.security import check_password_hash


# db_obj = DBHandler(app.config['DATABASE_URL'])

class User:
    """Class handles user object operations"""

    def __init__(self, email, username, password, is_admin):
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin

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
        user = User.database_url().create_user(self.email, self.username, self.password, self.is_admin)

        if user is None:
            return False
        else:
            return user


class Product:
    def __init__(self, username, product_name, unit_price, stock):
        self.username = username
        self.product_name = product_name
        self.unit_price = unit_price
        self.stock = stock

    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj

    def insert_product(self):
        response = Product.database_url().create_product(self.username, self.product_name, self.unit_price, self.stock)

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
                'username': response[1],
                'product_name': response[2],
                'unitprice': response[3],
                'stock': response[4]
            }


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

    def view_single_product(sale_id):
        sale_response = Sale.database_url().fetch_by_param('sales', 'sale_id', sale_id)

        if sale_response is None:
            return False
        else:
            return {
                'sale_id': sale_id[1],
                'username': sale_response[1],
                'product_name': sale_response[2],
                'quantity': sale_response[3],
                'total': sale_response[3]
            }

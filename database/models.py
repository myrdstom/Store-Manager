from database.db import DBHandler
from flask import current_app as app


class DatabaseUrl:
    def database_url():
        db_obj = DBHandler(app.config['DATABASE_URL'])
        return db_obj


class User:
    """Class handles user object operations"""

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def get_by_username(username):
        """Method to retrieve a username from the database"""
        user = DatabaseUrl.database_url().fetch_by_param('users', 'username', username)
        if user is None:
            return {}
        else:
            return dict(user_id=user[0], username=user[1], password=user[2], email=user[3], role=user[4])

    def get_by_email(email):
        """Method to retrieve a username from the database by email"""
        user = DatabaseUrl.database_url().fetch_by_param('users', 'email', email)
        if user is None:
            return {}
        else:
            return dict(user_id=user[0], username=user[1], password=user[2], email=user[3], role=user[4])

    @staticmethod
    def update_user_role(role, userId):
        user = DatabaseUrl.database_url().modify_users(role, userId)

        if user is None:
            return ()
        else:
            return user

    def insert_user(self):
        user = DatabaseUrl.database_url().create_user(self.username, self.password, self.email, self.role)

        if user is None:
            return ()
        else:
            return user


class Product:
    def __init__(self, product_name, unit_price, stock):
        self.product_name = product_name
        self.unit_price = unit_price
        self.stock = stock

    def insert_product(self):
        product = DatabaseUrl.database_url().create_product(self.product_name, self.unit_price, self.stock)

        if product is None:
            return ()
        else:
            return product

    def view_single_product(product_id):
        product = DatabaseUrl.database_url().fetch_by_param('products', 'product_id', product_id)

        if product is None:
            return {}
        else:
            return dict(product_id=product[0], product_name=product[1], unitprice=product[2], stock=product[3])

    @staticmethod
    def update_product(product_name, unit_price, stock, product_id):
        product = DatabaseUrl.database_url().modify_products(product_name, unit_price, stock, product_id)

        if product is None:
            return ()
        else:
            return product

    def find_product_by_name(product_name):
        """Method to retrieve a username from the database"""
        product = DatabaseUrl.database_url().fetch_by_param('products', 'product_name', product_name)

        if product is None:
            return ()
        else:
            return product

    def view_products():
        products = DatabaseUrl.database_url().view_all_products()
        return products

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
            return ()
        else:
            return sale_response

    def view_sales():
        sales = DatabaseUrl.database_url().view_all_sales()
        return sales

    def view_single_sale(sale_id):
        sale = DatabaseUrl.database_url().fetch_by_param('sales', 'sale_id', sale_id)

        if sale is None:
            return {}
        else:
            return dict(sale_id=sale[0], username=sale[1], product_name=sale[2], quantity=sale[3],
                    total=sale[4])

    @staticmethod
    def update_stock(stock, product_id):
        product = DatabaseUrl.database_url().modify_stock(stock, product_id)

        if product is None:
            return ()
        else:
            return product

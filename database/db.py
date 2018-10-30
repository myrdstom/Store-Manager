import psycopg2
from urllib.parse import urlparse

class DBHandler:
    def __init__(self, database_url):
        parsed_url = urlparse(database_url)
        dbname = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port
        self.conn = psycopg2.connect(
            database=dbname,
            user=username,
            password=password,
            host=hostname,
            port=port)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    '''Create tables'''

    def create_user_table(self):
        statement = "CREATE TABLE IF NOT EXISTS users (" \
                    "userId SERIAL PRIMARY KEY , " \
                    "email varchar NOT NULL UNIQUE, " \
                    "username varchar NOT NULL UNIQUE, " \
                    "password varchar NOT NULL, " \
                    "is_admin BOOL NOT NULL DEFAULT FALSE)"
        self.cur.execute(statement)

    def create_products_table(self):
        statement = "CREATE TABLE IF NOT EXISTS products (" \
                    "product_id SERIAL PRIMARY KEY , " \
                    "username varchar NOT NULL , " \
                    "product_name varchar NOT NULL UNIQUE, " \
                    "unit_price INT NOT NULL, " \
                    "stock INT NOT NULL)"
        self.cur.execute(statement)

    def create_sales_table(self):
        statement = "CREATE TABLE IF NOT EXISTS sales (" \
                    "sale_id SERIAL PRIMARY KEY , " \
                    "product_id  INT NOT NULL , " \
                    "username varchar NOT NULL, " \
                    "product_name varchar NOT NULL, " \
                    "quantity INT NOT NULL, " \
                    "total INT NOT NULL)"
        self.cur.execute(statement)

    '''Functions to handle users and authentication'''

    def create_user(self, email, username, password, admin):
        self.cur.execute("INSERT INTO users (email, username, password, is_admin) "
                         "VALUES( '{}', '{}', '{}', '{}');".format
                         (email, username, password, admin))

    def find_by_username(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        self.cur.execute(query, (username,))
        user = self.cur.fetchone()
        return user

    def find_by_email(self, email):
        query = "SELECT * FROM users WHERE email=%s"
        self.cur.execute(query, (email,))
        user = self.cur.fetchone()
        return user

    def view_user(self):
        statement = "SELECT name, username, email, is_admin FROM users;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        user_list = []
        user_dict = {}
        for row in rows:
            user_dict['email'] = row[1]
            user_dict['username'] = row[2]
            user_dict['is_admin'] = row[4]
            user_list.append(user_dict)
            user_dict = {}
        return user_list

    def auth_user(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        self.cur.execute(query, (username,))
        user = self.cur.fetchone()
        userDict = {"username": user[2], "password": user[3], "is_admin": user[4]}
        return userDict

    def fetch_by_param(self, table_name, column, value):
        """Fetches a single a parameter from a specific table and column"""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            table_name, column, value)
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def delete_by_param(self, table_name, column, value):
        """Fetches a single a parameter from a specific table and column"""
        query = "DELETE FROM {} WHERE {} = '{}'".format(
            table_name, column, value)
        self.cur.execute(query)

    '''Functions to handle Products'''

    def create_product(self, username, product_name, unit_price, stock):
        self.cur.execute("INSERT INTO products (username, product_name, unit_price, stock) "
                         "VALUES( '{}', '{}', '{}', '{}');".format
                         (username, product_name, unit_price, stock))


    def modify_products(self, data, product_id):
        self.cur.execute(
            "UPDATE products SET product_name=%s, unit_price=%s, stock=%s WHERE product_id=%s",
            (data['product_name'], data['unit_price'], data['stock'], product_id))
        self.cur.execute(
            "SELECT product_name, unit_price, stock FROM products WHERE product_id=%s", (product_id,))
        req = self.cur.fetchone()
        if req is None:
            return None
        product_dict = {"product_name": req[0], "unit_price": req[1],
                       "stock": req[2]}

        return product_dict



    '''Function to get all products'''
    def view_all_products(self):
        statement = "SELECT product_id, username, product_name, unit_price, stock FROM products;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        product_list = []
        product_dict = {}
        for row in rows:
            product_dict['product_id'] = row[0]
            product_dict['username'] = row[1]
            product_dict['product_name'] = row[2]
            product_dict['unit_price'] = row[3]
            product_dict['stock'] = row[4]
            product_list.append(product_dict)
            product_dict = {}
        return product_list


    """Functions to handle Sales"""

    """Function to create a sale"""
    def create_sale(self, product_id, username, product_name, quantity, total):
        self.cur.execute("INSERT INTO sales (product_id, username, product_name, quantity, total) "
                         "VALUES( '{}', '{}', '{}', '{}', '{}');".format
                         (product_id, username, product_name, quantity, total))


    '''Function to get all sales'''
    def view_all_sales(self):
        statement = "SELECT product_id, username, product_name, quantity, total FROM sales;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        sales_list = []
        sales_dict = {}
        for row in rows:
            sales_dict['product_id'] = row[0]
            sales_dict['username'] = row[1]
            sales_dict['product_name'] = row[2]
            sales_dict['quantity'] = row[3]
            sales_dict['total'] = row[4]
            sales_list.append(sales_dict)
            sales_dict = {}
        return sales_list



    """Trancating test database"""

    def trancate_table(self):
        self.cur.execute("DROP TABLE users;")
        self.cur.execute("DROP TABLE products;")
        self.cur.execute("DROP TABLE sales;")

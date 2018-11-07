import psycopg2
from urllib.parse import urlparse


class DBHandler:
    def __init__(self, database_url):
        try:
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
        except Exception:
            print("failed to connect")
            self.conn.rollback()

    '''Create tables'''

    def create_tables(self):
        try:
            statement = "CREATE TABLE IF NOT EXISTS users (" \
                        "userId SERIAL PRIMARY KEY , " \
                        "username varchar NOT NULL UNIQUE, " \
                        "password varchar NOT NULL, " \
                        "email varchar NOT NULL UNIQUE, " \
                        "role varchar NOT NULL); " \
                        "INSERT INTO users(username, password, email, role) " \
                        "SELECT 'admin', " \
                        "'sha256$v4XQKUWM$d11b300ec58696a119fc3f5bd5b0f07d64b49d2b56a7c1b2c8baed86ccec81e0', " \
                        "'admin@gmail.com','store-owner' WHERE NOT EXISTS (SELECT * FROM users WHERE username='admin');"
            self.cur.execute(statement)

            statement2 = "CREATE TABLE IF NOT EXISTS categories (" \
                         "category_id SERIAL PRIMARY KEY , " \
                         "category_name varchar NOT NULL UNIQUE)"
            self.cur.execute(statement2)

            statement3 = "CREATE TABLE IF NOT EXISTS products (" \
                         "product_id SERIAL PRIMARY KEY , " \
                         "product_name varchar NOT NULL, " \
                         "unit_price INT NOT NULL, " \
                         "stock INT NOT NULL," \
                         "category_name varchar NOT NULL, " \
                         "FOREIGN KEY (category_name) REFERENCES categories(category_name) ON DELETE CASCADE " \
                         "ON UPDATE CASCADE)"
            self.cur.execute(statement3)

            statement4 = "CREATE TABLE IF NOT EXISTS sales (" \
                         "sale_id SERIAL PRIMARY KEY , " \
                         "username varchar NOT NULL, " \
                         "product_name varchar NOT NULL, " \
                         "quantity INT NOT NULL, " \
                         "total INT NOT NULL)"
            self.cur.execute(statement4)
        except Exception:
            print("failed to create user table")
            self.conn.rollback()

    '''Functions to handle users and authentication'''

    def create_user(self, username, password, email, role):
        self.cur.execute("INSERT INTO users (username, password, email, role) "
                         "VALUES('{}', '{}', '{}','shop-attendant');".format
                         (username, password, email, role))

    def auth_user(self, username):
        query = "SELECT * FROM users WHERE username=%s"
        self.cur.execute(query, (username,))
        user = self.cur.fetchone()
        userDict = {"username": user[1], "password": user[2], "email": user[3], "role": user[4]}
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
        query = "DELETE FROM {} WHERE {} = '{}';".format(
            table_name, column, value)
        self.cur.execute(query)

    def modify_users(self, role, userId):
        self.cur.execute(
            "UPDATE users SET role=%s WHERE userId=%s",
            (role, userId))
        self.cur.execute(
            "SELECT role FROM users WHERE userId=%s", (userId,))
        req = self.cur.fetchone()
        if req is None:
            return None
        user_dict = {"role": req[0]}

        return user_dict

    """Functions to handle Categories"""

    """Function to create a category"""

    def create_category(self, category_name):
        self.cur.execute("INSERT INTO categories (category_name) "
                         "VALUES( '{}');".format
                         (category_name))

    """Function to update category"""

    def modify_category(self, category_name, category_id):
        self.cur.execute(
            "UPDATE categories SET category_name=%s WHERE category_id=%s",
            (category_name, category_id))
        self.cur.execute(
            "SELECT category_name FROM categories WHERE category_id=%s", (category_id,))
        req = self.cur.fetchone()
        if req is None:
            return None
        category_dict = {"category_name": req[0]}
        return category_dict

    def view_all_categories(self):
        statement = "SELECT category_id, category_name FROM categories;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        category_list = []
        category_dict = {}
        for row in rows:
            category_dict['category_id'] = row[0]
            category_dict['category_name'] = row[1]
            category_list.append(category_dict)
            category_dict = {}
        return category_list

    '''Functions to handle Products'''

    def create_product(self, product_name, unit_price, stock, category_name):
        self.cur.execute("INSERT INTO products (product_name, unit_price, stock, category_name) "
                         "VALUES( '{}', '{}', '{}', '{}');".format
                         (product_name, unit_price, stock, category_name))

    def modify_products(self, product_name, unit_price, stock, category_name, product_id):
        self.cur.execute(
            "UPDATE products SET product_name=%s, unit_price=%s, stock=%s, category_name=%s WHERE product_id=%s",
            (product_name, unit_price, stock, category_name, product_id))
        self.cur.execute(
            "SELECT product_name, unit_price, stock, category_name FROM products WHERE product_id=%s", (product_id,))
        req = self.cur.fetchone()
        if req is None:
            return None
        product_dict = {"product_name": req[0], "unit_price": req[1],
                        "stock": req[2], "category_name": req[3]}

        return product_dict

    """Function to update stock"""

    def modify_stock(self, stock, product_name):
        self.cur.execute(
            "UPDATE products SET stock=%s WHERE product_name=%s",
            (stock, product_name))

    '''Function to get all products'''

    def view_all_products(self):
        statement = "SELECT product_id, product_name, unit_price, stock, category_name FROM products;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        product_list = []
        product_dict = {}
        for row in rows:
            product_dict['product_id'] = row[0]
            product_dict['product_name'] = row[1]
            product_dict['unit_price'] = row[2]
            product_dict['stock'] = row[3]
            product_dict['category_name'] = row[4]
            product_list.append(product_dict)
            product_dict = {}
        return product_list

    """Functions to handle Sales"""

    """Function to create a sale"""

    def create_sale(self, username, product_name, quantity, total):
        self.cur.execute("INSERT INTO sales (username, product_name, quantity, total) "
                         "VALUES('{}', '{}', '{}', '{}');".format
                         (username, product_name, quantity, total))

    '''Function to get all sales'''

    def view_all_sales(self):
        statement = "SELECT sale_id, username, product_name, quantity, total FROM sales;"
        self.cur.execute(statement)
        rows = self.cur.fetchall()
        sales_list = []
        sales_dict = {}
        for row in rows:
            sales_dict['sale_id'] = row[0]
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
        self.cur.execute("DROP TABLE categories;")
        self.cur.execute("DROP TABLE sales;")

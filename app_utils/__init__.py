import re
import string


def empty_string_catcher(value):
    value = ' '.join(value.split())
    if not value:
        return False
    return True


def email_validator(value):
    if re.match(r"[a-zA-z0-9]+@[a-z]+\.[a-z]+", value):
        return True
    return False


def is_Bool(value):
    if isinstance(value, bool):
        return True
    return False


def is_string(value):
    if isinstance(value, str):
        return True
    return False


def is_integer(value):
    if isinstance(value, int) and value > 0:
        return True
    return False


def is_space(value):
    if re.search(r"\s", value):
        return True
    return False


def check_for_letters(value):
    response = ""
    for letter in value:
        if letter in string.punctuation:
            response += letter
    if response:
        return True
    return False


class ValidateUserData:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def validate_user(self):
        if not is_string(self.username) or not is_string(self.password) \
                or not empty_string_catcher(self.username) or not empty_string_catcher(self.password) \
                or not self.username.isalpha() or not email_validator(self.email):
            return True


class ValidateProductData:
    def __init__(self, product_name, unit_price, stock):
        self.product_name = product_name
        self.unit_price = unit_price
        self.stock = stock

    def validate_product_data(self):
        if not is_string(self.product_name) or not is_integer(self.unit_price) or not is_integer(self.stock) \
                or not empty_string_catcher(self.product_name) \
                or check_for_letters(self.product_name):
            return True


class ValidateCategoryData:
    def __init__(self, category_name):
        self.category_name = category_name

    def validate_category_data(self):
        if not is_string(self.category_name) or not empty_string_catcher(self.category_name) \
                or check_for_letters(self.category_name):
            return True

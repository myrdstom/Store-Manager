import re
import string

def empty_string_catcher(value):
    value = ' '.join(value.split())
    if not value:
        return False
    return True


def is_Bool(value):
    if isinstance(value,bool):
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

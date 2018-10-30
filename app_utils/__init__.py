import re



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
    if isinstance(value,bool):
        return True
    return False

def is_string(value):
    if isinstance(value, str):
        return True
    return False

def is_integer(value):
    if value > 0 and value.is_integer():
        return True
    return False


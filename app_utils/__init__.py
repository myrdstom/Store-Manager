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
    if isinstance(value, int) and value > 0:
        return True
    return False

def is_space(value):
    if re.search(r"\s", value):
        return True
    return False

    #num < 0 and num.is_integer()

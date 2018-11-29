from flask import Blueprint

auth_v1 = Blueprint('auth_v1', __name__, url_prefix='/api/v1')

from .views import *

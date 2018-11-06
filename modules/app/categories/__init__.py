from flask import Blueprint

accn_v1 = Blueprint('accn', __name__, url_prefix='/api/v1')

from .views import *

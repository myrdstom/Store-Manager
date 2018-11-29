from flask import Blueprint

apsn_v1 = Blueprint('apsn_v1', __name__, url_prefix='/api/v1')

from .views import *

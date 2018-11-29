from flask import Blueprint

apcn_v1 = Blueprint('apcn', __name__, url_prefix='/api/v1')

from .views import *

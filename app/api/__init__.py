from flask import Blueprint

apcn_v1 = Blueprint('apcn', __name__, url_prefix='/v1')
from  .products import *
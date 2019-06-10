from flask import Blueprint

apca_v1 = Blueprint('apca', __name__, url_prefix='/api/v1')

from .views import *

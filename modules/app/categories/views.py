from modules.app.products import accn_v1
from modules.app_utils import ValidateProductData
from flask import request
from database.models import Product
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
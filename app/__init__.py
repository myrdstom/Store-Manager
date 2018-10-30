from flask import Flask, jsonify
from Instance.config import DevelopmentConfig
from app.registration import auth_v1
from app.products import apcn_v1
from app.sales import apsn_v1
from flask_jwt_extended import JWTManager
import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=100)
    jwt = JWTManager(app)

    @app.errorhandler(404)
    def not_found(e):
        response = jsonify({'message': 'The requested Resource does not exist; Please review the URL'})
        response.status_code = 404
        return response

    app.register_blueprint(auth_v1)
    app.register_blueprint(apcn_v1)
    app.register_blueprint(apsn_v1)

    return app

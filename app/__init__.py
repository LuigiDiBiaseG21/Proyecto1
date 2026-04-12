from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidTokenError, ExpiredSignatureError, RevokedTokenError
from flask_migrate import Migrate
from .config import Config

# 1. Instanciamos extensiones (globales pero sin app)
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    # 2. Inicializamos las extensiones con la app
    db.init_app(application)
    ma.init_app(application)
    jwt.init_app(application)

    # Flask Error Handlers for JWT Exceptions - Catch before Flask-RESTful
    @application.errorhandler(NoAuthorizationError)
    def handle_no_authorization(error):
        return jsonify({"msg": "Missing Authorization Header"}), 401

    @application.errorhandler(InvalidTokenError)
    def handle_invalid_token(error):
        return jsonify({"msg": "Invalid token"}), 401

    @application.errorhandler(ExpiredSignatureError)
    def handle_expired_token(error):
        return jsonify({"msg": "Token has expired"}), 401

    @application.errorhandler(RevokedTokenError)
    def handle_revoked_token(error):
        return jsonify({"msg": "Token has been revoked"}), 401
    
    # 3. Importar modelos antes de inicializar Migrate
    # Esto permite que Alembic (el motor de Migrate) vea las tablas
    from .models import Blacklist 
    migrate.init_app(application, db)

    # 4. Configuración de API y Rutas
    from .resources import BlacklistResource, HealthCheck
    api = Api(application)
    
    api.add_resource(BlacklistResource, '/blacklists', '/blacklists/<email>')
    api.add_resource(HealthCheck, '/health')

    return application
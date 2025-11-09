from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import os
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config)

    LOG_PATH = "/var/log/services/user-service"

    # Configuração do logging
    if not app.debug:
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        file_handler = RotatingFileHandler(
            f"{LOG_PATH}/user-service.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("User service startup")
    
    db.init_app(app)

    with app.app_context():
        from . import routes
        
        # Registra os Blueprints
        from flask_restx import Api
        api = Api(app, title='Users API', version='1.0', description='API para gerenciamento de usuários', doc='/doc')
        api.add_namespace(routes.users_bp)

        # Cria as tabelas do banco de dados para nossos modelos
        db.create_all()

        return app

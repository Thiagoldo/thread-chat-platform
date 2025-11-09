import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

mongo = PyMongo()


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config)

    LOG_PATH = "/var/log/services/chat-service"

    # Configuração do logging
    if not app.debug:
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        file_handler = RotatingFileHandler(
            f"{LOG_PATH}/chat-service.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Chat service startup")

    mongo.init_app(app)

    with app.app_context():
        from . import routes

        # Registra os Blueprints
        from flask_restx import Api

        api = Api(
            app,
            title="Chat API",
            version="1.0",
            description="API para gerenciamento de chats",
            doc="/doc",
        )
        api.add_namespace(routes.chat_bp)

        return app

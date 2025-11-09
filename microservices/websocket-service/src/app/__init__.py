import eventlet
eventlet.monkey_patch()

from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import os
from .config import Config
from .queue_consumer import start_consumer
import threading
import logging
from logging.handlers import RotatingFileHandler
import sys

# Instancia sem parâmetros dependentes de configuração
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    LOG_PATH = "/var/log/services/websocket-service"

    # Configuração do logging
    if not app.debug:
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        file_handler = RotatingFileHandler(
            f"{LOG_PATH}/websocket-service.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Websocket service startup")


    # Inicializa com a configuração do app agora que está carregada
    socketio.init_app(app, message_queue=app.config['RABBITMQ_URL'])

    from . import events

    @app.route('/asyncapi')
    def serve_asyncapi():
        return send_from_directory(os.path.abspath(os.path.dirname('run.py')), 'asyncapi.yaml')

    # Inicia o consumidor do RabbitMQ em uma thread de fundo
    consumer_thread = threading.Thread(target=start_consumer, args=(socketio, app.config['RABBITMQ_URL'], app.logger))
    consumer_thread.daemon = True
    consumer_thread.start()

    return app, socketio

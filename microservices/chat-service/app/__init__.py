from flask import Flask
from flask_pymongo import PyMongo
from .config import Config

mongo = PyMongo()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)

    with app.app_context():
        from . import routes
        
        # Register Blueprints
        from flask_restx import Api
        api = Api(app, title='Chat API', version='1.0', description='API for chat management')
        api.add_namespace(routes.chat_bp)

        return app

from flask import Flask
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from elasticsearch import Elasticsearch
from flask_migrate import Migrate
from .utils import handle_auth_error, AuthError

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_error_handler(AuthError, handle_auth_error)

    db.init_app(app)
    migrate.init_app(app, db)

    app.es = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/_api')
    app.register_error_handler(AuthError, handle_auth_error)

    CORS(app, resources={r"/_api/*": {"origins": "*"}})
    return app

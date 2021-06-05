from flask import Flask
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_praetorian import Praetorian
from elasticsearch import Elasticsearch

from config import Config

guard = Praetorian()
db = SQLAlchemy()

def create_app(config_class=Config):
    # @TODO Initialize logging from dict
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    from app.models import User
    guard.init_app(app, User)

    app.es = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/_api')

    CORS(app, resources={r"/_api/*": {"origins": "*"}})
    return app

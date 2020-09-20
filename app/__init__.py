from flask import Flask

from flask_cors import CORS
from elasticsearch import Elasticsearch

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.es = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/internalapi')

    CORS(app, resources={r"/internalapi/*": {"origins": "*"}})
    return app

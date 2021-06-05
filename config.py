import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # directories
    POSTGRES = {
        'usr': 'postgres',
        'pw': 'postgres',
        'host': 'db',
        'db': 'annowiki2',
    }

    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or 'you-will-never-guess'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') \
        or 'http://es01:9200'

    # SQLA settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        f'postgresql://{POSTGRES["usr"]}:' \
        f'{POSTGRES["pw"]}@{POSTGRES["host"]}/{POSTGRES["db"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGING = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }

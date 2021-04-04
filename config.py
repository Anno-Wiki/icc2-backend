import os
from dotenv import load_dotenv

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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{POSTGRES["usr"]}:' \
        f'{POSTGRES["pw"]}@{POSTGRES["host"]}/{POSTGRES["db"]}'

    # SQLA settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH0_SECRET = os.environ.get('AUTH0_SECRET') \
        or 'you-will-never-guess'
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN') \
        or 'localhost:5000'
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE') \
        or 'localhost:5000'

    LOGGING = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] poop %(levelname)s in %(module)s: %(message)s',
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

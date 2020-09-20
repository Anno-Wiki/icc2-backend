import os

class Config:
    # directories
    POSTGRES = {
        'usr': 'postgres',
        'pw': 'postgres',
        'db': 'postgres',
    }

    SECRET_KEY = os.environ.get('SECRET_KEY') \
        or 'you-will-never-guess'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') \
        or 'http://es01:9200'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{POSTGRES["usr"]}:' \
        f'{POSTGRES["pw"]}@postgres/${POSTGRES["db"]}'

    # SQLA settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False


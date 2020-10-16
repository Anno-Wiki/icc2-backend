from datetime import datetime

from flask import current_app as app

from app.main import bp


@bp.route('/')
def index():
    results = app.es.get(index='text', id='1-0')
    return results

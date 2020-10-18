from datetime import datetime

from flask import current_app as app

from app.main import bp


@bp.route('/')
def index():
    results = app.es.get(index='toc', id='1-1')
    return results

from datetime import datetime

from flask import current_app as app

from app.main import bp


@bp.route('/')
def index():
    results = app.es.get(index='contents', id='yo')
    return results

@bp.route('/insert')
def insert():
    body = {
        'title': "yo",
        'content': "Yo, dawg, I heard you like databases, so we put a database"
                   "in your database.",
        'timestamp': datetime.now()
    }

    result = app.es.index(index='contents', id=body['title'], body=body)
    return result

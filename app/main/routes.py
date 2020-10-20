from datetime import datetime

from flask import current_app as app

from app.main import bp


@bp.route('/<toc_id>')
def index(toc_id):
    results = app.es.get(index='toc', id=toc_id)
    return results

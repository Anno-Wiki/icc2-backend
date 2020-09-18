from flask import jsonify
from flask import current_app as ca

from app.main import bp


@bp.route('/')
def index():
    results = ca.elasticsearch.get(index='contents', doc_type='title', id='yo')
    return jsonify(results)

from flask import request

from app import db
from app.main import bp
from .routes import getrange
from app.models.annotations import Annotation

@bp.route('/annotate/toc/<toc_id>', methods=['POST'])
def annotate(toc_id):
    offset = getrange(toc_id)['open']
    open = offset + request.json['start']
    close = offset + request.json['end']
    bookid = toc_id.split('-')[0]
    author = request.json['author']
    text = request.json['text']
    db.session.add(Annotation(bookid, author, open, close, text))
    db.session.commit()
    return "true"

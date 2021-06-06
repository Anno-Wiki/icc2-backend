from flask import request
from flask_praetorian import auth_required, current_user

from app import db
from app.main import bp
from .routes import getrange
from app.models.annotations import Annotation

@bp.route('/annotate/toc/<toc_id>', methods=['POST'])
@auth_required
def annotate(toc_id):
    print(request.json)
    offset = getrange(toc_id)['open']
    open = offset + request.json['start']
    close = offset + request.json['end']
    bookid = toc_id.split('-')[0]

    text = request.json['text']
    db.session.add(Annotation(bookid, current_user(), open, close, text))
    db.session.commit()
    return "true"

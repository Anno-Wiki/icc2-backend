from dateutil.parser import isoparse as ip
from flask import current_app as app, request

from app import db
from app.main import bp
from app.utils import requires_auth
from app.models.users import User

@bp.route('/users/login', methods=["POST"])
@requires_auth
def login():
    if request.json and request.json['sub']:
        u = User.query.filter_by(auth0id=request.json['sub']).first()
        if not u:
            u = User()
            u.displayname = request.json['displayname']
            u.auth0id = request.json['sub']
            db.session.add(u)
            db.session.commit()
        return 'true'
    return 'false'

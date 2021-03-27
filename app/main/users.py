from flask import current_app as app

from app.main import bp

@bp.route('/users/<auth0id>')
def login(auth0id):
    return auth0id

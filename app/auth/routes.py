from flask import request

from app import guard, db
from app.auth import bp
from app.models import User
from app.utils import custom_abort


@bp.route('/register', methods=['POST'])
def register():
    req = request.json
    username = req.get('username', None)
    password = req.get('password', None)

    if not username or not password:
        custom_abort("Required fields: 'username', 'password'")
    if User.query.filter(User.username==username).first():
        custom_abort("User {} already exists".format(username))

    u = User()
    u.username = username
    u.password = password
    db.session.add(u)
    db.session.commit()
    return {'success': True}


@bp.route('/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = request.json
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@bp.route('/refresh')
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refreshed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    token = request.headers.get('Authorization', '')
    try:
        token = token.split(' ')[-1]
    except:
        token = b''
    new_token = guard.refresh_jwt_token(token)
    ret = {'access_token': new_token}
    return ret, 200

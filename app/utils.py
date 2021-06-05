from flask import make_response, jsonify, abort
from app import db

def custom_abort(message, code=400):
    response = make_response(jsonify(message=message), code)
    db.session.rollback()
    abort(response)

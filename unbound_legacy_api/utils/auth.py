from time import time
from functools import wraps

import bcrypt
from flask import abort, jsonify, request, g, current_app
import jwt

from unbound_legacy_api.database.models import User

def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def create_token(username, password):
    '''
    Returns a token for the user if they exist and gave correct login info
    '''
    user = g.db.query(User).filter_by(username=username).one_or_none()

    if user is not None and bcrypt.checkpw(password, str(user.password)):
        return create_jwt(user.username)
    else:
        return None


def create_jwt(username, **kwargs):
    jwt_payload = {"iss"     : "api.unboundlegacy.com",
                   "username": username,
                   "exp"     : str(int(time()) + 36000)} # add in 10 hours

    token =  jwt.encode(jwt_payload, current_app.config['JWT_SECRET'], algorithm='HS256')
    return token

def auth_required(**token_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers['Authorization']
                decoded_token = jwt.decode(str(token), current_app.config['JWT_SECRET'])
            except KeyError:
                abort(401)
            except jwt.exceptions.DecodeError:
                abort(401)

            return func(*args, **kwargs)
        return wrapper
    return decorator

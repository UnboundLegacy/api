from time import time
from functools import wraps

import bcrypt
from flask import abort, jsonify, request, g, current_app, session, redirect
import jwt

from career_connections.database.models import User


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def check_credentials(username, password):
    user = g.db.query(User).filter_by(username=username).one_or_none()
    if user is not None and bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        return user
    return None


def login(username, password):
    user = check_credentials(username, password)
    if not user:
        return False

    session['is_authenticated'] = True
    session['user'] = user.to_dict(columns=['username', 'email', 'first_name', 'last_name'])

    return True


def logout():
    session['is_authenticated'] = False
    session['user'] = None


def auth_required(**token_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session['is_authenticated']:
                return redirect('/')

            return func(*args, **kwargs)
        return wrapper
    return decorator

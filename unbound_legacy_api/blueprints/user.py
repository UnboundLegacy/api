from flask import Blueprint, request, g

from unbound_legacy_api.database.models import User
from unbound_legacy_api.utils.auth import hash_password, create_token, auth_required
from unbound_legacy_api.utils.response import create_response

user_bp = Blueprint('user', __name__, url_prefix='/v1')

@user_bp.route('/auth', methods=['POST'])
def authentication():
    data = request.get_json()
    username = str(data['username'])
    password = str(data['password'])

    token = create_token(username, password)
    if token:
        return create_response(data=dict(token=token), status='success')
    else:
        return create_response(status='Invalid UN/PW', http_code=401)

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=str(data['username']),
                password=hash_password(str(data['password'])),
                email=str(data['email']))
    g.db.add(user)
    g.db.commit()

    return create_response(status='success')

@user_bp.route('/user', methods=['GET'])
@auth_required()
def get_users():
    users = g.db.query(User).all()
    users_list = [ user.to_dict() for user in users ]
    return create_response(data=dict(users=users_list))


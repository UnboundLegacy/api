import uuid

from flask import Blueprint, render_template, redirect, request, g, abort

from career_connections.database.models import PendingUser, User
from career_connections.utils.auth import auth_required
from career_connections.utils.email_agent import Message


admin_views_bp = Blueprint('admin_views', __name__)

@admin_views_bp.route('/admin/pendinguser/approve', methods=['POST', 'GET'])
@auth_required()
def approve_user():
    user_id = request.args.get('id')
    user = g.db.query(PendingUser).filter(PendingUser.pending_user_id==user_id).one()
    user.update(is_approved=True, invite_code=str(uuid.uuid4()))
    g.db.commit()

    # Improve: implement a task queue to offload sending email during a request
    ctx = user.to_dict()
    message = Message('unboundlegacyemails@gmail.com', user.email, 'email/accepted.html.j2', ctx)
    g.email.send_message(message)


    return redirect('/admin/pendinguser')

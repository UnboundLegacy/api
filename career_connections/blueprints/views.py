from flask import Blueprint, render_template

from career_connections.utils.auth import auth_required

views_bp = Blueprint('views', __name__)

@views_bp.route('/dashboard')
@auth_required()
def home():
    return render_template('base.j2')

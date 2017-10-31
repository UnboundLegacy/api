from flask import Blueprint

from unbound_legacy_api.utils.response import create_response

stats_bp = Blueprint('stats', __name__, url_prefix='/v1/stats')

@stats_bp.route('/ping')
def ping():
    """Generic ping route to check if api is up"""
    return create_response(status='success')

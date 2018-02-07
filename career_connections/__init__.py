from flask import Flask, g
from flask_admin import Admin

from .blueprints import views_bp, unauth_views_bp, admin_views_bp
from .database import init_app_db
from .admin import configure_admin
from .utils.email_agent import GmailAgent

def create_app(config=None, environment=None):
    app = Flask(__name__, static_folder='static', instance_relative_config=True)
    app.config.from_object('instance.base.Config')
    app.config.from_pyfile('settings.py', silent=True)

    init_app_db(app)
    configure_email(app)
    configure_hook(app)
    configure_admin(app, app.config['SESSION'])

    for blueprint in [unauth_views_bp, views_bp, admin_views_bp]:
        app.register_blueprint(blueprint)

    return app


def configure_email(app):
    app.config['EMAIL_AGENT'] = GmailAgent(app.config['EMAIL_USERNAME'],
                                           app.config['EMAIL_PASSWORD'])


def configure_hook(app):
    @app.before_request
    def create_session():
        g.db = app.config['SESSION']()
        g.email = app.config['EMAIL_AGENT']

    @app.teardown_request
    def teardown_request(exception):
        app.config['SESSION'].remove()

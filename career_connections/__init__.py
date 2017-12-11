from flask import Flask, g
from flask_admin import Admin

from .blueprints import views_bp, unauth_views_bp
from .database import init_app_db
from .admin import configure_admin

def create_app(config=None, environment=None):
    app = Flask(__name__, static_folder='static')
    app.config.from_object('instance.base.Config')
    app.config.from_pyfile('settings.py', silent=True)

    init_app_db(app)
    configure_hook(app)
    configure_admin(app, app.config['SESSION'])

    for blueprint in [unauth_views_bp, views_bp]:
        app.register_blueprint(blueprint)

    return app

def configure_hook(app):
    @app.before_request
    def create_session():
        g.db = app.config['SESSION']()

    @app.teardown_request
    def teardown_request(exception):
        app.config['SESSION'].remove()

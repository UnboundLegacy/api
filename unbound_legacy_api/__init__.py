from flask import Flask, g

from .blueprints import stats_bp, user_bp
from .database import init_app_db

def create_app(config=None, environment=None):
    app = Flask(__name__)
    app.config.from_object('instance.base.Config')

    init_app_db(app)
    configure_hook(app)

    for blueprint in [stats_bp, user_bp]:
        app.register_blueprint(blueprint)

    return app

def configure_hook(app):
    @app.before_request
    def create_session():
        g.db = app.config['SESSION']()

    @app.teardown_request
    def teardown_request(exception):
        app.config['SESSION'].remove()

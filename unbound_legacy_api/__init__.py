from flask import Flask

from .blueprints import stats_bp

def create_app(config=None, environment=None):
    app = Flask(__name__)

    for blueprint in [stats_bp]:
        app.register_blueprint(blueprint)

    return app

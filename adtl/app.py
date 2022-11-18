from flask import Flask

from adtl.routes import app_routes


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("common/config.py")
    app.register_blueprint(app_routes)
    return app

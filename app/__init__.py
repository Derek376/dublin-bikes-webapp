from flask import Flask


def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    from .api_routes import api
    app.register_blueprint(api)

    return app
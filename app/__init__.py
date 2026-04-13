from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .routes import main
    app.register_blueprint(main)

    from .api_routes import api
    app.register_blueprint(api)

    return app
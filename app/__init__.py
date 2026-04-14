from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    from app.routes.api_live import live_bp
    from app.routes.api_db import db_bp
    from app.routes.pages import pages_bp
    from app.routes.auth import auth_bp
    from app.routes.favorites import favorites_bp

    app.register_blueprint(live_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(favorites_bp)

    return app
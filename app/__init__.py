from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.api_live import live_bp
    from app.routes.api_db import db_bp
    from app.routes.pages import pages_bp

    app.register_blueprint(live_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(pages_bp)

    return app
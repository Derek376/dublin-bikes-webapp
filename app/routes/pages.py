from flask import Blueprint, render_template
from app.config import Config

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html", google_maps_api_key=Config.GOOGLE_MAPS_API_KEY)


@pages_bp.route("/health")
def health():
    return {"status": "ok"}
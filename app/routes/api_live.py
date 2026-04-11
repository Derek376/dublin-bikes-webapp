from flask import Blueprint, jsonify
from app.services.external_api import (
    fetch_jcdecaux_live,
    fetch_openweather_current_live,
    fetch_openweather_hourly_live,
    fetch_openweather_daily_live,
)

live_bp = Blueprint("live", __name__, url_prefix="/api/live")

@live_bp.route("/jcdecaux")
def get_jcdecaux_live():
    data = fetch_jcdecaux_live()
    return jsonify(data)

@live_bp.route("/weather/current")
def get_weather_current_live():
    data = fetch_openweather_current_live()
    return jsonify(data)

@live_bp.route("/weather/hourly")
def get_weather_hourly_live():
    data = fetch_openweather_hourly_live()
    return jsonify(data)

@live_bp.route("/weather/daily")
def get_weather_daily_live():
    data = fetch_openweather_daily_live()
    return jsonify(data)
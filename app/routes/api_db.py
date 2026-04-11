from flask import Blueprint, jsonify, request
from app.services.queries import (
    get_all_stations_latest,
    get_station_latest,
    get_station_history,
    get_current_weather_latest,
    get_hourly_forecast_latest,
    get_daily_forecast_latest,
)

db_bp = Blueprint("db", __name__, url_prefix="/api/db")

@db_bp.route("/stations")
def get_stations():
    data = get_all_stations_latest()
    return jsonify(data)

@db_bp.route("/stations/<int:station_number>")
def get_station(station_number):
    data = get_station_latest(station_number)
    return jsonify(data)

@db_bp.route("/stations/<int:station_number>/history")
def get_station_history_route(station_number):
    limit = request.args.get("limit", default=50, type=int)
    data = get_station_history(station_number, limit)
    return jsonify(data)

@db_bp.route("/weather/current")
def get_db_weather_current():
    data = get_current_weather_latest()
    return jsonify(data)

@db_bp.route("/weather/hourly")
def get_db_weather_hourly():
    limit = request.args.get("limit", default=24, type=int)
    data = get_hourly_forecast_latest(limit)
    return jsonify(data)

@db_bp.route("/weather/daily")
def get_db_weather_daily():
    limit = request.args.get("limit", default=16, type=int)
    data = get_daily_forecast_latest(limit)
    return jsonify(data)
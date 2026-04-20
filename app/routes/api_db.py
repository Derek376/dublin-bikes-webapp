from flask import Blueprint, jsonify, request
import joblib
import pandas as pd
from datetime import datetime

from app.services.queries import (
    get_all_stations_latest,
    get_station_latest,
    get_station_history,
    get_current_weather_latest,
    get_hourly_forecast_latest,
    get_daily_forecast_latest,
)

db_bp = Blueprint("db", __name__, url_prefix="/api/db")
model = joblib.load("ml/best_bike_model.joblib")


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


@db_bp.route("/predict", methods=["GET"])
def predict_available_bikes():
    station_id = request.args.get("station_id", type=int)
    date_str = request.args.get("date")
    time_str = request.args.get("time")

    if station_id is None or not date_str or not time_str:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Missing required query parameters: station_id, date, time",
                }
            ),
            400,
        )

    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Invalid date/time format. Expected date=YYYY-MM-DD and time=HH:MM",
                }
            ),
            400,
        )

    hour = dt.hour
    day_of_week = dt.weekday()
    month = dt.month

    try:
        forecasts = get_hourly_forecast_latest(limit=120)

        if not forecasts:
            return (
                jsonify(
                    {"status": "error", "message": "No hourly forecast data returned"}
                ),
                404,
            )

        def parse_future_dt(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                normalized = (
                    value.replace("Z", "+00:00") if value.endswith("Z") else value
                )
                return datetime.fromisoformat(normalized)
            raise ValueError("Unsupported future_dt type")

        nearest = min(
            forecasts,
            key=lambda item: abs(
                (
                    parse_future_dt(item.get("future_dt")).replace(tzinfo=None) - dt
                ).total_seconds()
            ),
        )

        temp = nearest.get("temp", 12.0)
        humidity = nearest.get("humidity", 75.0)
        pressure = nearest.get("pressure", 1010.0)

    except Exception as e:
        print(f"Weather lookup failed in predict_available_bikes: {e}")
        return (
            jsonify({"status": "error", "message": f"Weather lookup failed: {str(e)}"}),
            500,
        )

    features = pd.DataFrame(
        [
            {
                "station_id": station_id,
                "hour": hour,
                "day_of_week": day_of_week,
                "month": month,
                "max_air_temperature_celsius": temp,
                "max_relative_humidity_percent": humidity,
                "max_barometric_pressure_hpa": pressure,
            }
        ],
        columns=[
            "station_id",
            "hour",
            "day_of_week",
            "month",
            "max_air_temperature_celsius",
            "max_relative_humidity_percent",
            "max_barometric_pressure_hpa",
        ],
    )

    prediction = model.predict(features)[0]
    predicted_available_bikes = max(0, int(round(prediction)))

    return jsonify(
        {
            "status": "success",
            "predicted_available_bikes": predicted_available_bikes,
            "station_id": station_id,
        }
    )

# app/app.py
from flask import Flask, jsonify, request

from app.services.external_api import (
    fetch_jcdecaux_live,
    fetch_openweather_current_live,
    fetch_openweather_hourly_live,
    fetch_openweather_daily_live,
)
from app.services.queries import (
    get_all_stations_latest,
    get_station_latest,
    get_station_history,
    get_current_weather_latest,
    get_hourly_forecast_latest,
    get_daily_forecast_latest,
)

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Dublin Bikes API is running",
        "routes": [
            "/api/live/jcdecaux",
            "/api/live/weather/current",
            "/api/live/weather/hourly",
            "/api/live/weather/daily",
            "/api/db/stations",
            "/api/db/stations/<station_number>",
            "/api/db/stations/<station_number>/history?limit=50",
            "/api/db/weather/current",
            "/api/db/weather/hourly?limit=24",
            "/api/db/weather/daily?limit=16",
        ]
    })


# ---------------------------
# Sprint 2 - Part 1: Live APIs
# ---------------------------
@app.route("/api/live/jcdecaux")
def api_live_jcdecaux():
    try:
        data = fetch_jcdecaux_live()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/live/weather/current")
def api_live_weather_current():
    try:
        data = fetch_openweather_current_live()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/live/weather/hourly")
def api_live_weather_hourly():
    try:
        data = fetch_openweather_hourly_live()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/live/weather/daily")
def api_live_weather_daily():
    try:
        cnt = int(request.args.get("cnt", 16))
        data = fetch_openweather_daily_live(cnt=cnt)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# Sprint 2 - Part 2: DB APIs
# ---------------------------
@app.route("/api/db/stations")
def api_db_stations():
    try:
        rows = get_all_stations_latest()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/db/stations/<int:station_number>")
def api_db_station_detail(station_number):
    try:
        row = get_station_latest(station_number)
        if not row:
            return jsonify({"error": "station not found"}), 404
        return jsonify(row)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/db/stations/<int:station_number>/history")
def api_db_station_history(station_number):
    try:
        limit = int(request.args.get("limit", 100))
        rows = get_station_history(station_number, limit=limit)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/db/weather/current")
def api_db_weather_current():
    try:
        row = get_current_weather_latest()
        return jsonify(row or {})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/db/weather/hourly")
def api_db_weather_hourly():
    try:
        limit = int(request.args.get("limit", 24))
        rows = get_hourly_forecast_latest(limit=limit)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/db/weather/daily")
def api_db_weather_daily():
    try:
        limit = int(request.args.get("limit", 16))
        rows = get_daily_forecast_latest(limit=limit)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
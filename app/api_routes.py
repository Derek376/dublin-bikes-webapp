import requests
import pymysql
from flask import Blueprint, jsonify

from scraper.dbinfo import (
    JCDECAUX_STATIONS_URI, JCDECAUX_API_KEY, JCDECAUX_CONTRACT,
    CURRENT_URL, OPENWEATHER_API_KEY, OPENWEATHER_LAT, OPENWEATHER_LON,
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME,
)

api = Blueprint("api", __name__)


# ---------- 数据库连接 ----------
def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


# ========== 1) 实时 JCDecaux ==========
@api.get("/api/jcdecaux/live")
def jcdecaux_live():
    try:
        resp = requests.get(JCDECAUX_STATIONS_URI, params={
            "apiKey": JCDECAUX_API_KEY,
            "contract": JCDECAUX_CONTRACT,
        }, timeout=20)
        resp.raise_for_status()
        return jsonify(resp.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502


# ========== 2) 实时 OpenWeather ==========
@api.get("/api/weather/live")
def weather_live():
    try:
        resp = requests.get(CURRENT_URL, params={
            "lat": OPENWEATHER_LAT,
            "lon": OPENWEATHER_LON,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }, timeout=20)
        resp.raise_for_status()
        return jsonify(resp.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502


# ========== 3) DB 读站点数据 ==========
@api.get("/api/stations")
def stations_from_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT number, name, address,
                       position_lat, position_lng,
                       banking, bike_stands
                FROM station
                ORDER BY number
            """)
            rows = cur.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ========== 4) DB 读最新天气 ==========
@api.get("/api/weather")
def weather_from_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT dt, temp, feels_like, humidity, pressure,
                       wind_speed, wind_gust, rain_1h, snow_1h,
                       clouds, visibility, weather_id,
                       sunrise, sunset
                FROM `current`
                ORDER BY dt DESC
                LIMIT 1
            """)
            row = cur.fetchone()
        return jsonify(row or {}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
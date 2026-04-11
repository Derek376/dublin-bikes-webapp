# app/services/external_api.py
import requests
from app.config import Config


def fetch_jcdecaux_live():
    params = {
        "apiKey": Config.JCDECAUX_API_KEY,
        "contract": Config.JCDECAUX_CONTRACT
    }
    r = requests.get(Config.JCDECAUX_STATIONS_URI, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_current_live():
    params = {
        "lat": Config.OPENWEATHER_LAT,
        "lon": Config.OPENWEATHER_LON,
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(Config.CURRENT_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_hourly_live():
    params = {
        "lat": Config.OPENWEATHER_LAT,
        "lon": Config.OPENWEATHER_LON,
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(Config.HOURLY_4D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_daily_live(cnt=16):
    params = {
        "lat": Config.OPENWEATHER_LAT,
        "lon": Config.OPENWEATHER_LON,
        "cnt": int(cnt),
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(Config.DAILY_16D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()
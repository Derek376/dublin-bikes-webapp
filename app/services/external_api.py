# app/services/external_api.py
import os
import sys
import requests
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(CURRENT_DIR, "..", "..")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

SCRAPER_DIR = os.path.join(PROJECT_ROOT, "scraper")
if SCRAPER_DIR not in sys.path:
    sys.path.append(SCRAPER_DIR)

from dbinfo import (  # noqa
    JCDECAUX_API_KEY, JCDECAUX_CONTRACT, JCDECAUX_STATIONS_URI,
    OPENWEATHER_API_KEY, OPENWEATHER_LAT, OPENWEATHER_LON,
    CURRENT_URL, HOURLY_4D_URL, DAILY_16D_URL
)


def fetch_jcdecaux_live():
    params = {
        "apiKey": JCDECAUX_API_KEY,
        "contract": JCDECAUX_CONTRACT
    }
    r = requests.get(JCDECAUX_STATIONS_URI, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_current_live():
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(CURRENT_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_hourly_live():
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(HOURLY_4D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_openweather_daily_live(cnt=16):
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "cnt": int(cnt),
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    r = requests.get(DAILY_16D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()
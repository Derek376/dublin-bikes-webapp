import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # MySQL
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")  # forced to be read from the environment.
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME")

    # JCDecaux
    JCDECAUX_API_KEY = os.getenv("JCDECAUX_API_KEY")
    JCDECAUX_CONTRACT = os.getenv("JCDECAUX_CONTRACT", "dublin")
    JCDECAUX_STATIONS_URI = os.getenv(
        "JCDECAUX_STATIONS_URI", "https://api.jcdecaux.com/vls/v1/stations"
    )

    # OpenWeather
    # Developer plan allows:
    # - Hourly forecast: 4 days
    # - Daily forecast: 16 days
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    OPENWEATHER_LAT = float(os.getenv("OPENWEATHER_LAT", "53.3498"))  # Dublin
    OPENWEATHER_LON = float(os.getenv("OPENWEATHER_LON", "-6.2603"))
    CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
    HOURLY_4D_URL = "https://pro.openweathermap.org/data/2.5/forecast/hourly"
    DAILY_16D_URL = "https://api.openweathermap.org/data/2.5/forecast/daily"

    # Scraping intervals (in seconds)
    JCDECAUX_SCRAPE_INTERVAL = int(
        os.getenv("JCDECAUX_SCRAPE_INTERVAL", "300")
    )  # 5 min
    OPENWEATHER_SCRAPE_INTERVAL = int(
        os.getenv("OPENWEATHER_SCRAPE_INTERVAL", "600")
    )  # 10 min
    MAIN_LOOP_SLEEP = int(
        os.getenv("MAIN_LOOP_SLEEP", "30")
    )  # Sleep time between checks in the main loop

    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
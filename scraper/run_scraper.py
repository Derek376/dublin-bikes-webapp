# scraper/run_scraper.py
import time
import traceback
from datetime import datetime, UTC

from scraper.create_tables import create_database, create_tables
from scraper.scrape_jcdecaux import scrape_once as scrape_jcdecaux_once
from scraper.scrape_openweather import scrape_once as scrape_openweather_once
from app.config import Config


def main():
    create_database()
    create_tables()

    last_jc = 0.0
    last_ow = 0.0

    print("Scraper started.")
    while True:
        now = time.time()

        # JCDecaux
        if now - last_jc >= Config.JCDECAUX_SCRAPE_INTERVAL:
            try:
                n = scrape_jcdecaux_once()
                print(f"[{datetime.now(UTC)}] JCDecaux updated: {n} stations")
                last_jc = now
            except Exception:
                print("[JCDecaux] scrape failed:")
                print(traceback.format_exc())

        # OpenWeather
        if now - last_ow >= Config.OPENWEATHER_SCRAPE_INTERVAL:
            try:
                scrape_openweather_once()
                print(f"[{datetime.now(UTC)}] OpenWeather updated")
                last_ow = now
            except Exception:
                print("[OpenWeather] scrape failed:")
                print(traceback.format_exc())

        time.sleep(Config.MAIN_LOOP_SLEEP)


if __name__ == "__main__":
    main()
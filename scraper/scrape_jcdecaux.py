# scraper/scrape_jcdecaux.py
from datetime import UTC, datetime, timezone
import requests
import pymysql

from dbinfo import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
    JCDECAUX_API_KEY, JCDECAUX_CONTRACT, JCDECAUX_STATIONS_URI
)


def get_conn():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4", autocommit=True
    )


def ms_epoch_to_dt(ms: int):
    # JCDecaux last_update: Unix epoch milliseconds
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=UTC).replace(tzinfo=None)


def fetch_stations():
    params = {
        "apiKey": JCDECAUX_API_KEY,
        "contract": JCDECAUX_CONTRACT
    }
    r = requests.get(JCDECAUX_STATIONS_URI, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def upsert_station_and_availability(stations):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            station_sql = """
                INSERT INTO station (
                    number, address, banking, bike_stands, name, position_lat, position_lng
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    address=VALUES(address),
                    banking=VALUES(banking),
                    bike_stands=VALUES(bike_stands),
                    name=VALUES(name),
                    position_lat=VALUES(position_lat),
                    position_lng=VALUES(position_lng);
            """
            availability_sql = """
                INSERT INTO availability (
                    number, last_update, available_bikes, available_bike_stands, status
                ) VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    available_bikes=VALUES(available_bikes),
                    available_bike_stands=VALUES(available_bike_stands),
                    status=VALUES(status);
            """

            for s in stations:
                pos = s.get("position") or {}
                number = s.get("number")
                if number is None:
                    continue

                # station (static)
                cur.execute(station_sql, (
                    number,
                    s.get("address"),
                    int(bool(s.get("banking"))) if s.get("banking") is not None else None,
                    s.get("bike_stands"),
                    s.get("name"),
                    pos.get("lat"),
                    pos.get("lng")
                ))

                # availability (dynamic)
                last_update = ms_epoch_to_dt(s.get("last_update"))
                if last_update is None:
                    continue

                cur.execute(availability_sql, (
                    number,
                    last_update,
                    s.get("available_bikes"),
                    s.get("available_bike_stands"),
                    s.get("status")
                ))
    finally:
        conn.close()


def scrape_once():
    stations = fetch_stations()
    upsert_station_and_availability(stations)
    return len(stations)


if __name__ == "__main__":
    n = scrape_once()
    print(f"JCDecaux scrape done. stations fetched: {n}")

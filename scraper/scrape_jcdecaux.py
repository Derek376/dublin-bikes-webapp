import time
from datetime import datetime, timezone
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import dbinfo


def to_dt_from_ms(ms: int) -> datetime:
    """
    JCDecaux last_update is an epoch timestamp in milliseconds.
    Convert it to a Python datetime (UTC naive) for MySQL DATETIME insertion.
    """
    if ms is None:
        return datetime.utcnow()
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(tzinfo=None)


def fetch_stations_json() -> list:
    """Fetch the station JSON list from JCDecaux."""
    resp = requests.get(dbinfo.JCD_STATIONS_URL, timeout=dbinfo.HTTP_TIMEOUT_SECONDS)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("JCDecaux response is not a list.")
    return data


def upsert_station(conn, stations: list) -> int:
    """
    Write to station (static information).
    Use ON DUPLICATE KEY UPDATE to upsert by primary key `number`.
    """
    sql = text("""
        INSERT INTO station (
            number, address, banking, bike_stands, name, position_lat, position_lng
        ) VALUES (
            :number, :address, :banking, :bike_stands, :name, :position_lat, :position_lng
        )
        ON DUPLICATE KEY UPDATE
            address = VALUES(address),
            banking = VALUES(banking),
            bike_stands = VALUES(bike_stands),
            name = VALUES(name),
            position_lat = VALUES(position_lat),
            position_lng = VALUES(position_lng);
    """)

    rows = []
    for s in stations:
        pos = s.get("position", {}) or {}
        rows.append(
            {
                "number": s.get("number"),
                "address": s.get("address"),
                "banking": int(bool(s.get("banking"))) if s.get("banking") is not None else None,
                "bike_stands": s.get("bike_stands"),
                "name": s.get("name"),
                "position_lat": pos.get("lat"),
                "position_lng": pos.get("lng"),
            }
        )

    # executemany
    conn.execute(sql, rows)
    return len(rows)


def insert_availability(conn, stations: list) -> int:
    """
    Write to availability (dynamic snapshots).
    Primary key is (number, last_update); duplicates are ignored via INSERT IGNORE.
    """
    sql = text("""
        INSERT IGNORE INTO availability (
            number, last_update, available_bikes, available_bike_stands, status
        ) VALUES (
            :number, :last_update, :available_bikes, :available_bike_stands, :status
        );
    """)

    rows = []
    for s in stations:
        rows.append(
            {
                "number": s.get("number"),
                "last_update": to_dt_from_ms(s.get("last_update")),
                "available_bikes": s.get("available_bikes"),
                "available_bike_stands": s.get("available_bike_stands"),
                "status": s.get("status"),
            }
        )

    conn.execute(sql, rows)
    return len(rows)


def run_once(engine) -> None:
    """Fetch once and write to the database."""
    stations = fetch_stations_json()

    with engine.begin() as conn:
        n_station = upsert_station(conn, stations)
        n_avail = insert_availability(conn, stations)

    print(
        f"[{datetime.utcnow().isoformat()}] "
        f"station upsert: {n_station}, availability insert attempt: {n_avail}"
    )


def main():
    # Use DB_URI from dbinfo.py
    engine = create_engine(dbinfo.DB_URI, pool_pre_ping=True, future=True)

    # Scrape interval in seconds; default is 300 seconds (5 minutes)
    interval = getattr(dbinfo, "SCRAPE_INTERVAL_SECONDS", 300)

    print("JCDecaux scraper started.")
    print(f"Interval: {interval}s")
    print("Press Ctrl+C to stop.")

    while True:
        try:
            run_once(engine)
        except requests.RequestException as e:
            print(f"[NETWORK ERROR] {e}")
        except SQLAlchemyError as e:
            print(f"[DB ERROR] {e}")
        except Exception as e:
            print(f"[UNEXPECTED ERROR] {e}")

        time.sleep(interval)


if __name__ == "__main__":
    main()

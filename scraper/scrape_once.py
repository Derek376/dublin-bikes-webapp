import requests
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
import dbinfo

def get_engine():
    conn = f"mysql+pymysql://{dbinfo.DB_USER}:{dbinfo.DB_PASSWORD}@{dbinfo.DB_HOST}:{dbinfo.DB_PORT}/{dbinfo.DB_NAME}"
    return create_engine(conn, future=True)

def fetch_stations():
    params = {"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME}
    r = requests.get(dbinfo.STATIONS_URI, params=params, timeout=20)
    r.raise_for_status()  # throw exception if not 200 OK
    data = r.json()
    if not isinstance(data, list):
        raise ValueError("Unexpected API response format: not a list")
    return data

def ms_to_datetime(ms):
    # JCDecaux API returns timestamps in milliseconds since epoch, convert to datetime
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(tzinfo=None)

def upsert_station(conn, s):
    sql = text("""
        INSERT INTO station (number, name, address, latitude, longitude, banking, bikestands, status)
        VALUES (:number, :name, :address, :lat, :lng, :banking, :bikestands, :status)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            address = VALUES(address),
            latitude = VALUES(latitude),
            longitude = VALUES(longitude),
            banking = VALUES(banking),
            bikestands = VALUES(bikestands),
            status = VALUES(status);
    """)
    conn.execute(sql, {
        "number": s.get("number"),
        "name": s.get("name"),
        "address": s.get("address"),
        "lat": s.get("position", {}).get("lat"),
        "lng": s.get("position", {}).get("lng"),
        "banking": int(bool(s.get("banking"))),
        "bikestands": s.get("bike_stands"),
        "status": s.get("status")
    })

def insert_availability(conn, s):
    last_update = s.get("last_update")
    if last_update is None:
        return

    sql = text("""
        INSERT INTO availability (number, available_bikes, available_bike_stands, status, last_update)
        VALUES (:number, :available_bikes, :available_bike_stands, :status, :last_update);
    """)
    conn.execute(sql, {
        "number": s.get("number"),
        "available_bikes": s.get("available_bikes"),
        "available_bike_stands": s.get("available_bike_stands"),
        "status": s.get("status"),
        "last_update": ms_to_datetime(last_update)
    })

def main():
    engine = get_engine()
    stations = fetch_stations()

    with engine.begin() as conn:  #  commit/rollback
        for s in stations:
            upsert_station(conn, s)      # upsert static info
            insert_availability(conn, s) # insert dynamic snapshot

    print(f"Done. Inserted snapshot for {len(stations)} stations.")

if __name__ == "__main__":
    main()

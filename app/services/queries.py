# app/services/queries.py
from app.db import get_conn


def get_all_stations_latest():
    """
    each station's latest availability, join with station info
    """
    sql = """
    SELECT
        s.number,
        s.name,
        s.address,
        s.position_lat,
        s.position_lng,
        s.bike_stands,
        a.available_bikes,
        a.available_bike_stands,
        a.status,
        a.last_update
    FROM station s
    JOIN availability a
      ON s.number = a.number
    JOIN (
        SELECT number, MAX(last_update) AS max_last_update
        FROM availability
        GROUP BY number
    ) latest
      ON a.number = latest.number
     AND a.last_update = latest.max_last_update
    ORDER BY s.number;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


def get_station_latest(station_number: int):
    sql = """
    SELECT
        s.number,
        s.name,
        s.address,
        s.position_lat,
        s.position_lng,
        s.bike_stands,
        a.available_bikes,
        a.available_bike_stands,
        a.status,
        a.last_update
    FROM station s
    JOIN availability a ON s.number = a.number
    WHERE s.number = %s
    ORDER BY a.last_update DESC
    LIMIT 1;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (station_number,))
            return cur.fetchone()
    finally:
        conn.close()


def get_station_history(station_number: int, limit: int = 100):
    sql = """
    SELECT
        number,
        last_update,
        available_bikes,
        available_bike_stands,
        status
    FROM availability
    WHERE number = %s
    ORDER BY last_update DESC
    LIMIT %s;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (station_number, limit))
            return cur.fetchall()
    finally:
        conn.close()


def get_current_weather_latest():
    sql = """
    SELECT *
    FROM current
    ORDER BY dt DESC
    LIMIT 1;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchone()
    finally:
        conn.close()


def get_hourly_forecast_latest(limit: int = 24):
    """
    fetch the latest hourly forecast, which contains multiple rows for different future hours
    """
    sql = """
    SELECT *
    FROM hourly
    WHERE dt = (SELECT MAX(dt) FROM hourly)
    ORDER BY future_dt ASC
    LIMIT %s;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()
    finally:
        conn.close()


def get_daily_forecast_latest(limit: int = 16):
    sql = """
    SELECT *
    FROM daily
    WHERE dt = (SELECT MAX(dt) FROM daily)
    ORDER BY future_dt ASC
    LIMIT %s;
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()
    finally:
        conn.close()
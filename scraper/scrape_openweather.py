# scrape_openweather.py
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from collections import defaultdict

import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import dbinfo


def unix_to_dt(ts: Optional[int]) -> Optional[datetime]:
    """
    Convert Unix timestamp (seconds) to UTC naive datetime for MySQL DATETIME.
    """
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)


def safe_get(d: Dict[str, Any], path: List[str], default=None):
    """
    Safely get nested dictionary values.
    """
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def build_weather_url() -> str:
    """
    Build OpenWeather Current Weather API URL (free plan).
    """
    return (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={dbinfo.OWM_LAT}&lon={dbinfo.OWM_LON}"
        f"&appid={dbinfo.OWM_API_KEY}&units=metric"
    )


def build_forecast_url() -> str:
    """
    Build OpenWeather 5 day / 3 hour Forecast API URL (free plan).
    """
    return (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={dbinfo.OWM_LAT}&lon={dbinfo.OWM_LON}"
        f"&appid={dbinfo.OWM_API_KEY}&units=metric"
    )


def fetch_json(url: str, timeout_sec: int) -> Dict[str, Any]:
    """
    Fetch JSON from URL and validate response object type.
    """
    resp = requests.get(url, timeout=timeout_sec)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, dict):
        raise ValueError("API response is not a JSON object.")
    return data


def insert_current(conn, current_data: Dict[str, Any]) -> int:
    """
    Insert one row into `current` table from /weather response.
    Duplicate primary key (dt) is ignored.
    """
    weather_arr = current_data.get("weather", []) or []
    weather_id = weather_arr[0].get("id") if weather_arr else None

    rain_1h = safe_get(current_data, ["rain", "1h"])
    snow_1h = safe_get(current_data, ["snow", "1h"])

    row = {
        "dt": unix_to_dt(current_data.get("dt")),
        "feels_like": safe_get(current_data, ["main", "feels_like"]),
        "humidity": safe_get(current_data, ["main", "humidity"]),
        "pressure": safe_get(current_data, ["main", "pressure"]),
        "sunrise": unix_to_dt(safe_get(current_data, ["sys", "sunrise"])),
        "sunset": unix_to_dt(safe_get(current_data, ["sys", "sunset"])),
        "temp": safe_get(current_data, ["main", "temp"]),
        "weather_id": weather_id,
        "wind_gust": safe_get(current_data, ["wind", "gust"]),
        "wind_speed": safe_get(current_data, ["wind", "speed"]),
        "rain_1h": rain_1h,
        "snow_1h": snow_1h,
        "clouds": safe_get(current_data, ["clouds", "all"]),
        "visibility": current_data.get("visibility"),
    }

    if row["dt"] is None:
        return 0

    sql = text("""
        INSERT IGNORE INTO `current` (
            dt, feels_like, humidity, pressure, sunrise, sunset, `temp`,
            weather_id, wind_gust, wind_speed, rain_1h, snow_1h, clouds, visibility
        ) VALUES (
            :dt, :feels_like, :humidity, :pressure, :sunrise, :sunset, :temp,
            :weather_id, :wind_gust, :wind_speed, :rain_1h, :snow_1h, :clouds, :visibility
        );
    """)
    conn.execute(sql, row)
    return 1


def insert_hourly(conn, forecast_data: Dict[str, Any], scrape_dt: datetime) -> int:
    """
    Insert forecast slots (3-hour intervals) into `hourly` table.
    Primary key is (dt, future_dt).
    """
    items = forecast_data.get("list", []) or []
    rows = []

    for item in items:
        weather_arr = item.get("weather", []) or []
        weather_id = weather_arr[0].get("id") if weather_arr else None

        # In forecast API, rain/snow keys may be "3h"
        rain_3h = safe_get(item, ["rain", "3h"])
        snow_3h = safe_get(item, ["snow", "3h"])

        # Map 3h precipitation to *_1h columns by keeping raw amount in same field for consistency.
        row = {
            "dt": scrape_dt,
            "future_dt": unix_to_dt(item.get("dt")),
            "feels_like": safe_get(item, ["main", "feels_like"]),
            "humidity": safe_get(item, ["main", "humidity"]),
            "pop": item.get("pop"),
            "pressure": safe_get(item, ["main", "pressure"]),
            "temp": safe_get(item, ["main", "temp"]),
            "weather_id": weather_id,
            "wind_speed": safe_get(item, ["wind", "speed"]),
            "wind_gust": safe_get(item, ["wind", "gust"]),
            "rain_1h": rain_3h,
            "snow_1h": snow_3h,
            "clouds": safe_get(item, ["clouds", "all"]),
            "visibility": item.get("visibility"),
        }

        if row["future_dt"] is not None:
            rows.append(row)

    if not rows:
        return 0

    sql = text("""
        INSERT IGNORE INTO hourly (
            dt, future_dt, feels_like, humidity, pop, pressure, `temp`,
            weather_id, wind_speed, wind_gust, rain_1h, snow_1h, clouds, visibility
        ) VALUES (
            :dt, :future_dt, :feels_like, :humidity, :pop, :pressure, :temp,
            :weather_id, :wind_speed, :wind_gust, :rain_1h, :snow_1h, :clouds, :visibility
        );
    """)
    conn.execute(sql, rows)
    return len(rows)


def aggregate_daily_from_forecast(forecast_items: List[Dict[str, Any]], scrape_dt: datetime) -> List[Dict[str, Any]]:
    """
    Aggregate 3-hour forecast items into daily rows for `daily` table.
    """
    grouped = defaultdict(list)
    for item in forecast_items:
        dt_obj = unix_to_dt(item.get("dt"))
        if dt_obj is None:
            continue
        day_key = dt_obj.date()
        grouped[day_key].append(item)

    daily_rows = []
    for day_key, items in grouped.items():
        temps = [safe_get(x, ["main", "temp"]) for x in items if safe_get(x, ["main", "temp"]) is not None]
        humidities = [safe_get(x, ["main", "humidity"]) for x in items if safe_get(x, ["main", "humidity"]) is not None]
        pressures = [safe_get(x, ["main", "pressure"]) for x in items if safe_get(x, ["main", "pressure"]) is not None]
        pops = [x.get("pop") for x in items if x.get("pop") is not None]
        wind_speeds = [safe_get(x, ["wind", "speed"]) for x in items if safe_get(x, ["wind", "speed"]) is not None]
        wind_gusts = [safe_get(x, ["wind", "gust"]) for x in items if safe_get(x, ["wind", "gust"]) is not None]
        clouds = [safe_get(x, ["clouds", "all"]) for x in items if safe_get(x, ["clouds", "all"]) is not None]

        rain_total = 0.0
        snow_total = 0.0
        weather_counter = defaultdict(int)

        for x in items:
            r = safe_get(x, ["rain", "3h"])
            s = safe_get(x, ["snow", "3h"])
            if r is not None:
                rain_total += float(r)
            if s is not None:
                snow_total += float(s)

            w_arr = x.get("weather", []) or []
            if w_arr and isinstance(w_arr[0], dict) and w_arr[0].get("id") is not None:
                weather_counter[w_arr[0]["id"]] += 1

        weather_id = None
        if weather_counter:
            weather_id = max(weather_counter.items(), key=lambda kv: kv[1])[0]

        future_dt = datetime(day_key.year, day_key.month, day_key.day)

        row = {
            "dt": scrape_dt,
            "future_dt": future_dt,
            "humidity": int(sum(humidities) / len(humidities)) if humidities else None,
            "pop": max(pops) if pops else None,
            "pressure": int(sum(pressures) / len(pressures)) if pressures else None,
            "temp_max": max(temps) if temps else None,
            "temp_min": min(temps) if temps else None,
            "weather_id": weather_id,
            "wind_speed": sum(wind_speeds) / len(wind_speeds) if wind_speeds else None,
            "wind_gust": max(wind_gusts) if wind_gusts else None,
            "rain": rain_total if rain_total > 0 else None,
            "snow": snow_total if snow_total > 0 else None,
            "clouds": int(sum(clouds) / len(clouds)) if clouds else None,
        }
        daily_rows.append(row)

    return daily_rows


def insert_daily(conn, forecast_data: Dict[str, Any], scrape_dt: datetime) -> int:
    """
    Insert aggregated daily rows into `daily` table.
    """
    items = forecast_data.get("list", []) or []
    rows = aggregate_daily_from_forecast(items, scrape_dt)

    if not rows:
        return 0

    sql = text("""
        INSERT IGNORE INTO daily (
            dt, future_dt, humidity, pop, pressure, temp_max, temp_min,
            weather_id, wind_speed, wind_gust, rain, snow, clouds
        ) VALUES (
            :dt, :future_dt, :humidity, :pop, :pressure, :temp_max, :temp_min,
            :weather_id, :wind_speed, :wind_gust, :rain, :snow, :clouds
        );
    """)
    conn.execute(sql, rows)
    return len(rows)


def run_once(engine) -> None:
    """
    Fetch weather and forecast once, then write to current/hourly/daily tables.
    """
    timeout_sec = getattr(dbinfo, "HTTP_TIMEOUT_SECONDS", 20)
    current_json = fetch_json(build_weather_url(), timeout_sec)
    forecast_json = fetch_json(build_forecast_url(), timeout_sec)

    scrape_dt = unix_to_dt(current_json.get("dt")) or datetime.utcnow()

    with engine.begin() as conn:
        n_current = insert_current(conn, current_json)
        n_hourly = insert_hourly(conn, forecast_json, scrape_dt)
        n_daily = insert_daily(conn, forecast_json, scrape_dt)

    print(
        f"[{datetime.utcnow().isoformat()}] "
        f"current: {n_current}, hourly: {n_hourly}, daily: {n_daily}"
    )


def main():
    """
    Main loop with periodic execution.
    """
    engine = create_engine(dbinfo.DB_URI, pool_pre_ping=True, future=True)
    interval = getattr(dbinfo, "WEATHER_INTERVAL_SECONDS", 600)

    print("OpenWeather (free plan) scraper started.")
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

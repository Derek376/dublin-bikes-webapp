# scraper/scrape_openweather.py
from datetime import datetime, timezone, UTC
import requests
import pymysql

from dbinfo import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
    OPENWEATHER_API_KEY, OPENWEATHER_LAT, OPENWEATHER_LON, CURRENT_URL, HOURLY_4D_URL, DAILY_16D_URL
)

def get_conn():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, charset="utf8mb4", autocommit=True
    )


def unix_to_dt(sec):
    if sec is None:
        return None
    return datetime.fromtimestamp(int(sec), tz=UTC).replace(tzinfo=None)


def _weather_id(obj: dict):
    w = (obj.get("weather") or [{}])[0]
    return w.get("id")


def fetch_current():
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "appid": (OPENWEATHER_API_KEY or "").strip(),
        "units": "metric"
    }
    r = requests.get(CURRENT_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_hourly_4days():
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "appid": (OPENWEATHER_API_KEY or "").strip(),
        "units": "metric"
    }
    r = requests.get(HOURLY_4D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_daily(cnt=16):
    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "cnt": int(cnt),
        "appid": (OPENWEATHER_API_KEY or "").strip(),
        "units": "metric"
    }
    r = requests.get(DAILY_16D_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def insert_current(cur_json):
    """
    /data/2.5/weather
    """
    dt_now = unix_to_dt(cur_json.get("dt"))
    if dt_now is None:
        return

    main = cur_json.get("main") or {}
    wind = cur_json.get("wind") or {}
    clouds = (cur_json.get("clouds") or {}).get("all")
    visibility = cur_json.get("visibility")
    sys = cur_json.get("sys") or {}

    # rain/snow 1h may be missing, or rain/snow itself may be missing. Use (dict.get() or {}) to avoid KeyError.
    rain_1h = (cur_json.get("rain") or {}).get("1h")
    snow_1h = (cur_json.get("snow") or {}).get("1h")

    sql = """
        INSERT INTO current (
            dt, sunrise, sunset,
            temp, feels_like,
            humidity, pressure,
            wind_speed, wind_gust,
            weather_id, clouds, visibility,
            rain_1h, snow_1h
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            sunrise=VALUES(sunrise),
            sunset=VALUES(sunset),
            temp=VALUES(temp),
            feels_like=VALUES(feels_like),
            humidity=VALUES(humidity),
            pressure=VALUES(pressure),
            wind_speed=VALUES(wind_speed),
            wind_gust=VALUES(wind_gust),
            weather_id=VALUES(weather_id),
            clouds=VALUES(clouds),
            visibility=VALUES(visibility),
            rain_1h=VALUES(rain_1h),
            snow_1h=VALUES(snow_1h);
    """

    vals = (
        dt_now,
        unix_to_dt(sys.get("sunrise")),
        unix_to_dt(sys.get("sunset")),
        main.get("temp"),
        main.get("feels_like"),
        main.get("humidity"),
        main.get("pressure"),
        wind.get("speed"),
        wind.get("gust"),
        _weather_id(cur_json),
        clouds,
        visibility,
        rain_1h,
        snow_1h
    )

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, vals)
    finally:
        conn.close()


def insert_hourly(hourly_json):
    """
    pro /data/2.5/forecast/hourly
    JSON 通常包含 list: [{dt, main{temp,feels_like,pressure,humidity}, pop, clouds{all}, wind{speed,gust}, rain{1h}, snow{1h}, weather[...]}, ...]
    """
    base_dt = datetime.now(UTC)  # record the time we fetch the data, to calculate future_dt in SQL
    rows = hourly_json.get("list") or []

    sql = """
        INSERT INTO hourly (
            dt, future_dt,
            temp, feels_like,
            humidity, pressure,
            pop, clouds,
            wind_speed, wind_gust,
            weather_id, rain_1h, snow_1h
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            temp=VALUES(temp),
            feels_like=VALUES(feels_like),
            humidity=VALUES(humidity),
            pressure=VALUES(pressure),
            pop=VALUES(pop),
            clouds=VALUES(clouds),
            wind_speed=VALUES(wind_speed),
            wind_gust=VALUES(wind_gust),
            weather_id=VALUES(weather_id),
            rain_1h=VALUES(rain_1h),
            snow_1h=VALUES(snow_1h);
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for h in rows:
                main = h.get("main") or {}
                wind = h.get("wind") or {}
                clouds = (h.get("clouds") or {}).get("all")
                rain_1h = (h.get("rain") or {}).get("1h")
                snow_1h = (h.get("snow") or {}).get("1h")

                vals = (
                    base_dt,
                    unix_to_dt(h.get("dt")),
                    main.get("temp"),
                    main.get("feels_like"),
                    main.get("humidity"),
                    main.get("pressure"),
                    h.get("pop"),
                    clouds,
                    wind.get("speed"),
                    wind.get("gust"),
                    _weather_id(h),
                    rain_1h,
                    snow_1h
                )
                cur.execute(sql, vals)
    finally:
        conn.close()


def insert_daily(daily_json):
    """
    /data/2.5/forecast/daily?cnt=16
    list: [{dt, temp{min,max}, pressure, humidity, speed, gust, clouds, rain, snow, weather[...]}, ...]
    """
    base_dt = datetime.now(UTC)
    rows = daily_json.get("list") or []

    sql = """
        INSERT INTO daily (
            dt, future_dt,
            temp_min, temp_max,
            humidity, pressure,
            clouds,
            wind_speed, wind_gust,
            weather_id, rain, snow
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            temp_min=VALUES(temp_min),
            temp_max=VALUES(temp_max),
            humidity=VALUES(humidity),
            pressure=VALUES(pressure),
            clouds=VALUES(clouds),
            wind_speed=VALUES(wind_speed),
            wind_gust=VALUES(wind_gust),
            weather_id=VALUES(weather_id),
            rain=VALUES(rain),
            snow=VALUES(snow);
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for d in rows:
                temp = d.get("temp") or {}
                vals = (
                    base_dt,
                    unix_to_dt(d.get("dt")),
                    temp.get("min"),
                    temp.get("max"),
                    d.get("humidity"),
                    d.get("pressure"),
                    d.get("clouds"),
                    d.get("speed"),
                    d.get("gust"),
                    _weather_id(d),
                    d.get("rain"),
                    d.get("snow")
                )
                cur.execute(sql, vals)
    finally:
        conn.close()


def scrape_once():
    # 1) current
    cur = fetch_current()
    insert_current(cur)

    # 2) hourly 4 days (pro)
    hourly = fetch_hourly_4days()
    insert_hourly(hourly)

    # 3) daily 16 days
    daily = fetch_daily(cnt=16)
    insert_daily(daily)

    return True


if __name__ == "__main__":
    scrape_once()
    print("OpenWeather (2.5/pro endpoints) scrape done.")
# scraper/create_tables.py
import pymysql
from app.config import Config


def get_conn(with_db: bool = True):
    params = dict(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset="utf8mb4",
        autocommit=True
    )
    if with_db:
        params["database"] = Config.DB_NAME
    return pymysql.connect(**params)


def create_database():
    conn = get_conn(with_db=False)
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4;")
    finally:
        conn.close()


def create_tables():
    conn = get_conn(with_db=True)
    try:
        with conn.cursor() as cur:
            # 1) station (static)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS station (
                    number INTEGER NOT NULL,
                    address VARCHAR(128),
                    banking INTEGER,
                    bike_stands INTEGER,
                    name VARCHAR(128),
                    position_lat FLOAT,
                    position_lng FLOAT,
                    PRIMARY KEY (number)
                );
            """)

            # 2) availability (dynamic)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS availability (
                    number INTEGER NOT NULL,
                    last_update DATETIME NOT NULL,
                    available_bikes INTEGER,
                    available_bike_stands INTEGER,
                    status VARCHAR(128),
                    PRIMARY KEY (number, last_update),
                    INDEX idx_availability_last_update (last_update),
                    CONSTRAINT fk_availability_station
                        FOREIGN KEY (number) REFERENCES station(number)
                        ON DELETE CASCADE ON UPDATE CASCADE
                );
            """)

            # 3) current (from /data/2.5/weather)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS current (
                    dt DATETIME NOT NULL,
                    sunrise DATETIME,
                    sunset DATETIME,
                    temp FLOAT,
                    feels_like FLOAT,
                    humidity INTEGER,
                    pressure INTEGER,
                    wind_speed FLOAT,
                    wind_gust FLOAT,
                    weather_id INTEGER,
                    clouds INTEGER,
                    visibility INTEGER,
                    rain_1h FLOAT,
                    snow_1h FLOAT,
                    PRIMARY KEY (dt),
                    INDEX idx_current_dt (dt)
                );
            """)

            # 4) hourly (from pro /data/2.5/forecast/hourly)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS hourly (
                    dt DATETIME NOT NULL,
                    future_dt DATETIME NOT NULL,
                    temp FLOAT,
                    feels_like FLOAT,
                    humidity INTEGER,
                    pressure INTEGER,
                    pop FLOAT,
                    clouds INTEGER,
                    wind_speed FLOAT,
                    wind_gust FLOAT,
                    weather_id INTEGER,
                    rain_1h FLOAT,
                    snow_1h FLOAT,
                    PRIMARY KEY (dt, future_dt),
                    INDEX idx_hourly_future_dt (future_dt)
                );
            """)

            # 5) daily (from /data/2.5/forecast/daily?cnt=16)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS daily (
                    dt DATETIME NOT NULL,
                    future_dt DATETIME NOT NULL,
                    temp_min FLOAT,
                    temp_max FLOAT,
                    humidity INTEGER,
                    pressure INTEGER,
                    clouds INTEGER,
                    wind_speed FLOAT,
                    wind_gust FLOAT,
                    weather_id INTEGER,
                    rain FLOAT,
                    snow FLOAT,
                    PRIMARY KEY (dt, future_dt),
                    INDEX idx_daily_future_dt (future_dt)
                );
            """)
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    create_tables()
    print("Database and 5 tables created successfully (OpenWeather 2.5/pro schema).")
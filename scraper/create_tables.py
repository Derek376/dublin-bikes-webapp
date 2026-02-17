# create_tables.py
from sqlalchemy import create_engine, text
import dbinfo


def main():
    engine = create_engine(dbinfo.DB_URI, pool_pre_ping=True, future=True)

    sql_statements = [
        # 1) Static station info
        """
        CREATE TABLE IF NOT EXISTS station (
            number INT NOT NULL,
            address VARCHAR(128),
            banking TINYINT,
            bike_stands INT,
            name VARCHAR(128),
            position_lat FLOAT,
            position_lng FLOAT,
            PRIMARY KEY (number)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # 2) Dynamic bike availability snapshots
        """
        CREATE TABLE IF NOT EXISTS availability (
            number INT NOT NULL,
            last_update DATETIME NOT NULL,
            available_bikes INT,
            available_bike_stands INT,
            status VARCHAR(64),
            PRIMARY KEY (number, last_update),
            INDEX idx_availability_last_update (last_update),
            CONSTRAINT fk_availability_station
                FOREIGN KEY (number) REFERENCES station(number)
                ON UPDATE CASCADE ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # 3) Current weather (free plan compatible)
        """
        CREATE TABLE IF NOT EXISTS `current` (
            dt DATETIME NOT NULL,
            feels_like FLOAT,
            humidity INT,
            pressure INT,
            sunrise DATETIME,
            sunset DATETIME,
            `temp` FLOAT,
            weather_id INT,
            wind_gust FLOAT,
            wind_speed FLOAT,
            rain_1h FLOAT,
            snow_1h FLOAT,
            clouds INT,
            visibility INT,
            PRIMARY KEY (dt)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # 4) "Hourly" table (store 3-hour forecast slots from free forecast API)
        """
        CREATE TABLE IF NOT EXISTS hourly (
            dt DATETIME NOT NULL,           -- scrape time
            future_dt DATETIME NOT NULL,    -- forecast time
            feels_like FLOAT,
            humidity INT,
            pop FLOAT,
            pressure INT,
            `temp` FLOAT,
            weather_id INT,
            wind_speed FLOAT,
            wind_gust FLOAT,
            rain_1h FLOAT,
            snow_1h FLOAT,
            clouds INT,
            visibility INT,
            PRIMARY KEY (dt, future_dt),
            INDEX idx_hourly_future_dt (future_dt)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # 5) Daily table (optional aggregation from 3-hour forecast)
        """
        CREATE TABLE IF NOT EXISTS daily (
            dt DATETIME NOT NULL,           -- scrape time
            future_dt DATETIME NOT NULL,    -- day representative datetime (e.g., 00:00)
            humidity INT,
            pop FLOAT,
            pressure INT,
            temp_max FLOAT,
            temp_min FLOAT,
            weather_id INT,
            wind_speed FLOAT,
            wind_gust FLOAT,
            rain FLOAT,
            snow FLOAT,
            clouds INT,
            PRIMARY KEY (dt, future_dt),
            INDEX idx_daily_future_dt (future_dt)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    ]

    with engine.begin() as conn:
        for stmt in sql_statements:
            conn.execute(text(stmt))

    print(" Tables created/verified successfully:")


if __name__ == "__main__":
    main()

from sqlalchemy import create_engine, text
import dbinfo

def get_engine(with_db=False):
    if with_db:
        conn = f"mysql+pymysql://{dbinfo.DB_USER}:{dbinfo.DB_PASSWORD}@{dbinfo.DB_HOST}:{dbinfo.DB_PORT}/{dbinfo.DB_NAME}"
    else:
        conn = f"mysql+pymysql://{dbinfo.DB_USER}:{dbinfo.DB_PASSWORD}@{dbinfo.DB_HOST}:{dbinfo.DB_PORT}"
    return create_engine(conn, future=True)

def main():
    engine_server = get_engine(with_db=False)

    # 1) create database if not exists
    with engine_server.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {dbinfo.DB_NAME};"))
        conn.commit()

    engine = get_engine(with_db=True)

    # 2) create station table(static)
    create_station_sql = """
    CREATE TABLE IF NOT EXISTS station (
        number INT PRIMARY KEY,
        name VARCHAR(256),
        address VARCHAR(256),
        latitude DOUBLE,
        longitude DOUBLE,
        banking BOOLEAN,
        bikestands INT,
        status VARCHAR(64)
    );
    """

    # 3) create availability table (dynamic)
    create_availability_sql = """
    CREATE TABLE IF NOT EXISTS availability (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        number INT NOT NULL,
        available_bikes INT,
        available_bike_stands INT,
        status VARCHAR(64),
        last_update DATETIME NOT NULL,
        FOREIGN KEY (number) REFERENCES station(number),
        INDEX idx_station_time (number, last_update)
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_station_sql))
        conn.execute(text(create_availability_sql))
        conn.commit()

    print("Database and tables are ready.")

if __name__ == "__main__":
    main()

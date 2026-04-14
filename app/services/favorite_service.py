from app.db import get_conn


def get_user_favorites(user_id: int):
    sql = """
    SELECT
        f.id,
        f.station_number,
        s.name,
        s.address,
        s.position_lat,
        s.position_lng,
        f.created_at
    FROM favorites f
    JOIN station s ON f.station_number = s.number
    WHERE f.user_id = %s
    ORDER BY f.created_at DESC;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchall()
    finally:
        conn.close()


def add_favorite(user_id: int, station_number: int):
    sql = """
    INSERT INTO favorites (user_id, station_number)
    VALUES (%s, %s);
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id, station_number))
            return cur.lastrowid
    finally:
        conn.close()


def remove_favorite(user_id: int, station_number: int):
    sql = """
    DELETE FROM favorites
    WHERE user_id = %s AND station_number = %s;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            rows = cur.execute(sql, (user_id, station_number))
            return rows > 0
    finally:
        conn.close()


def is_favorite(user_id: int, station_number: int):
    sql = """
    SELECT id
    FROM favorites
    WHERE user_id = %s AND station_number = %s
    LIMIT 1;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id, station_number))
            return cur.fetchone() is not None
    finally:
        conn.close()
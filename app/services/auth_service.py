from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_conn


def create_user(email: str, password: str):
    password_hash = generate_password_hash(password)

    sql = """
    INSERT INTO users (email, password_hash)
    VALUES (%s, %s);
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email, password_hash))
            return cur.lastrowid
    finally:
        conn.close()


def get_user_by_email(email: str):
    sql = """
    SELECT id, email, password_hash, created_at
    FROM users
    WHERE email = %s
    LIMIT 1;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email,))
            return cur.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    sql = """
    SELECT id, email, created_at
    FROM users
    WHERE id = %s
    LIMIT 1;
    """

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchone()
    finally:
        conn.close()


def verify_user(email: str, password: str):
    user = get_user_by_email(email)

    if not user:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return {
        "id": user["id"],
        "email": user["email"],
        "created_at": user["created_at"],
    }

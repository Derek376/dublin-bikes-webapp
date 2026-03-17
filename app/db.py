import os
import sys
import pymysql
from dotenv import load_dotenv

# let the .env file be in the project root, so both scraper and app can use it
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(CURRENT_DIR, "..")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# add scraper dir to sys.path, so we can import dbinfo.py
SCRAPER_DIR = os.path.join(PROJECT_ROOT, "scraper")
if SCRAPER_DIR not in sys.path:
    sys.path.append(SCRAPER_DIR)

from dbinfo import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME  # noqa


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,  # return results as dicts instead of tuples
    )
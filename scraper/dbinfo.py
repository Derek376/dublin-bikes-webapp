
# JCDecaux API
JCD_API_KEY = "100d9751eb8f4e110ec04bd283a12327aef3d1af"
JCD_CONTRACT = "dublin"
JCD_BASE_URL = "https://api.jcdecaux.com/vls/v1/stations"
JCD_STATIONS_URL = (
    f"{JCD_BASE_URL}?apiKey={JCD_API_KEY}&contract={JCD_CONTRACT}"
)

# Database (MySQL)
DB_USER = "root"
DB_PWD = "000123"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "local_databasejcdecaux"
DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"


# OpenWeather API
OWM_API_KEY = "fcea9769e36b42d4c88fcec1939165b7"
OWM_LAT = 53.3498
OWM_LON = -6.2603

OWM_ONECALL_URL = (
    "https://api.openweathermap.org/data/3.0/onecall"
    f"?lat={OWM_LAT}&lon={OWM_LON}&appid={OWM_API_KEY}&units=metric"
)

# Scraper runtime settings
SCRAPE_INTERVAL_SECONDS = 300
WEATHER_INTERVAL_SECONDS = 600
HTTP_TIMEOUT_SECONDS = 20
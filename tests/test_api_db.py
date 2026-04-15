from unittest.mock import patch


@patch("app.routes.api_db.get_all_stations_latest")
def test_get_all_stations(mock_get, client):
    mock_get.return_value = [
        {
            "number": 1,
            "name": "Station A",
            "available_bikes": 5,
            "available_bike_stands": 10
        }
    ]

    response = client.get("/api/db/stations")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["number"] == 1


@patch("app.routes.api_db.get_station_latest")
def test_get_single_station(mock_get, client):
    mock_get.return_value = {
        "number": 42,
        "name": "Pearse Street",
        "available_bikes": 7
    }

    response = client.get("/api/db/stations/42")
    assert response.status_code == 200

    data = response.get_json()
    assert data["number"] == 42
    assert data["name"] == "Pearse Street"


@patch("app.routes.api_db.get_station_history")
def test_get_station_history(mock_get, client):
    mock_get.return_value = [
        {"last_update": "2026-04-15T09:00:00", "available_bikes": 6},
        {"last_update": "2026-04-15T09:05:00", "available_bikes": 7},
    ]

    response = client.get("/api/db/stations/42/history?limit=2")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


@patch("app.routes.api_db.get_current_weather_latest")
def test_get_current_weather(mock_get, client):
    mock_get.return_value = {
        "temp": 11.5,
        "humidity": 75,
        "pressure": 1010
    }

    response = client.get("/api/db/weather/current")
    assert response.status_code == 200

    data = response.get_json()
    assert data["temp"] == 11.5


@patch("app.routes.api_db.get_hourly_forecast_latest")
def test_get_hourly_weather(mock_get, client):
    mock_get.return_value = [
        {"future_dt": "2026-04-15T10:00:00", "temp": 12.0}
    ]

    response = client.get("/api/db/weather/hourly?limit=1")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["temp"] == 12.0
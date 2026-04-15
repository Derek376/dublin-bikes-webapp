from unittest.mock import patch


@patch("app.routes.api_live.fetch_jcdecaux_live")
def test_live_jcdecaux_route(mock_fetch, client):
    mock_fetch.return_value = [{"number": 1, "available_bikes": 5}]

    response = client.get("/api/live/jcdecaux")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["number"] == 1


@patch("app.routes.api_live.fetch_openweather_current_live")
def test_live_weather_current_route(mock_fetch, client):
    mock_fetch.return_value = {"temp": 12, "humidity": 80}

    response = client.get("/api/live/weather/current")
    assert response.status_code == 200

    data = response.get_json()
    assert data["temp"] == 12


@patch("app.routes.api_live.fetch_openweather_hourly_live")
def test_live_weather_hourly_route(mock_fetch, client):
    mock_fetch.return_value = [
        {"dt": "2026-04-15T10:00:00", "temp": 13}
    ]

    response = client.get("/api/live/weather/hourly")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["temp"] == 13
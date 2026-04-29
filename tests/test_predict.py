from unittest.mock import patch


def test_predict_missing_params(client):
    response = client.get("/api/db/predict")
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"


def test_predict_invalid_datetime(client):
    response = client.get("/api/db/predict?station_id=42&date=2026/04/15&time=10:00")
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"


@patch("app.routes.api_db.model")
@patch("app.routes.api_db.get_hourly_forecast_latest")
def test_predict_no_weather_data_uses_default_weather(mock_forecast, mock_model, client):
    mock_forecast.return_value = []
    mock_model.predict.return_value = [6]

    response = client.get("/api/db/predict?station_id=42&date=2026-04-15&time=10:00")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "success"
    assert data["predicted_available_bikes"] == 6


@patch("app.routes.api_db.get_hourly_forecast_latest")
@patch("app.routes.api_db.model")
def test_predict_no_weather_data_uses_defaults(mock_model, mock_forecast, client):
    mock_forecast.return_value = []
    mock_model.predict.return_value = [6]

    response = client.get("/api/db/predict?station_id=42&date=2026-04-15&time=10:00")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["predicted_available_bikes"] == 6
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


@patch("app.routes.api_db.get_hourly_forecast_latest")
def test_predict_no_weather_data(mock_forecast, client):
    mock_forecast.return_value = []

    response = client.get("/api/db/predict?station_id=42&date=2026-04-15&time=10:00")
    assert response.status_code in [400, 404]

    data = response.get_json()
    assert data["status"] == "error"


@patch("app.routes.api_db.get_hourly_forecast_latest")
@patch("app.routes.api_db.model")
def test_predict_success(mock_model, mock_forecast, client):
    mock_forecast.return_value = [
        {
            "future_dt": "2026-04-15T10:00:00",
            "temp": 14.0,
            "humidity": 70.0,
            "pressure": 1012.0
        }
    ]
    mock_model.predict.return_value = [7]

    response = client.get("/api/db/predict?station_id=42&date=2026-04-15&time=10:00")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert data["predicted_available_bikes"] == 7
    assert data["station_id"] == 42
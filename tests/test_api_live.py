from app import create_app


def test_live_jcdecaux_route_exists():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/api/live/jcdecaux")

    assert response.status_code != 404


def test_live_weather_current_route_exists():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/api/live/weather/current")

    assert response.status_code != 404
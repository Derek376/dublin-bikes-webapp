def test_home_route_exists(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "ok"
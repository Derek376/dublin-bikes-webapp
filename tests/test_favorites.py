def test_list_favorites_requires_login(client):
    response = client.get("/api/favorites")
    assert response.status_code == 401


def test_add_favorite_requires_login(client):
    response = client.post("/api/favorites/42")
    assert response.status_code == 401


def test_list_favorites_with_session(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/api/favorites")
    assert response.status_code in [200, 404]
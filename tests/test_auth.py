def test_register_requires_email_and_password(client):
    response = client.post("/auth/register", json={})
    assert response.status_code == 400


def test_login_requires_email_and_password(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 400


def test_register_missing_password(client):
    response = client.post("/auth/register", json={"email": "test@example.com"})
    assert response.status_code == 400
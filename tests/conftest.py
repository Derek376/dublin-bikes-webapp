import os
import pytest

os.environ["FLASK_ENV"] = "testing"

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
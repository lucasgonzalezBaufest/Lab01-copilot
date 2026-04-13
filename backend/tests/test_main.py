import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_tokens():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()


class TestLogin:
    def test_valid_credentials(self):
        data = get_tokens()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 300

    def test_invalid_password(self):
        response = client.post(
            "/token",
            data={"username": "admin", "password": "wrong"},
        )
        assert response.status_code == 401

    def test_invalid_user(self):
        response = client.post(
            "/token",
            data={"username": "notauser", "password": "admin123"},
        )
        assert response.status_code == 401


class TestProtectedEndpoint:
    def test_me_with_valid_token(self):
        data = get_tokens()
        response = client.get(
            "/me",
            headers={"Authorization": f"Bearer {data['access_token']}"},
        )
        assert response.status_code == 200
        assert response.json() == {"username": "admin"}

    def test_me_without_token(self):
        response = client.get("/me")
        assert response.status_code == 401

    def test_me_with_invalid_token(self):
        response = client.get(
            "/me",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        assert response.status_code == 401

    def test_me_with_refresh_token_rejected(self):
        data = get_tokens()
        # Refresh tokens should be rejected on /me (type != "access")
        response = client.get(
            "/me",
            headers={"Authorization": f"Bearer {data['refresh_token']}"},
        )
        assert response.status_code == 401


class TestRefreshToken:
    def test_valid_refresh(self):
        data = get_tokens()
        response = client.post(
            "/token/refresh",
            json={"refresh_token": data["refresh_token"]},
        )
        assert response.status_code == 200
        refreshed = response.json()
        assert "access_token" in refreshed
        assert "refresh_token" in refreshed
        assert refreshed["token_type"] == "bearer"
        assert refreshed["expires_in"] == 300

    def test_invalid_refresh_token(self):
        response = client.post(
            "/token/refresh",
            json={"refresh_token": "notarealtoken"},
        )
        assert response.status_code == 401

    def test_access_token_rejected_as_refresh(self):
        data = get_tokens()
        # Access tokens should be rejected on /token/refresh (type != "refresh")
        response = client.post(
            "/token/refresh",
            json={"refresh_token": data["access_token"]},
        )
        assert response.status_code == 401

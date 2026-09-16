from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestAuthSignup:
    def test_signup_success(self, client: TestClient):
        response = client.post(
            "/api/auth/signup",
            json={"email": "teste@example.com", "password": "123456"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["email"] == "teste@example.com"
        assert data["token_type"] == "bearer"

    def test_signup_duplicate_email(self, client: TestClient):
        client.post(
            "/api/auth/signup",
            json={"email": "dupe@example.com", "password": "123456"},
        )
        response = client.post(
            "/api/auth/signup",
            json={"email": "dupe@example.com", "password": "654321"},
        )
        assert response.status_code == 409
        assert "ja cadastrado" in response.json()["detail"]

    def test_signup_weak_password(self, client: TestClient):
        response = client.post(
            "/api/auth/signup",
            json={"email": "weak@example.com", "password": "12345"},
        )
        assert response.status_code == 422

    def test_signup_invalid_email(self, client: TestClient):
        response = client.post(
            "/api/auth/signup",
            json={"email": "", "password": "123456"},
        )
        assert response.status_code == 422


class TestAuthLogin:
    def test_login_success(self, client: TestClient):
        client.post(
            "/api/auth/signup",
            json={"email": "logintest@example.com", "password": "123456"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "logintest@example.com", "password": "123456"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["email"] == "logintest@example.com"

    def test_login_wrong_password(self, client: TestClient):
        client.post(
            "/api/auth/signup",
            json={"email": "wrongpw@example.com", "password": "123456"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "wrongpw@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "incorretos" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient):
        response = client.post(
            "/api/auth/login",
            json={"email": "noone@example.com", "password": "123456"},
        )
        assert response.status_code == 401

    def test_login_empty_email(self, client: TestClient):
        response = client.post(
            "/api/auth/login",
            json={"email": "", "password": "123456"},
        )
        assert response.status_code == 422


class TestAuthLogout:
    def test_logout_success(self, client: TestClient):
        resp = client.post(
            "/api/auth/signup",
            json={"email": "logouttest@example.com", "password": "123456"},
        )
        token = resp.json()["access_token"]

        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["detail"] == "Logout realizado com sucesso"

    def test_logout_twice(self, client: TestClient):
        resp = client.post(
            "/api/auth/signup",
            json={"email": "logout2@example.com", "password": "123456"},
        )
        token = resp.json()["access_token"]

        client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
        response = client.post(
            "/api/auth/logout", headers={"Authorization": f"Bearer {token}"}
        )
        # Token ja invalidado, segunda tentativa ainda funciona (idempotente)
        assert response.status_code == 200

    def test_logout_without_token(self, client: TestClient):
        response = client.post("/api/auth/logout")
        assert response.status_code == 401

    def test_logout_prevents_chat_access(self, client: TestClient):
        resp = client.post(
            "/api/auth/signup",
            json={"email": "reuse@example.com", "password": "123456"},
        )
        token = resp.json()["access_token"]

        # Logout
        client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})

        # Tentar usar o mesmo token no chat
        response = client.post(
            "/api/chat",
            json={"message": "Ola"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401
        assert "invalidado" in response.json()["detail"]


class TestAuthMe:
    def test_me_authenticated(self, client: TestClient):
        resp = client.post(
            "/api/auth/signup",
            json={"email": "me@example.com", "password": "123456"},
        )
        token = resp.json()["access_token"]

        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "me@example.com"

    def test_me_unauthenticated(self, client: TestClient):
        response = client.get("/api/auth/me")
        assert response.status_code == 401


class TestChatProtected:
    def test_chat_without_auth_rejected(self, client: TestClient):
        response = client.post(
            "/api/chat",
            json={"message": "Ola"},
        )
        assert response.status_code == 401

    def test_chat_with_auth_allowed(self, client: TestClient):
        resp = client.post(
            "/api/auth/signup",
            json={"email": "chatuser@example.com", "password": "123456"},
        )
        token = resp.json()["access_token"]

        # Com auth, o endpoint responde (espera 503 sem API key real)
        response = client.post(
            "/api/chat",
            json={"message": "Ola"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code in (200, 422, 503)

    def test_health_still_public(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200

    def test_root_still_public(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
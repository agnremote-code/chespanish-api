from fastapi.testclient import TestClient

from app.api.dependencies import get_auth_service
from app.main import app
from app.schemas.auth import (
    AuthLoginRequest,
    AuthResponse,
    AuthSession,
    AuthSignUpRequest,
    AuthUser,
)


class FakeAuthService:
    async def sign_up(self, payload: AuthSignUpRequest) -> AuthResponse:
        return AuthResponse(
            user=AuthUser(id="user-123", email=payload.email),
            session=None,
            message="Signup created. Email confirmation may be required before login.",
        )

    async def login(self, payload: AuthLoginRequest) -> AuthResponse:
        return AuthResponse(
            user=AuthUser(id="user-123", email=payload.email),
            session=AuthSession(
                access_token="access-token",
                refresh_token="refresh-token",
                expires_in=3600,
            ),
            message="Login successful.",
        )


def override_auth_service() -> FakeAuthService:
    return FakeAuthService()


def test_signup_returns_created_user() -> None:
    app.dependency_overrides[get_auth_service] = override_auth_service
    client = TestClient(app)

    response = client.post(
        "/auth/signup",
        json={
            "email": "student@example.com",
            "password": "strong-password",
            "username": "student",
            "first_name": "Student",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json() == {
        "user": {"id": "user-123", "email": "student@example.com"},
        "session": None,
        "message": "Signup created. Email confirmation may be required before login.",
    }


def test_login_returns_session() -> None:
    app.dependency_overrides[get_auth_service] = override_auth_service
    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "strong-password"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "user": {"id": "user-123", "email": "student@example.com"},
        "session": {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "bearer",
            "expires_in": 3600,
            "expires_at": None,
        },
        "message": "Login successful.",
    }

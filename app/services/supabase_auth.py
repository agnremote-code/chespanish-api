from typing import Any

import httpx

from app.core.config import Settings
from app.schemas.auth import (
    AuthLoginRequest,
    AuthResponse,
    AuthSession,
    AuthSignUpRequest,
    AuthUser,
)


class SupabaseAuthConfigurationError(RuntimeError):
    pass


class SupabaseAuthError(RuntimeError):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class SupabaseAuthService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def sign_up(self, payload: AuthSignUpRequest) -> AuthResponse:
        data = {
            "email": str(payload.email),
            "password": payload.password,
            "data": {
                "username": payload.username,
                "first_name": payload.first_name,
            },
        }

        response_data = await self._post("/auth/v1/signup", data)

        return AuthResponse(
            user=_parse_user(response_data.get("user") or response_data),
            session=_parse_session(response_data.get("session")),
            message="Signup created. Email confirmation may be required before login.",
        )

    async def login(self, payload: AuthLoginRequest) -> AuthResponse:
        response_data = await self._post(
            "/auth/v1/token?grant_type=password",
            {"email": str(payload.email), "password": payload.password},
        )

        return AuthResponse(
            user=_parse_user(response_data.get("user")),
            session=_parse_session(response_data),
            message="Login successful.",
        )

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.supabase_url or not self.settings.supabase_anon_key:
            raise SupabaseAuthConfigurationError(
                "Supabase auth is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY."
            )

        url = f"{self.settings.supabase_url.rstrip('/')}{path}"
        headers = {
            "apikey": self.settings.supabase_anon_key,
            "Authorization": f"Bearer {self.settings.supabase_anon_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code >= 400:
            raise SupabaseAuthError(
                message=_parse_error_message(response),
                status_code=response.status_code,
            )

        return response.json()


def _parse_user(data: dict[str, Any] | None) -> AuthUser | None:
    if not data or not data.get("id"):
        return None

    return AuthUser(id=str(data["id"]), email=data.get("email"))


def _parse_session(data: dict[str, Any] | None) -> AuthSession | None:
    if not data or not data.get("access_token") or not data.get("refresh_token"):
        return None

    return AuthSession(
        access_token=str(data["access_token"]),
        refresh_token=str(data["refresh_token"]),
        token_type=str(data.get("token_type") or "bearer"),
        expires_in=data.get("expires_in"),
        expires_at=data.get("expires_at"),
    )


def _parse_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return "Supabase auth request failed."

    message = data.get("msg") or data.get("message") or data.get("error_description")
    return str(message or "Supabase auth request failed.")

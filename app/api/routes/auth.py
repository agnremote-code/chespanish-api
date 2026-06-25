from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_auth_service
from app.schemas.auth import AuthLoginRequest, AuthResponse, AuthSignUpRequest
from app.services.supabase_auth import (
    SupabaseAuthConfigurationError,
    SupabaseAuthError,
    SupabaseAuthService,
)

router = APIRouter(prefix="/auth", tags=["auth"])
AuthServiceDependency = Annotated[SupabaseAuthService, Depends(get_auth_service)]


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    payload: AuthSignUpRequest,
    auth_service: AuthServiceDependency,
) -> AuthResponse:
    try:
        return await auth_service.sign_up(payload)
    except SupabaseAuthConfigurationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except SupabaseAuthError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: AuthLoginRequest,
    auth_service: AuthServiceDependency,
) -> AuthResponse:
    try:
        return await auth_service.login(payload)
    except SupabaseAuthConfigurationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except SupabaseAuthError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error

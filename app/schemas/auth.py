from pydantic import BaseModel, EmailStr, Field


class AuthSignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    username: str | None = Field(default=None, min_length=3, max_length=32)
    first_name: str | None = Field(default=None, min_length=1, max_length=80)


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class AuthUser(BaseModel):
    id: str
    email: EmailStr | None = None


class AuthSession(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    expires_at: int | None = None


class AuthResponse(BaseModel):
    user: AuthUser | None = None
    session: AuthSession | None = None
    message: str

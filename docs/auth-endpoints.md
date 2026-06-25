# Auth endpoints

The API owns the first signup/login boundary.

Supabase Auth still stores and verifies credentials. FastAPI receives the request from clients and forwards the credential operation to Supabase Auth.

## Sign up

```text
POST /auth/signup
```

Request:

```json
{
  "email": "student@example.com",
  "password": "strong-password",
  "username": "student",
  "first_name": "Student"
}
```

Response:

```json
{
  "user": {
    "id": "supabase-user-id",
    "email": "student@example.com"
  },
  "session": null,
  "message": "Signup created. Email confirmation may be required before login."
}
```

Notes:

- `password` must be at least 8 characters.
- `username` and `first_name` are optional.
- Supabase may return no session if email confirmation is required.
- The database trigger creates `public.profiles` from user metadata.

## Login

```text
POST /auth/login
```

Request:

```json
{
  "email": "student@example.com",
  "password": "strong-password"
}
```

Response:

```json
{
  "user": {
    "id": "supabase-user-id",
    "email": "student@example.com"
  },
  "session": {
    "access_token": "access-token",
    "refresh_token": "refresh-token",
    "token_type": "bearer",
    "expires_in": 3600,
    "expires_at": 1790000000
  },
  "message": "Login successful."
}
```

Clients should store the session securely and use the access token for authenticated API calls:

```text
Authorization: Bearer <access_token>
```

## Required environment variables

```text
SUPABASE_URL=
SUPABASE_ANON_KEY=
```

`SUPABASE_ANON_KEY` is the Supabase publishable/anon key. Do not use the service role key in clients.

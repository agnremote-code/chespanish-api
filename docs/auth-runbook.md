# Auth runbook

## Current status

The API signup/login flow is working against the Supabase project:

```text
Project: CHE!spanish
Project ref: idpibwekwxqeslmmullb
Region: us-west-2
```

Implemented endpoints:

```text
POST /auth/signup
POST /auth/login
```

Database table:

```text
public.profiles
```

Supabase-managed auth table:

```text
auth.users
```

## What was done

1. Created the FastAPI auth endpoints.
2. Added Supabase Auth service integration through HTTP calls to Supabase Auth.
3. Created and applied the `public.profiles` migration.
4. Enabled Row Level Security on `public.profiles`.
5. Added policies for users to read, insert, and update their own profile.
6. Added a database trigger that creates a profile when Supabase creates a user.
7. Linked the local repo to the remote Supabase project with Supabase CLI.
8. Applied the Supabase migration remotely.
9. Created local API `.env` values for Supabase URL and anon/publishable key.
10. Disabled email confirmation for development to avoid Supabase default email rate limits.
11. Tested signup and login against the remote Supabase project.
12. Confirmed that signup creates both `auth.users` and `public.profiles`.

## Important implementation detail

The app does not store passwords in `public.profiles` or any application table.

Password handling is delegated to Supabase Auth:

```text
client -> FastAPI -> Supabase Auth -> auth.users
```

Application profile data lives in:

```text
public.profiles
```

## Development config

The local Supabase config is versioned here:

```text
supabase/config.toml
```

For development, email confirmation is disabled:

```toml
[auth.email]
enable_confirmations = false
```

Reason:

- Supabase default auth email provider hit `over_email_send_rate_limit`.
- This blocked signup/login testing after a confirmation email was sent.
- Disabling confirmation lets us validate the API auth flow while developing locally.

Before production, revisit this setting.

## Commands used

Link project:

```bash
npx supabase link --project-ref idpibwekwxqeslmmullb
```

Push migrations:

```bash
npx supabase db push
```

Push config:

```bash
npx supabase config push
```

Check migration status:

```bash
npx supabase migration list
```

Run API tests:

```bash
py -m pytest
```

Run lint:

```bash
py -m ruff check .
```

## Manual API testing

Run the API locally:

```bash
py -m uvicorn app.main:app --reload
```

Open Swagger:

```text
http://localhost:8000/docs
```

Signup request:

```json
{
  "email": "student@example.com",
  "password": "strong-password-123",
  "username": "student",
  "first_name": "Student"
}
```

Login request:

```json
{
  "email": "student@example.com",
  "password": "strong-password-123"
}
```

Expected login result:

```text
200 OK with user and session tokens
```

Do not paste access tokens into docs or commits.

## Verification queries

Check recent users:

```sql
select id, email, email_confirmed_at, created_at
from auth.users
order by created_at desc
limit 10;
```

Check profiles:

```sql
select id, username, first_name, created_at
from public.profiles
order by created_at desc
limit 10;
```

## Known warning

Tests currently show a non-blocking FastAPI/Starlette TestClient warning.

Details:

```text
docs/testing-notes.md
```

## Next steps

1. Implement authenticated `GET /me`.
2. Add JWT validation for Supabase access tokens in FastAPI.
3. Return the current user's profile from `public.profiles`.
4. Add tests for missing token, invalid token, and valid token.
5. Implement `PATCH /me` to update profile fields.
6. Decide how clients should store tokens.
7. Add a simple smoke test script for local auth flow.
8. Decide when to re-enable email confirmation.
9. Configure custom SMTP before production if email confirmation is needed.
10. Add CI to run `pytest` and `ruff check .` on GitHub.

## Production follow-up

Before production:

- turn email confirmation back on or define a deliberate no-confirmation policy
- configure custom SMTP to avoid default email provider limits
- review RLS policies
- review API token validation and error handling
- add refresh-token handling strategy
- avoid logging tokens or passwords
- add rate limiting at the API layer
- add monitoring for auth failures

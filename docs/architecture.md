# API architecture

## Stack decision

The Chespanish API will use:

- FastAPI
- Python
- Supabase Postgres
- Pydantic
- SQLAlchemy or SQLModel
- Alembic
- Pytest

## Role in the product

The API is the backend application for Chespanish. It should be consumed by:

- landing
- mobile app
- future admin tools

The API owns product backend logic and should become the long-term path for writing product data.

## Supabase usage

Supabase will provide:

- Postgres database
- Auth candidate
- Storage candidate for future media

The API should treat Postgres as the source of truth. Supabase Auth is the default auth direction, but the exact auth flow still needs a final implementation decision.

## Proposed project structure

```text
app/
  main.py
  api/
    routes/
      health.py
      waitlist.py
      users.py
      progress.py
      lessons.py
  core/
    config.py
    security.py
  db/
    session.py
    models.py
  schemas/
    waitlist.py
    users.py
    progress.py
    lessons.py
  services/
    waitlist_service.py
    user_service.py
    progress_service.py
    lesson_service.py
tests/
  test_health.py
alembic/
```

## Initial endpoints

```text
GET /health
POST /waitlist/leads
GET /me
PATCH /me
GET /me/progress
PUT /me/progress
POST /me/progress/missions/{mission_id}
GET /levels
GET /lessons
GET /lessons/{lesson_id}
```

## Environment variables

Expected variables:

```text
APP_ENV=local
API_CORS_ORIGINS=http://localhost:3000,http://localhost:8081
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
```

The service role key must stay server-side only. It should never be exposed to landing or mobile clients.

## First milestone

The first API milestone is intentionally small:

- FastAPI app boots locally
- `GET /health` returns ok
- tests pass
- env config is documented
- CORS allows the local landing and Expo app
- empty Supabase connection path is ready

After that, implement `POST /waitlist/leads` and connect the landing waitlist form to the API.

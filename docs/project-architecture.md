# Chespanish project architecture

## Decision

Chespanish will use three separate applications:

- `landing`: public web app built with Next.js
- `mobile`: mobile app built with Expo and React Native
- `api`: backend API built with FastAPI and Python

The shared database platform will be Supabase, using Postgres as the source of truth.

## Repository layout

```text
chespanish-workspace/
  landing/   -> github.com/agnremote-code/chespanish-app
  mobile/    -> github.com/agnremote-code/chespanish-mobile
  api/       -> github.com/agnremote-code/chespanish-api
```

Each application has its own repository, dependencies, deployment target, and release cycle.

## System flow

```text
landing app -> API -> Supabase Postgres
mobile app  -> API -> Supabase Postgres
```

The landing and mobile apps should not own product backend logic. They can keep temporary local/demo behavior while the API is being built, but long-term writes should go through the API.

## Stack

Landing:

- Next.js
- TypeScript
- Tailwind CSS
- Vercel deployment

Mobile:

- Expo
- React Native
- TypeScript
- Expo Router
- EAS Build later, when native builds are needed

API:

- FastAPI
- Python
- Pydantic
- SQLAlchemy or SQLModel
- Alembic
- Pytest

Database:

- Supabase
- Postgres
- Supabase Auth as the default candidate
- Supabase Storage later for audio/images if needed

## Auth direction

Default direction: Supabase Auth.

Likely starting flow:

```text
client -> Supabase Auth
client -> API with Supabase access token
API -> validate token -> Supabase Postgres
```

Open question: whether sign in/sign up should be handled directly by clients through Supabase Auth or wrapped by the API.

## Initial product domains

- waitlist leads
- users/profiles
- lessons
- levels
- demo progress
- mobile learning progress
- missions/checkpoints
- future AI/audio feedback

## Development order

1. Scaffold the FastAPI repo with project structure, health endpoint, tests, linting, formatting, and environment config.
2. Create the Supabase project and define the first Postgres schema.
3. Connect the API to Supabase locally.
4. Replace the landing waitlist fallback with `POST /waitlist/leads`.
5. Scaffold the Expo app and connect it to the API health endpoint.
6. Build the first mobile auth/progress loop.

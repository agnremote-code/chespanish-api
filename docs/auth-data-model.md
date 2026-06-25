# Auth data model

## Decision

Chespanish will use Supabase Auth for registration and login credentials.

The API/database must not store plaintext passwords in application tables.

## Why passwords are not in `profiles`

Passwords are sensitive credentials. They should be handled by Supabase Auth, which stores credentials in its managed auth schema and handles password hashing/session issuance.

The application schema should store user profile data only:

```text
auth.users        -> managed by Supabase Auth
public.profiles   -> managed by Chespanish
```

## Initial table

```text
public.profiles
```

Fields:

```text
id uuid primary key references auth.users(id)
username text unique
first_name text
avatar_url text
created_at timestamptz
updated_at timestamptz
```

## Registration flow

Expected first flow:

```text
client -> Supabase Auth sign up with email/password
Supabase Auth -> creates auth.users row
database trigger -> creates public.profiles row
client -> API with Supabase access token
API -> validates user and reads/writes profile/product data
```

## Migration

The initial SQL migration is:

```text
supabase/migrations/20260625211500_create_profiles.sql
```

Run it in Supabase SQL Editor or later through Supabase CLI migrations.

## Security

Row Level Security is enabled on `public.profiles`.

Initial policies:

- users can read their own profile
- users can insert their own profile
- users can update their own profile

The API can use the Supabase service role key for trusted backend operations, but that key must only live in the FastAPI environment.

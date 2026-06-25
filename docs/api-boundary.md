# API boundary

The API is a separate application from the landing and the mobile app.

## Responsibility

The API should own backend concerns shared by every client:

- users and profiles
- authentication/session verification, depending on the final auth provider
- progress persistence
- lesson/content data
- waitlist leads
- integrations with third-party services

## Candidate endpoints

These endpoints are a starting point for product discussion, not a final contract.

```text
POST /auth/signup
POST /auth/login
POST /waitlist/leads
GET /me
PATCH /me
GET /me/progress
PUT /me/progress/demo
POST /me/progress/missions/{missionId}
POST /auth/session
DELETE /auth/session
```

## Clients

The landing and mobile app should eventually call this API instead of writing directly to the database.

Until the API stack is chosen, the landing may keep temporary client-side Firebase/localStorage helpers so the demo keeps working.

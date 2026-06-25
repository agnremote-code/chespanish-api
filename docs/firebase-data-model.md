# Firebase data model reference

This document captures the backend/data work that was explored from the landing repo.
It is reference material for the future API and database design, not a final stack decision.

## Current concept

The landing experimented with Firebase Authentication and Firestore from the browser.
The future API should decide whether to keep Firebase as the primary backend, wrap it behind API endpoints, or replace it with another backend/database stack.

## Auth

Explored auth provider:

- Firebase Authentication
- Email/password sign up
- Email/password sign in

Passwords are handled by Firebase Authentication. The app should not store raw passwords in any database.

## Data model

User profile:

```text
users/{uid}
```

Fields:

```text
uid
email
firstName
goal
level
createdAt
updatedAt
source
```

Demo progress:

```text
users/{uid}/progress/demo
```

Fields:

```text
xp
combustible
currentStop
unlockedStop
completedMissions
completedStops
lastCompletedAt
updatedAt
```

Waitlist leads:

```text
waitlistLeads/{autoId}
```

Fields:

```text
email
firstName
goal
level
source
createdAt
```

## Draft security rules

These rules were only a draft for review.

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;

      match /progress/{progressId} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
    }

    match /waitlistLeads/{leadId} {
      allow create: if true;
      allow read, update, delete: if false;
    }
  }
}
```

## Frontend fallback behavior

The landing currently works even when Firebase or an API endpoint is missing.

```text
demo progress -> localStorage
waitlist lead -> NEXT_PUBLIC_WAITLIST_ENDPOINT if present, otherwise localStorage
```

If Firebase is configured from the landing, it can also write:

```text
demo progress -> localStorage plus Firestore
waitlist lead -> endpoint if configured plus Firestore
```

This is a temporary client-side experiment. The API repo should become the owner of backend logic once the stack is selected.

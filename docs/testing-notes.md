# Testing notes

## Current test status

The initial API scaffold has one test:

```text
tests/test_health.py
```

It verifies:

```text
GET /health -> {"status": "ok", "service": "chespanish-api"}
```

Current result:

```text
1 passed
```

## Non-blocking warning

Running `pytest` currently shows this warning from FastAPI/Starlette's test stack:

```text
StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

This is non-blocking because the test still passes and the API behavior is correct.

Meaning:

- the current test client still works
- Starlette is signaling that the preferred dependency path may change
- a future dependency upgrade could require adjusting the test client setup

Decision:

- keep moving for now
- do not block the API scaffold on this warning
- revisit when setting up CI or when adding broader API tests

Possible future fix:

- follow FastAPI/Starlette's current testing recommendation
- install or migrate to the recommended `httpx2` path if it becomes required
- pin compatible test dependencies if the warning becomes noisy or unstable

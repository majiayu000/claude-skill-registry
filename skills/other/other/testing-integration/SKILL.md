---
name: testing-integration
description: Run and debug integration tests (real Postgres via Prisma) for Drasil.
compatibility: opencode
---

Use this when validating workflows end-to-end against a real database.

## Commands

- Unit tests: `npm test`
- Integration tests: `npm run test:integration`

## Environment

- Integration tests are enabled by `JEST_INTEGRATION=1` (the integration test runner sets this).
- Provide one of:
  - `TEST_DATABASE_URL` (preferred)
  - `DATABASE_URL` (fallback)
- Optional but often needed:
  - `POSTGRES_DB_URL` (admin connection string used to create extensions)

## What the harness does

- Runs `prisma migrate deploy`
- Ensures extensions exist (uuid-ossp)
- Truncates tables between tests

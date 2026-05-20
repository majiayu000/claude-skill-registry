---
name: env-spinup
description: Spin up the local development environment — Docker, database, schema push, and test validation. Use before running tests.
disable-model-invocation: true
---

# Environment Spin-Up

Run before every test validation. Full restart each time.

```bash
docker compose down && docker compose up -d
until docker compose exec db pg_isready -U postgres 2>/dev/null; do sleep 1; done
docker compose exec db psql -U postgres -c "CREATE DATABASE bricktrack;" 2>/dev/null || true
npx drizzle-kit push
npm run test:unit
npm run test:e2e
```

## Key Details

- Playwright auto-starts dev server via `webServer` config in `playwright.config.ts`
- `.env.local` DATABASE_URL must point to `bricktrack` database (not `property_tracker`)
- E2E requires: `BETTER_AUTH_SECRET`, `E2E_CLERK_USER_EMAIL`, `E2E_CLERK_USER_PASSWORD` in `.env.local`
- DB runs via Docker Compose with `pgvector/pg16`
- Must manually create `bricktrack` db after fresh container (the `CREATE DATABASE` command above handles this)

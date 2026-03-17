---
name: quality-check-all
description: Runs quality checks across all components (backend, frontend, landing). Use before creating PRs, merging, or to verify overall code quality.
allowed-tools: Bash(task:*), Bash(pnpm:*), Bash(uv run:*)
---

# Quality Check All

Runs quality checks across all components.

## Quick Run

```bash
# Backend
cd back && task format && task tests

# Frontend
cd front && pnpm type-check && pnpm lint && pnpm test

# Landing
cd landing && pnpm type-check && pnpm lint
```

## Component Checks

### Backend

| Check | Command |
|-------|---------|
| Format | `cd back && task format` |
| Lint | `cd back && uv run ruff check src tests` |
| Tests | `cd back && task tests` |

### Frontend

| Check | Command |
|-------|---------|
| TypeScript | `cd front && pnpm type-check` |
| Lint | `cd front && pnpm lint` |
| Tests | `cd front && pnpm test` |
| Build | `cd front && pnpm build` |

### Landing

| Check | Command |
|-------|---------|
| TypeScript | `cd landing && pnpm type-check` |
| Lint | `cd landing && pnpm lint` |
| Build | `cd landing && pnpm build` |

## Pre-PR Checklist

Run all checks before creating a PR:

```bash
# 1. Backend
cd back
task format
task tests

# 2. Frontend
cd ../front
pnpm type-check
pnpm lint
pnpm test

# 3. Landing (if changed)
cd ../landing
pnpm type-check
pnpm lint

# 4. Verify builds work
cd ../front && pnpm build
cd ../landing && pnpm build
```

## CI/CD Quality Gates

GitHub Actions runs these checks automatically:
- Backend: lint, tests
- Frontend: type-check, lint, tests, build
- Landing: type-check, lint, build

## Common Issues

### Backend Test Failures
```bash
# Ensure Docker containers are running
docker compose up -d

# Reset database if needed
docker compose down && docker compose up -d
```

### Frontend Type Errors
```bash
# Regenerate API types
cd front && pnpm run generate:api
```

### Import Errors
```bash
# Fix imports automatically
cd back && task format
cd front && pnpm lint:fix
```

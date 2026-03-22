---
name: pre-release
description: Run all validation checks before tagging a new release
---

# Pre-Release Checks

Run this before tagging a new version to ensure everything works.

## Step 0: Verify main is green on CI

**Do this first, before any local checks.**

```bash
# Must be on main
git branch --show-current  # expect: main

# Check the latest CI run on main
gh run list --branch main --limit 1 --json conclusion,displayTitle,databaseId
```

Expected: `conclusion: "success"`. If CI is failing or in-progress, **stop and resolve before continuing**. All branches should already be merged to main before starting the pre-release process.

## Step 1: Clean shared types build

Nuke the shared dist to simulate CI's clean checkout. This catches missing build steps.

```bash
rm -rf shared/dist shared/tsconfig.tsbuildinfo
cd shared && npm run build
```

Expected: Build succeeds and `shared/dist/` is populated.

## Step 2: Local checks (parallel)

Run steps 2a-2e in parallel where possible (server and client checks are independent).

### 2a. Server Unit Tests
```bash
cd server && npm test
```
Expected: All tests pass

### 2b. Server Linter + Type Check
```bash
cd server && npm run lint
cd server && npx tsc --noEmit
```
Expected: No errors (warnings OK)

### 2c. Client Unit Tests
```bash
cd client && npm test
```
Expected: All tests pass

### 2d. Client Linter
```bash
cd client && npm run lint
```
Expected: No errors (warnings OK)

### 2e. Integration Tests
```bash
cd server && npm run test:integration
```
Expected: All tests pass
Note: Requires testEntities.ts to be configured

## Step 3: Build checks

### 3a. Client Build
```bash
cd client && npm run build
```
Expected: Build succeeds without errors

### 3b. Docker Build
```bash
docker build -f Dockerfile.production -t peek:test .
```
Expected: Image builds successfully

## Fixing Failures

When a check fails, invoke the relevant skill for guidance before attempting fixes:

| Failure | Skill to invoke |
|---|---|
| Test failures (writing/fixing tests) | `writing-tests` |
| TypeScript type errors | `typescript-advanced-types` |
| Prisma/migration issues | `prisma-sqlite-expert` |
| Docker build failures | `docker-best-practices` |
| React/client lint or build errors | `vercel-react-best-practices` |
| Server lint or runtime errors | `nodejs-backend-patterns` |

## After All Checks Pass

Report summary:
- CI on main: Green
- Shared types: Clean build
- Unit tests: X passed (client) + X passed (server)
- Integration tests: X passed
- Linter: Clean
- Type check: Clean
- Client build: Success
- Docker: Success

Ready to proceed with release tagging.

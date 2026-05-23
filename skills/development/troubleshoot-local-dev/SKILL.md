---
name: troubleshoot-local-dev
description: Diagnose and fix common local development environment issues
---

# Troubleshoot Local Dev Skill

Use this skill when local services fail to start or behave unexpectedly.

---

## Diagnostic Steps

### 1. Check Service Status

```bash
docker compose ps
```

If PostgreSQL isn't running or is unhealthy, start it:
```bash
task compose:up
```

### 2. Check Logs

```bash
# Database logs
docker compose logs postgres

# If running API/importer/evaluator in terminal, check that output
```

### 3. Verify Configuration

```bash
# Check .env exists and has required values
cat .env | grep POSTGRES
```

Required variables:
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

---

## Common Issues

### Database Connection Refused

**Symptoms:** Services fail with "connection refused" or "could not connect"

**Diagnosis:**
```bash
docker compose ps  # Is postgres running?
docker compose logs postgres  # Any errors?
```

**Fixes:**
- Start database: `task compose:up`
- Check `POSTGRES_HOST` in `.env` (should be `postgres` in DevContainer, `localhost` outside)

---

### Port Already in Use

**Symptoms:** "address already in use" error on startup

**Diagnosis:**
```bash
lsof -i :8080  # or whatever port
```

**Fixes:**
```bash
kill -9 <PID>
# or change the port in .env
```

---

### Migrations Not Applied

**Symptoms:** "relation does not exist" SQL errors

**Diagnosis:**
```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"
```

**Fixes:**
```bash
task migrate:up
```

---

### Empty Database / Missing Data

**Symptoms:** API returns empty results, evaluator finds nothing to process

**Diagnosis:**
```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT COUNT(*) FROM weapons;"
```

**Fixes:**
```bash
task importer:start:use-cache
```

---

### Stale or Corrupted Data

**Symptoms:** Unexpected behavior, data inconsistencies

**Full reset:**
```bash
task compose:down
docker compose down -v  # removes volumes
task compose:up
task migrate:up
task importer:start
```

---

### Build Failures

**Symptoms:** `task api:build` or similar fails

**Diagnosis:**
```bash
go build ./...  # See actual error
```

**Common fixes:**
- Missing dependencies: `go mod tidy`
- Syntax errors: Check the error message for file/line

---

## Database Inspection

Quick commands for checking database state:

```bash
# Connect to database
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# Once connected:
\dt                          # List tables
SELECT COUNT(*) FROM weapons;
SELECT COUNT(*) FROM weapon_mods;
SELECT COUNT(*) FROM optimum_builds;
\q                           # Exit
```

---
name: start-local-dev
description: Start the local development environment with all services (database, API, importer, evaluator)
---

# Start Local Dev Skill

Use this skill when starting or managing local development services.

---

## Quick Start

```bash
# Start database (in DevContainer, usually already running)
task compose:up

# Start the API
task api:start

# Optional: import data (if database is empty)
task importer:start:use-cache

# Optional: compute builds (if optimum_builds is empty)
task evaluator:start:test-mode
```

---

## Services

| Service | Command | Purpose |
|---------|---------|---------|
| PostgreSQL | `task compose:up` | Database (required by all services) |
| API | `task api:start` | HTTP endpoints at `localhost:8080` |
| Importer | `task importer:start` | Populate database from tarkov.dev |
| Evaluator | `task evaluator:start` | Compute optimal builds |

### Importer Variants

| Command | Use Case |
|---------|----------|
| `task importer:start` | Fetch fresh data from API |
| `task importer:start:use-cache` | Use local cache (faster) |
| `task importer:start:cache-only` | Update cache only, skip DB |

### Evaluator Variants

| Command | Use Case |
|---------|----------|
| `task evaluator:start` | Full evaluation (slow) |
| `task evaluator:start:test-mode` | Limited subset (fast, for development) |

---

## Service Dependencies

```
PostgreSQL
    ├── API (reads builds)
    ├── Importer (writes data)
    └── Evaluator (reads data, writes builds)
```

**Typical startup order:**
1. Database: `task compose:up`
2. Migrations: `task migrate:up` (if not already applied)
3. Importer: `task importer:start:use-cache` (if database is empty)
4. Evaluator: `task evaluator:start:test-mode` (to compute builds)
5. API: `task api:start`

---

## Common Workflows

### API Development
```bash
task compose:up
task api:start
```

### Import Pipeline Development
```bash
task compose:up
task importer:start:use-cache
```

### Evaluator Development
```bash
task compose:up
task importer:start:use-cache
task evaluator:start:test-mode
```

---

## Troubleshooting

**Database connection fails:**
- Check if database is running: `docker compose ps`
- Verify `.env` has correct `POSTGRES_*` values

**Port already in use:**
- Find process: `lsof -i :8080`
- Kill it: `kill -9 <PID>`

**Stale data:**
```bash
task compose:down
docker compose down -v  # removes volumes
task compose:up
task migrate:up
task importer:start
```

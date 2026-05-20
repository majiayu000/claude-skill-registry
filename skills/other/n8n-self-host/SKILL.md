---
name: n8n-self-host
description: >-
  Self-host, configure, scale, and manage n8n instances. Use when a user asks
  to install n8n with Docker, set up n8n in production, configure n8n
  environment variables, scale n8n with workers, back up n8n workflows, restore
  n8n data, manage n8n via CLI or REST API, monitor n8n, troubleshoot n8n
  issues, set up n8n with PostgreSQL, or deploy n8n with a reverse proxy.
  For designing n8n workflows and nodes, see n8n-workflow.
license: Apache-2.0
compatibility: "Requires Docker 20+ or Node.js 18+ for n8n installation"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["n8n", "self-hosting", "docker", "postgresql", "infrastructure"]
---

# n8n Self-Host

## Overview

Install, configure, scale, and operate self-hosted n8n instances. Covers Docker Compose production setups, CLI administration, REST API automation, queue-mode scaling with Redis workers, backup/restore, monitoring, and troubleshooting. For building n8n workflows and configuring nodes, see the `n8n-workflow` skill.

## Instructions

### Task A: Production Docker Compose Setup

Basic setup with PostgreSQL (recommended over default SQLite):

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - db_storage:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - WEBHOOK_URL=${WEBHOOK_URL}
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE:-UTC}
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
      - N8N_RUNNERS_ENABLED=true
    volumes:
      - n8n_storage:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  db_storage:
  n8n_storage:
```

Create a `.env` alongside with `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `ENCRYPTION_KEY` (generate with `openssl rand -hex 24`), `WEBHOOK_URL`, and `GENERIC_TIMEZONE`. Start with `docker compose up -d`.

### Task B: Scale with Queue Mode (Redis + Workers)

For high-volume workloads, add Redis and worker processes:

```yaml
# Add to docker-compose.yml
x-n8n-shared: &n8n-shared
  image: docker.n8n.io/n8nio/n8n
  restart: always
  environment:
    - DB_TYPE=postgresdb
    - DB_POSTGRESDB_HOST=postgres
    - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
    - DB_POSTGRESDB_USER=${POSTGRES_USER}
    - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    - EXECUTIONS_MODE=queue
    - QUEUE_BULL_REDIS_HOST=redis
    - QUEUE_HEALTH_CHECK_ACTIVE=true
    - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
  volumes:
    - n8n_storage:/home/node/.n8n
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy

services:
  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_storage:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 5s

  n8n:
    <<: *n8n-shared
    ports:
      - "5678:5678"

  n8n-worker:
    <<: *n8n-shared
    command: worker
    # Scale with: docker compose up -d --scale n8n-worker=3
```

### Task C: CLI Administration

Run CLI commands inside Docker: `docker exec -u node -it n8n n8n <command>`.

```bash
# Export/import workflows
n8n export:workflow --backup --output=backups/
n8n export:workflow --id=<ID> --output=workflow.json
n8n import:workflow --input=workflow.json
n8n import:workflow --separate --input=backups/

# Export/import credentials (--decrypted for cross-instance migration)
n8n export:credentials --backup --output=backups/
n8n export:credentials --all --decrypted --output=creds.json
n8n import:credentials --input=creds.json

# Full database backup/restore
n8n export:entities --outputDir=./backup --includeExecutionHistoryDataTables=true
n8n import:entities --inputDir=./backup --truncateTables=true

# Execute a workflow by ID
n8n execute --id=<ID>

# Activate/deactivate workflows
n8n update:workflow --id=<ID> --active=true
n8n update:workflow --all --active=false

# User management
n8n user-management:reset          # Reset to setup state (forgot password)
n8n mfa:disable --email=user@x.com # Disable MFA for locked-out user

# Security audit
n8n audit

# Database migration rollback
n8n db:revert
```

### Task D: REST API Automation

Enable the API at `/api/v1/docs`. Authenticate with `X-N8N-API-KEY` header.

```bash
# List all workflows
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows | jq '.data[].name'

# Activate a workflow
curl -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows/<ID>/activate

# Deactivate a workflow
curl -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows/<ID>/deactivate

# Retry a failed execution
curl -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/executions/<ID>/retry

# List failed executions
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "http://localhost:5678/api/v1/executions?status=error" | jq '.data[] | {id, workflowId, status}'

# Create a variable
curl -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"key":"ENV","value":"production"}' http://localhost:5678/api/v1/variables
```

### Task E: Key Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DB_TYPE` | `sqlite` | `sqlite` or `postgresdb` |
| `N8N_ENCRYPTION_KEY` | random | Credential encryption (preserve across restarts) |
| `WEBHOOK_URL` | auto | Public URL for webhooks behind reverse proxy |
| `EXECUTIONS_MODE` | `regular` | `regular` or `queue` (for scaling) |
| `EXECUTIONS_DATA_PRUNE` | `true` | Auto-prune old execution data |
| `EXECUTIONS_DATA_MAX_AGE` | `336` | Max execution age in hours |
| `N8N_METRICS` | `false` | Enable Prometheus `/metrics` endpoint |
| `N8N_LOG_LEVEL` | `info` | `error`, `warn`, `info`, `debug` |
| `N8N_LOG_OUTPUT` | `console` | `console`, `file` (comma-separated) |
| `N8N_CONCURRENCY_PRODUCTION_LIMIT` | `-1` | Max concurrent production executions |
| `N8N_RUNNERS_ENABLED` | `false` | Enable task runners for Code nodes |
| `GENERIC_TIMEZONE` | `America/New_York` | Timezone for schedule triggers |

Use `_FILE` suffix for Docker Secrets (e.g., `DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_pass`).

## Examples

### Example 1: Deploy n8n with PostgreSQL in production

**User request:** "Set up n8n in production with Docker Compose"

**Actions taken:**

```bash
$ mkdir n8n-production && cd n8n-production

# Generate secrets
$ openssl rand -hex 24
> a1b2c3d4e5f6...

# Create .env with POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB,
# ENCRYPTION_KEY, WEBHOOK_URL, GENERIC_TIMEZONE

# Create docker-compose.yml (Task A template)

$ docker compose up -d
> [+] Running 3/3
>  ✔ Network n8n-production_default   Created
>  ✔ Container postgres               Started
>  ✔ Container n8n                     Started

$ docker compose logs n8n --tail 5
> n8n  | Editor is now accessible via: http://localhost:5678
```

### Example 2: Back up and restore workflows

**User request:** "Back up all my n8n workflows and credentials"

**Actions taken:**

```bash
$ docker exec -u node n8n n8n export:workflow --backup --output=/home/node/.n8n/backups/
> Successfully exported 12 workflows

$ docker exec -u node n8n n8n export:credentials --backup --output=/home/node/.n8n/backups/
> Successfully exported 8 credentials

# Copy backups out of the container
$ docker cp n8n:/home/node/.n8n/backups/ ./n8n-backups/

# Restore on a new instance
$ docker cp ./n8n-backups/ n8n-new:/home/node/.n8n/backups/
$ docker exec -u node n8n-new n8n import:workflow --separate --input=/home/node/.n8n/backups/
> Successfully imported 12 workflows
```

### Example 3: Troubleshoot a failing instance

**User request:** "My n8n instance is crashing after update"

**Actions taken:**

```bash
$ docker compose logs n8n --tail 30
> error: Migration failed: column "x" already exists

# Rollback the last migration
$ docker exec -u node n8n n8n db:revert
> Reverted migration: AddColumnX1234567890

# Pin to previous working version in docker-compose.yml
# image: docker.n8n.io/n8nio/n8n:1.80.0

$ docker compose up -d
> n8n  | Editor is now accessible via: http://localhost:5678
```

## Guidelines

- Always set `N8N_ENCRYPTION_KEY` explicitly and back it up. Without it, credentials cannot be decrypted on a new instance.
- Use PostgreSQL for any instance running more than a few workflows. SQLite doesn't handle concurrent writes well.
- Set `WEBHOOK_URL` when behind a reverse proxy — webhooks fail silently without it.
- Use `n8n export:credentials --decrypted` when migrating between instances with different encryption keys.
- Enable execution pruning (`EXECUTIONS_DATA_PRUNE=true`) to prevent database bloat.
- In queue mode, all instances must share the same `N8N_ENCRYPTION_KEY` and PostgreSQL database.
- Scale workers with `docker compose up -d --scale n8n-worker=N`.
- Run `n8n audit` periodically to detect security issues in your instance configuration.
- For health checks, use `/healthz` (basic) and `/healthz/readiness` (DB-aware).
- Use `N8N_LOG_LEVEL=debug` temporarily when troubleshooting, then revert to `info`.

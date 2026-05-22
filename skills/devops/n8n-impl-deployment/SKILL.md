---
name: n8n-impl-deployment
description: >
  Use when deploying n8n v1.x to production or configuring Docker/queue mode.
  Prevents data loss from missing volume mounts or incorrect database
  configuration. Covers Docker/Docker Compose setup, 100+ environment variables,
  queue mode with Redis/BullMQ, worker processes, webhook processor,
  PostgreSQL/SQLite configuration, Traefik reverse proxy, scaling strategies,
  CLI commands (export/import/execute), backup strategies, and updating.
  Keywords: n8n, Docker, deployment, queue mode, Redis, PostgreSQL, backup.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Deployment & Operations

## Quick Reference

| Aspect | Value |
|--------|-------|
| Docker image | `docker.n8n.io/n8nio/n8n` |
| Default port | `5678` |
| Data volume | `/home/node/.n8n` |
| Files volume | `/files` |
| Default DB | SQLite (use PostgreSQL for production) |
| Queue broker | Redis (BullMQ) |
| Config method | Environment variables (primary) |

### Default Ports

| Service | Port |
|---------|------|
| n8n | 5678 |
| Redis | 6379 |
| PostgreSQL | 5432 |
| Task Runner Broker | 5679 |

---

## Decision Trees

### Which Database?

```
Need queue mode or multi-instance?
  YES -> ALWAYS use PostgreSQL (DB_TYPE=postgresdb)
  NO -> Single user / dev environment?
    YES -> SQLite is acceptable (default)
    NO  -> ALWAYS use PostgreSQL for production
```

### Which Deployment Mode?

```
Expected workflow volume?
  Low (< 50 active workflows, single user)
    -> Single Docker container, regular mode
  Medium (50-200 workflows, team use)
    -> Docker Compose with PostgreSQL, regular mode
  High (200+ workflows, high webhook traffic)
    -> Queue mode: main + workers + Redis + PostgreSQL
  Very High (enterprise, HA required)
    -> Multi-main + workers + Redis + PostgreSQL + load balancer
```

### Which Backup Strategy?

```
Database type?
  SQLite -> Volume backup (stop container, tar archive)
  PostgreSQL -> pg_dump (ALWAYS preferred for production)
ALWAYS also export workflows/credentials via CLI
ALWAYS back up N8N_ENCRYPTION_KEY separately
```

---

## Critical Rules

- **ALWAYS** set `N8N_ENCRYPTION_KEY` explicitly in production and back it up. Losing this key means ALL stored credentials become unrecoverable.
- **ALWAYS** share the SAME `N8N_ENCRYPTION_KEY` across ALL instances (main, workers, webhook processors).
- **ALWAYS** use PostgreSQL for queue mode. SQLite does NOT support queue mode.
- **ALWAYS** set `NODE_ENV=production` for production deployments.
- **ALWAYS** set `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true` in Docker.
- **ALWAYS** set `N8N_RUNNERS_ENABLED=true` for task runner support.
- **ALWAYS** configure `WEBHOOK_URL` when behind a reverse proxy.
- **ALWAYS** use the same n8n version across ALL instances in queue mode.
- **NEVER** use SQLite for multi-instance or queue mode deployments.
- **NEVER** expose n8n directly to the internet without TLS termination.
- **NEVER** store `N8N_ENCRYPTION_KEY` in version control.
- **NEVER** export credentials with `--decrypted` flag in production environments.

---

## Docker Deployment

### Basic Docker Run

```bash
docker volume create n8n_data

docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e GENERIC_TIMEZONE="Europe/Amsterdam" \
  -e TZ="Europe/Amsterdam" \
  -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true \
  -e N8N_RUNNERS_ENABLED=true \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### Docker Run with PostgreSQL

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e DB_TYPE=postgresdb \
  -e DB_POSTGRESDB_DATABASE=n8n \
  -e DB_POSTGRESDB_HOST=postgres-host \
  -e DB_POSTGRESDB_PORT=5432 \
  -e DB_POSTGRESDB_USER=postgres \
  -e DB_POSTGRESDB_PASSWORD=secret \
  -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true \
  -e N8N_RUNNERS_ENABLED=true \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### Volume Mounts

| Volume | Mount Point | Purpose |
|--------|-------------|---------|
| `n8n_data` | `/home/node/.n8n` | SQLite DB, encryption key, settings |
| `traefik_data` | `/letsencrypt` | TLS/SSL certificates (Let's Encrypt) |
| `./local-files` | `/files` | Host directory for workflow file access |

### Configuration Methods

1. **Environment variables** (primary): `-e VAR=value` or `environment:` in Compose
2. **Docker Compose file**: Variables in `docker-compose.yml`
3. **`_FILE` suffix**: Load secrets from files (Docker Secrets, Kubernetes Secrets)
   - Example: `DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/db_password`

### Updating

```bash
docker pull docker.n8n.io/n8nio/n8n          # Latest
docker pull docker.n8n.io/n8nio/n8n:1.81.0   # Specific version
docker stop <container_id> && docker rm <container_id>
docker run --name n8n [options] -d docker.n8n.io/n8nio/n8n
```

---

## Queue Mode Architecture

Queue mode separates n8n into distinct scaling components:

```
                    +------------------+
                    |  Load Balancer   |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
     +--------v--------+          +--------v--------+
     |  Main Instance  |          | Webhook Processor|
     |  (triggers,     |          | (optional, for   |
     |   scheduling)   |          |  high traffic)   |
     +--------+--------+          +--------+---------+
              |                             |
              +-------------+---------------+
                            |
                    +-------v-------+
                    |    Redis      |
                    |   (BullMQ)   |
                    +-------+-------+
                            |
              +-------------+-------------+
              |             |             |
     +--------v--+  +------v----+  +-----v-----+
     |  Worker 1  |  |  Worker 2 |  |  Worker N |
     +--------+---+  +------+----+  +-----+-----+
              |             |             |
              +-------------+-------------+
                            |
                    +-------v-------+
                    |  PostgreSQL   |
                    +---------------+
```

### Queue Mode Requirements

- PostgreSQL 13+ (NEVER SQLite)
- Redis for message queue
- S3-compatible storage for binary data
- Same n8n version on ALL instances
- Same `N8N_ENCRYPTION_KEY` on ALL instances
- Session-persistent load balancer for multi-main

### Starting Workers

```bash
# Native
n8n worker
n8n worker --concurrency=5

# Docker
docker run --name n8n-worker \
  -e EXECUTIONS_MODE=queue \
  -e QUEUE_BULL_REDIS_HOST=redis-host \
  -e N8N_ENCRYPTION_KEY=<shared-key> \
  -e DB_TYPE=postgresdb \
  -e DB_POSTGRESDB_HOST=postgres-host \
  -e DB_POSTGRESDB_DATABASE=n8n \
  -e DB_POSTGRESDB_PASSWORD=secret \
  docker.n8n.io/n8nio/n8n worker
```

### Webhook Processor (Optional)

```bash
# Separate webhook handler for high-traffic setups
docker run --name n8n-webhook -p 5679:5678 \
  -e EXECUTIONS_MODE=queue \
  -e QUEUE_BULL_REDIS_HOST=redis-host \
  -e N8N_ENCRYPTION_KEY=<shared-key> \
  docker.n8n.io/n8nio/n8n webhook
```

---

## CLI Commands

### Workflow Operations

```bash
n8n execute --id <ID>                                    # Execute workflow
n8n update:workflow --id=<ID> --active=true               # Activate
n8n update:workflow --id=<ID> --active=false               # Deactivate
n8n update:workflow --all --active=false                   # Deactivate all
```

### Export

```bash
n8n export:workflow --all --output=backups/               # All workflows
n8n export:workflow --id=<ID> --output=workflow.json       # Single workflow
n8n export:workflow --backup --output=backups/latest/      # Backup format
n8n export:credentials --backup --output=backups/creds/    # All credentials
n8n export:credentials --all --decrypted --output=dec.json # DANGER: decrypted
```

### Import

```bash
n8n import:workflow --input=file.json                     # From file
n8n import:workflow --separate --input=backups/latest/     # From directory
n8n import:credentials --input=file.json                  # Credentials
```

### Other CLI

```bash
n8n audit                                                 # Security audit
n8n license:info                                          # License details
n8n user-management:reset                                 # Reset user mgmt
n8n mfa:disable --email=user@example.com                  # Disable MFA
```

---

## Backup Strategies

### Strategy 1: CLI Export (Small Instances)

```bash
n8n export:workflow --backup --output=/backups/workflows/
n8n export:credentials --backup --output=/backups/credentials/
```

### Strategy 2: Database Dump (Production)

```bash
pg_dump -U postgres n8n > /backups/n8n-$(date +%Y%m%d).sql
# With Docker:
docker exec postgres pg_dump -U postgres n8n > /backups/n8n-$(date +%Y%m%d).sql
```

### Strategy 3: Volume Backup (SQLite Only)

```bash
docker stop n8n
docker run --rm -v n8n_data:/data -v $(pwd)/backup:/backup \
  alpine tar czf /backup/n8n-data.tar.gz /data
docker start n8n
```

### Critical Backup Items

- Workflow definitions (JSON export)
- Credentials (encrypted export — ALWAYS needs same `N8N_ENCRYPTION_KEY` to restore)
- `N8N_ENCRYPTION_KEY` itself (store securely, separate from backups)
- Database (PostgreSQL dump or SQLite file copy)
- Binary data (filesystem path or S3 bucket)

---

## Production Checklist

1. PostgreSQL database (NOT SQLite)
2. `N8N_ENCRYPTION_KEY` explicitly set and backed up securely
3. `NODE_ENV=production`
4. `N8N_PROTOCOL=https` with TLS termination (Traefik/nginx/Caddy)
5. `WEBHOOK_URL` set to public-facing URL
6. `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`
7. `N8N_RUNNERS_ENABLED=true`
8. Execution data pruning configured (`EXECUTIONS_DATA_PRUNE=true`)
9. Regular automated backups (database + encryption key)
10. Reverse proxy with HTTPS and rate limiting

---

## Reference Files

- [references/methods.md](references/methods.md) — Complete environment variable reference (100+ vars by category)
- [references/examples.md](references/examples.md) — Docker Compose production configs, queue mode setup, CLI scripts, backup automation
- [references/anti-patterns.md](references/anti-patterns.md) — Deployment mistakes, security misconfigurations, scaling pitfalls

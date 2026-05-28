---
name: ops-arango
description: >
  Manage ArangoDB operations including backups with automatic retention,
  health checks, embedding gap detection, duplicate detection, and integrity verification.
  Works with local or containerized ArangoDB.
triggers:
  - backup arangodb
  - dump arango
  - create database backup
  - arango dump
  - backup memory database
  - arango ops
  - check database health
  - find missing embeddings
  - detect duplicates
  - database maintenance
  - cleanup orphans
  - verify integrity
allowed-tools: Bash
metadata:
  short-description: ArangoDB operations, backups, and maintenance
---

# Arango Ops

Reliable ArangoDB operations: backups, health checks, and maintenance.

## Commands

```bash
# Create dump (Local 'arangodump' binary must be in PATH)
./run.sh dump

# Create dump from Docker Container
CONTAINER=arangodb ./run.sh dump

# Run all health checks
./run.sh check

# Find documents missing embeddings
./run.sh embeddings --fix

# Detect duplicate lessons
./run.sh duplicates --report

# Find orphaned edges
./run.sh orphans --fix

# Verify referential integrity
./run.sh integrity

# Collection statistics
./run.sh stats

# Full maintenance cycle
./run.sh full --fix
```

## Health Checks

| Check | Description |
|-------|-------------|
| `embeddings` | Find lessons/episodes without embedding vectors |
| `duplicates` | Detect lessons with similar titles/content |
| `orphans` | Find edges pointing to deleted documents |
| `integrity` | Verify all foreign keys resolve |
| `stats` | Collection sizes and document counts |

## Output Format

All commands support `--json` for machine-readable output:

```bash
./run.sh check --json
```

```json
{
  "status": "healthy|warning|critical",
  "checks": {
    "embeddings": {"missing": 0, "total": 1234},
    "duplicates": {"found": 5, "clusters": 2},
    "orphans": {"edges": 0},
    "integrity": {"errors": 0}
  },
  "recommendations": []
}
```

## Backup Output Location

Backups saved to: `~/.local/state/devops-agent/arangodumps/<timestamp>/`

## Features

- **Explicit Mode**: Set `CONTAINER` env var to use Docker. Default is local binary.
- **Integrity Check**: Verifies `manifest.json` existence after dump.
- **Safe Retention**: Keeps last N backups automatically (default 7).
- **Embedding Gaps**: Detects and optionally fixes missing embeddings.
- **Orphan Cleanup**: Removes edges pointing to deleted documents.
- **Duplicate Detection**: Finds lessons with identical titles.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ARANGO_URL` | `http://127.0.0.1:8529` | ArangoDB endpoint |
| `ARANGO_DB` | `memory` | Database name |
| `ARANGO_USER` | `root` | Username |
| `ARANGO_PASS` | - | Password |
| `CONTAINER` | - | **Required for Docker dump**. Container name. |
| `RETENTION_N` | `7` | Number of backups to keep |
| `EMBEDDING_SERVICE_URL` | - | Required for `embeddings --fix` |
| `DRY_RUN` | `0` | Set to `1` for preview mode |

## Scheduling

Add to your project's services.yaml for automated maintenance:

```yaml
scheduled:
  db-maintenance-daily:
    description: "Daily database health check"
    command: ".pi/skills/ops-arango/run.sh check --json"
    schedule: "0 1 * * *"  # 1am daily
    enabled: true

  db-maintenance-weekly:
    description: "Weekly full maintenance with fixes"
    command: ".pi/skills/ops-arango/run.sh full --fix"
    schedule: "0 0 * * 0"  # Midnight Sunday
    enabled: true

  db-backup-daily:
    description: "Daily ArangoDB backup"
    command: ".pi/skills/ops-arango/run.sh dump"
    schedule: "0 3 * * *"  # 3am daily
    enabled: true
```

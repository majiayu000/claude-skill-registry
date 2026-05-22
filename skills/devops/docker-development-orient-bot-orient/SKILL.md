---
name: docker-development
description: Local Docker development workflow for the Orient. Use when asked to build Docker images, run containers locally, debug container issues, optimize builds, use docker-compose, or troubleshoot containerization problems. Covers per-package Dockerfiles, compose layering, build optimization, and local debugging.
---

# Docker Development

## Quick Reference

```bash
# Development mode (hot-reload, uses local code)
./run.sh dev              # Start dev environment
./run.sh dev stop         # Stop services
./run.sh dev logs         # View logs
./run.sh dev status       # Show service status

# Testing mode (full Docker stack)
./run.sh test             # Build and start containers
./run.sh test pull        # Use pre-built images
./run.sh test status      # Check health
./run.sh test stop        # Stop containers
./run.sh test clean       # Remove volumes (fresh start)
```

## Instance Naming Conventions

| Mode             | Container Names | Ports            |
| ---------------- | --------------- | ---------------- |
| Dev (instance 0) | `orienter-*-0`  | 80, 5432, 9000   |
| Test             | `orienter-*`    | 80, 5432, 9000   |
| Instance N       | `orienter-*-N`  | 80+N\*1000, etc. |

## Compose File Layering

```bash
# Base configuration
docker-compose.v2.yml           # Service definitions

# Environment overlays
docker-compose.local.yml        # Local builds
docker-compose.prod.yml         # Production images
docker-compose.staging.yml      # Staging config

# Usage
docker compose -f docker-compose.v2.yml -f docker-compose.local.yml up
```

## Container Lifecycle

### Starting Containers

```bash
# With build (slow, may hang on metadata)
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.local.yml --profile slack up -d

# Without build (use existing images)
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.local.yml --profile slack up -d --no-build
```

### Stopping Containers

```bash
# Stop test stack
./run.sh test stop

# Stop specific containers (dev instance 0)
docker stop orienter-nginx-0 orienter-postgres-0 orienter-minio-0
docker rm orienter-nginx-0 orienter-postgres-0 orienter-minio-0
```

### Viewing Logs

```bash
docker logs orienter-opencode --tail 100 -f    # Follow logs
docker logs orienter-bot-slack 2>&1 | tail -50 # Last 50 lines
```

### Health Checks

```bash
./run.sh test status    # Quick health overview
docker ps               # Container status
docker inspect --format='{{.State.Health.Status}}' orienter-opencode
```

## Common Issues

### 1. Port Conflicts

**Symptom**: `Bind for 0.0.0.0:9000 failed: port is already allocated`

**Fix**: Stop conflicting containers:

```bash
# Find what's using the port
lsof -i :9000

# Stop dev containers before starting test
docker stop orienter-nginx-0 orienter-postgres-0 orienter-minio-0
docker rm orienter-nginx-0 orienter-postgres-0 orienter-minio-0
```

### 2. Build Hangs on Metadata Loading (macOS)

**Symptom**: `./run.sh test` hangs at "load metadata for docker.io/library/node:20-alpine"

**Cause**: Docker buildx slow to fetch from Docker Hub.

**Workarounds**:

```bash
# Option 1: Pre-pull images
docker pull node:20-alpine
docker pull node:20-slim

# Option 2: Use existing local images
docker compose ... up -d --no-build

# Option 3: Use ghcr.io images (requires auth)
./run.sh test pull
```

### 3. ECONNRESET During Tests

**Symptom**: E2E tests fail with `fetch failed` / `ECONNRESET`

**Cause**: Container crashed or restarted during test run.

**Debug**:

```bash
# Check container status
docker ps -a | grep opencode

# Check if recently restarted
# Look for "Up X seconds" when tests ran for minutes

# View crash logs
docker logs orienter-opencode 2>&1 | tail -100
```

### 4. Container Won't Start

**Debug steps**:

```bash
# Check exit code
docker ps -a --filter "name=orienter-opencode"

# Check logs for errors
docker logs orienter-opencode 2>&1

# Check if image exists
docker images | grep docker-opencode

# Rebuild single service
docker compose ... build opencode
```

### 5. ghcr.io Authentication

**Symptom**: `./run.sh test pull` fails with 401 Unauthorized

**Fix**:

```bash
# Authenticate to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

## Switching Between Stacks

**Always stop one stack before starting another:**

```bash
# From dev to test
./run.sh dev stop
./run.sh test

# From test to dev
./run.sh test stop
./run.sh dev
```

## Building Images

```bash
# Build all services
docker compose -f docker-compose.v2.yml -f docker-compose.local.yml build

# Build single service
docker compose -f docker-compose.v2.yml -f docker-compose.local.yml build dashboard

# Build with no cache
docker compose ... build --no-cache opencode

# Build with progress output
docker compose ... build dashboard --progress=plain
```

## Environment Variables

Compose files use `--env-file ../.env` to load environment. Required vars:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`
- `ANTHROPIC_API_KEY`
- `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET` (for Slack profile)

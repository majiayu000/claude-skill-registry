---
name: docker-vigil-orchestration
description: Docker Compose orchestration for Vigil Guard v2.0.0 microservices (11 services). Use when deploying services, managing containers, troubleshooting Docker network issues, working with vigil-net, configuring docker-compose.yml, handling service dependencies, or working with 3-branch detection services (heuristics, semantic, prompt-guard).
version: 2.0.0
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Docker Orchestration for Vigil Guard v2.0.0

## Overview

Multi-service Docker deployment orchestration for Vigil Guard's 3-branch parallel detection architecture with 11 microservices.

## When to Use This Skill

- Starting/stopping services
- Debugging container issues
- Managing Docker network (vigil-net)
- Modifying docker-compose.yml
- Viewing service logs
- Checking service health
- Troubleshooting port conflicts
- Understanding service dependencies
- Managing 3-branch detection services

## Service Architecture (v2.0.0)

### All Services (11 containers)

```yaml
services:
  # 3-Branch Detection Engine
  heuristics-service:    # Branch A - Pattern detection (5005)
  semantic-service:      # Branch B - Embedding similarity (5006)
  prompt-guard-api:      # Branch C - LLM safety (8000)

  # PII & Language Detection
  presidio-pii-api:      # Dual-language PII detection (5001)
  language-detector:     # Hybrid language detection (5002)

  # Core Platform
  n8n:                   # Workflow engine - 24-node pipeline (5678)
  web-ui-backend:        # Express API server (8787)
  web-ui-frontend:       # React SPA (80 internal)

  # Monitoring Stack
  clickhouse:            # Analytics database (8123, 9000)
  grafana:               # Dashboards (3001)

  # Infrastructure
  caddy:                 # Reverse proxy (80, 443)
```

### Service Ports

| Service | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------|
| heuristics-service | 5005 | 5005 | Branch A detection |
| semantic-service | 5006 | 5006 | Branch B detection |
| prompt-guard-api | 8000 | 8000 | Branch C detection |
| presidio-pii-api | 5001 | 5001 | PII detection |
| language-detector | 5002 | 5002 | Language detection |
| n8n | 5678 | 5678 | Workflow engine |
| web-ui-backend | 8787 | 8787 | Config API |
| web-ui-frontend | 80 | - | React UI (via Caddy) |
| clickhouse | 8123, 9000 | 8123, 9000 | Analytics DB |
| grafana | 3000 | 3001 | Monitoring |
| caddy | 80, 443 | 80, 443 | Reverse proxy |

### Docker Network

All services communicate via `vigil-net` external network.

**Internal hostnames:**
- `heuristics-service` (Branch A)
- `semantic-service` (Branch B)
- `prompt-guard-api` (Branch C)
- `vigil-presidio-pii` or `presidio-pii-api`
- `vigil-language-detector` or `language-detector`
- `vigil-clickhouse` or `clickhouse`
- `vigil-n8n` or `n8n`
- `web-ui-backend`
- `web-ui-frontend`

## Service Dependencies (Startup Order)

```
                    vigil-net (network)
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
clickhouse            grafana              caddy
    │
    ├── heuristics-service
    ├── semantic-service (depends: clickhouse)
    ├── prompt-guard-api
    │
    ├── presidio-pii-api
    ├── language-detector
    │
    └── n8n (depends: all detection services)
            │
            └── web-ui-backend (depends: n8n, clickhouse)
                    │
                    └── web-ui-frontend
```

## Common Commands

### Start All Services

```bash
docker-compose up -d
```

### Start Services by Function

```bash
# 3-Branch Detection only
docker-compose up -d heuristics-service semantic-service prompt-guard-api

# PII Detection only
docker-compose up -d presidio-pii-api language-detector

# Monitoring only
docker-compose up -d clickhouse grafana

# Web UI only
docker-compose up -d web-ui-backend web-ui-frontend caddy

# Workflow engine
docker-compose up -d n8n
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f heuristics-service

# Last 100 lines
docker-compose logs --tail=100 n8n

# Multiple services
docker-compose logs -f heuristics-service semantic-service prompt-guard-api
```

### Restart Services

```bash
# All
docker-compose restart

# Specific
docker-compose restart heuristics-service

# 3-Branch services
docker-compose restart heuristics-service semantic-service prompt-guard-api
```

### Stop and Remove

```bash
# Stop all
docker-compose down

# Stop and remove volumes (DESTRUCTIVE!)
docker-compose down -v
```

### Rebuild After Changes

```bash
# Rebuild all
docker-compose up --build -d

# Rebuild specific
docker-compose up --build -d heuristics-service

# Rebuild with no cache
docker-compose build --no-cache heuristics-service
```

## Service Health Checks

### Check Running Containers

```bash
docker ps
# Should show 11 containers: vigil-*, heuristics-service, semantic-service, etc.
```

### Test Service Endpoints

```bash
# Branch A - Heuristics
curl http://localhost:5005/health

# Branch B - Semantic
curl http://localhost:5006/health

# Branch C - LLM Guard
curl http://localhost:8000/health

# PII Detection
curl http://localhost:5001/health

# Language Detection
curl http://localhost:5002/health

# n8n
curl http://localhost:5678/healthz

# ClickHouse
curl http://localhost:8123/ping

# Grafana
curl -I http://localhost:3001

# Backend API
curl http://localhost:8787/api/files

# Proxy
curl -I http://localhost/ui/
```

### Check All Services Script

```bash
#!/bin/bash
# scripts/health-check.sh

services=(
  "5005:Heuristics"
  "5006:Semantic"
  "8000:LLM Guard"
  "5001:Presidio"
  "5002:Language"
  "5678:n8n"
  "8123:ClickHouse"
  "3001:Grafana"
  "8787:Backend"
)

for svc in "${services[@]}"; do
  port="${svc%%:*}"
  name="${svc##*:}"
  if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
    echo "✅ $name (:$port)"
  else
    echo "❌ $name (:$port)"
  fi
done
```

## Docker Network

### Inspect Network

```bash
docker network inspect vigil-net
```

### Create Network (if missing)

```bash
docker network create vigil-net
```

### Test Inter-Service Connectivity

```bash
# From n8n to heuristics
docker exec vigil-n8n curl -s http://heuristics-service:5005/health

# From n8n to semantic
docker exec vigil-n8n curl -s http://semantic-service:5006/health

# From n8n to prompt-guard
docker exec vigil-n8n curl -s http://prompt-guard-api:8000/health
```

## Volume Management

### List Volumes

```bash
docker volume ls | grep vigil
```

### Backup Volumes

```bash
# ClickHouse data
docker run --rm -v vigil_clickhouse_data:/data -v $(pwd):/backup alpine tar czf /backup/clickhouse-backup.tar.gz /data

# n8n data
docker run --rm -v vigil_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup.tar.gz /data

# Semantic embeddings
docker run --rm -v vigil_semantic_data:/data -v $(pwd):/backup alpine tar czf /backup/semantic-backup.tar.gz /data
```

### Remove Volumes (DESTRUCTIVE!)

```bash
docker volume rm vigil_clickhouse_data
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :5005

# Kill process (if needed)
kill -9 <PID>
```

### Service Won't Start

```bash
# Check logs
docker-compose logs heuristics-service

# Check network
docker network inspect vigil-net

# Verify environment variables
docker-compose config

# Check dependencies
docker-compose ps
```

### Container Crashes

```bash
# View last logs before crash
docker logs --tail=100 heuristics-service

# Check restart count
docker ps -a | grep vigil

# Inspect container
docker inspect heuristics-service
```

### Network Issues

```bash
# Restart networking
docker-compose down
docker network rm vigil-net
docker network create vigil-net
docker-compose up -d
```

### Branch Timeout Issues

```bash
# Check branch timing in ClickHouse
docker exec vigil-clickhouse clickhouse-client -q "
  SELECT
    avg(branch_a_timing_ms) as a_avg,
    avg(branch_b_timing_ms) as b_avg,
    avg(branch_c_timing_ms) as c_avg
  FROM n8n_logs.events_processed
  WHERE timestamp > now() - INTERVAL 1 HOUR
"

# Check service resource usage
docker stats heuristics-service semantic-service prompt-guard-api
```

## Environment Variables

Loaded from `.env` file:

```bash
# ClickHouse
CLICKHOUSE_USER=admin
CLICKHOUSE_PASSWORD=<auto-generated>

# Grafana
GF_SECURITY_ADMIN_PASSWORD=<auto-generated>

# Backend
SESSION_SECRET=<auto-generated>
JWT_SECRET=<auto-generated>

# Heuristics Service
HEURISTICS_PORT=5005
HEURISTICS_TIMEOUT=1000

# Semantic Service
SEMANTIC_PORT=5006
SEMANTIC_TIMEOUT=2000
EMBEDDING_MODEL=all-MiniLM-L6-v2

# LLM Guard
PROMPT_GUARD_PORT=8000
PROMPT_GUARD_TIMEOUT=3000
```

## Development vs Production

### Development (individual services)

```bash
# Backend dev server
cd services/web-ui/backend && npm run dev

# Frontend dev server
cd services/web-ui/frontend && npm run dev

# Heuristics dev
cd services/heuristics-service && npm run dev

# Semantic dev
cd services/semantic-service && python app.py
```

### Production (Docker)

```bash
# Build and start all
docker-compose up --build -d

# Verify all healthy
./scripts/status.sh
```

## Monitoring Resources

### Container Stats

```bash
docker stats
```

### Disk Usage

```bash
docker system df
```

### Prune Unused Resources

```bash
# Remove unused containers, images, networks
docker system prune

# Remove volumes too (CAREFUL!)
docker system prune -a --volumes
```

## Related Skills

- `n8n-vigil-workflow` - 24-node workflow service
- `clickhouse-grafana-monitoring` - Database management
- `pattern-library-manager` - Heuristics patterns
- `presidio-pii-specialist` - PII detection service

## References

- Docker Compose: `docker-compose.yml`
- Heuristics: `services/heuristics-service/`
- Semantic: `services/semantic-service/`
- Environment: `.env`

## Version History

- **v2.0.0** (Current): 11 services, 3-branch architecture
- **v1.6.11**: 9 services (no heuristics, no semantic)
- **v1.6.0**: Added presidio-pii-api, language-detector

---
name: installation-orchestrator
description: Expert management of install.sh (2000+ lines). Use for installation troubleshooting, idempotency checks, secret generation, volume migration, 11 services startup order (including heuristics and semantic), and user onboarding.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Installation Orchestrator (v2.0.0)

## Overview

Expert management of install.sh (2000+ lines bash) including idempotency, secret generation, volume migration, 11-service orchestration with 3-branch detection startup, and troubleshooting installation failures.

## When to Use This Skill

- Troubleshooting installation failures
- Managing install.sh modifications
- Secret generation and validation
- Volume migration between versions
- Idempotency checks
- User onboarding flow
- 3-branch service startup order (v2.0.0)

## v2.0.0 Architecture

### 11 Docker Services

```yaml
Core Services:
  - clickhouse (data storage, port 8123)
  - grafana (monitoring, port 3001)
  - n8n (workflow engine, port 5678)

3-Branch Detection (v2.0.0):
  - heuristics-service (Branch A, port 5005, 30% weight)
  - semantic-service (Branch B, port 5006, 35% weight)
  - prompt-guard-api (Branch C, port 8000, 35% weight)

PII Detection:
  - presidio-pii-api (port 5001)
  - language-detector (port 5002)

Web Interface:
  - web-ui-backend (port 8787)
  - web-ui-frontend (via proxy)
  - proxy (Caddy, port 80)
```

## Installation Flow

### 1. Pre-flight Checks

```bash
- Docker installed and running
- Ports available (80, 5678, 8123, 3001, 8787, 5005, 5006, 8000)
- Disk space >10GB
- No existing .install-state.lock
```

### 2. Secret Generation

```bash
CLICKHOUSE_PASSWORD=$(openssl rand -base64 32)
GF_SECURITY_ADMIN_PASSWORD=$(openssl rand -base64 32)
SESSION_SECRET=$(openssl rand -base64 64)
JWT_SECRET=$(openssl rand -base64 32)
WEB_UI_ADMIN_PASSWORD=$(openssl rand -base64 24)
```

### 3. Service Startup Order (v2.0.0)

```yaml
Phase 1 - Data Layer:
  1. clickhouse (data storage)
  2. grafana (monitoring)

Phase 2 - Detection Core:
  3. n8n (workflow engine)
  4. heuristics-service (Branch A - fast pattern matching)
  5. semantic-service (Branch B - embedding analysis)
  6. prompt-guard-api (Branch C - LLM validation, optional)

Phase 3 - PII Services:
  7. presidio-pii-api (dual-language PII)
  8. language-detector (hybrid detection)

Phase 4 - Web Interface:
  9. web-ui-backend (Express API)
  10. web-ui-frontend (React app)
  11. proxy (Caddy reverse proxy)
```

### 4. Health Checks (v2.0.0)

```bash
# Core services
for service in clickhouse grafana n8n web-ui; do
  wait_for_health $service 120s || fail
done

# 3-Branch detection services (v2.0.0)
wait_for_health heuristics-service 60s || warn "Branch A degraded"
wait_for_health semantic-service 90s || warn "Branch B degraded"
wait_for_health prompt-guard-api 120s || warn "Branch C degraded"

# PII services
wait_for_health presidio-pii-api 90s || warn "PII detection degraded"
wait_for_health language-detector 30s || warn "Language detection degraded"
```

### 5. Idempotency Lock

```bash
touch .install-state.lock
echo "INSTALL_DATE=$(date)" >> .install-state.lock
echo "VERSION=2.0.0" >> .install-state.lock
echo "SERVICES=11" >> .install-state.lock
```

## Common Tasks

### Task 1: Fresh Installation

```bash
./install.sh

# Prompts:
# 1. Generate secrets? [Y/n]
# 2. Set admin password (or auto-generate)
# 3. Delete existing vigil_data? [y/N]
# 4. Download Llama model? [Y/n] (for Branch C)
```

### Task 2: Troubleshoot Failed Installation

```bash
# Check state
cat .install-state.lock

# View logs
docker-compose logs --tail=100

# Check 3-branch services specifically (v2.0.0)
docker logs vigil-heuristics-service --tail 50
docker logs vigil-semantic-service --tail 50
docker logs vigil-prompt-guard-api --tail 50

# Retry specific service
docker-compose up -d heuristics-service
docker logs vigil-heuristics-service

# Clean slate
rm .install-state.lock .env vigil_data -rf
./install.sh
```

### Task 3: Validate Environment

```bash
./scripts/validate-env.sh

# Checks:
# - All required env vars present
# - Passwords meet requirements (min 8 chars)
# - Ports not in use (including 5005, 5006 for branches)
# - Docker network exists (vigil-net)
# - 11 services defined in docker-compose.yml
```

### Task 4: Migrate Volumes (v1.x → v2.0.0)

```bash
# Backup old data
docker run --rm -v vigil_clickhouse_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/clickhouse-v1.x-$(date +%Y%m%d).tar.gz /data

# Run v2.0.0 migration SQL (adds branch columns)
docker exec vigil-clickhouse clickhouse-client < services/monitoring/sql/migrations/v2.0.0.sql

# Verify migration (branch columns added)
docker exec vigil-clickhouse clickhouse-client -q "
  DESCRIBE n8n_logs.events_processed
" | grep -E "branch_[abc]_score|arbiter_decision"

# Expected output:
# branch_a_score    Float32
# branch_b_score    Float32
# branch_c_score    Float32
# arbiter_decision  String
```

### Task 5: Verify 3-Branch Services (v2.0.0)

```bash
#!/bin/bash
# scripts/verify-branches.sh

echo "🔍 Verifying 3-Branch Detection Services..."

# Branch A: Heuristics
BRANCH_A=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5005/health)
if [ "$BRANCH_A" == "200" ]; then
  echo "✅ Branch A (Heuristics): Healthy"
else
  echo "❌ Branch A (Heuristics): Down (HTTP $BRANCH_A)"
fi

# Branch B: Semantic
BRANCH_B=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5006/health)
if [ "$BRANCH_B" == "200" ]; then
  echo "✅ Branch B (Semantic): Healthy"
else
  echo "❌ Branch B (Semantic): Down (HTTP $BRANCH_B)"
fi

# Branch C: LLM Guard
BRANCH_C=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$BRANCH_C" == "200" ]; then
  echo "✅ Branch C (LLM Guard): Healthy"
else
  echo "⚠️  Branch C (LLM Guard): Down (HTTP $BRANCH_C) - Optional"
fi

echo ""
echo "3-Branch Status: $([ "$BRANCH_A" == "200" ] && [ "$BRANCH_B" == "200" ] && echo "OPERATIONAL" || echo "DEGRADED")"
```

## Troubleshooting

### Issue: Port already in use

```bash
# Check all v2.0.0 ports
for port in 80 5678 8123 3001 8787 5001 5002 5005 5006 8000; do
  lsof -i :$port && echo "Port $port in use"
done

# Kill specific process
kill -9 $(lsof -t -i:5005)
```

### Issue: Branch service won't start

```bash
# Check heuristics-service
docker logs vigil-heuristics-service --tail 100
# Common issue: missing patterns directory
# Fix: docker-compose build heuristics-service

# Check semantic-service
docker logs vigil-semantic-service --tail 100
# Common issue: model download failed
# Fix: docker exec vigil-semantic-service python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Issue: ClickHouse won't start

```bash
# Check volume permissions
ls -la vigil_data/clickhouse/

# Reset volume
docker-compose down -v
docker volume rm vigil_clickhouse_data
./install.sh
```

### Issue: Secrets not loaded

```bash
# Verify .env file
cat .env | grep -E "(CLICKHOUSE|JWT|SESSION)_"

# Reload
docker-compose down
docker-compose up -d
```

### Issue: Semantic service model download fails

```bash
# Pre-download model (run before install)
docker run --rm -v vigil_semantic_models:/models python:3.11-slim bash -c "
  pip install sentence-transformers &&
  python -c \"from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/models')\"
"

# Restart semantic service
docker-compose restart semantic-service
```

## Port Reference (v2.0.0)

| Port | Service | Description |
|------|---------|-------------|
| 80 | proxy | Caddy reverse proxy (main entry) |
| 3001 | grafana | Monitoring dashboard |
| 5001 | presidio-pii-api | Dual-language PII detection |
| 5002 | language-detector | Hybrid language detection |
| 5005 | heuristics-service | Branch A (30% weight) |
| 5006 | semantic-service | Branch B (35% weight) |
| 5678 | n8n | Workflow engine |
| 8000 | prompt-guard-api | Branch C (35% weight) |
| 8123 | clickhouse | Analytics database |
| 8787 | web-ui-backend | Configuration API |

## Quick Reference

```bash
# Fresh install
./install.sh

# Status check (all 11 services)
./scripts/status.sh

# Verify 3-branch detection (v2.0.0)
./scripts/verify-branches.sh

# View logs
./scripts/logs.sh

# Restart
./scripts/restart.sh

# Uninstall
docker-compose down -v
rm -rf vigil_data .env .install-state.lock
```

## Integration Points

### With docker-vigil-orchestration:
```yaml
when: Service won't start
action:
  1. Check vigil-net network connectivity
  2. Verify service dependencies
  3. Check port conflicts
  4. Review Docker resource limits
```

### With clickhouse-grafana-monitoring:
```yaml
when: Migration to v2.0.0
action:
  1. Run SQL migration script
  2. Verify branch columns exist
  3. Test ClickHouse queries
  4. Update Grafana dashboards
```

---

**Last Updated:** 2025-12-09
**Install Script:** 2000+ lines bash
**Services:** 11 containers (v2.0.0)
**3-Branch Ports:** 5005 (Heuristics), 5006 (Semantic), 8000 (LLM Guard)

## Version History

- **v2.0.0** (Current): 11 services, 3-branch detection startup, migration scripts
- **v1.6.11**: 9 services, sequential detection

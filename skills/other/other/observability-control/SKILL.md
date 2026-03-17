---
name: observability-control
description: Manage observability stack lifecycle (start, stop, backup, restore, upgrade). Use when controlling the LGTM stack for Claude Code monitoring.
---

# Observability Control

Manage the lifecycle of the observability stack for Claude Code telemetry.

## Stack Locations

| Environment | Docker Compose Path |
|-------------|---------------------|
| Primary Stack | `/mnt/c/data/github/botaniqal-medtech/botaniqal-medtech/observability/docker-compose.yml` |
| Skill-based Stack | `/mnt/c/data/github/.observability/docker-compose.yml` |

## Components

| Service | Port | Purpose |
|---------|------|---------|
| Grafana | 3000 | Dashboards and visualization |
| Prometheus | 9090 | Metrics storage |
| Loki | 3100 | Log aggregation |
| Tempo | 3200 | Distributed tracing |
| OTEL Collector | 4317/4318 | Telemetry receiver |
| Promtail | - | Log shipping |

## Operations

### `start`
Start observability stack.
```bash
docker compose -f /mnt/c/data/github/botaniqal-medtech/botaniqal-medtech/observability/docker-compose.yml up -d
```

### `stop`
Stop stack gracefully (preserves data).
```bash
docker compose -f /mnt/c/data/github/botaniqal-medtech/botaniqal-medtech/observability/docker-compose.yml down
```

### `restart [service]`
Restart specific service or all services.
```bash
# Restart all
docker compose -f /path/docker-compose.yml restart

# Restart specific
docker restart loki
```

### `status`
Health check all components.
```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(otel|loki|grafana|prometheus|tempo)"
```
**Output**: Running services, health status.

### `health`
Verify service endpoints.
```bash
curl -s http://localhost:3000/api/health  # Grafana
curl -s http://localhost:9090/-/healthy   # Prometheus
curl -s http://localhost:3100/ready       # Loki
curl -s http://localhost:3200/ready       # Tempo
```

### `backup`
Export dashboards and configurations.
```bash
# Backup dashboards
curl -s http://localhost:3000/api/search -u admin:admin | \
  jq -r '.[].uid' | \
  xargs -I {} curl -s http://localhost:3000/api/dashboards/uid/{} -u admin:admin > backup/dashboards.json
```
**Output**: `.observability/backups/YYYYMMDD_HHMMSS/`

### `restore <backup-path>`
Restore from backup.
```bash
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -u admin:admin \
  -d @backup/dashboards.json
```

### `logs [service]`
View logs from stack components.
```bash
docker logs loki --tail 100
docker logs otel-collector --tail 100
docker logs grafana --tail 100
```

### `fix-permissions`
Fix volume permission issues (common with Tempo).
```bash
docker volume rm observability_tempo-data
docker volume create observability_tempo-data
docker run --rm -v observability_tempo-data:/tempo alpine chown -R 10001:10001 /tempo
docker restart tempo
```

## Quick Commands

```bash
# Check all services status
docker ps | grep -E "(otel|loki|grafana|prometheus|tempo|promtail)"

# View recent logs for issues
docker logs otel-collector --tail 50 2>&1 | grep -i error

# Test OTLP endpoint
curl -v http://localhost:4317

# Query Loki for recent data
curl -s "http://localhost:3100/loki/api/v1/labels"

# List Grafana dashboards
curl -s http://localhost:3000/api/search -u admin:admin | python3 -c "import sys,json; [print(d['title']) for d in json.load(sys.stdin)]"
```

## Troubleshooting

### OTEL Collector Unhealthy
```bash
docker logs otel-collector --tail 30
# Common fix: Ensure Prometheus has --web.enable-remote-write-receiver
```

### Loki Unhealthy
```bash
docker logs loki --tail 30
# Common fix: Disable frontend_worker for single-node mode
```

### Tempo Permission Denied
```bash
# Fix volume permissions
docker volume rm observability_tempo-data
docker volume create observability_tempo-data
docker run --rm -v observability_tempo-data:/tempo alpine chown -R 10001:10001 /tempo
docker restart tempo
```

### No Data in Grafana
1. Check telemetry env vars: `env | grep OTEL`
2. Check hooks configured: `cat .claude/settings.json`
3. Verify Loki receiving: `curl "http://localhost:3100/loki/api/v1/labels"`

## Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |
| Loki | http://localhost:3100 | - |
| OTLP gRPC | localhost:4317 | - |
| OTLP HTTP | localhost:4318 | - |

## Scripts

- `scripts/start-stack.sh` - Start observability stack
- `scripts/stop-stack.sh` - Stop stack gracefully
- `scripts/health-check.sh` - Check all service health
- `scripts/backup-dashboards.sh` - Export Grafana dashboards
- `scripts/restore-dashboards.sh` - Import dashboards from backup

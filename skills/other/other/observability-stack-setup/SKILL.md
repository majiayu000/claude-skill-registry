---
name: observability-stack-setup
description: Automated LGTM + Alloy observability stack deployment using Docker Compose. Use when setting up Claude Code observability infrastructure locally.
---

# Observability Stack Setup

Automated deployment of the complete LGTM (Loki, Grafana, Tempo, Mimir/Prometheus) + Alloy observability stack for Claude Code monitoring.

## When to Use

- Setting up Claude Code observability for the first time
- Deploying local development observability infrastructure
- Need to monitor Claude Code operations (tool calls, costs, errors, performance)
- Want pre-configured dashboards for Claude Code analysis

## What This Skill Does

Automatically deploys and configures:
- **Grafana Alloy**: OTEL collector (receives telemetry from Claude Code)
- **Loki**: Log aggregation (stores all Claude Code logs)
- **Tempo**: Distributed tracing (tracks tool calls, API requests)
- **Prometheus**: Metrics storage (token usage, costs, performance)
- **Grafana**: Visualization with pre-built Claude Code dashboards

## Quick Start

### Prerequisites

```bash
# Verify Docker installed
docker --version  # Requires ≥ 20.10

# Verify Docker Compose installed
docker compose version  # Requires ≥ 2.0
```

### Deploy Stack

**Invoke this skill** and it will:
1. Create `.observability/` directory structure
2. Generate all configuration files
3. Start the stack with `docker compose up -d`
4. Import Claude Code dashboards
5. Verify all services healthy
6. Output access URLs and next steps

**Estimated time**: 5-10 minutes

## What Gets Deployed

### Services

| Service | Port | Purpose |
|---------|------|---------|
| Grafana | 3000 | Dashboards and visualization |
| Grafana Alloy | 4317 (gRPC), 4318 (HTTP), 12345 (metrics) | OTLP receiver |
| Loki | 3100 | Log storage and querying |
| Tempo | 3200 | Trace storage and querying |
| Prometheus | 9090 | Metrics storage and querying |

### Volumes

All data persisted in `.observability/volumes/`:
- `alloy-data/` - Alloy configuration and state
- `loki-data/` - Log storage
- `tempo-data/` - Trace storage
- `prometheus-data/` - Metrics storage
- `grafana-data/` - Dashboards, datasources, settings

### Pre-built Dashboards

1. **Claude Code Overview**
   - Session count, duration, active time
   - Token usage and cost trends
   - Error rates by tool
   - Top operations

2. **Tool Performance Matrix**
   - Call counts per tool
   - Average/P95/P99 latency
   - Success/failure rates
   - Most common errors

3. **Cost Analysis**
   - Daily/weekly/monthly costs
   - Token usage breakdown
   - Budget tracking
   - Cost projections

4. **Error Tracking**
   - Error timeline
   - Error types distribution
   - Affected tools
   - Recent error details

5. **Session Analysis**
   - Session duration distribution
   - Sessions per day/week
   - Conversation depth
   - Active vs idle time

## Workflow

### Step 1: Verify Prerequisites

Checks Docker and Docker Compose installed with compatible versions.

### Step 2: Create Directory Structure

```
.observability/
├── docker-compose.yml          # Main stack definition
├── alloy/
│   └── config.yaml            # OTLP receiver + exporters config
├── grafana/
│   ├── datasources/
│   │   ├── loki.yml           # Loki datasource
│   │   ├── prometheus.yml     # Prometheus datasource
│   │   └── tempo.yml          # Tempo datasource
│   └── dashboards/
│       ├── claude-code-overview.json
│       ├── tool-performance.json
│       ├── cost-analysis.json
│       ├── error-tracking.json
│       └── session-analysis.json
└── volumes/                   # Persistent data
    ├── alloy/
    ├── loki/
    ├── tempo/
    ├── prometheus/
    └── grafana/
```

### Step 3: Generate Configurations

Creates all configuration files from templates (see `references/` for details).

### Step 4: Start Stack

```bash
docker compose -f .observability/docker-compose.yml up -d
```

### Step 5: Health Checks

Verifies each service:
- Alloy: `http://localhost:12345/metrics`
- Loki: `http://localhost:3100/ready`
- Tempo: `http://localhost:3200/ready`
- Prometheus: `http://localhost:9090/-/healthy`
- Grafana: `http://localhost:3000/api/health`

### Step 6: Import Dashboards

Uses Grafana API to import all pre-built dashboards.

### Step 7: Output Success

Displays:
- Access URLs for all services
- Default credentials (admin/admin)
- OTLP endpoint for Claude Code configuration
- Next step: Enable Claude Code telemetry

## Configuration Details

### Grafana Alloy (OTLP Collector)

Receives telemetry from Claude Code via OTLP protocol:
- **gRPC endpoint**: `localhost:4317`
- **HTTP endpoint**: `localhost:4318`

Routes telemetry to backends:
- Logs → Loki
- Traces → Tempo
- Metrics → Prometheus

### Retention Policies

**Default: 365 days** (configurable in docker-compose.yml)

- **Loki**: 365 days (`-ingester.max-chunk-age=365d`)
- **Tempo**: 365 days (`-storage.trace.local.path retention`)
- **Prometheus**: 365 days (`--storage.tsdb.retention.time=365d`)

### Privacy Settings

**Full logging enabled** (no redactions):
- User prompts: Full content logged
- File paths: Complete paths visible
- Tool execution: Full command details
- API requests: All parameters visible

This configuration assumes observability for personal use with full data access.

## Troubleshooting

### Port Already in Use

If ports 3000, 3100, 3200, 4317, 4318, 9090, or 12345 are in use:

**Option 1**: Stop conflicting services
```bash
# Find process using port
sudo lsof -i :3000
# Stop the process
sudo kill <PID>
```

**Option 2**: Modify ports in `docker-compose.yml`

### Services Not Starting

Check logs:
```bash
docker compose -f .observability/docker-compose.yml logs [service_name]
```

Common issues:
- Insufficient disk space (check with `df -h`)
- Insufficient memory (Alloy needs ~512MB, others ~256MB each)
- Permission issues on volume directories

### Dashboards Not Appearing

Manually import:
```bash
# Copy dashboard JSON to container
docker cp .observability/grafana/dashboards/claude-code-overview.json \
  observability-grafana-1:/tmp/

# Import via API
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -u admin:admin \
  -d @.observability/grafana/dashboards/claude-code-overview.json
```

## Next Steps

After stack is running:

1. **Enable Claude Code telemetry**: Use `claude-code-telemetry-enable` skill
2. **Use Claude Code**: Run tools, read files, execute commands
3. **View dashboards**: Open http://localhost:3000, explore pre-built dashboards
4. **Verify data flowing**: Check Grafana → Explore → Loki/Prometheus/Tempo

## Stopping the Stack

**Graceful shutdown** (preserves data):
```bash
docker compose -f .observability/docker-compose.yml down
```

**Complete removal** (deletes data):
```bash
docker compose -f .observability/docker-compose.yml down -v
```

## References

- `references/docker-compose-full.yml` - Complete Docker Compose configuration
- `references/alloy-config.yaml` - Grafana Alloy OTLP receiver configuration
- `references/grafana-datasources/` - Datasource YAML configurations
- `references/dashboards/` - Pre-built dashboard JSON files
- `references/troubleshooting.md` - Common issues and solutions

## Scripts

- `scripts/setup-stack.sh` - Main setup script (automated deployment)
- `scripts/verify-health.sh` - Health check all services
- `scripts/import-dashboards.sh` - Import Grafana dashboards

## Version Information

**Component Versions** (latest as of 2025-11-22):
- Grafana: 11.5.2
- Grafana Alloy: 1.5.0
- Loki: 3.4.2
- Tempo: 2.7.1
- Prometheus: 2.55.0

All versions pinned in docker-compose.yml for reproducibility.

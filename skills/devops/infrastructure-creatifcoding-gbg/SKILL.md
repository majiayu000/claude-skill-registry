---
name: infrastructure
description: TMNL Docker infrastructure documentation. Service topology, health checks, troubleshooting. Model-invoked when debugging containers or understanding service architecture.
model_invoked: true
triggers:
  - "infrastructure"
  - "docker architecture"
  - "service topology"
  - "container health"
  - "why is service down"
  - "container not starting"
  - "port conflict"
  - "what's running"
  - "infra status"
  - "check containers"
---

# TMNL Infrastructure

Docker-based infrastructure for the TMNL stack. All services defined in `docker/docker-compose.yml`.

## Visualization Protocol

When presenting infrastructure status, **generate ASCII diagrams dynamically** based on actual container state:

1. **Collect data**: Run `/infra:status --json --resources`
2. **Analyze state**: Count healthy/unhealthy, identify issues
3. **Render diagram**: Draw topology with health indicators

### Health Indicators
- `●` (green) — healthy/running
- `○` (red) — unhealthy/exited
- `◐` (yellow) — starting/created

### Example Dynamic Output

```
┌─────────────────────────────────────────────────────────────────┐
│                    TMNL Infrastructure Status                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CORE SERVICES                                                  │
│   ┌─────────────┐      ┌─────────────────┐                      │
│   │  postgres   │─────▶│    electric     │                      │
│   │ ● :5432     │      │ ● :3000         │                      │
│   └─────────────┘      └─────────────────┘                      │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────────┐                                           │
│   │ durable-streams │                                           │
│   │ ● :3030         │                                           │
│   └─────────────────┘                                           │
│                                                                  │
│   SUPPORT SERVICES                                               │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐                         │
│   │  nats   │  │  minio  │  │ y-sweet │                         │
│   │ ● :4222 │  │ ○ :9000 │  │ ● :8080 │                         │
│   └─────────┘  └─────────┘  └─────────┘                         │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ ● healthy (5)  ○ unhealthy (1)  CPU: 8%  MEM: 1.2GB            │
└─────────────────────────────────────────────────────────────────┘
```

### Smart Routing

Choose output depth based on state:

| Condition | Response |
|-----------|----------|
| All healthy | Compact topology with summary |
| Unhealthy services | Full diagnostic with logs |
| Resource pressure | Resource-focused view |
| Connectivity issues | Network topology focus |
| Specific service query | Service detail + dependencies |

## Service Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                         TMNL Stack                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐     ┌─────────────────┐     ┌───────────────┐  │
│  │  postgres   │────▶│    electric     │────▶│  search-*     │  │
│  │  (5432)     │     │    (3000)       │     │  (8100-8102)  │  │
│  └─────────────┘     └─────────────────┘     └───────────────┘  │
│         │                                           │            │
│         │            ┌─────────────────┐           │            │
│         └───────────▶│ durable-streams │◀──────────┘            │
│                      │    (3030)       │                        │
│                      └─────────────────┘                        │
│                                                                  │
│  ┌─────────────┐     ┌─────────────────┐     ┌───────────────┐  │
│  │    nats     │     │     minio       │     │   y-sweet     │  │
│  │ (4222/8222) │     │  (9000/9001)    │     │    (8080)     │  │
│  └─────────────┘     └─────────────────┘     └───────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Reference

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| **postgres** | 5432 | PostGIS + TimescaleDB | `pg_isready` |
| **durable-streams** | 3030 | Persistent event streams | HTTP /health |
| **electric** | 3000 | Real-time Postgres sync | HTTP /health |
| **search-cluster-coordinator** | 8100 | Effect Cluster coordinator | TCP |
| **search-cluster-sources** | 8101 | Effect Cluster data sources | TCP |
| **ingestion-cluster** | 8102 | Data ingestion RPC | TCP |
| **nats** | 4222, 8222 | Message broker | HTTP monitoring |
| **minio** | 9000, 9001 | S3 object storage | HTTP /minio/health |
| **y-sweet** | 8080 | Yjs document sync | TCP |

## Service Groups

| Group | Services | Use Case |
|-------|----------|----------|
| **core** | postgres, durable-streams, electric | Essential services |
| **cluster** | search-cluster-*, ingestion-cluster | Effect Cluster nodes |
| **collab** | y-sweet, nats | Real-time collaboration |
| **access** | ssh, ngrok | Remote access |

## Commands

```bash
/infra:up                          # Start core services
/infra:up --group cluster          # Start cluster services
/infra:up --all                    # Start everything
/infra:down                        # Stop core services
/infra:status                      # Check health (table)
/infra:status --json --resources   # Full data for visualization
/infra:logs postgres               # View logs
/infra:rebuild <service>           # Rebuild service
/infra:query "why is X failing"    # Ask infrastructure questions
```

## Dependency Chain

```
postgres (foundation)
    └── electric (requires postgres logical replication)
        └── search-cluster-* (requires electric sync)
            └── ingestion-cluster (requires search cluster)

minio (independent)
    └── y-sweet (stores documents in minio)

durable-streams (independent)
    └── all services can emit events

nats (independent)
    └── real-time messaging between services
```

## Common Issues & Fixes

### Electric Restart Loop
**Symptom**: Electric container constantly restarting
**Cause**: Missing `ELECTRIC_INSECURE=true` for dev mode
**Fix**: Add to docker-compose.yml environment

### Postgres Not Ready
**Symptom**: Services fail waiting for postgres
**Cause**: TimescaleDB extension loading takes time
**Fix**: Wait for `start_period: 30s` to complete

### Search Cluster Connection Refused
**Symptom**: 8100/8101/8102 not accessible
**Cause**: Service not built or health check failing
**Fix**: `/infra:rebuild search-cluster-coordinator`

### NATS WebSocket Issues
**Symptom**: Browser can't connect to NATS
**Cause**: Port 9222 not exposed or config missing
**Fix**: Check `nats-server.conf` has websocket block

## Documentation

### Service Briefings

Detailed documentation for each service:

- [postgres](./briefings/postgres.md) - PostGIS + TimescaleDB
- [durable-streams](./briefings/durable-streams.md) - Event streaming
- [electric](./briefings/electric.md) - Real-time sync
- [search-cluster](./briefings/search-cluster.md) - Effect Cluster search
- [ingestion-cluster](./briefings/ingestion-cluster.md) - Data ingestion
- [nats](./briefings/nats.md) - Message broker
- [minio](./briefings/minio.md) - Object storage
- [y-sweet](./briefings/y-sweet.md) - Yjs sync
- [ngrok](./briefings/ngrok.md) - Remote access

### Journals

Runbooks and troubleshooting guides:

- [troubleshooting](./journals/troubleshooting.md) - Common issues
- [build-issues](./journals/build-issues.md) - Build problems
- [changelog](./journals/changelog.md) - Infrastructure changes

## Quick Diagnostics

```bash
# Check all container status
docker compose ps

# Check specific service health
docker compose ps postgres

# View recent logs
docker compose logs --tail 50 postgres

# Check network connectivity
docker compose exec postgres pg_isready

# Check electric replication
docker compose exec postgres psql -U tmnl -c "SELECT * FROM pg_replication_slots;"
```

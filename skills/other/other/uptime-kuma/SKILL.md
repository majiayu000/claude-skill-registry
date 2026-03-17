---
name: uptime-kuma
description: |
  Manage Uptime Kuma monitoring via the Python API. Use when:
  (1) User asks to add, remove, or list monitors,
  (2) User asks about service uptime or monitoring status,
  (3) User asks to check what's being monitored,
  (4) User deploys a new service and needs monitoring added,
  (5) User mentions "uptime", "monitoring", "health check", or "uptime kuma".
  Uptime Kuma v2 running in Kubernetes, managed via uptime-kuma-api Python library.
author: Claude Code
version: 1.0.0
date: 2026-02-14
---

# Uptime Kuma Monitoring Management

## Overview
- **URL**: `https://uptime.viktorbarzin.me`
- **Internal**: `uptime-kuma.uptime-kuma.svc.cluster.local:80`
- **Image**: `louislam/uptime-kuma:2`
- **Storage**: NFS at `/mnt/main/uptime-kuma` -> `/app/data`
- **API Library**: `uptime-kuma-api` (pip, available via PYTHONPATH)
- **Credentials**: admin / (from `UPTIME_KUMA_PASSWORD` env var)

## Python API Access

### Connection Pattern
```python
import os
from uptime_kuma_api import UptimeKumaApi, MonitorType

api = UptimeKumaApi('https://uptime.viktorbarzin.me')
api.login('admin', os.environ.get('UPTIME_KUMA_PASSWORD', ''))

# ... operations ...

api.disconnect()
```

### Execution
```bash
python3 -c "
import os
from uptime_kuma_api import UptimeKumaApi, MonitorType
api = UptimeKumaApi('https://uptime.viktorbarzin.me')
api.login('admin', os.environ.get('UPTIME_KUMA_PASSWORD', ''))
# ... your code ...
api.disconnect()
"
```

### Common Operations

#### List All Monitors
```python
monitors = api.get_monitors()
for m in monitors:
    print(f'{m["id"]:3d} | {m["name"]:30s} | {m["type"]:15s} | interval={m["interval"]}s')
```

#### Add HTTP Monitor
```python
api.add_monitor(
    type=MonitorType.HTTP,
    name="Service Name",
    url="http://service.namespace.svc.cluster.local",
    interval=120,
    maxretries=2,
)
```

#### Add PING Monitor
```python
api.add_monitor(
    type=MonitorType.PING,
    name="Host Name",
    hostname="10.0.20.1",
    interval=30,
    maxretries=3,
)
```

#### Add PORT Monitor
```python
api.add_monitor(
    type=MonitorType.PORT,
    name="Service Port",
    hostname="service.namespace.svc.cluster.local",
    port=8080,
    interval=120,
    maxretries=2,
)
```

#### Edit Monitor
```python
api.edit_monitor(monitor_id, interval=120, maxretries=2)
```

#### Delete Monitor
```python
api.delete_monitor(monitor_id)
```

#### Pause/Resume Monitor
```python
api.pause_monitor(monitor_id)
api.resume_monitor(monitor_id)
```

## Monitor Types
- `MonitorType.HTTP` — HTTP(S) endpoint check
- `MonitorType.PING` — ICMP ping
- `MonitorType.PORT` — TCP port check
- `MonitorType.POSTGRES` — PostgreSQL connection
- `MonitorType.REDIS` — Redis connection
- `MonitorType.DNS` — DNS resolution check

## Tiered Monitoring System

Monitors use tiered intervals to balance responsiveness with resource usage:

| Tier | Interval | Retries | Use For |
|------|----------|---------|---------|
| **1 - Critical** | 30s | 3 | Core infra (DNS, gateway, ingress, NFS, K8s API, auth, mail) |
| **2 - Important** | 120s | 2 | Actively used services (Nextcloud, Immich, Vaultwarden, etc.) |
| **3 - Standard** | 300s | 1 | Auxiliary/optional services (blog, games, tools) |

### Tier Assignment Guidelines
- **Tier 1**: If it goes down, multiple other services fail or the cluster is unreachable
- **Tier 2**: User-facing services that are actively used daily
- **Tier 3**: Nice-to-have services, tools, dashboards

### When Adding a New Service
Match the tier to the service's DEFCON level from CLAUDE.md:
- DEFCON 1-2 → Tier 1 (30s)
- DEFCON 3-4 → Tier 2 (120s)
- DEFCON 5 → Tier 3 (300s)

## Internal Service URL Pattern
Most K8s services follow: `http://<service-name>.<namespace>.svc.cluster.local:<port>`

Common port is 80. Exceptions:
- Homepage: port 3000
- Ollama: port 11434
- Loki: port 3100 (use `/ready` endpoint)
- Traefik dashboard: port 8080 (use `/dashboard/` path)
- K8s API: `https://10.0.20.100:6443`
- Immich: port 2283 (use `/api/server/ping`)

## Notes
1. Uptime Kuma uses Socket.IO (WebSocket) for its API, not REST
2. The `uptime-kuma-api` Python library wraps Socket.IO
3. Add `time.sleep(0.3)` between bulk operations to avoid overloading
4. Homepage dashboard widget slug: `cluster-internal`
5. Cloudflare-proxied at `uptime.viktorbarzin.me`

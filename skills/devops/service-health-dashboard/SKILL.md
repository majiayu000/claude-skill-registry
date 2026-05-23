---
name: vibe-service-health-dashboard
description: Queries all configured services for health status — uptime, restarts, errors, resources. Use when checking the health of running services.
user-invocable: true
---

# vibe-service-health-dashboard

Know what's running, what's crashed, and what's about to crash.

## When to Use This Skill

- Checking service health after deployment
- Investigating performance or availability issues
- Morning standup health check
- After infrastructure changes

## When NOT to Use This Skill

- No services running (pure library/CLI project)
- Already have a monitoring dashboard (Grafana, Datadog, etc.)
- Development-only local services that don't need monitoring

## Steps

1. **Discover services** — Check for:
   - systemd: `systemctl --user list-units --type=service --state=running`
   - Docker: `docker ps`
   - PM2: `pm2 list`
   - Kubernetes: `kubectl get pods`

2. **For each service, collect**:
   - Status (running/stopped/crashed)
   - Uptime
   - Last restart time and reason
   - Recent error count (from logs)
   - Resource usage (CPU, memory) if available

3. **Identify issues**:
   - Crashed services (not running when expected)
   - High-restart services (restarted >3 times recently)
   - Resource-hungry processes (>80% CPU or memory)
   - Error spikes (more errors than usual)

4. **Provide remediation** commands for each issue

## Output Format

### Service Health Dashboard

**Services**: X running, Y stopped, Z error
**Overall**: HEALTHY / DEGRADED / CRITICAL

| Service | Status | Uptime | Restarts | Errors (1h) | CPU | Memory |
|---------|--------|--------|----------|-------------|-----|--------|
| api | ✓ Running | 3d 4h | 0 | 2 | 15% | 256MB |
| worker | ✗ Crashed | - | 5 | 38 | - | - |

### Issues
1. **worker** crashed — Last error: "OOM killed"
   - Fix: `systemctl --user restart worker` or increase memory limit

### Recommended Actions
1. [Action with command]

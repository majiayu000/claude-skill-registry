---
name: production-monitoring
description: Use when the Production Engineer is assessing production health, setting up monitoring, defining health checks, evaluating SLA compliance, or responding to incidents. Activates when discussing production readiness, system health, alerting, or incident response.
version: 1.0.0
---

# Production Monitoring Expertise

## When This Applies

Apply this guidance when:
- Assessing whether a release is production-ready
- Setting up or reviewing health checks
- Evaluating system stability after a deployment
- Defining monitoring and alerting requirements
- Responding to production incidents

## Health Check Design

### Application Health Endpoint

Every service should expose a health endpoint:

```
GET /health
Response:
{
  "status": "healthy" | "degraded" | "unhealthy",
  "version": "1.2.3",
  "timestamp": "2026-02-28T10:00:00Z",
  "checks": {
    "database": "healthy",
    "cache": "healthy",
    "external_api": "degraded"
  }
}
```

### Health Check Levels

| Level | What to Check | Frequency |
|-------|--------------|-----------|
| **Liveness** | Process is running | Every 10s |
| **Readiness** | Can handle requests | Every 30s |
| **Deep health** | All dependencies ok | Every 60s |

## Key Metrics to Monitor

### The Four Golden Signals

1. **Latency** — Response time distribution (p50, p95, p99)
2. **Traffic** — Request rate (requests/second)
3. **Errors** — Error rate (5xx responses / total)
4. **Saturation** — Resource utilization (CPU, memory, disk, connections)

### Service-Level Indicators (SLIs)

| SLI | Target | Measurement |
|-----|--------|-------------|
| Availability | 99.9% | Successful responses / total |
| Latency | p95 < 200ms | Response time percentiles |
| Error rate | < 0.1% | Error responses / total |
| Throughput | > N req/s | Requests per second |

## Post-Deployment Verification

After merging to main and deploying:

### Immediate (0-5 minutes)
- [ ] Health endpoint returns `healthy`
- [ ] No error spike in logs
- [ ] Response times are within normal range
- [ ] Key user flows work (manual smoke test)

### Short-term (5-30 minutes)
- [ ] Error rate is stable or improving
- [ ] No memory leaks (memory usage stable)
- [ ] No connection pool exhaustion
- [ ] No increase in support tickets or alerts

### Medium-term (30 min - 2 hours)
- [ ] Performance metrics are within historical norms
- [ ] Background jobs are processing normally
- [ ] No data integrity issues reported
- [ ] All scheduled tasks ran successfully

## Alerting Guidelines

### Alert Severity

| Severity | Condition | Response |
|----------|-----------|----------|
| **Critical** | Service down, data loss risk | Page on-call, immediate action |
| **Warning** | Degraded performance, elevated errors | Investigate within 30 min |
| **Info** | Anomaly detected, approaching threshold | Review during business hours |

### Alert Design Rules

1. **Actionable** — Every alert should have a clear response action
2. **No noise** — If an alert fires > 5 times/day without action needed, fix or remove it
3. **Contextual** — Include what's wrong, what threshold was breached, and where to look
4. **Escalation** — If not acknowledged within N minutes, escalate to next level

## Incident Documentation

After any production incident, document in `reports/INCIDENT_<YYYYMMDD>_<NNN>.md`:

```markdown
# Incident Report — <date>

## Summary
<One-line description of what happened>

## Timeline
- HH:MM — Issue detected
- HH:MM — Investigation started
- HH:MM — Root cause identified
- HH:MM — Fix applied
- HH:MM — Verified resolved

## Impact
- Duration: X minutes
- Users affected: N
- Data impact: None / Describe

## Root Cause
<What caused the issue>

## Resolution
<How it was fixed>

## Prevention
<What changes will prevent recurrence>
```

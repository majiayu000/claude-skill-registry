---
name: infra-operations
description: "Perform routine infrastructure maintenance: health checks, log rotation, certificate renewal, dependency updates, database maintenance, cache management, and capacity monitoring. Use when the user says 'check system health', 'rotate logs', 'update dependencies', 'check SSL certificates', 'database maintenance', 'clear cache', 'disk space', 'check service status', or 'infrastructure checkup'. Also triggers on 'infrastructure operations', 'ops maintenance', 'system health', 'capacity planning', 'service monitoring', 'operational readiness', 'server maintenance', or 'infrastructure audit'."
version: 1.0.0
---

# Infrastructure Operations Skill

## Purpose

Infrastructure doesn't maintain itself. Unattended: disks fill, certificates expire, dependencies accumulate vulnerabilities, caches grow stale. This skill provides structured procedures for routine maintenance that prevents incidents.

The best incident is the one that never happens. Routine maintenance is cheaper than emergency response by orders of magnitude. A 15-minute weekly check prevents the 3 AM page.

## When to Activate

- Scheduled infrastructure checkups (daily, weekly, monthly)
- Pre-deployment readiness verification
- Post-incident recovery and verification
- Dependency update cycles
- SSL/TLS certificate management
- Database vacuum, analyze, and reindex operations
- Log rotation and archival
- Cache size and hit-rate review
- Capacity planning and growth projection

## Core Workflow

### Step 1: Assess Scope

Determine what needs maintenance:

- **Full checkup**: All systems, all checks. Monthly cadence.
- **Targeted maintenance**: Specific subsystem (database, certs, deps). As needed.
- **Pre-deploy verification**: Services healthy, resources available, rollback path clear.
- **Post-incident**: Verify systems recovered, check for collateral damage.

### Step 2: Run Health Checks

Use `scripts/health_check.sh` for automated system-level checks, or run the health check framework manually:

```
INFRASTRUCTURE HEALTH CHECK
===========================
System Resources:
- [ ] Disk usage < 80% on all volumes
- [ ] Memory usage < 85% sustained
- [ ] CPU usage < 70% sustained
- [ ] Swap usage < 10%

Services:
- [ ] All health endpoints responding
- [ ] DB connections within pool limits
- [ ] Cache hit rate > 80%
- [ ] Queue depth within normal range

Security:
- [ ] SSL certs > 30 days from expiry
- [ ] No critical dependency vulnerabilities
- [ ] Secrets rotation within policy
- [ ] Backup verification (last < 24h)

Data:
- [ ] DB size within expected growth
- [ ] Log volume within normal range
- [ ] Temp files cleaned
- [ ] Orphaned resources identified
```

See `references/health-check-patterns.md` for platform-specific commands and thresholds.

### Step 3: Execute Maintenance

Follow the appropriate runbook from `references/maintenance-runbooks.md`:

- **Dependency Updates**: audit, categorize, update, test, deploy (with rollback plan)
- **Database Maintenance**: vacuum, analyze, reindex, connection pool check
- **Log Management**: rotation, archival, cleanup, retention enforcement
- **Cache Operations**: size check, hit rate analysis, selective invalidation, cold start plan
- **Certificate Management**: expiry check, renewal, verification, distribution
- **Cleanup**: temp files, orphaned uploads, dangling Docker images, stale branches

Every runbook follows the same structure: pre-conditions, step-by-step procedure, verification, rollback, estimated time.

### Step 4: Verify and Report

After maintenance:

1. Re-run health checks to confirm improvement
2. Record what was done and any anomalies found
3. Update maintenance log with date, actions, and results
4. Schedule follow-up if issues were deferred

## Operational Cadence

### Daily

- Health endpoint checks (automated)
- Error rate monitoring (dashboards)
- Disk usage on high-churn volumes
- Backup completion verification

### Weekly

- Dependency vulnerability scan (`npm audit`, `pip audit`, `trivy`)
- Log volume review (unexpected growth?)
- Backup restoration test (sample, not full)
- Queue depth and dead letter queue review

### Monthly

- Full health check (all systems, all checks)
- SSL certificate expiry scan (everything, not just the ones you remember)
- Capacity review and growth projection (see `references/capacity-planning.md`)
- Dependency updates (patch and minor)
- Database maintenance (vacuum, analyze, reindex)

### Quarterly

- Security audit (secrets rotation, access review, firewall rules)
- Cost review (right-sizing, reserved instances, idle resources)
- Architecture review (bottlenecks, scaling limits, tech debt)
- Disaster recovery test (full restore, failover, runbook validation)
- Major dependency updates (with thorough testing)

## Capacity Planning

Reference `references/capacity-planning.md` for detailed methods. Summary:

- **Disk**: Measure weekly growth rate over 4 weeks, project days until full. Action at 70% (plan), 80% (warn), 90% (act).
- **Database**: Track table sizes over time, estimate index overhead, size connection pools to peak load plus headroom.
- **Traffic/Compute**: Analyze peak vs average, review p95/p99 latencies, understand scaling trigger history.
- **Cost**: Right-size instances based on utilization, identify idle resources, evaluate reserved vs on-demand.

The goal: never be surprised by resource exhaustion. If you can project it 30 days out, you can plan instead of panic.

## Maintenance Report Template

```
MAINTENANCE REPORT
==================
Date: [timestamp]
Operator: [who]
Type: [scheduled / pre-deploy / post-incident]

Checks Performed:
- [check]: [PASS/WARN/FAIL] [details]
- [check]: [PASS/WARN/FAIL] [details]

Actions Taken:
- [action]: [result]
- [action]: [result]

Issues Found:
- [issue]: [severity] [action taken or deferred]

Follow-Up Required:
- [ ] [task] by [date]

Summary: X pass, Y warn, Z fail
```

## Gotchas

**VACUUM FULL locks the table.** Use `VACUUM` (without `FULL`) for routine maintenance. `VACUUM FULL` rewrites the entire table and requires an exclusive lock. Schedule `VACUUM FULL` only during true maintenance windows with application downtime.

**Never update dependencies and deploy simultaneously.** Update, test, then deploy as separate steps. If something breaks, you need to know whether it was the dependency update or the deployment that caused it.

**Log rotation race conditions.** Rotating a log file while the application writes to it requires coordination. Most applications need a signal (SIGHUP) or graceful reload to reopen log file handles after rotation. Without this, the app writes to the old (now rotated) file descriptor.

**Certificate renewal automation fails silently.** Certbot and similar tools fail if DNS or HTTP challenges are misconfigured. Always verify the certificate after renewal: check the expiry date, the subject, and the chain. Automated renewal without automated verification is a time bomb.

**`df` shows filesystem usage, not inode usage.** An inode-exhausted filesystem appears to have free space but cannot create new files. Check with `df -i`. Common cause: millions of tiny files (session files, cache fragments, mail queue).

**`docker system prune` without `--volumes` preserves volumes.** With `--volumes` it deletes database data. Always specify exactly what to prune: `docker image prune`, `docker container prune`, `docker network prune`. Only use `--volumes` when you are certain no persistent data lives in Docker volumes.

**A backup that has never been restored is not a backup.** It is a hope. Test restores regularly. A backup system that runs without errors does not guarantee the data is complete or usable. Verify with actual restoration to a test environment.

**Inode exhaustion is invisible until it isn't.** Standard monitoring often tracks only disk space percentage. Add inode monitoring. When inodes run out, the system behaves as if the disk is full even though `df -h` shows available space.

**Connection pool exhaustion looks like the database is down.** When all pool slots are occupied by idle or leaked connections, new requests fail with connection timeouts. The database itself is healthy. Check `pg_stat_activity` for idle connections, not just total connection count.

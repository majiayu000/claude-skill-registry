---
name: Runbooks & Ops
description: Comprehensive guide to creating operational runbooks including incident response, deployment procedures, troubleshooting guides, and on-call playbooks
---

# Runbooks & Ops

## Overview

Runbooks are documented procedures for operational tasks, incident response, and troubleshooting. Essential for maintaining reliable systems and enabling team members to handle issues independently.

## Why This Matters

- **Faster resolution**: Step-by-step guides reduce MTTR
- **Consistency**: Same procedure every time
- **Knowledge sharing**: Reduce bus factor
- **Onboarding**: New team members can handle ops tasks

---

## Runbook Structure

### Standard Template

```markdown
# [Runbook Title]

**Last Updated:** [Date]
**Owner:** [Team/Person]
**Severity:** [P0/P1/P2/P3]

## Overview
Brief description of what this runbook covers.

## When to Use
Specific scenarios when this runbook applies.

## Prerequisites
- Access required (AWS console, database, etc.)
- Tools needed
- Knowledge required

## Procedure

### Step 1: [Action]
Detailed instructions with commands.

### Step 2: [Action]
Expected output and what to do if different.

### Step 3: [Action]
Verification steps.

## Verification
How to confirm the issue is resolved.

## Rollback
How to undo changes if needed.

## Escalation
When to escalate and to whom.

## Related Runbooks
Links to related procedures.
```

---

## Incident Response Runbooks

### Service Down

```markdown
# Runbook: Service Down

**Severity:** P0
**Owner:** Platform Team

## Symptoms
- Health check failing
- 5xx errors spiking
- Users reporting "service unavailable"

## Immediate Actions

### 1. Acknowledge Alert
```bash
# Acknowledge in PagerDuty
pd incident acknowledge <incident-id>
```

### 2. Check Service Status
```bash
# Check if service is running
kubectl get pods -n production

# Check recent deployments
kubectl rollout history deployment/api -n production

# Check logs
kubectl logs -f deployment/api -n production --tail=100
```

### 3. Quick Health Checks
```bash
# Database connectivity
psql -h db.example.com -U app -c "SELECT 1"

# Redis connectivity
redis-cli -h redis.example.com ping

# External API
curl https://api.partner.com/health
```

## Common Causes & Solutions

### Cause 1: Recent Deployment
```bash
# Rollback to previous version
kubectl rollout undo deployment/api -n production

# Verify rollback
kubectl rollout status deployment/api -n production
```

### Cause 2: Database Connection Pool Exhausted
```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Kill idle connections
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' 
AND state_change < now() - interval '5 minutes';

# Restart application to reset pool
kubectl rollout restart deployment/api -n production
```

### Cause 3: Memory Leak / OOM
```bash
# Check memory usage
kubectl top pods -n production

# Restart affected pods
kubectl delete pod <pod-name> -n production
```

## Verification
- [ ] Health check returns 200
- [ ] Error rate < 0.1%
- [ ] Response time < 200ms
- [ ] No alerts firing

## Communication
1. Update incident channel: "Investigating service down"
2. Post status page update
3. When resolved: "Service restored. Root cause: [X]"

## Post-Incident
- [ ] Write incident report
- [ ] Schedule post-mortem
- [ ] Update runbook if needed
```

---

## Deployment Runbooks

### Production Deployment

```markdown
# Runbook: Production Deployment

**Owner:** DevOps Team
**Frequency:** As needed

## Prerequisites
- [ ] Code reviewed and approved
- [ ] Tests passing in CI
- [ ] Staging deployment successful
- [ ] Change request approved
- [ ] Deployment window scheduled

## Pre-Deployment

### 1. Notify Team
```bash
# Post in Slack
"🚀 Production deployment starting
Service: API
Version: v1.2.3
ETA: 15 minutes
Deployer: @john"
```

### 2. Backup Database
```bash
# Create backup
pg_dump -h db.example.com -U app production > backup_$(date +%Y%m%d_%H%M%S).sql

# Verify backup
ls -lh backup_*.sql
```

### 3. Enable Maintenance Mode (if needed)
```bash
# Set maintenance flag
kubectl set env deployment/api MAINTENANCE_MODE=true -n production
```

## Deployment

### 1. Deploy New Version
```bash
# Update image tag
kubectl set image deployment/api api=myapp:v1.2.3 -n production

# Watch rollout
kubectl rollout status deployment/api -n production
```

### 2. Monitor Metrics
```
Watch dashboards:
- Error rate
- Response time
- CPU/Memory
- Database connections
```

### 3. Smoke Tests
```bash
# Health check
curl https://api.example.com/health

# Critical endpoints
curl https://api.example.com/api/users/me

# Database connectivity
curl https://api.example.com/api/status
```

## Post-Deployment

### 1. Verify Success
- [ ] All pods running
- [ ] Health checks passing
- [ ] Error rate normal
- [ ] No alerts firing

### 2. Disable Maintenance Mode
```bash
kubectl set env deployment/api MAINTENANCE_MODE=false -n production
```

### 3. Notify Team
```bash
"✅ Deployment complete
Service: API
Version: v1.2.3
Status: Success
No issues detected"
```

## Rollback Procedure

### If Issues Detected
```bash
# Rollback to previous version
kubectl rollout undo deployment/api -n production

# Verify rollback
kubectl rollout status deployment/api -n production

# Notify team
"⚠️ Deployment rolled back
Reason: [describe issue]
Investigating..."
```

## Escalation
If rollback doesn't resolve:
1. Page on-call engineer
2. Notify engineering manager
3. Consider full rollback (database + code)
```

---

## Troubleshooting Runbooks

### High Database CPU

```markdown
# Runbook: High Database CPU

**Severity:** P1
**Owner:** Database Team

## Symptoms
- Database CPU > 80%
- Slow query warnings
- Application timeouts

## Investigation

### 1. Check Active Queries
```sql
-- Long-running queries
SELECT pid, now() - query_start as duration, query 
FROM pg_stat_activity 
WHERE state = 'active' 
ORDER BY duration DESC 
LIMIT 10;
```

### 2. Check Query Stats
```sql
-- Most expensive queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

### 3. Check Locks
```sql
-- Blocked queries
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query,
       blocking_activity.query AS blocking_query
FROM pg_locks blocked_locks
JOIN pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## Solutions

### Solution 1: Kill Long-Running Query
```sql
-- Terminate specific query
SELECT pg_terminate_backend(<pid>);
```

### Solution 2: Add Missing Index
```sql
-- Check missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public'
AND correlation < 0.1;

-- Add index (if safe)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Solution 3: Scale Database
```bash
# Increase instance size (AWS RDS)
aws rds modify-db-instance \
    --db-instance-identifier prod-db \
    --db-instance-class db.r5.2xlarge \
    --apply-immediately
```

## Prevention
- [ ] Review slow query log daily
- [ ] Add indexes for common queries
- [ ] Implement query timeout
- [ ] Set up connection pooling
```

---

## On-Call Playbooks

### On-Call Checklist

```markdown
# On-Call Playbook

## Before Your Shift

- [ ] Test PagerDuty notifications
- [ ] Verify VPN access
- [ ] Check laptop battery
- [ ] Review recent incidents
- [ ] Read handoff notes
- [ ] Join #incidents Slack channel

## During Your Shift

### When Alert Fires

1. **Acknowledge** (within 5 minutes)
   ```bash
   pd incident acknowledge <id>
   ```

2. **Assess Severity**
   - P0: Service down, data loss
   - P1: Degraded performance
   - P2: Non-critical issue
   - P3: Monitoring only

3. **Communicate**
   ```
   Post in #incidents:
   "🚨 P0: API service down
   Investigating...
   ETA: 15 minutes"
   ```

4. **Follow Runbook**
   - Find relevant runbook
   - Execute steps
   - Document actions

5. **Escalate if Needed**
   - Can't resolve in 30 min → Escalate
   - Outside expertise → Page specialist
   - Critical impact → Page manager

### After Resolution

1. **Verify Fix**
   - Check metrics
   - Run smoke tests
   - Monitor for 15 minutes

2. **Communicate**
   ```
   "✅ Resolved: API service restored
   Root cause: Database connection pool exhausted
   Fix: Restarted application
   Post-mortem: Tomorrow 2pm"
   ```

3. **Document**
   - Update incident ticket
   - Note actions taken
   - Identify improvements

## After Your Shift

- [ ] Write handoff notes
- [ ] Update runbooks if needed
- [ ] Schedule post-mortems
- [ ] Review incident metrics
```

---

## Maintenance Runbooks

### Database Backup

```markdown
# Runbook: Database Backup

**Frequency:** Daily (automated)
**Owner:** Database Team

## Automated Backup
```bash
#!/bin/bash
# /scripts/backup_db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.sql"

# Create backup
pg_dump -h db.example.com -U app production > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Upload to S3
aws s3 cp ${BACKUP_FILE}.gz s3://backups/database/

# Cleanup old backups (keep 30 days)
find . -name "backup_*.sql.gz" -mtime +30 -delete

# Verify backup
if [ $? -eq 0 ]; then
    echo "✅ Backup successful: ${BACKUP_FILE}.gz"
else
    echo "❌ Backup failed"
    # Alert team
    curl -X POST https://hooks.slack.com/... -d "Backup failed"
fi
```

## Manual Backup (Emergency)
```bash
# Create backup
pg_dump -h db.example.com -U app production > emergency_backup.sql

# Verify
ls -lh emergency_backup.sql
```

## Restore Procedure
```bash
# Download backup
aws s3 cp s3://backups/database/backup_20240116.sql.gz .

# Decompress
gunzip backup_20240116.sql.gz

# Restore
psql -h db.example.com -U app production < backup_20240116.sql

# Verify
psql -h db.example.com -U app -c "SELECT count(*) FROM users"
```
```

---

## Best Practices

### 1. Keep Runbooks Updated
```
✓ Review quarterly
✓ Update after incidents
✓ Version control (Git)
✓ Include last updated date
```

### 2. Make Them Actionable
```
✓ Step-by-step instructions
✓ Copy-paste commands
✓ Expected outputs
✓ What to do if different
```

### 3. Include Context
```
✓ When to use
✓ Why each step matters
✓ Common pitfalls
✓ Related runbooks
```

### 4. Test Regularly
```
✓ Run through procedures
✓ Verify commands work
✓ Update outdated steps
✓ Practice in staging
```

---

## Runbook Categories

```
Incident Response:
- Service down
- High error rate
- Performance degradation
- Security incident

Deployment:
- Production deployment
- Rollback procedure
- Database migration
- Feature flag toggle

Troubleshooting:
- High CPU/Memory
- Slow queries
- Connection issues
- Cache problems

Maintenance:
- Database backup
- Log rotation
- Certificate renewal
- Dependency updates

On-Call:
- Shift checklist
- Escalation paths
- Communication templates
- Post-incident tasks
```

---

## Summary

**Runbooks:** Documented operational procedures

**Key Components:**
- Clear steps
- Commands to run
- Expected outputs
- Verification
- Rollback
- Escalation

**Types:**
- Incident response
- Deployment
- Troubleshooting
- Maintenance
- On-call playbooks

**Best Practices:**
- Keep updated
- Make actionable
- Include context
- Test regularly

**Benefits:**
- Faster resolution
- Consistency
- Knowledge sharing
- Reduced stress

---
name: runbook-creation
description: Create operational runbooks, playbooks, standard operating procedures (SOPs), and incident response guides. Use when documenting operational procedures, on-call guides, or incident response processes.
---

# Runbook Creation

## Overview

Create comprehensive operational runbooks that provide step-by-step procedures for common operational tasks, incident response, and system maintenance.

## When to Use

- Incident response procedures
- Standard operating procedures (SOPs)
- On-call playbooks
- System maintenance guides
- Disaster recovery procedures
- Deployment runbooks
- Escalation procedures
- Service restoration guides

## Incident Response Runbook Template

```markdown
# Incident Response Runbook

## Quick Reference

**Severity Levels:**
- P0 (Critical): Complete outage, data loss, security breach
- P1 (High): Major feature down, significant user impact
- P2 (Medium): Minor feature degradation, limited user impact
- P3 (Low): Cosmetic issues, minimal user impact

**Response Times:**
- P0: Immediate (24/7)
- P1: 15 minutes (business hours), 1 hour (after hours)
- P2: 4 hours (business hours)
- P3: Next business day

**Escalation Contacts:**
- On-call Engineer: PagerDuty rotation
- Engineering Manager: +1-555-0100
- VP Engineering: +1-555-0101
- CTO: +1-555-0102

## Table of Contents

1. [Service Down](#service-down)
2. [Database Issues](#database-issues)
3. [High CPU/Memory Usage](#high-cpu-memory-usage)
4. [API Performance Degradation](#api-performance-degradation)
5. [Security Incidents](#security-incidents)
6. [Data Loss Recovery](#data-loss-recovery)
7. [Rollback Procedures](#rollback-procedures)

---

## Service Down

### Symptoms
- Health check endpoint returning 500 errors
- Users unable to access application
- Load balancer showing all instances unhealthy
- Alerts: `service_down`, `health_check_failed`

### Severity: P0 (Critical)

### Initial Response (5 minutes)

1. **Acknowledge the incident**
   ```bash
   # Acknowledge in PagerDuty
   # Post in #incidents Slack channel
   ```

2. **Create incident channel**
   ```
   Create Slack channel: #incident-YYYY-MM-DD-service-down
   Post incident details and status updates
   ```

3. **Assess impact**
   ```bash
   # Check service status
   kubectl get pods -n production

   # Check recent deployments
   kubectl rollout history deployment/api -n production

   # Check logs
   kubectl logs -f deployment/api -n production --tail=100
   ```

### Investigation Steps

#### Check Application Health

```bash
# 1. Check pod status
kubectl get pods -n production -l app=api

# Expected output: All pods Running
# NAME                   READY   STATUS    RESTARTS   AGE
# api-7d8c9f5b6d-4xk2p   1/1     Running   0          2h
# api-7d8c9f5b6d-7nm8r   1/1     Running   0          2h

# 2. Check pod logs for errors
kubectl logs -f deployment/api -n production --tail=100 | grep -i error

# 3. Check application endpoints
curl -v https://api.example.com/health
curl -v https://api.example.com/api/v1/status

# 4. Check database connectivity
kubectl exec -it deployment/api -n production -- sh
psql $DATABASE_URL -c "SELECT 1"
```

#### Check Infrastructure

```bash
# 1. Check load balancer
aws elb describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State]' \
  --output table

# 2. Check DNS resolution
dig api.example.com
nslookup api.example.com

# 3. Check SSL certificates
echo | openssl s_client -connect api.example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 4. Check network connectivity
kubectl exec -it deployment/api -n production -- \
  curl -v https://database.example.com:5432
```

#### Check Database

```bash
# 1. Check database connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity"

# 2. Check for locks
psql $DATABASE_URL -c "
  SELECT pid, usename, pg_blocking_pids(pid) as blocked_by, query
  FROM pg_stat_activity
  WHERE cardinality(pg_blocking_pids(pid)) > 0
"

# 3. Check database size
psql $DATABASE_URL -c "
  SELECT pg_size_pretty(pg_database_size(current_database()))
"

# 4. Check long-running queries
psql $DATABASE_URL -c "
  SELECT pid, now() - query_start as duration, query
  FROM pg_stat_activity
  WHERE state = 'active'
  ORDER BY duration DESC
  LIMIT 10
"
```

### Resolution Steps

#### Option 1: Restart Pods (Quick Fix)

```bash
# Restart all pods (rolling restart)
kubectl rollout restart deployment/api -n production

# Watch restart progress
kubectl rollout status deployment/api -n production

# Verify pods are healthy
kubectl get pods -n production -l app=api
```

#### Option 2: Scale Up (If Overload)

```bash
# Check current replicas
kubectl get deployment api -n production

# Scale up
kubectl scale deployment/api -n production --replicas=10

# Watch scaling
kubectl get pods -n production -l app=api -w
```

#### Option 3: Rollback (If Bad Deploy)

```bash
# Check deployment history
kubectl rollout history deployment/api -n production

# Rollback to previous version
kubectl rollout undo deployment/api -n production

# Rollback to specific revision
kubectl rollout undo deployment/api -n production --to-revision=5

# Verify rollback
kubectl rollout status deployment/api -n production
```

#### Option 4: Database Connection Reset

```bash
# If database connection pool exhausted
kubectl exec -it deployment/api -n production -- sh
kill -HUP 1  # Reload process, reset connections

# Or restart database connection pool
psql $DATABASE_URL -c "SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE application_name = 'api'
  AND state = 'idle'"
```

### Verification

```bash
# 1. Check health endpoint
curl https://api.example.com/health
# Expected: {"status": "healthy"}

# 2. Check API endpoints
curl https://api.example.com/api/v1/users
# Expected: Valid JSON response

# 3. Check metrics
# Visit https://grafana.example.com
# Verify:
# - Error rate < 1%
# - Response time < 500ms
# - All pods healthy

# 4. Check logs for errors
kubectl logs deployment/api -n production --tail=100 | grep -i error
# Expected: No new errors
```

### Communication

**Initial Update (within 5 minutes):**
```
🚨 INCIDENT: Service Down

Status: Investigating
Severity: P0
Impact: All users unable to access application
Start Time: 2025-01-15 14:30 UTC

We are investigating reports of users unable to access the application.
Our team is working to identify the root cause.

Next update in 15 minutes.
```

**Progress Update (every 15 minutes):**
```
🔍 UPDATE: Service Down

Status: Identified
Root Cause: Database connection pool exhausted
Action: Restarting application pods
ETA: 5 minutes

We have identified the issue and are implementing a fix.
```

**Resolution Update:**
```
✅ RESOLVED: Service Down

Status: Resolved
Resolution: Restarted application pods, reset database connections
Duration: 23 minutes

The service is now fully operational. We are monitoring closely
and will conduct a post-mortem to prevent future occurrences.
```

### Post-Incident

1. **Create post-mortem document**
   - Timeline of events
   - Root cause analysis
   - Action items to prevent recurrence

2. **Update monitoring**
   - Add alerts for this scenario
   - Improve detection time

3. **Update runbook**
   - Document any new findings
   - Add shortcuts for faster resolution

---

## Database Issues

### High Connection Count

**Symptoms:**
- Database rejecting new connections
- Error: "too many connections"
- Alert: `db_connections_high`

**Quick Fix:**

```bash
# 1. Check connection count
psql $DATABASE_URL -c "
  SELECT count(*), application_name
  FROM pg_stat_activity
  GROUP BY application_name
"

# 2. Kill idle connections
psql $DATABASE_URL -c "
  SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
  WHERE state = 'idle'
  AND query_start < now() - interval '10 minutes'
"

# 3. Restart connection pools
kubectl rollout restart deployment/api -n production
```

### Slow Queries

**Symptoms:**
- API response times > 5 seconds
- Database CPU at 100%
- Alert: `slow_query_detected`

**Investigation:**

```sql
-- Find slow queries
SELECT
  pid,
  now() - query_start as duration,
  query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC
LIMIT 10;

-- Check for missing indexes
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_scan DESC
LIMIT 10;

-- Kill long-running query (if needed)
SELECT pg_terminate_backend(12345);  -- Replace with actual PID
```

---

## High CPU/Memory Usage

### Symptoms
- Pods being OOMKilled
- Response times increasing
- Alert: `high_memory_usage`, `high_cpu_usage`

### Investigation

```bash
# 1. Check pod resources
kubectl top pods -n production

# 2. Check resource limits
kubectl describe pod <pod-name> -n production | grep -A 5 Limits

# 3. Check for memory leaks
kubectl logs deployment/api -n production | grep -i "out of memory"

# 4. Profile application (if needed)
kubectl exec -it <pod-name> -n production -- sh
# Run profiler: node --inspect, py-spy, etc.
```

### Resolution

```bash
# Option 1: Increase resources
kubectl set resources deployment/api -n production \
  --limits=cpu=2000m,memory=4Gi \
  --requests=cpu=1000m,memory=2Gi

# Option 2: Scale horizontally
kubectl scale deployment/api -n production --replicas=6

# Option 3: Restart problematic pods
kubectl delete pod <pod-name> -n production
```

---

## Rollback Procedures

### Application Rollback

```bash
# 1. List deployment history
kubectl rollout history deployment/api -n production

# 2. Check specific revision
kubectl rollout history deployment/api -n production --revision=5

# 3. Rollback to previous
kubectl rollout undo deployment/api -n production

# 4. Rollback to specific revision
kubectl rollout undo deployment/api -n production --to-revision=5

# 5. Verify rollback
kubectl rollout status deployment/api -n production
kubectl get pods -n production
```

### Database Rollback

```bash
# 1. Check migration status
npm run db:migrate:status

# 2. Rollback last migration
npm run db:migrate:undo

# 3. Rollback to specific migration
npm run db:migrate:undo --to 20250115120000-migration-name

# 4. Verify database state
psql $DATABASE_URL -c "\dt"
```

---

## Escalation Path

1. **Level 1 - On-call Engineer** (You)
   - Initial response and investigation
   - Attempt standard fixes from runbook

2. **Level 2 - Senior Engineers**
   - Escalate if not resolved in 30 minutes
   - Escalate if issue is complex/unclear
   - Contact via PagerDuty or Slack

3. **Level 3 - Engineering Manager**
   - Escalate if not resolved in 1 hour
   - Escalate if cross-team coordination needed

4. **Level 4 - VP Engineering / CTO**
   - Escalate for P0 incidents > 2 hours
   - Escalate for security breaches
   - Escalate for data loss

---

## Useful Commands

```bash
# Kubernetes
kubectl get pods -n production
kubectl logs -f <pod-name> -n production
kubectl describe pod <pod-name> -n production
kubectl exec -it <pod-name> -n production -- sh
kubectl top pods -n production

# Database
psql $DATABASE_URL -c "SELECT version()"
psql $DATABASE_URL -c "SELECT * FROM pg_stat_activity"

# AWS
aws ecs list-tasks --cluster production
aws rds describe-db-instances
aws cloudwatch get-metric-statistics ...

# Monitoring URLs
# Grafana: https://grafana.example.com
# Datadog: https://app.datadoghq.com
# PagerDuty: https://example.pagerduty.com
# Status Page: https://status.example.com
```
```

## Best Practices

### ✅ DO
- Include quick reference section at top
- Provide exact commands to run
- Document expected outputs
- Include verification steps
- Add communication templates
- Define severity levels clearly
- Document escalation paths
- Include useful links and contacts
- Keep runbooks up-to-date
- Test runbooks regularly
- Include screenshots/diagrams
- Document common gotchas

### ❌ DON'T
- Use vague instructions
- Skip verification steps
- Forget to document prerequisites
- Assume knowledge of tools
- Skip communication guidelines
- Forget to update after incidents

## Resources

- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Google SRE Book](https://sre.google/books/)
- [Atlassian Incident Handbook](https://www.atlassian.com/incident-management/handbook)

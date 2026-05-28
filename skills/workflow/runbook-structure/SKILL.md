---
name: runbooks-structure
description: Use when creating structured operational runbooks for human operators. Covers runbook organization, documentation patterns, and best practices for clear operational procedures.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Runbooks - Structure

Creating clear, actionable runbooks for operational tasks, maintenance, and troubleshooting.

## What is a Runbook?

A runbook is step-by-step documentation for operational tasks:

- **Troubleshooting** - Diagnosing and fixing issues
- **Incident Response** - Handling production incidents
- **Maintenance** - Routine operational tasks
- **On-Call** - Reference for on-call engineers

## Basic Runbook Structure

### Minimum Viable Runbook

```markdown
# Service Name: Task/Issue

## Overview
Brief description of what this runbook covers.

## Prerequisites
- Required access/permissions
- Tools needed
- Knowledge required

## Steps

### 1. First Step
Detailed instructions for first action.

### 2. Second Step
Detailed instructions for second action.

## Validation
How to verify the task was completed successfully.

## Rollback (if applicable)
How to undo the changes if needed.
```

## Comprehensive Runbook Template

```markdown
# [Service]: [Task/Issue Title]

**Last Updated:** 2025-01-15
**Owner:** Platform Team
**Severity:** High/Medium/Low
**Estimated Time:** 15 minutes

## Overview

Brief description of the problem or task this runbook addresses.

## When to Use This Runbook

- Alert fired: `high_cpu_usage`
- Customer report: slow response times
- Scheduled maintenance window

## Prerequisites

- [ ] VPN access to production network
- [ ] AWS console access (read/write)
- [ ] kubectl configured for production cluster
- [ ] Slack access to #incidents channel

## Context

### Architecture Overview
Brief explanation of relevant system architecture.

### Common Causes
- Database connection pool exhaustion
- Memory leaks in worker processes
- Third-party API rate limiting

## Diagnosis Steps

### 1. Check System Health

```bash
# Check pod status
kubectl get pods -n production

# Expected output: All pods Running
```

**Decision Point:** If pods are CrashLooping, proceed to step 2. Otherwise, skip to step 3.

### 2. Check Application Logs

```bash
# View recent logs
kubectl logs -n production deployment/api-server --tail=100
```

**Look for:**

- Error messages containing "connection refused"
- Stack traces
- Repeated warnings

### 3. Check Database Performance

```bash
# Connect to RDS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=prod-db
```

## Resolution Steps

### Option A: Restart Services (Quick Fix)

1. **Drain pod gracefully:**

   ```bash
   kubectl drain pod/api-server-abc123 --ignore-daemonsets
   ```

2. **Verify new pod is healthy:**

   ```bash
   kubectl get pods -n production | grep api-server
   ```

3. **Monitor for 5 minutes:**
   Check Datadog dashboard for error rates.

### Option B: Scale Resources (Long-term Fix)

1. **Increase database connection pool:**

   ```bash
   # Edit configmap
   kubectl edit configmap app-config -n production

   # Change: DB_POOL_SIZE: "10"
   # To: DB_POOL_SIZE: "20"
   ```

2. **Restart deployment:**

   ```bash
   kubectl rollout restart deployment/api-server -n production
   ```

3. **Monitor rollout:**

   ```bash
   kubectl rollout status deployment/api-server -n production
   ```

## Validation

- [ ] All pods in Running state: `kubectl get pods -n production`
- [ ] Error rate < 1%: Check Datadog dashboard
- [ ] Response time < 200ms p95: Check Datadog dashboard
- [ ] No alerts firing: Check PagerDuty

## Rollback

If the fix causes issues:

```bash
# Rollback to previous version
kubectl rollout undo deployment/api-server -n production

# Verify rollback
kubectl rollout status deployment/api-server -n production
```

## Follow-up Actions

- [ ] Create post-mortem ticket: JIRA-1234
- [ ] Update monitoring alerts if needed
- [ ] Schedule post-incident review
- [ ] Document learnings in team wiki

## Related Runbooks

- [Database Connection Troubleshooting](./database-connections.md)
- [Pod Restart Procedures](./pod-restart.md)
- [Incident Response Guide](./incident-response.md)

## Contact Information

- **Primary On-Call:** Check PagerDuty schedule
- **Escalation:** Platform Team Lead
- **Slack Channel:** #platform-incidents

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-01-15 | Alice | Added validation steps |
| 2025-01-10 | Bob | Initial version |

```

## Runbook Organization

### Directory Structure

```

runbooks/
├── README.md                    # Index of all runbooks
├── templates/
│   ├── troubleshooting.md      # Template for troubleshooting
│   ├── maintenance.md          # Template for maintenance tasks
│   └── incident-response.md    # Template for incidents
├── services/
│   ├── api-gateway/
│   │   ├── high-latency.md
│   │   ├── connection-errors.md
│   │   └── scaling.md
│   └── database/
│       ├── slow-queries.md
│       └── replication-lag.md
├── infrastructure/
│   ├── kubernetes/
│   │   ├── pod-restart.md
│   │   └── node-drain.md
│   └── networking/
│       └── firewall-rules.md
└── on-call/
    ├── first-responder.md
    ├── escalation-guide.md
    └── common-alerts.md

```

## Best Practices

### Write for Clarity

```markdown
# Good: Clear, specific steps
## Restart the API Server

1. Check current pod status:
   ```bash
   kubectl get pods -n production -l app=api-server
   ```

1. Delete the pod (it will auto-restart):

   ```bash
   kubectl delete pod <pod-name> -n production
   ```

2. Verify new pod is running:

   ```bash
   kubectl get pods -n production -l app=api-server
   ```

   Expected: STATUS = Running

```

```markdown
# Bad: Vague, assumes knowledge
## Fix API Issues

1. Restart the thing
2. Check if it works
3. If not, try something else
```

### Include Decision Trees

```markdown
## Diagnosis

1. Check if service is responding:
   ```bash
   curl -f https://api.example.com/health
   ```

   **If succeeds:** Service is up. Check application logs (Step 3).
   **If fails:** Service is down. Check pod status (Step 2).

1. Check pod status:

   ```bash
   kubectl get pods -n production
   ```

   **If CrashLooping:** Check logs for errors (Step 4).
   **If Pending:** Check node resources (Step 5).
   **If Running:** Service should be up. Check DNS (Step 6).

```

### Provide Expected Outputs

```markdown
## Check Database Connection

```bash
psql -h prod-db.example.com -U app -c "SELECT 1"
```

**Expected output:**

```
 ?column?
----------
        1
(1 row)
```

**If you see "connection refused":**

- Check security groups allow traffic
- Verify database is running
- Check credentials in secrets manager

```

### Use Checklists

```markdown
## Pre-Deployment Checklist

- [ ] Code reviewed and approved
- [ ] Tests passing in CI
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured
- [ ] On-call engineer notified
- [ ] Deploy window scheduled
```

## Common Patterns

### Emergency Response

```markdown
# EMERGENCY: Database Down

**Time-Sensitive:** Complete within 5 minutes

## Immediate Actions (Do First)

1. **Page database team:**
   Use PagerDuty incident: "Database outage"

2. **Notify stakeholders:**
   Post in #incidents: "Database is down. Investigating."

3. **Enable maintenance mode:**
   ```bash
   kubectl set env deployment/api-server MAINTENANCE_MODE=true
   ```

## Investigation (While Waiting)

1. Check RDS console for instance status
2. Review CloudWatch logs for errors
3. Check recent changes in deploy history

## Communication Template

**Update every 10 minutes in #incidents:**

> **[HH:MM]** Database still down. Database team investigating.
> Impact: All API requests failing.
> ETA: Unknown.

```

### Routine Maintenance

```markdown
# Monthly Database Maintenance

**Schedule:** First Sunday of each month, 2 AM UTC
**Duration:** ~2 hours
**Downtime:** None (rolling maintenance)

## Pre-Maintenance

**1 week before:**
- [ ] Announce maintenance window in #engineering
- [ ] Create calendar event
- [ ] Prepare rollback plan

**1 day before:**
- [ ] Verify backup is recent (< 24 hours)
- [ ] Test backup restoration (staging)
- [ ] Confirm on-call coverage

## Maintenance Steps

1. **Take snapshot:**
   ```bash
   aws rds create-db-snapshot \
     --db-instance-identifier prod-db \
     --db-snapshot-identifier maintenance-$(date +%Y%m%d)
   ```

1. **Apply updates:**
   Follow RDS console update wizard

2. **Monitor reboot:**
   Watch CloudWatch metrics for 15 minutes

## Post-Maintenance

- [ ] Verify all services healthy
- [ ] Post completion in #engineering
- [ ] Update maintenance log

```

### Knowledge Transfer

```markdown
# New Engineer Onboarding: Deploy Process

## Learning Objectives

After completing this runbook, you will:
- Understand our deployment pipeline
- Know how to deploy to staging
- Know how to rollback a bad deploy

## Step 1: Understanding the Pipeline

Our deployment flow:
```

GitHub → CI (GitHub Actions) → ArgoCD → Kubernetes

```

**Exercise:** Review a recent deploy in ArgoCD

## Step 2: Deploying to Staging

**Shadowing:** Watch a senior engineer deploy first.

1. Create feature branch
2. Open pull request
3. Wait for CI to pass
4. Merge to main
5. Watch ArgoCD sync

**Practice:** Deploy your own change to staging.

## Step 3: Deploying to Production

**Requirements before production deploy:**
- [ ] Completed 3+ staging deploys
- [ ] Reviewed with team lead
- [ ] Read incident response runbook

**Hands-on:** Pair with team lead for first production deploy.

## Certification

- [ ] Completed 5 staging deploys
- [ ] Completed 1 production deploy (supervised)
- [ ] Can explain rollback procedure

**Certified by:** _________________ Date: _______
```

## Anti-Patterns

### Don't Leave Out Context

```markdown
## Bad: No context

### Fix the API

Run this command:
```bash
kubectl delete pod api-server-abc
```

## Good: Explain why

### Restart API Server

**When to use:** API returning 500 errors, logs show memory leak.

**Why this works:** Deletes pod, Kubernetes creates fresh pod with clean state.

```bash
kubectl delete pod api-server-abc
```

**What to expect:** ~30 seconds downtime while new pod starts.

```

### Don't Skip Validation Steps

```markdown
# Bad: No validation
## Deploy New Version

1. Update image tag
2. Apply changes
3. Done!

# Good: Include validation
## Deploy New Version

1. Update image tag in deployment.yaml
2. Apply changes:
   ```bash
   kubectl apply -f deployment.yaml
   ```

1. **Verify rollout:**

   ```bash
   kubectl rollout status deployment/api-server
   ```

   Wait for "successfully rolled out"

2. **Check pod health:**

   ```bash
   kubectl get pods -l app=api-server
   ```

   All pods should show STATUS: Running

3. **Verify endpoints:**

   ```bash
   curl https://api.example.com/health
   ```

   Should return 200 OK

```

### Don't Assume Knowledge

```markdown
# Bad: Uses jargon without explanation
## Fix Pod

Check the ingress and make sure the service mesh is working.

# Good: Explains terms
## Fix Pod Connectivity

1. **Check ingress** (the load balancer that routes traffic to pods):
   ```bash
   kubectl get ingress -n production
   ```

1. **Verify service mesh** (Istio, manages pod-to-pod communication):

   ```bash
   kubectl get pods -n istio-system
   ```

   All Istio control plane pods should be Running.

```

## Related Skills

- **troubleshooting-guides**: Creating diagnostic procedures
- **incident-response**: Handling production incidents

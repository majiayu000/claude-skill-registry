---
name: runbook-generator
description: Эксперт по runbooks. Используй для создания операционных процедур, incident response и maintenance документации.
---

# Runbook Generator

Expert in creating comprehensive, standardized runbooks for operational procedures, incident response, and system maintenance tasks.

## Runbook Structure

```yaml
runbook_template:
  metadata:
    title: "Runbook title"
    version: "1.0"
    last_updated: "2024-01-15"
    owner: "Team/Person"
    reviewers: ["Name 1", "Name 2"]

  overview:
    purpose: "What this runbook accomplishes"
    scope: "Systems/services affected"
    audience: "Who should use this"

  prerequisites:
    access:
      - "AWS Console access"
      - "SSH key for production servers"
      - "Database credentials"
    tools:
      - "kubectl configured"
      - "AWS CLI installed"
      - "jq for JSON parsing"
    knowledge:
      - "Basic Kubernetes concepts"
      - "Understanding of service architecture"

  execution:
    estimated_time: "15-30 minutes"
    risk_level: "Medium"
    requires_change_ticket: true
    requires_approval: true
    can_be_automated: true

  steps: []  # Detailed steps below

  verification: []  # How to confirm success

  rollback: []  # How to undo changes

  troubleshooting: []  # Common issues

  contacts:
    primary_oncall: "PagerDuty"
    escalation: "Engineering Manager"
    subject_experts: ["DBA Team", "Platform Team"]
```

## Standard Runbook Template

```markdown
# [Runbook Title]

**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Owner:** Team Name
**Risk Level:** Low | Medium | High | Critical

## Overview

### Purpose
Brief description of what this runbook accomplishes.

### When to Use
- Trigger condition 1
- Trigger condition 2
- Alert: "Alert Name" fires

### Scope
Systems and services affected:
- Service A
- Database B
- External dependency C

## Prerequisites

### Required Access
- [ ] Production AWS Console
- [ ] Kubernetes cluster access
- [ ] Database read/write permissions

### Required Tools
```bash
# Verify kubectl
kubectl version --client

# Verify AWS CLI
aws sts get-caller-identity

# Verify database connectivity
psql -h $DB_HOST -U $DB_USER -c "SELECT 1"
```

### Required Knowledge
- Kubernetes pod management
- Service architecture overview
- Incident response process

## Pre-Execution Checklist

- [ ] Change ticket created: CHG-XXXXX
- [ ] Approval obtained from: [Name]
- [ ] Backup verified (if applicable)
- [ ] Stakeholders notified
- [ ] Maintenance window scheduled (if applicable)

## Execution Steps

### Step 1: [Action Name]

**Purpose:** Why this step is necessary

**Command:**
```bash
kubectl get pods -n production -l app=myservice
```

**Expected Output:**
```
NAME                        READY   STATUS    RESTARTS   AGE
myservice-abc123-xyz        1/1     Running   0          2d
myservice-def456-uvw        1/1     Running   0          2d
```

**Verification:** Confirm all pods show STATUS=Running

**If unexpected:** See Troubleshooting section

---

### Step 2: [Next Action]

**Purpose:** Description

**Command:**
```bash
# Command with explanation
kubectl scale deployment myservice --replicas=3 -n production
```

**Expected Output:**
```
deployment.apps/myservice scaled
```

**Verification:**
```bash
# Verify new replicas are running
kubectl get pods -n production -l app=myservice -w
```

**Wait for:** All 3 pods to show Running status (typically 2-5 minutes)

---

## Post-Execution Verification

### Verify Service Health

```bash
# Check deployment status
kubectl rollout status deployment/myservice -n production

# Check service endpoints
kubectl get endpoints myservice -n production

# Verify application health
curl -s https://api.example.com/health | jq .
```

**Expected:**
```json
{
  "status": "healthy",
  "version": "1.2.3",
  "uptime": "2h30m"
}
```

### Verify Metrics

- [ ] Error rate returned to normal (<0.1%)
- [ ] Latency within SLA (<200ms p99)
- [ ] No new alerts firing

## Rollback Procedure

### When to Rollback
- Error rate exceeds 1%
- Latency exceeds 500ms p99
- Critical functionality broken

### Rollback Steps

```bash
# Rollback to previous deployment
kubectl rollout undo deployment/myservice -n production

# Verify rollback
kubectl rollout status deployment/myservice -n production

# Confirm previous version
kubectl get deployment myservice -n production -o jsonpath='{.spec.template.spec.containers[0].image}'
```

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Pods stuck in Pending | Resource constraints | Check node capacity: `kubectl describe nodes` |
| CrashLoopBackOff | Application error | Check logs: `kubectl logs -f <pod>` |
| ImagePullBackOff | Registry auth issue | Verify secret: `kubectl get secret regcred` |
| Connection refused | Service not ready | Wait for readiness probe, check endpoints |

### Common Issues

**Issue: Deployment times out**
```bash
# Check pod events
kubectl describe pod <pod-name> -n production

# Check resource limits
kubectl top pods -n production
```

**Issue: Database connection failures**
```bash
# Verify database connectivity
kubectl exec -it <pod> -n production -- psql -h $DB_HOST -c "SELECT 1"

# Check connection pool
kubectl logs <pod> -n production | grep -i "connection"
```

## Emergency Contacts

| Role | Contact | When to Engage |
|------|---------|----------------|
| On-call Engineer | PagerDuty | Any issue |
| Database Team | #dba-oncall | Database issues |
| Platform Team | #platform-oncall | Infrastructure issues |
| Engineering Manager | [Name] | Escalation |

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-01-15 | Author | Initial version |

## Related Documentation

- [Service Architecture](link)
- [Incident Response Process](link)
- [Monitoring Dashboard](link)
```

## Runbook Types

### Incident Response Runbook

```yaml
incident_runbook:
  sections:
    detection:
      alert_name: "High Error Rate - Payment Service"
      threshold: "Error rate > 5% for 5 minutes"
      severity: "P1"

    immediate_actions:
      - step: "Acknowledge alert"
        command: "In PagerDuty, acknowledge incident"
        time: "< 5 min"

      - step: "Assess impact"
        command: |
          # Check error rate
          curl -s "https://metrics.example.com/api/v1/query?query=rate(http_errors[5m])"
        time: "< 2 min"

      - step: "Notify stakeholders"
        action: "Post in #incident-channel"
        template: |
          🚨 INCIDENT: Payment Service High Errors
          Severity: P1
          Status: Investigating
          Impact: Payment processing affected
          IC: @oncall

    investigation:
      - "Check recent deployments"
      - "Review error logs"
      - "Check dependent services"
      - "Review infrastructure metrics"

    mitigation:
      options:
        - name: "Rollback deployment"
          when: "Error started after deploy"
          command: "kubectl rollout undo deployment/payment -n prod"

        - name: "Scale up"
          when: "Load-related errors"
          command: "kubectl scale deployment/payment --replicas=10 -n prod"

        - name: "Enable circuit breaker"
          when: "Downstream dependency failing"
          command: "Toggle feature flag: payment.circuit_breaker=true"

    resolution:
      checklist:
        - "[ ] Error rate < 0.1%"
        - "[ ] No P1 alerts"
        - "[ ] Stakeholders notified"
        - "[ ] Incident documented"
```

### Deployment Runbook

```yaml
deployment_runbook:
  pre_deployment:
    checklist:
      - "[ ] Code review approved"
      - "[ ] CI/CD pipeline passed"
      - "[ ] Staging tested"
      - "[ ] Change ticket approved"
      - "[ ] Rollback plan documented"

    verification:
      - step: "Verify staging health"
        command: |
          curl -s https://staging.example.com/health

      - step: "Check deployment queue"
        command: |
          kubectl get pods -n staging -l app=myservice

  deployment:
    - step: "Apply deployment"
      command: |
        kubectl apply -f k8s/production/deployment.yaml

    - step: "Monitor rollout"
      command: |
        kubectl rollout status deployment/myservice -n production --timeout=10m

    - step: "Verify new version"
      command: |
        kubectl get deployment myservice -n production \
          -o jsonpath='{.spec.template.spec.containers[0].image}'

  post_deployment:
    - step: "Smoke test"
      command: |
        ./scripts/smoke-test.sh production

    - step: "Monitor metrics"
      duration: "15 minutes"
      watch:
        - "Error rate"
        - "Latency p99"
        - "Request rate"

    - step: "Update ticket"
      action: "Mark CHG ticket as completed"
```

### Maintenance Runbook

```yaml
maintenance_runbook:
  log_rotation:
    schedule: "Weekly, Sunday 02:00 UTC"

    steps:
      - step: "Connect to server"
        command: |
          ssh admin@logs.example.com

      - step: "Rotate logs"
        command: |
          sudo logrotate -f /etc/logrotate.d/application

      - step: "Verify rotation"
        command: |
          ls -la /var/log/application/
          # Should see rotated files with date suffix

      - step: "Clean old logs"
        command: |
          # Remove logs older than 30 days
          find /var/log/application/ -name "*.log.*" -mtime +30 -delete

      - step: "Verify disk space"
        command: |
          df -h /var/log
          # Should show > 20% free

  database_maintenance:
    schedule: "Monthly, first Sunday 03:00 UTC"

    steps:
      - step: "Check table sizes"
        command: |
          psql -c "
            SELECT tablename,
                   pg_size_pretty(pg_total_relation_size(tablename::text))
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(tablename::text) DESC
            LIMIT 10;
          "

      - step: "Run VACUUM ANALYZE"
        command: |
          psql -c "VACUUM ANALYZE;"

      - step: "Reindex if needed"
        command: |
          psql -c "REINDEX DATABASE mydb;"
```

## Writing Guidelines

```yaml
principles:
  clarity:
    - "Use active voice"
    - "Be explicit, never assume"
    - "One action per step"

  completeness:
    - "Include all commands"
    - "Show expected output"
    - "Document verification"

  safety:
    - "Test in non-prod first"
    - "Include rollback steps"
    - "Document risks"

formatting:
  commands:
    - "Use code blocks with language"
    - "Include full paths"
    - "Add comments for complex commands"

  steps:
    - "Number sequentially"
    - "Include purpose"
    - "Show expected result"
    - "Note time estimate"

  variables:
    format: "$VARIABLE_NAME or <placeholder>"
    document: "List all variables at start"
```

## Quality Checklist

```yaml
validation:
  structure:
    - "[ ] Clear title and metadata"
    - "[ ] Prerequisites listed"
    - "[ ] Steps numbered and clear"
    - "[ ] Expected outputs included"
    - "[ ] Verification steps present"
    - "[ ] Rollback documented"
    - "[ ] Troubleshooting section"
    - "[ ] Contacts listed"

  testing:
    - "[ ] All commands tested"
    - "[ ] Outputs verified"
    - "[ ] Rollback tested"
    - "[ ] Time estimates accurate"

  maintenance:
    - "[ ] Version number updated"
    - "[ ] Change log maintained"
    - "[ ] Quarterly review scheduled"
    - "[ ] Owner assigned"
```

## Лучшие практики

1. **Test everything** — каждая команда должна быть проверена
2. **Show expected output** — пользователь должен знать что увидит
3. **Include rollback** — всегда план отката
4. **Keep updated** — ревью каждый квартал
5. **Version control** — runbooks в git
6. **Automate when possible** — автоматизируй повторяющиеся процедуры

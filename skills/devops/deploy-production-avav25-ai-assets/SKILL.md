---
name: deploy-production
description: Deploy to production workflow — final checks, approval gate, deploy, verify, rollback plan. Uses the `deploy-to-production` skill. Requires explicit APPROVE before any production mutation.
disable-model-invocation: true
argument-hint: [service-name] [version]
---

# Deploy to Production

Production deployment with mandatory approval gates, verification, and rollback plan. Every step that mutates production requires explicit user APPROVE.

**⚠️ SAFETY: No production mutation runs without explicit user APPROVE.**

## 1. Pre-Deployment Checklist

### 1a. Staging Verification

Confirm that staging deployment was successful:

- [ ] `/deploy-staging` completed successfully
- [ ] QA testing passed on staging
- [ ] No critical bugs found in staging
- [ ] Performance acceptable on staging

If staging was not verified — **STOP**. Run `/deploy-staging` first.

### 1b. Release Readiness

- [ ] Version tagged (`/release` completed)
- [ ] Changelog updated
- [ ] All tests pass on the release branch
- [ ] Database migrations tested (forward and rollback)
- [ ] Feature flags configured (if applicable)
- [ ] Monitoring dashboards ready
- [ ] On-call team notified

### 1c. Risk Assessment

| Factor | Assessment |
|---|---|
| **Breaking changes** | Yes/No — migration guide ready? |
| **Database migrations** | Yes/No — reversible? |
| **Infrastructure changes** | Yes/No — `/infra-change` completed? |
| **Third-party dependencies** | Yes/No — API compatibility verified? |
| **Traffic impact** | Low/Medium/High |
| **Rollback complexity** | Simple (revert image) / Complex (DB migration) |

If Risk = HIGH, apply `Agent(sre-engineer)` for SLO impact assessment.

## 2. Prepare Deployment

### 2a. Identify Deployment Method

Same as `/deploy-staging` Step 1c — but with production configuration.

### 2b. Backup Current State

```
# Record current deployment state for rollback
kubectl get deployment -n production -o yaml > pre-deploy-state.yaml
```

Or for Helm:
```
helm get values <release> -n production > pre-deploy-values.yaml
helm history <release> -n production
```

### 2c. Deployment Plan

Present the deployment plan:

```
## Production Deployment Plan
- **Version**: [current] → [new]
- **Method**: [K8s/Helm/Docker/Platform]
- **Migrations**: [list if any]
- **Config changes**: [list if any]
- **Expected downtime**: [none / X minutes]
- **Rollback plan**: [documented in Step 5]
- **Monitoring**: [dashboards to watch]
```

**⚠️ STOP. Request APPROVE before proceeding to Step 3.**

## 3. Deploy — REQUIRES EXPLICIT APPROVE

Only after the user explicitly approves:

### 3a. Run Migrations (if applicable)

```
# Database migration
<migration-command>
```

Verify migration completed successfully before proceeding.

### 3b. Deploy Application

**Kubernetes / Helm:**
```
helm upgrade --install <release> <chart> \
  -n production \
  -f values-production.yaml \
  --set image.tag=<tag>
```

**Rolling update strategy** — monitor pod rollout:
```
kubectl rollout status deployment/<name> -n production --timeout=300s
```

### 3c. Canary (if applicable)

If using canary deployment:
1. Deploy to canary (small % of traffic)
2. Monitor error rates and latency for 5–10 minutes
3. If metrics are healthy → proceed to full rollout
4. If degradation detected → rollback canary immediately

## 4. Post-Deployment Verification

### 4a. Health Check

```
// turbo
kubectl get pods -n production -o wide
```

```
curl -s <production-url>/health
```

### 4b. Smoke Tests

- [ ] Application responds on production URL
- [ ] Health endpoint returns 200
- [ ] Authentication flow works
- [ ] Core API endpoints respond correctly
- [ ] Key user journeys functional

### 4c. Monitor (5–10 minutes)

Watch for:
- **Error rate**: Should not increase vs pre-deploy baseline
- **Latency**: P50, P95, P99 within SLO targets
- **CPU/Memory**: No unusual spikes
- **Logs**: No new error patterns

```
// turbo
kubectl logs -n production -l app=<app-name> --tail=100 --since=5m
```

```
// turbo
kubectl get events -n production --sort-by='.lastTimestamp' --field-selector type!=Normal
```

## 5. Rollback Plan

If issues detected — execute rollback immediately:

**Helm:**
```
helm rollback <release> <previous-revision> -n production
```

**Kubernetes:**
```
kubectl rollout undo deployment/<name> -n production
```

**Database migration rollback:**
```
<rollback-migration-command>
```

After rollback:
- Verify application is healthy
- Notify team of rollback
- Create incident ticket for investigation

## 6. Summary

```
## Production Deployment Summary
- **Version**: [old] → [new]
- **Deployed at**: [timestamp]
- **Method**: [K8s/Helm/Docker/Platform]
- **Migrations**: [applied/N/A]
- **Health check**: [pass/fail]
- **Smoke tests**: [pass/fail]
- **Monitoring**: [stable/issues detected]
- **Rollback**: [not needed / executed at timestamp]
- **Production URL**: [url]
- **Next steps**: [monitoring period, team notification, release announcement]
```

## Integration

- **Preceded by**: `/deploy-staging` (staging verification), `/release` (version tag)
- **Roles**: `Agent(devops-engineer)`, `Agent(sre-engineer)`, `Agent(devops-architect)` (deployment strategy design)
- **Skills**: `deploy-to-production` skill

---
name: deploy-to-production
description: Production deployment procedures with rollback plans, health checks, and verification steps. Use when deploying to production, planning rollback strategies, or verifying production health after deployment.
user-invocable: false
---

# Deploy to Production

Production deployment skill providing rollback procedures, health check patterns, and verification checklists. Ensures safe, repeatable production deployments.

## When to Use

- Deploying application updates to production
- Planning rollback strategies before deployment
- Verifying production health after deployment
- Investigating post-deployment issues

## When NOT to Use

- Deploying to staging (use `/deploy-staging` workflow)
- Making infrastructure changes (use `/infra-change` workflow)
- Planning release version and changelog (use `/release` workflow)

## Deployment Strategies

| Strategy | When to Use | Risk | Downtime |
|---|---|---|---|
| **Rolling update** | Standard deploys, stateless services | Low | Zero |
| **Blue-Green** | Critical services, instant rollback needed | Low | Zero |
| **Canary** | High-risk changes, gradual validation | Medium | Zero |
| **Recreate** | Stateful services, breaking schema changes | High | Brief |

### Rolling Update (Default)

- Gradually replace old pods with new ones
- Health checks gate the rollout — unhealthy pods stop the rollout
- Configure `maxSurge` and `maxUnavailable` for rollout speed
- Monitor error rates during rollout window

### Canary Deployment

1. Deploy new version to small subset (5–10% traffic)
2. Monitor error rate, latency, and business metrics for 5–10 minutes
3. If healthy → gradually increase traffic (25% → 50% → 100%)
4. If degraded → route all traffic back to stable version

### Blue-Green Deployment

1. Deploy new version alongside current (green alongside blue)
2. Run full smoke tests against green
3. Switch traffic from blue to green
4. Keep blue running for instant rollback (15–30 minutes)
5. Decommission blue after confidence period

## Pre-Deployment Checklist

- [ ] All tests pass on release branch
- [ ] Staging deployment verified
- [ ] Database migrations tested (forward and rollback)
- [ ] Feature flags configured
- [ ] Monitoring dashboards ready
- [ ] On-call team notified
- [ ] Rollback plan documented and tested
- [ ] Release notes prepared

## Post-Deployment Verification

- [ ] Health endpoint returns 200
- [ ] Error rate ≤ pre-deploy baseline
- [ ] Latency P95 within SLO target
- [ ] No new error patterns in logs
- [ ] Key user journeys functional
- [ ] Database connections stable
- [ ] External integrations responding
- [ ] Alerts not firing

## Integration

- **Follows rules**: `Agent(devops-engineer)` (infrastructure), `Agent(sre-engineer)` (SLOs, monitoring)
- **Used by workflows**: `/deploy-production`, `/deploy-staging`
- **Companion resources**: `rollback-procedure.md`

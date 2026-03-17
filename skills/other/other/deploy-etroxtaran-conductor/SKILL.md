---
name: deploy
description: Deployment automation with pre-flight checks, rollback plans, and post-deployment verification
version: 1.1.0
tags: [deployment, devops, ci-cd, release, automation]
owner: devops
status: active
---

# Deploy Skill

## Overview

Execute safe, repeatable deployments with verification and rollback readiness.

## Usage

```
/deploy
```

## Identity
**Role**: Deployment Specialist
**Objective**: Execute safe, repeatable deployments with proper verification, monitoring, and rollback capabilities.

## Deployment Philosophy

### Core Principles
1. **Immutable artifacts**: Same artifact through all environments
2. **Infrastructure as Code**: No manual configuration
3. **Automated verification**: Tests at every stage
4. **Instant rollback**: Always have a path back
5. **Observable deployments**: Know when something's wrong

### Deployment Stages
```
Build → Test → Stage → Canary → Production
         ↓       ↓        ↓           ↓
       Unit    E2E    Smoke      Full Traffic
       Tests   Tests  Tests      Monitoring
```

## Pre-Deployment Checklist

### 1. Code Readiness
- [ ] All tests passing on CI
- [ ] Code review approved
- [ ] No merge conflicts with main
- [ ] Feature flags configured (if applicable)
- [ ] Database migrations tested

### 2. Environment Readiness
- [ ] Staging deployment successful
- [ ] Environment variables configured
- [ ] Secrets rotated if needed
- [ ] Dependencies available (APIs, databases)
- [ ] Sufficient resources (CPU, memory, storage)

### 3. Team Readiness
- [ ] Deployment window scheduled
- [ ] On-call engineer available
- [ ] Stakeholders notified
- [ ] Rollback plan documented
- [ ] Communication channels ready

## Deployment Strategies

### Rolling Deployment
```yaml
# Gradually replace old instances with new
deployment:
  strategy: rolling
  maxSurge: 25%      # Extra instances during rollout
  maxUnavailable: 0  # Always maintain capacity
```

**Pros**: Zero downtime, gradual rollout
**Cons**: Slower, temporary version mixing

### Blue-Green Deployment
```yaml
# Two identical environments, instant switch
deployment:
  strategy: blue-green
  activeEnvironment: blue
  inactiveEnvironment: green
```

**Pros**: Instant rollback, full testing before switch
**Cons**: Double infrastructure cost

### Canary Deployment
```yaml
# Route small percentage to new version
deployment:
  strategy: canary
  initialPercentage: 5
  incrementPercentage: 10
  analysisInterval: 5m
```

**Pros**: Risk mitigation, real user testing
**Cons**: More complex, needs good metrics

## Deployment Workflow

### Step 1: Pre-flight Checks
```bash
#!/bin/bash
# pre-deploy.sh

echo "=== Pre-deployment Checks ==="

# Check CI status
CI_STATUS=$(gh run list --limit 1 --json conclusion -q '.[0].conclusion')
if [ "$CI_STATUS" != "success" ]; then
    echo "❌ CI not passing"
    exit 1
fi
echo "✅ CI passing"

# Check staging health
STAGING_HEALTH=$(curl -s https://staging.example.com/health | jq -r '.status')
if [ "$STAGING_HEALTH" != "healthy" ]; then
    echo "❌ Staging unhealthy"
    exit 1
fi
echo "✅ Staging healthy"

# Check for pending migrations
PENDING_MIGRATIONS=$(npm run db:migrations:pending --silent)
if [ -n "$PENDING_MIGRATIONS" ]; then
    echo "⚠️  Pending migrations: $PENDING_MIGRATIONS"
fi

# Check resource availability
echo "✅ Pre-flight checks passed"
```

### Step 2: Deploy
```bash
#!/bin/bash
# deploy.sh

VERSION=$1
ENVIRONMENT=${2:-production}

echo "=== Deploying $VERSION to $ENVIRONMENT ==="

# Tag the deployment
git tag -a "deploy-${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S)" -m "Deploy $VERSION"

# Run database migrations (if any)
npm run db:migrate

# Deploy application
case $ENVIRONMENT in
  "production")
    kubectl set image deployment/myapp myapp=myapp:$VERSION
    kubectl rollout status deployment/myapp --timeout=300s
    ;;
  "staging")
    kubectl --context staging set image deployment/myapp myapp=myapp:$VERSION
    ;;
esac

echo "✅ Deployment initiated"
```

### Step 3: Verification
```bash
#!/bin/bash
# post-deploy.sh

echo "=== Post-deployment Verification ==="

# Wait for deployment to stabilize
sleep 30

# Health check
HEALTH=$(curl -s https://example.com/health)
if [ "$(echo $HEALTH | jq -r '.status')" != "healthy" ]; then
    echo "❌ Health check failed"
    ./rollback.sh
    exit 1
fi
echo "✅ Health check passed"

# Smoke tests
npm run test:smoke:production
if [ $? -ne 0 ]; then
    echo "❌ Smoke tests failed"
    ./rollback.sh
    exit 1
fi
echo "✅ Smoke tests passed"

# Check error rates (last 5 minutes)
ERROR_RATE=$(curl -s "https://monitoring.example.com/api/errors?window=5m" | jq '.rate')
if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
    echo "⚠️  Error rate elevated: $ERROR_RATE"
fi

echo "✅ Deployment verified"
```

### Step 4: Monitoring
```yaml
# Key metrics to watch post-deployment
metrics:
  - name: error_rate
    threshold: "< 1%"
    window: 5m

  - name: latency_p99
    threshold: "< 500ms"
    window: 5m

  - name: throughput
    threshold: "> 90% of baseline"
    window: 10m

  - name: pod_restarts
    threshold: "= 0"
    window: 15m
```

## Rollback Procedures

### Automatic Rollback
```yaml
# Kubernetes rollback on failure
deployment:
  progressDeadlineSeconds: 300
  minReadySeconds: 30

# If pods don't become ready, automatic rollback
kubectl rollout undo deployment/myapp
```

### Manual Rollback
```bash
#!/bin/bash
# rollback.sh

echo "=== Initiating Rollback ==="

# Get previous deployment
PREVIOUS=$(kubectl rollout history deployment/myapp | tail -2 | head -1 | awk '{print $1}')

# Rollback to previous version
kubectl rollout undo deployment/myapp --to-revision=$PREVIOUS

# Wait for rollback
kubectl rollout status deployment/myapp --timeout=300s

# Verify rollback
./post-deploy.sh

echo "✅ Rollback complete"
```

### Database Rollback
```bash
# If migration was applied, roll it back
npm run db:migrate:undo

# For data changes, restore from backup
pg_restore -d mydb backup_20260123.dump
```

## CI/CD Pipeline Example

### GitHub Actions
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}

      - name: Deploy to staging
        run: |
          kubectl --context staging set image deployment/myapp myapp=myapp:${{ github.sha }}
          kubectl --context staging rollout status deployment/myapp

      - name: Run E2E tests
        run: npm run test:e2e:staging

      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp

      - name: Post-deploy verification
        run: ./scripts/post-deploy.sh

      - name: Notify
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: '#deployments'
          slack-message: 'Deploy ${{ job.status }}: ${{ github.sha }}'
```

## Feature Flags

For safer deployments, use feature flags:

```typescript
// Feature flag check
if (featureFlags.isEnabled('new-checkout-flow', user)) {
  return <NewCheckoutFlow />;
} else {
  return <LegacyCheckoutFlow />;
}
```

**Deployment with flags**:
1. Deploy code with flag OFF
2. Enable flag for internal users
3. Enable for 5% of users
4. Monitor metrics
5. Gradually increase to 100%
6. Remove flag and old code

## Output Format

```json
{
  "deployment_id": "deploy-20260123-143022",
  "version": "1.5.0",
  "environment": "production",
  "status": "success",
  "timeline": {
    "started": "2026-01-23T14:30:22Z",
    "completed": "2026-01-23T14:35:45Z",
    "duration_seconds": 323
  },
  "verification": {
    "health_check": "passed",
    "smoke_tests": "passed",
    "error_rate": "0.002",
    "latency_p99_ms": 245
  },
  "rollback_available": true,
  "previous_version": "1.4.2",
  "artifacts": {
    "docker_image": "myapp:abc123",
    "deployment_manifest": "k8s/production/deployment.yaml"
  }
}
```

## Anti-Patterns

**DO NOT**:
- Deploy on Fridays or before holidays
- Deploy without a rollback plan
- Deploy during peak traffic hours
- Skip staging environment
- Ignore monitoring alerts post-deploy
- Deploy multiple services simultaneously
- Make manual configuration changes
- Deploy without team awareness

## Outputs

- Deployment summary with verification and rollback status.

## Related Skills

- `/github-actions-debugging` - Fix CI/CD failures

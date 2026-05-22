---
name: mistral-prod-checklist
description: |
  Execute Mistral AI production deployment checklist and rollback procedures.
  Use when deploying Mistral AI integrations to production, preparing for launch,
  or implementing go-live procedures.
  Trigger with phrases like "mistral production", "deploy mistral",
  "mistral go-live", "mistral launch checklist".
allowed-tools: Read, Bash(kubectl:*), Bash(curl:*), Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Production Checklist

## Overview
Complete checklist for deploying Mistral AI integrations to production.

## Prerequisites
- Staging environment tested and verified
- Production API keys available
- Deployment pipeline configured
- Monitoring and alerting ready

## Instructions

### Step 1: Pre-Deployment Configuration

**Secrets & Configuration**
- [ ] Production API key in secure vault (AWS Secrets Manager, GCP Secret Manager, etc.)
- [ ] Environment variables set in deployment platform
- [ ] API key validated with test request
- [ ] Fallback configuration ready (if Mistral unavailable)

**Verify API Key:**
```bash
# Test production key
curl -H "Authorization: Bearer ${MISTRAL_API_KEY_PROD}" \
  https://api.mistral.ai/v1/models | jq '.data[].id'
```

### Step 2: Code Quality Verification

**Code Review**
- [ ] All tests passing (`npm test`)
- [ ] No hardcoded credentials (`grep -r "MISTRAL_API_KEY" src/`)
- [ ] Error handling covers all error types (401, 429, 500, etc.)
- [ ] Rate limiting/backoff implemented
- [ ] Logging is production-appropriate (no sensitive data)
- [ ] TypeScript types are strict

**Run Verification:**
```bash
# Full test suite
npm test

# Type checking
npm run typecheck

# Check for hardcoded secrets
grep -r "sk-" src/ --include="*.ts" --include="*.js"

# Lint
npm run lint
```

### Step 3: Infrastructure Setup

**Health Checks**
- [ ] Health check endpoint includes Mistral connectivity test
- [ ] Readiness probe configured
- [ ] Liveness probe configured

```typescript
// /health endpoint
app.get('/health', async (req, res) => {
  const mistralHealth = await checkMistralHealth();

  res.status(mistralHealth.healthy ? 200 : 503).json({
    status: mistralHealth.healthy ? 'healthy' : 'degraded',
    services: {
      mistral: mistralHealth,
    },
    timestamp: new Date().toISOString(),
  });
});

async function checkMistralHealth() {
  const start = Date.now();
  try {
    await client.models.list();
    return { healthy: true, latencyMs: Date.now() - start };
  } catch (error) {
    return { healthy: false, latencyMs: Date.now() - start, error: 'API unreachable' };
  }
}
```

**Monitoring & Alerting**
- [ ] Prometheus/Datadog metrics configured
- [ ] Alert rules defined (error rate, latency, rate limits)
- [ ] Dashboard created
- [ ] On-call rotation scheduled

### Step 4: Resilience Patterns

**Circuit Breaker**
- [ ] Circuit breaker pattern implemented
- [ ] Graceful degradation configured
- [ ] Fallback responses defined

```typescript
class MistralCircuitBreaker {
  private failures = 0;
  private lastFailure?: Date;
  private isOpen = false;

  private readonly failureThreshold = 5;
  private readonly resetTimeout = 60000; // 1 minute

  async call<T>(fn: () => Promise<T>, fallback?: () => T): Promise<T> {
    // Check if circuit is open
    if (this.isOpen) {
      if (Date.now() - (this.lastFailure?.getTime() || 0) > this.resetTimeout) {
        this.isOpen = false;
        this.failures = 0;
      } else {
        if (fallback) return fallback();
        throw new Error('Mistral service temporarily unavailable');
      }
    }

    try {
      const result = await fn();
      this.failures = 0;
      return result;
    } catch (error: any) {
      this.failures++;
      this.lastFailure = new Date();

      if (this.failures >= this.failureThreshold) {
        this.isOpen = true;
        console.error('Mistral circuit breaker opened');
      }

      if (fallback && this.isOpen) return fallback();
      throw error;
    }
  }
}
```

### Step 5: Documentation Requirements

- [ ] Incident runbook created
- [ ] Key rotation procedure documented
- [ ] Rollback procedure documented
- [ ] On-call escalation path defined
- [ ] API usage limits documented

### Step 6: Deploy with Gradual Rollout

```bash
# Pre-flight checks
echo "=== Pre-flight Checks ==="

# 1. Check Mistral status
echo -n "Mistral API: "
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${MISTRAL_API_KEY_PROD}" \
  https://api.mistral.ai/v1/models
echo ""

# 2. Check staging health
echo -n "Staging health: "
curl -sf https://staging.yourapp.com/health | jq -r '.status'

# 3. Verify tests pass
npm test

# Gradual rollout
echo "=== Starting Gradual Rollout ==="

# Deploy to canary (10% traffic)
kubectl set image deployment/mistral-app app=image:new --record
kubectl rollout pause deployment/mistral-app

# Monitor for 10 minutes
echo "Monitoring canary for 10 minutes..."
sleep 600

# Check error rates
kubectl logs -l app=mistral-app --since=10m | grep -c "error" || echo "0 errors"

# If healthy, continue to 50%
kubectl rollout resume deployment/mistral-app
kubectl rollout pause deployment/mistral-app

sleep 300

# Complete rollout to 100%
kubectl rollout resume deployment/mistral-app
kubectl rollout status deployment/mistral-app
```

### Step 7: Post-Deployment Verification

```bash
# Verify deployment
echo "=== Post-Deployment Verification ==="

# Health check
curl -sf https://yourapp.com/health | jq

# Test chat endpoint
curl -X POST https://yourapp.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}' | jq

# Check logs for errors
kubectl logs -l app=mistral-app --since=5m | grep -i error
```

## Output
- Deployed Mistral AI integration
- Health checks passing
- Monitoring active
- Rollback procedure documented

## Alert Configuration

| Alert | Condition | Severity |
|-------|-----------|----------|
| API Down | 5xx errors > 10/min | P1 - Critical |
| High Latency | p99 > 5000ms for 5min | P2 - High |
| Rate Limited | 429 errors > 5/min | P2 - High |
| Auth Failures | 401 errors > 0 | P1 - Critical |
| Circuit Open | Circuit breaker triggered | P2 - High |

## Rollback Procedure

```bash
# Immediate rollback
echo "=== Emergency Rollback ==="

# 1. Rollback deployment
kubectl rollout undo deployment/mistral-app

# 2. Verify rollback
kubectl rollout status deployment/mistral-app

# 3. Check health
curl -sf https://yourapp.com/health | jq

# 4. Notify team
# Send alert to Slack/PagerDuty
```

## Resources
- [Mistral AI Status](https://status.mistral.ai/)
- [Mistral AI Console](https://console.mistral.ai/)

## Next Steps
For version upgrades, see `mistral-upgrade-migration`.

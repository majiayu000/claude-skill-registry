---
name: cicd-pipeline-architecture
description: Use when setting up CI/CD pipelines, experiencing deployment failures, slow feedback loops, or production incidents after deployment - provides deployment strategies, test gates, rollback mechanisms, and environment promotion patterns to prevent downtime and enable safe continuous delivery
---

# CI/CD Pipeline Architecture

## Overview

**Design CI/CD pipelines with deployment verification, rollback capabilities, and zero-downtime strategies from day one.**

**Core principle:** "Deploy to production" is not a single step - it's a sequence of gates, health checks, gradual rollouts, and automated rollback triggers. Skipping these "for speed" causes production incidents.

## When to Use

Use this skill when:
- **Setting up new CI/CD pipelines** (before writing workflow files)
- **Experiencing deployment failures** in production
- **CI feedback loops are too slow** (tests taking too long)
- **No confidence in deployments** (fear of breaking production)
- **Manual rollbacks required** after bad deploys
- **Downtime during deployments** is acceptable (it shouldn't be)
- **Migrations cause production issues**

**Do NOT skip this for:**
- "Quick MVP" or "demo" pipelines (these become production)
- "Simple" applications (complexity comes from deployment, not code)
- "We'll improve it later" (later never comes, incidents do)

## Core Pipeline Architecture

### Mandatory Pipeline Stages

**Every production pipeline MUST include:**

```
1. Build → 2. Test → 3. Deploy to Staging → 4. Verify Staging → 5. Deploy to Production → 6. Verify Production → 7. Monitor
```

**Missing any stage = production incidents waiting to happen.**

### 1. Build Stage

**Purpose:** Compile, package, create artifacts

```yaml
build:
  - Compile code (if applicable)
  - Run linters and formatters
  - Build container image
  - Tag with commit SHA (NOT "latest")
  - Push to registry
  - Create immutable artifact
```

**Key principle:** Build once, deploy everywhere. Same artifact to staging and production.

### 2. Test Stage

**Test Pyramid in CI:**

```
       /\
      /E2\      ← Few, critical paths only (5-10 tests)
     /----\
    / Intg \    ← API contracts, DB integration (50-100 tests)
   /--------\
  /   Unit   \  ← Fast, isolated, thorough (100s-1000s)
 /____________\
```

**Optimization strategies:**

- **Parallel execution:** Split test suite across multiple runners
- **Smart triggers:** Run full suite on main, subset on PRs
- **Caching:** Cache dependencies, build artifacts, test databases
- **Fail fast:** Run fastest tests first

**Anti-pattern:** "Tests are slow, let's skip some" → Optimize execution, don't remove coverage

### 3. Deploy to Staging

**Staging MUST match production:**
- Same infrastructure (containers, K8s, serverless)
- Same environment variables structure
- Same database migration process
- Similar data volume (use anonymized production data)

**Deployment process:**
```yaml
1. Run database migrations (with rollback tested)
2. Deploy new version alongside old (blue-green)
3. Run smoke tests
4. Cutover traffic
5. Keep old version running for quick rollback
```

### 4. Verify Staging

**Automated verification (not manual testing):**

```yaml
verify_staging:
  - Health check endpoint returns 200
  - Critical API endpoints respond correctly
  - Database migrations applied successfully
  - Background jobs processing
  - External integrations functional
```

**Failure = stop pipeline, do NOT proceed to production.**

### 5. Deploy to Production

**Deployment Strategies (choose one):**

#### Blue-Green Deployment
```
Old (Blue) ← 100% traffic
New (Green) ← deployed, health checked, 0% traffic

→ Switch traffic to Green
→ Keep Blue running for 1 hour for rollback
→ Terminate Blue after monitoring shows Green is stable
```

**Pros:** Instant rollback, zero downtime
**Cons:** Double infrastructure cost during deployment

#### Canary Deployment
```
Old ← 95% traffic
New ← 5% traffic (canary)

→ Monitor error rates, latency for 15 min
→ If healthy: 50% traffic
→ If healthy: 100% traffic
→ If unhealthy: immediate rollback to 100% old
```

**Pros:** Gradual risk, early warning
**Cons:** More complex monitoring

#### Rolling Deployment
```
Instances: [A, B, C, D, E]

→ Deploy to A, health check
→ Deploy to B, health check
→ Deploy to C, D, E sequentially

If any fails → stop, rollback deployed instances
```

**Pros:** No extra infrastructure
**Cons:** Mixed versions during deployment

**Choose based on:**
- Blue-Green: Critical systems, tolerance for double cost
- Canary: High-traffic systems with good metrics
- Rolling: Cost-sensitive, moderate traffic

**NEVER:** Direct deployment with restart (causes downtime)

### 6. Verify Production

**Automated post-deployment verification:**

```yaml
verify_production:
  - HTTP 200 from health endpoint
  - Response time < baseline + 20%
  - Error rate < 1%
  - Critical user flows functional (synthetic tests)
  - Database connections healthy
  - Cache hit rates normal
```

**Auto-rollback triggers:**
- Health check fails for 2 consecutive checks
- Error rate > 5% for 3 minutes
- Response time > 2x baseline
- Critical endpoint returns 5xx

### 7. Monitor

**Observe for 1 hour post-deployment:**
- Error rates (by endpoint, by user segment)
- Latency percentiles (p50, p95, p99)
- Resource usage (CPU, memory, DB connections)
- Business metrics (conversions, signups)

**Dashboard must show:**
- Current deployment version
- Time since last deployment
- Comparison to pre-deployment metrics
- Rollback button (one-click)

## Database Migrations in CI/CD

### Migration Strategy

```
1. Write backward-compatible migrations
   - Add columns as nullable first
   - Create new tables before dropping old
   - Add indexes with CONCURRENTLY (Postgres)

2. Deploy application code that works with old AND new schema

3. Run migration

4. Deploy code that uses new schema exclusively

5. Clean up old schema (separate deployment)
```

**This takes 3 deployments, not 1. That's correct.**

### Migration Testing

```yaml
test_migrations:
  - Apply migration to test DB
  - Run application tests against migrated schema
  - Test rollback (down migration)
  - Verify data integrity
```

**Never skip migration rollback testing.** You'll need it in production.

## Secrets Management

**Anti-patterns from baseline:**

❌ **Hardcoded in workflow:**
```yaml
env:
  DATABASE_URL: postgresql://user:pass@localhost/db
```

✅ **Correct:**
```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**Secrets checklist:**
- Store in CI/CD secret manager (GitHub Secrets, GitLab CI/CD variables)
- Rotate regularly (automated)
- Different secrets per environment
- Never log secret values
- Use secret scanning tools

## Environment Promotion

**Progression:**
```
Developer → CI Tests → Staging → Production
```

**Gates between environments:**

1. **CI → Staging:** All tests pass
2. **Staging → Production:**
   - Staging verification passes
   - Manual approval (for critical systems)
   - Business hours only (optional)
   - Monitoring shows staging is healthy

## Quick Reference: Pipeline Checklist

**Before deploying to production, verify:**

- [ ] Tests run and pass in CI
- [ ] Build creates immutable, tagged artifact
- [ ] Staging environment exists and matches production
- [ ] Migrations tested with rollback
- [ ] Deployment strategy chosen (blue-green/canary/rolling)
- [ ] Health check endpoint implemented
- [ ] Automated verification tests written
- [ ] Auto-rollback triggers configured
- [ ] Monitoring dashboard shows deployment metrics
- [ ] Rollback procedure tested
- [ ] Secrets managed securely
- [ ] On-call engineer notified of deployment

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| "Just restart the service" | Causes downtime, no rollback | Use blue-green or canary deployment |
| "Tests are slow, skip some" | Removes safety net | Parallel execution, smart caching |
| "We'll add staging later" | Production becomes your staging | Create staging first, before production pipeline |
| "Migrations in deployment script" | Can't roll back safely | Backward-compatible migrations, 3-step deployment |
| "Manual verification after deploy" | Slow, error-prone, doesn't scale | Automated health checks and smoke tests |
| "Deploy on main merge" | No gate, broken main can deploy | Require staging verification first |
| Hardcoded database credentials | Security risk, can't rotate | Use secret manager |
| "Single server is fine for now" | Downtime during deployment | Use multiple instances from day one |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "This is just an MVP/demo" | MVP pipelines become production pipelines. Build it right once. |
| "Staging is expensive" | Production incidents are more expensive. Staging prevents them. |
| "Blue-green doubles our costs" | Downtime and incidents cost more than temporary double infrastructure. |
| "We'll add rollback later" | You need rollback when a deployment fails. Later = too late. |
| "Health checks are overkill" | Silent failures in production are worse than no deployment. |
| "Migrations always work" | They don't. Test rollbacks before you need them. |
| "Our app is too simple for this" | Deployment complexity isn't about code complexity. |

## Red Flags - Stop and Fix Pipeline

If you catch yourself thinking:

- "Just push to main, it'll be fine" → Add staging gate
- "Tests passed locally, skip CI" → Never skip CI
- "Restart is faster than blue-green" → Downtime is never acceptable
- "We'll monitor manually after deploy" → Automate verification
- "If it breaks, we'll fix forward" → Implement auto-rollback
- "Migrations can run during deployment" → Backward-compatible migrations first
- "One environment is enough" → Minimum: staging + production

**All of these mean: Your pipeline will cause production incidents.**

## Cross-References

**Related skills:**
- **test-automation-architecture** (ordis-quality-engineering) - Which tests to run where
- **observability-and-monitoring** (ordis-quality-engineering) - Deployment monitoring
- **testing-in-production** (ordis-quality-engineering) - Canary + feature flags
- **api-testing** (axiom-web-backend) - Contract tests in CI
- **database-integration** (axiom-web-backend) - Migration patterns

## The Bottom Line

**"Deploy to production" is not one step. It's:**

1. Build immutable artifact
2. Deploy to staging
3. Verify staging
4. Deploy with zero-downtime strategy
5. Verify production automatically
6. Monitor with auto-rollback triggers

**Skipping steps to "move fast" causes incidents. This IS moving fast.**

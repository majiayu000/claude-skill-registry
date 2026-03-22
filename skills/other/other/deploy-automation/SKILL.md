---
name: deploy-automation
description: Workflows and best practices for CI/CD automation, deployment strategies, and production releases. Use when implementing or improving deployment pipelines, managing environments, or planning production releases.
---

# Deploy Automation Skill

This skill provides comprehensive workflows, patterns, and best practices for automating deployments across different environments and platforms.

## When to Use This Skill

Use this skill when:
- Setting up CI/CD pipelines from scratch
- Implementing deployment strategies (blue-green, canary, rolling)
- Managing multiple environments (dev, staging, production)
- Automating database migrations
- Planning zero-downtime deployments
- Creating rollback procedures
- Managing feature flags
- Implementing GitOps workflows

## Core Principles

### 1. Automation First

**Always automate:**
- Build processes
- Testing (unit, integration, E2E)
- Security scanning
- Deployment to all environments
- Rollback procedures
- Notifications

**Never manual:**
- Production deployments without approval
- Database migrations without backup
- Configuration changes without versioning
- Certificate renewals

### 2. Safety Mechanisms

**Implement at every stage:**
- Automated testing gates
- Security scanning gates
- Manual approval gates (production)
- Health checks before traffic switch
- Automatic rollback on failure
- Comprehensive logging

### 3. Reversibility

**Every deployment must have:**
- Documented rollback procedure
- Automated rollback capability
- Database migration rollback
- Configuration versioning
- Backup before deployment

## Deployment Strategies

### Strategy Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│ Choose deployment strategy based on:                        │
├─────────────────────────────────────────────────────────────┤
│ • Risk tolerance         • Team size                        │
│ • Traffic volume         • Infrastructure complexity        │
│ • Release frequency      • Database changes                 │
│ • Downtime tolerance     • Testing confidence               │
└─────────────────────────────────────────────────────────────┘

Strategy Recommendations:

High availability required (99.9%+):
  → Blue-Green or Canary

Frequent releases (multiple/day):
  → Rolling or Canary with feature flags

Database schema changes:
  → Expand-Contract pattern + Blue-Green

Low traffic / Internal tools:
  → Rolling or Recreate

Microservices architecture:
  → Canary per service + Feature flags
```

### Rolling Deployment

**Best for:** Low-risk changes, frequent deployments

```yaml
# Key characteristics
- Gradual rollout (10% → 25% → 50% → 100%)
- Automatic progression on health checks
- Fast rollback by stopping rollout
- No infrastructure duplication
- Brief period with mixed versions

# Implementation checklist
- [ ] Health checks configured (readiness + liveness)
- [ ] Rollout parameters set (maxSurge, maxUnavailable)
- [ ] Monitoring dashboards ready
- [ ] Alert thresholds configured
- [ ] Rollback script tested
```

See `resources/deployment-strategies.md` for complete implementation.

### Blue-Green Deployment

**Best for:** Zero-downtime, high-confidence releases, database changes

```yaml
# Key characteristics
- Two identical environments (Blue + Green)
- Instant traffic switch via load balancer
- Full rollback capability (switch back)
- Requires 2x infrastructure
- Testing on inactive environment before switch

# Implementation checklist
- [ ] Duplicate infrastructure configured
- [ ] Load balancer rules ready
- [ ] Database migration strategy defined
- [ ] Smoke tests prepared
- [ ] Traffic switch procedure documented
- [ ] Rollback procedure tested
```

See `resources/deployment-strategies.md` for complete implementation.

### Canary Deployment

**Best for:** High-traffic applications, risk mitigation, gradual validation

```yaml
# Key characteristics
- Gradual traffic shift (1% → 5% → 25% → 50% → 100%)
- Real user validation at each stage
- Automatic rollback on metrics degradation
- Requires traffic management (service mesh, ingress)
- Longer deployment time but lower risk

# Implementation checklist
- [ ] Metrics baseline established
- [ ] Analysis templates configured
- [ ] Traffic routing rules ready
- [ ] Alert thresholds defined
- [ ] Automatic rollback configured
```

See `resources/deployment-strategies.md` for complete implementation.

## CI/CD Pipeline Structure

### Standard Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Source → Build → Test → Security → Package → Deploy → Verify  │
│    │        │       │        │         │         │        │     │
│    │        │       │        │         │         │        │     │
│   lint    compile  unit     SAST     docker   staging  smoke    │
│   validate         integration SCA    tag      prod     health   │
│                  coverage   secrets  push      canary   tests    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Each stage must:
✓ Pass to proceed
✓ Fail fast on errors
✓ Generate artifacts/logs
✓ Be reproducible
```

### Pipeline Configuration

**Essential stages for every pipeline:**

1. **Source Validation**
   - Branch protection
   - Code ownership
   - Commit message validation

2. **Build**
   - Dependency installation
   - Compilation/transpilation
   - Asset generation

3. **Test**
   - Unit tests (required)
   - Integration tests (required)
   - E2E tests (staging/production)
   - Performance tests (periodic)

4. **Security**
   - SAST (Static Application Security Testing)
   - SCA (Software Composition Analysis)
   - Secret scanning
   - Container scanning

5. **Package**
   - Container build
   - Image signing
   - Artifact storage
   - Version tagging

6. **Deploy**
   - Environment-specific configuration
   - Database migrations
   - Service deployment
   - Health verification

7. **Verify**
   - Smoke tests
   - Health checks
   - Metric validation
   - User notification

## Environment Management

### Environment Strategy

```yaml
environments:
  development:
    purpose: Developer testing
    deployment: Automatic on commit
    data: Mock/synthetic
    access: Development team
    monitoring: Basic
    
  staging:
    purpose: Pre-production validation
    deployment: Automatic on main branch
    data: Anonymized production copy
    access: QA + Dev teams
    monitoring: Full
    
  production:
    purpose: Live user traffic
    deployment: Manual approval required
    data: Real user data
    access: Restricted
    monitoring: Comprehensive + alerting
```

### Configuration Management

**Best practices:**

1. **Separate config from code**
   ```
   Code → Same across environments
   Config → Environment-specific
   Secrets → Managed separately
   ```

2. **Use environment variables**
   ```bash
   # Never in code
   ❌ DB_PASSWORD="secret123"
   
   # Use environment variables
   ✅ DB_PASSWORD=${DATABASE_PASSWORD}
   ```

3. **Configuration hierarchy**
   ```
   1. Code defaults (lowest priority)
   2. Config files (per environment)
   3. Environment variables
   4. Secret manager (highest priority)
   ```

## Database Deployments

### Migration Strategies

**Expand-Contract Pattern:**

```
Phase 1: Expand (Deploy with old + new schema)
  - Add new columns (nullable)
  - Deploy code that writes to both
  - Backfill data gradually
  
Phase 2: Migrate (Switch to new schema)
  - Update code to read from new
  - Verify data consistency
  - Monitor for issues
  
Phase 3: Contract (Clean up old schema)
  - Remove old columns
  - Clean up code
  - Deploy cleanup
```

**Migration Checklist:**

- [ ] Backup created and verified
- [ ] Migration tested on staging
- [ ] Rollback script prepared
- [ ] Downtime estimated and communicated
- [ ] Monitoring alerts configured
- [ ] Team on standby

## Rollback Procedures

### Automatic Rollback Triggers

```yaml
# Configure automatic rollback when:
rollback_triggers:
  error_rate:
    threshold: "> 1%"
    window: "5m"
    
  latency_p95:
    threshold: "> 500ms"
    window: "10m"
    
  health_checks:
    threshold: "> 3 failures"
    window: "2m"
    
  business_metrics:
    threshold: "< baseline - 20%"
    window: "15m"
```

### Rollback Execution

```bash
#!/bin/bash
# Rollback procedure template

# 1. Stop current deployment
kubectl rollout pause deployment/app

# 2. Rollback to previous version
kubectl rollout undo deployment/app

# 3. Monitor rollback
kubectl rollout status deployment/app --timeout=300s

# 4. Verify health
./scripts/smoke-tests.sh

# 5. Notify team
./scripts/notify-rollback.sh

# 6. Document incident
./scripts/create-incident-report.sh
```

## Feature Flags

### Feature Flag Strategy

```yaml
# Use feature flags for:
- Gradual rollouts
- A/B testing
- Kill switches
- Environment-specific features
- User segment targeting

# Flag types:
release_flags:    # Short-term (days/weeks)
  - New feature rollout
  - Bug fix validation
  
experiment_flags: # Medium-term (weeks/months)
  - A/B tests
  - UI experiments
  
permission_flags: # Long-term (months/years)
  - Beta features
  - Enterprise features
  
ops_flags:        # Immediate control
  - Kill switches
  - Maintenance mode
```

## Monitoring & Alerting

### Deployment Metrics

**Track these metrics:**

1. **Deployment Frequency**
   - Deployments per day/week
   - Lead time for changes

2. **Deployment Success Rate**
   - Successful deployments / Total
   - Rollback rate

3. **Recovery Metrics**
   - MTTR (Mean Time To Recovery)
   - Time to detect failures

4. **Quality Metrics**
   - Change failure rate
   - Defect escape rate

### Alert Configuration

```yaml
# Critical alerts (page immediately)
critical:
  - Deployment failed in production
  - Rollback initiated
  - Error rate spike (> 5%)
  - Service unavailable

# Warning alerts (notify channel)
warning:
  - Deployment taking longer than expected
  - Health check warnings
  - Resource utilization high
  - Canary analysis concerns

# Info alerts (log only)
info:
  - Deployment started
  - Deployment completed
  - Environment status changes
```

## Security in CI/CD

### Pipeline Security Checklist

- [ ] Secrets managed via secret manager (not in code)
- [ ] Service accounts with minimal permissions
- [ ] Container images signed and verified
- [ ] Dependency scanning enabled
- [ ] SAST/SCA tools configured
- [ ] Network policies in place
- [ ] Audit logging enabled
- [ ] Branch protection rules enforced

### Secrets Management

```yaml
# Never store in repository:
❌ API keys
❌ Database passwords
❌ SSH private keys
❌ TLS certificates
❌ OAuth credentials

# Use secret managers:
✅ AWS Secrets Manager
✅ HashiCorp Vault
✅ GCP Secret Manager
✅ Azure Key Vault
✅ Doppler
```

## Common Patterns

### Deployment Windows

```yaml
# Recommended deployment windows:
optimal:
  - Tuesday-Thursday
  - 10:00-15:00 (team available)
  
avoid:
  - Monday mornings (catching up)
  - Friday afternoons (weekend risk)
  - Holidays
  - End of month/quarter
  
# Emergency deployments:
require:
  - Engineering manager approval
  - Product owner notification
  - Extra monitoring
  - Rollback ready
```

### Pre-Deployment Checklist

```markdown
## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] Code review approved
- [ ] Linting passes
- [ ] No security vulnerabilities

### Testing
- [ ] Unit tests: ✅
- [ ] Integration tests: ✅
- [ ] E2E tests: ✅
- [ ] Performance tests: ✅

### Security
- [ ] SAST scan: Clean
- [ ] Dependency scan: Clean
- [ ] Secret scan: Clean
- [ ] Container scan: Clean

### Documentation
- [ ] CHANGELOG updated
- [ ] API docs updated
- [ ] Runbook updated
- [ ] Team notified

### Rollback Ready
- [ ] Backup created
- [ ] Rollback script tested
- [ ] Database migration rollback ready
- [ ] Team briefed on rollback

### Monitoring
- [ ] Dashboards updated
- [ ] Alerts configured
- [ ] On-call notified
- [ ] Status page ready
```

## Implementation Resources

Refer to the following resources in this skill for detailed implementations:

- **`resources/ci-cd-patterns.md`**: Complete CI/CD pipeline configurations for GitHub Actions, GitLab CI, Jenkins
- **`resources/deployment-strategies.md`**: Detailed implementations of rolling, blue-green, and canary deployments
- **`resources/rollback-procedures.md`**: Rollback scripts and procedures for different platforms
- **`resources/database-migrations.md`**: Safe database deployment patterns and migration scripts

## Tool Usage

### Recommended Tools

**CI/CD Platforms:**
- GitHub Actions (GitHub repositories)
- GitLab CI (GitLab repositories)
- Jenkins (self-hosted, complex workflows)
- CircleCI (SaaS, easy setup)
- ArgoCD (Kubernetes GitOps)

**Deployment:**
- Kubernetes Deployments
- Docker Compose (simple deployments)
- AWS CodeDeploy
- Google Cloud Deploy
- Azure DevOps

**Monitoring:**
- Prometheus + Grafana
- Datadog
- New Relic
- Sentry (error tracking)

## Anti-Patterns

**Avoid these deployment anti-patterns:**

❌ **Deploying on Friday** (unless emergency)
❌ **Manual deployment steps** (automate everything)
❌ **No rollback plan** (always have exit strategy)
❌ **Skipping tests** (never compromise on testing)
❌ **Deploying multiple changes** (one change at a time)
❌ **No monitoring** (blind deployments are dangerous)
❌ **Database changes after code** (schema first, then code)
❌ **Ignoring failed health checks** (always investigate)
❌ **No post-deployment verification** (always run smoke tests)
❌ **Secrets in environment variables** (use secret managers)

## Success Metrics

**Measure deployment success with:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Deployment Frequency | Daily/Weekly | Deployments per time period |
| Lead Time | < 1 day | Commit to production |
| Change Failure Rate | < 5% | Failed deployments / Total |
| MTTR | < 1 hour | Time to recover from failure |
| Rollback Rate | < 10% | Rollbacks / Total deployments |

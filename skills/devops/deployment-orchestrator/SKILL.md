---
activation_code: DEPLOYMENT_ORCHESTRATOR_V1
phase: 11
prerequisites:
  - All tests passing
  - Production readiness validated
  - Phase 5 complete
outputs:
  - Deployment artifacts
  - .signals/phase6-complete.json
  - Production deployment status
description: |
  Orchestrates deployment to production after all validations pass.
  Activates via codeword [ACTIVATE:DEPLOYMENT_ORCHESTRATOR_V1] injected by hooks
  automatically after Phase 5 completes.

  Activation trigger: [ACTIVATE:DEPLOYMENT_ORCHESTRATOR_V1]
---

# Deployment Orchestrator Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:DEPLOYMENT_ORCHESTRATOR_V1]
```

This occurs when:
- Phase 10 E2E tests pass
- Task #26 (deployment) is active
- Automatically triggered after Phase 10 completion

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-6-task-1`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 6 1
cd ./worktrees/phase-6-task-1

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# Deployment orchestration with isolation
```

### Deployment Isolation Strategy
1. **Secure deployment environment**: Deployment operations in isolated workspace
2. **Artifact isolation**: Build and deployment artifacts contained within worktree
3. **Configuration isolation**: Deployment configs managed without contamination
4. **Rollback preparation**: Rollback scripts and artifacts isolated and ready
5. **Production merge**: Final deployment merged to main with full validation


## What This Skill Does

Automates Phase 11: Production deployment in isolated worktree (fully autonomous)

- **Infrastructure validation** (Docker, Kubernetes, services)
- **Container build and startup** (docker-compose up)
- **Health check validation** (all services healthy)
- **Staging deployment** (validate) in isolated environment
- **Canary deployment** (monitor) with isolated deployment artifacts
- **Production rollout** (gradual or immediate) from clean workspace
- **Automatic progression** through all deployment stages
- **Rollback capability** (if issues detected) with isolated rollback scripts
- **NEW**: Isolated deployment environment prevents contamination
- **NEW**: Secure artifact management within worktree boundaries

## Execution Flow

```
Stage 0: Automated Validation
         - Run security validation
         - Run load testing
         - Validate performance targets
         - BLOCK if any validation fails
Stage 1: Infrastructure Setup
         - Build Docker containers (docker-compose build)
         - Start all services (docker-compose up -d)
         - Validate health checks
         - Verify connectivity
Stage 2: Pre-Deployment Validation
         - Check all tests passing
         - Validate production readiness score
Stage 3: Staging Deployment
         - Deploy to staging environment
         - Run smoke tests
         - Validate monitoring
         - Auto-proceed on success
Stage 4: Canary Deployment
         - Deploy to 5% of production traffic
         - Monitor metrics
         - Compare metrics vs baseline
         - Auto-proceed if metrics healthy
Stage 5: Production Rollout
         - Gradual rollout (10% → 50% → 100%)
         - OR immediate (100%)
         - Monitor continuously
Stage 6: Post-Deployment Validation
         - Verify all services healthy
         - Confirm metrics normal
         - Generate completion report
```

## Deployment Strategy

### Stage 0: Automated Validation (MUST RUN FIRST)

```bash
# Run all automated validators - BLOCKS deployment if any fail
echo "==============================================================================="
echo "Stage 0: Automated Validation"
echo "==============================================================================="

# Security validation
echo ""
echo "Running security validation..."
./hooks/security-validator.sh || {
    echo "❌ Security validation FAILED - deployment blocked"
    exit 1
}

# Load testing
echo ""
echo "Running load tests..."
./hooks/load-test-validator.sh || {
    echo "❌ Load testing FAILED - deployment blocked"
    exit 1
}

# Performance validation
echo ""
echo "Validating performance targets..."
./hooks/performance-validator.sh || {
    echo "⚠️  Performance validation failed but continuing (check PRD requirements)"
}

echo ""
echo "✅ All automated validations PASSED"
echo "Proceeding to infrastructure setup..."
```

**CRITICAL:**
- These validators MUST pass before proceeding
- Security failures = hard block
- Load test failures = hard block
- Performance failures = warning (may continue if targets not in PRD)

---

### Infrastructure Setup
```bash
# Build and start Docker containers
docker-compose build
docker-compose up -d

# Wait for services to be healthy
timeout 300 bash -c 'until docker-compose ps | grep -v "unhealthy\|starting"; do sleep 10; done'

# Verify all services running
docker-compose ps
docker-compose logs --tail=50
```

### Staging
```bash
# Deploy to staging
./scripts/deploy.sh staging

# Run smoke tests
npm test:smoke

# Validate
./scripts/health-check.sh staging
```

### Canary (automatic)
```bash
# Deploy 5% traffic
./scripts/deploy.sh canary --traffic=5

# Monitor metrics automatically
# Watch: error rate, latency, throughput

# Auto-proceed if metrics healthy
# Auto-rollback if metrics degrade
```

### Production (automatic)
```bash
# Gradual rollout
./scripts/deploy.sh prod --traffic=10
# Monitor, auto-proceed if healthy
./scripts/deploy.sh prod --traffic=50
# Monitor, auto-proceed if healthy
./scripts/deploy.sh prod --traffic=100

# OR immediate (if canary validated)
./scripts/deploy.sh prod --traffic=100
```

## Automatic Validation Gates

### Gate 1: Staging → Canary (Auto)
**Required checks (automated):**
- ✅ Staging deployment successful
- ✅ Smoke tests passing
- ✅ No errors in logs
- ✅ Monitoring dashboards healthy

**Action:** Auto-proceed to canary if all checks pass

### Gate 2: Canary → Production (Auto)
**Required checks (automated):**
- ✅ Canary metrics stable
- ✅ Error rate ≤ baseline
- ✅ Latency ≤ baseline +10%

**Action:** Auto-proceed to production if metrics healthy

## Rollback Triggers

**Automatic rollback if:**
- Error rate > baseline + 50%
- Latency > baseline + 100%
- Critical service down > 1 min

**Manual rollback:**
```bash
./scripts/rollback.sh
```

## Monitoring Dashboard

**Key metrics:**
- Request rate (req/sec)
- Error rate (%)
- Latency (p50, p95, p99)
- CPU usage (%)
- Memory usage (%)
- Database connections

## Time Estimates

| Phase | Duration |
|-------|----------|
| Staging | 30 min |
| Canary | 24 hours |
| Production | 2-8 hours |
| **Total** | **25-32 hours** |

## Completion Signal

```json
{
  "phase": 11,
  "status": "success",
  "summary": {
    "deployed_to": "production",
    "traffic": 100,
    "health": "green",
    "rollbacks": 0
  },
  "pipeline_complete": true
}
```

## Output Files

```
.taskmaster/
├── DEPLOYMENT_REPORT.md
└── .signals/phase11-complete.json

logs/
├── deployment-staging.log
├── deployment-canary.log
└── deployment-production.log
```

## CRITICAL: Fully Autonomous Deployment

**DO NOT ASK THE USER FOR PERMISSION AT ANY DEPLOYMENT STAGE.**

This skill automatically progresses through all deployment stages:
1. Staging → (auto-proceed on success)
2. Canary → (auto-proceed if metrics healthy)
3. Production → (auto-proceed with gradual rollout)

When deployment is complete, output:
```
✅ PHASE 11 COMPLETE - DEPLOYMENT SUCCESSFUL
[SIGNAL:PHASE11_COMPLETE]
🎉 PIPELINE COMPLETE - Application deployed to production
```

**The entire pipeline from Phase 6 onward is fully autonomous.**
**Do not ask "Would you like to proceed?" at any stage - just proceed automatically.**

## See Also

- Pipeline Orchestrator (triggers this, manages approvals)
- E2E Validator (Phase 10, provides GO decision)
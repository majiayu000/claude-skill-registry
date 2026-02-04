---
name: deployment-validator
description: Validate release readiness through comprehensive pre-deployment checks. Use before deploying schedules, features, or infrastructure changes to production.
model_tier: opus
parallel_hints:
  can_parallel_with: [code-review, test-writer, security-audit]
  must_serialize_with: [database-migration]
  preferred_batch_size: 1
context_hints:
  max_file_context: 30
  compression_level: 2
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "FAIL|BLOCK"
    reason: "Deployment blockers require human decision"
  - keyword: ["database", "migration", "schema"]
    reason: "Database changes need careful validation"
---

# Deployment Validator Skill

Comprehensive pre-deployment validation to ensure production readiness and minimize deployment risk.

## When This Skill Activates

- Before deploying any code to production
- Before finalizing a new schedule for deployment
- Before applying database migrations
- Before infrastructure changes
- During emergency hotfix deployment

## Validation Framework

### Pre-Deployment Checklist

**Code Quality Gate**
- [ ] All tests passing (unit, integration, e2e)
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Code coverage requirements met
- [ ] Security audit completed
- [ ] No critical/blocker issues

**Database Migration Gate**
- [ ] Migration tested on staging
- [ ] Rollback procedure documented
- [ ] Data backup created
- [ ] Migration time estimated
- [ ] Backward compatibility verified

**Schedule Deployment Gate**
- [ ] Schedule validated for ACGME compliance
- [ ] Coverage gaps resolved
- [ ] Faculty approvals obtained
- [ ] Resident notifications ready
- [ ] Contingency plan documented

**Infrastructure Gate**
- [ ] Capacity verified
- [ ] Monitoring configured
- [ ] Alerting rules active
- [ ] Rollback plan documented
- [ ] Health checks configured

### Phase 1: Code and Quality Validation

```
1. Check test results
   - Unit tests: must pass
   - Integration tests: must pass
   - Coverage: must exceed threshold

2. Run security checks
   - OWASP Top 10 scan
   - Dependency vulnerability check
   - Secrets detection

3. Verify code quality
   - Linting: must pass
   - Type checking: must pass
   - Complexity: within limits
```

### Phase 2: Database Readiness

```
1. Migration validation
   - Syntactically correct
   - No unsafe operations
   - Tested on copy of prod data
   - Rollback working

2. Data integrity
   - Backup created
   - Constraints still satisfied
   - Foreign keys valid
   - Indexes updated

3. Performance
   - Migration time acceptable
   - No long locks
   - Monitoring in place
```

### Phase 3: Schedule Validation

```
1. Compliance check
   - ACGME rules verified
   - Coverage adequate
   - Staffing realistic

2. Operational check
   - Faculty confirmed availability
   - Rotation timing valid
   - Contingencies in place

3. Communication
   - Residents notified
   - Faculty acknowledged
   - Adjustments documented
```

### Phase 4: Infrastructure and Monitoring

```
1. Capacity verification
   - CPU/memory adequate
   - Database connections sufficient
   - Network bandwidth available

2. Monitoring setup
   - Metrics collection active
   - Alerting rules configured
   - Dashboards ready
   - Health checks in place

3. Incident response
   - On-call team ready
   - Rollback procedure documented
   - Communication channels ready
```

## Risk Assessment Matrix

| Risk Factor | Low | Medium | High |
|-------------|-----|--------|------|
| Code changes | <100 lines | 100-500 lines | >500 lines |
| Test coverage | >90% | 80-90% | <80% |
| Database changes | Add column | Schema restructure | Table drop |
| Deployment scope | Single component | Multiple components | System-wide |
| Rollback time | <5 minutes | 5-30 minutes | >30 minutes |

**Risk Score = Sum of risk levels**
- Low risk (0-5): Proceed with review
- Medium risk (6-12): Require additional testing
- High risk (13+): Escalate to human decision

## Deployment Validation Report

```markdown
## Deployment Readiness Report

**Release:** [VERSION]
**Date:** [DATETIME]
**Deployment Type:** [CODE/DATABASE/SCHEDULE/INFRA]

### Risk Assessment
- Overall Risk Level: [LOW/MEDIUM/HIGH]
- Risk Score: [N/10]
- Blockers: [COUNT]

### Quality Gates
- [x] Code quality
- [x] Tests passing
- [x] Security audit
- [x] Performance acceptable
- [x] Monitoring ready

### Deployment Checklist
- [ ] Pre-deployment steps complete
- [ ] Rollback procedure documented
- [ ] Team notification sent
- [ ] Health checks configured
- [ ] On-call team briefed

### Critical Items
[List anything requiring attention before deployment]

### Recommendation
- [APPROVED / CONDITIONAL / BLOCKED]

### Next Steps
1. [Action 1]
2. [Action 2]
```

## Quick Validation Commands

```bash
# Full deployment validation
python -m app.deployment.validator --release=current --full

# Skip tests (if already run)
python -m app.deployment.validator --release=current --skip-tests

# Database migration check
python -m app.deployment.validator --type=migration --path=alembic/versions/xxx

# Schedule deployment validation
python -m app.deployment.validator --type=schedule --schedule_id=current
```

## Common Deployment Scenarios

### Scenario 1: Hotfix Deployment
**Risk:** Medium (time pressure + changes)
**Validation:**
- Tests for hotfix passes
- No regression in related tests
- Rollback tested
- Communication plan ready

### Scenario 2: Major Feature Release
**Risk:** High (large change scope)
**Validation:**
- Full test suite passes
- Staged rollout plan
- Monitoring for metrics
- Communication multi-channel

### Scenario 3: Database Migration
**Risk:** Variable (depends on scope)
**Validation:**
- Migration tested on staging
- Data backup confirmed
- Rollback tested
- Downtime window approved

### Scenario 4: Schedule Deployment
**Risk:** Medium (operational impact)
**Validation:**
- ACGME compliant
- Coverage verified
- Staffing confirmed
- Contingency documented

## Escalation Decision Tree

```
Are there deployment blockers?
├─ YES → BLOCK deployment
│  └─ Escalate to human decision
└─ NO → Continue

Are there critical warnings?
├─ YES → Require human approval
│  └─ Document reasoning
└─ NO → Continue

Is rollback time acceptable?
├─ NO → Require automated rollback setup
└─ YES → Proceed

Is on-call team ready?
├─ NO → Delay deployment
└─ YES → APPROVED for deployment
```

## References

- See PROMPT_LIBRARY.md for deployment validation templates
- See CLAUDE.md for deployment procedures
- Incident response procedures in incident-responder skill


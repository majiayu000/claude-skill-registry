---
name: deployment-automation-enforcer
description: 'Use when designing deployment pipelines, CI/CD, terraform, or infrastructure
  automation. Enforces rollback checkpoint then TodoWrite with 19+ items. Triggers:
  "deploy", "CI/CD", "kubernetes", "terrafo'
---

---
name: deployment-automation-enforcer
description: Use when designing deployment pipelines, CI/CD, terraform, or infrastructure automation. Enforces rollback checkpoint then TodoWrite with 19+ items. Triggers: "deploy", "CI/CD", "kubernetes", "terraform". If thinking "rollback later" - use this first.
---

# Deployment Automation Enforcer

## ROLLBACK CHECKPOINT (COMPLETE FIRST)

**MANDATORY before creating TodoWrite:**

- [ ] Rollback script exists? [Path: _______ | or "NEW - will create first"]
- [ ] Tested in staging? [Date: _______ | or "must test before production"]
- [ ] Duration measured? [_____ minutes]
- [ ] Triggers defined? [List: _______]

**Why first:** 27% skip rollback when checkpoint appears later.

---

## TodoWrite Requirements

**CREATE TodoWrite** with 4 sections (19+ items total):

| Section | Min Items | Order |
|---------|-----------|-------|
| Automation | 5+ | 1st |
| Observability | 5+ | 2nd (BEFORE Failure Recovery) |
| Failure Recovery | 5+ | 3rd (requires Observability) |
| Verification | 4+ | 4th |

**Section order matters:** You cannot define failure recovery without observability to detect failures.

---

## Verification Checkpoint

After creating TodoWrite, verify 3 random items:

**Each item must have ALL THREE:**
- ✓ Concrete numbers/thresholds ("error rate > 5%", "15 min timeout")
- ✓ Specific tools ("GitHub Actions", "CloudWatch", "PagerDuty")
- ✓ Measurable outcome ("rollback tested on [date]", "alert fires within 5min")

| ❌ FAILS | ✅ PASSES |
|----------|-----------|
| "Add monitoring" | "CloudWatch: `deployment.duration_seconds`, Grafana dashboard at `/dashboards/deployments`, PagerDuty alert if error rate > 5% for 3min" |
| "Implement rollback" | "Rollback `.github/workflows/rollback.yml` reverts to previous Docker tag from S3 `deployment-history/latest-stable.txt`. Triggers: manual OR error rate > 5% for 3min. Target: < 5 minutes. Test staging on [date]" |

---

## Section Requirements

### Automation (5+ items)
- [ ] Identify manual steps in current deployment
- [ ] Replace with automated scripts/workflows (GitHub Actions, GitLab CI)
- [ ] Idempotency checks for safe re-runs
- [ ] Rollback automation for this change
- [ ] Document exceptions for remaining manual steps

### Observability (5+ items) - BEFORE Failure Recovery
- [ ] Deployment logging (structured: deployment-id, timestamps, steps)
- [ ] Failure alerts (PagerDuty/SNS on failure, error rate spike)
- [ ] Metrics (duration, success rate in CloudWatch/Datadog)
- [ ] Health endpoint (`/health` returns 200 + dependency status)
- [ ] Log/metric locations documented

### Failure Recovery (5+ items) - AFTER Observability
- [ ] Failure scenarios defined (won't start, migration fails, health check fails)
- [ ] Automated rollback triggers (error rate > X%, failed health checks Y minutes)
- [ ] Health checks post-deployment
- [ ] Rollback tested in staging (date, duration, success)
- [ ] Manual recovery documentation as last resort

### Verification (4+ items)
- [ ] Pre-deployment tests automated (unit, integration, lint)
- [ ] Smoke tests post-deployment (critical flows, key endpoints)
- [ ] Monitoring/alerts verified working (trigger test alert)
- [ ] Rollback procedure accessible (script in repo, documented)

---

## Red Flags - STOP When You Think:

| Thought | Reality | Data |
|---------|---------|------|
| "Manual deploy is broken, need automation fast" | Automating without rollback creates WORSE problems | 27% skip rollback |
| "We'll add monitoring/rollback after" | Can't detect/recover from failures without them | 80% never add "later" |
| "Rollback is overkill" | Manual recovery ALWAYS takes 10x longer | 30+ min manual vs 2 min automated |
| "We can manually revert" | Detect (no monitoring) + find version (no automation) + apply (error-prone) | 30+ min |

---

## Response Templates

### "We'll Add Rollback Later"

❌ **BLOCKED**: Cannot deploy without rollback capability.

- 27% skip rollback when not required upfront
- 80% of "add later" items never get added
- Manual recovery takes 30+ minutes vs 2 minutes automated
- Production incidents without rollback = extended downtime + customer impact

**Required to override:**
1. Specific retrofit date (not "later")
2. Budget allocated (engineer-weeks + incident risk cost)
3. Risk acceptance signed by decision maker
4. Interim mitigation plan (24/7 on-call? manual monitoring?)

---

## Override Requirements

To skip ANY requirement, provide ALL 4:
1. Specific retrofit date (not "later")
2. Budget allocated (engineer-weeks + incident risk)
3. Risk acceptance signed by decision maker
4. Interim mitigation plan (24/7 on-call? manual monitoring?)

---

## Self-Grading Before Complete

```
[ ] 19+ items across 4 sections
[ ] 80%+ items have concrete numbers
[ ] 80%+ items name specific tools
[ ] 100% items have measurable outcomes
[ ] 3 random items pass specificity test
[ ] Rollback checkpoint completed
[ ] Observability BEFORE Failure Recovery (correct order)

Grade 7+/8: Ready to proceed
Grade <7: Revise TodoWrite
```

---

## Evidence Collection

Before marking complete:
- [ ] Automation code link (workflow file URL)
- [ ] Staging deployment log (screenshot/excerpt)
- [ ] Monitoring dashboard screenshot
- [ ] Rollback test evidence (log with timestamp, duration)
- [ ] Alert test confirmation

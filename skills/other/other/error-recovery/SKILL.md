---
name: error-recovery
description: Classify workflow failures and attempt automatic recovery. Use when sprint/feature fails during implementation to determine if auto-fix is possible or manual intervention required.
---

<objective>
Classify workflow failures into actionable categories and execute recovery strategies.

Use this skill when:
- Sprint fails during /implement-epic
- Feature fails during /implement
- Quality gate blocks deployment
- Any workflow phase returns FAILED status
</objective>

<quick_start>
When a workflow component fails:

1. **Classify the failure** using the decision tree below
2. **If fixable**: Execute auto-fix strategies (max 3 attempts)
3. **If critical**: Stop immediately, report to user
4. **If unknown**: Treat as critical (safe default)

Classification determines whether workflow can auto-recover or requires user intervention.
</quick_start>

<failure_classification>
## Critical Blockers (MUST STOP)

These failures require manual intervention - never auto-retry:

| Failure Type | Detection | Why Critical |
|--------------|-----------|--------------|
| CI Pipeline | `ci_pipeline_failed: true` in state.yaml | GitHub Actions/GitLab CI failed - indicates code issue |
| Security Scan | `security_scan_failed: true` | High/Critical CVEs found - security risk |
| Deployment | `deployment_failed: true` | Production/staging crashed - user-facing impact |
| Contract Violation | `contract_violations > 0` | API contract broken - breaks consumers |

**Action**: Stop workflow, report error details, require `/continue` after manual fix.

## Fixable Issues (CAN AUTO-RETRY)

These failures often resolve with automated fixes:

| Failure Type | Detection | Auto-Fix Strategies |
|--------------|-----------|---------------------|
| Test Failures | `tests_failed: true` (no CI failure) | re-run-tests, check-dependencies |
| Build Failures | `build_failed: true` | clear-cache, reinstall-deps, rebuild |
| Dependency Issues | `dependencies_failed: true` | clean-install, clear-lockfile |
| Infrastructure | `infrastructure_issues: true` | restart-services, check-ports |
| Type Errors | `type_check_failed: true` | (manual fix usually required) |

**Action**: Attempt auto-fix strategies (max 3 attempts), then escalate if all fail.

## Classification Decision Tree

```
Is CI pipeline failing?
├── Yes → CRITICAL (code issue, needs manual fix)
└── No → Continue...

Is security scan failing?
├── Yes → CRITICAL (security risk, needs review)
└── No → Continue...

Is deployment failing?
├── Yes → CRITICAL (production impact, needs rollback)
└── No → Continue...

Are tests failing (locally only)?
├── Yes → FIXABLE (try: re-run, check deps, clear cache)
└── No → Continue...

Is build failing?
├── Yes → FIXABLE (try: clear cache, reinstall, rebuild)
└── No → Continue...

Unknown failure?
└── CRITICAL (safe default - don't auto-retry unknown issues)
```
</failure_classification>

<auto_fix_strategies>
## Strategy Execution

Execute strategies in order until one succeeds. Progressive delays between attempts.

### re-run-tests
```bash
# Tests may be flaky - simple re-run often works
cd "${SPRINT_DIR}" && npm test
# or: pytest, cargo test, etc.
```
**Timeout**: 120s
**When**: Test failures that aren't CI-related

### check-dependencies
```bash
# Verify all dependencies installed
cd "${SPRINT_DIR}" && npm list --depth=0
# If missing deps found:
npm install
```
**Timeout**: 120s
**When**: Import errors, module not found

### clear-cache
```bash
# Clear build/test caches
cd "${SPRINT_DIR}"
rm -rf .next .cache coverage node_modules/.cache dist build
npm run build
```
**Timeout**: 180s
**When**: Stale cache causing build issues

### clean-install
```bash
# Nuclear option for dependency issues
cd "${SPRINT_DIR}"
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```
**Timeout**: 300s
**When**: Corrupted node_modules, lockfile conflicts

### rebuild
```bash
# Full rebuild from scratch
cd "${SPRINT_DIR}"
rm -rf dist build .next
npm run build
```
**Timeout**: 180s
**When**: Build artifacts corrupted

### restart-services
```bash
# Restart Docker/database services
docker-compose down
docker-compose up -d
sleep 10  # Wait for services to initialize
```
**Timeout**: 150s
**When**: Database connection failures, service unavailable

### check-ports
```bash
# Kill processes blocking required ports
lsof -ti:3000,5432,6379 | xargs kill -9 2>/dev/null || true
```
**Timeout**: 30s
**When**: Port already in use errors

## Retry Logic

```
Attempt 1: Try all strategies in order
  ↓ (wait 5s)
Attempt 2: Try all strategies again
  ↓ (wait 10s)
Attempt 3: Final attempt
  ↓ (if still failing)
Escalate to user (all strategies exhausted)
```

Maximum total retry time: ~15 minutes before escalation.
</auto_fix_strategies>

<usage_in_commands>
## How to Use This Skill

### In implement-epic.md or implement.md:

```markdown
When sprint/feature fails:

1. Load error-recovery skill:
   Skill("error-recovery")

2. Classify failure:
   - Read state.yaml for failure indicators
   - Apply decision tree from skill
   - Determine: CRITICAL or FIXABLE

3. If FIXABLE and auto-mode enabled:
   - Execute strategies from skill (max 3 attempts)
   - Re-check status after each attempt
   - If recovered: continue workflow
   - If exhausted: escalate

4. If CRITICAL or auto-fix exhausted:
   - Stop workflow
   - Report error with classification
   - Instruct: "Fix manually, then /continue"
```

### Example Integration:

```bash
# After sprint execution returns failure
SPRINT_STATE=$(cat "${EPIC_DIR}/sprints/${SPRINT_ID}/state.yaml")

# Check for critical blockers first
if echo "$SPRINT_STATE" | grep -q "ci_pipeline_failed: true"; then
    echo "CRITICAL: CI pipeline failed - manual fix required"
    exit 1
fi

if echo "$SPRINT_STATE" | grep -q "security_scan_failed: true"; then
    echo "CRITICAL: Security vulnerabilities detected - manual review required"
    exit 1
fi

# Check for fixable issues
if echo "$SPRINT_STATE" | grep -q "tests_failed: true"; then
    echo "FIXABLE: Tests failing - attempting auto-recovery..."
    # Execute strategies from skill
fi
```
</usage_in_commands>

<reporting>
## Error Reporting Format

When escalating to user, provide structured report:

```
═══════════════════════════════════════════════════════════════
❌ WORKFLOW FAILURE - Manual Intervention Required
═══════════════════════════════════════════════════════════════

Classification: CRITICAL | FIXABLE (exhausted)
Component: Sprint S01 | Feature F003 | Phase: optimize
Location: epics/001-auth/sprints/S01/state.yaml

Error Details:
  Type: [ci_pipeline_failed | security_scan_failed | etc.]
  Message: [Specific error message from logs]

Auto-Fix Attempts: 3/3 exhausted (if applicable)
  - re-run-tests: Failed (timeout)
  - clear-cache: Failed (build error persists)
  - clean-install: Failed (same error)

Suggested Actions:
  1. Review error logs in [path]
  2. Fix the underlying issue
  3. Run: /epic continue (or /feature continue)

═══════════════════════════════════════════════════════════════
```
</reporting>

<constraints>
## Rules

1. **Never auto-retry CRITICAL failures** - These indicate real issues needing human judgment
2. **Maximum 3 retry attempts** - Avoid infinite loops on persistent failures
3. **Progressive delays** - 5s, 10s, 15s between attempts to avoid hammering
4. **Log all attempts** - User needs visibility into what was tried
5. **Default to CRITICAL** - Unknown failures should not be auto-retried
6. **Respect auto-mode setting** - Only auto-fix when user opted in
</constraints>

<validation>
After using this skill, verify:

- [ ] Failure was correctly classified (critical vs fixable)
- [ ] Auto-fix attempts logged with results
- [ ] User received clear error report if escalated
- [ ] Workflow state updated to reflect failure
- [ ] Recovery path documented (/continue instruction)
</validation>

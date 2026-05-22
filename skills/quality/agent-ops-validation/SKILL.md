---
name: agent-ops-validation
description: "Pre-commit and pre-merge validation checks. Use before committing changes or declaring work complete to ensure all quality gates pass."
category: core
invokes: [agent-ops-state, agent-ops-baseline, agent-ops-tasks, agent-ops-api-review]
invoked_by: [agent-ops-implementation, agent-ops-critical-review, agent-ops-git]
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Validation Workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Purpose

Ensure all quality gates pass before committing changes or declaring work complete. This skill consolidates all validation checks into a single, consistent procedure.

## Validation Commands (from constitution)

```bash
# Example commands — read actual commands from .agent/constitution.md
build: npm run build          # or: uv run python -m build
lint: npm run lint            # or: uv run ruff check .
test: npm run test            # or: uv run pytest
format: npm run format        # or: uv run ruff format .
```

## Issue Operations After Validation (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create regression issue | Append to `.agent/issues/high.md` with BUG type |
| Update issue status | Edit `status:` field directly in priority file |
| List blocking issues | Search priority files for `status: blocked` |

### Example: Post-Validation Issue Creation (File-Based)

1. Read `.agent/issues/.counter`, increment, write back
2. Generate new ID: `BUG-{counter}@{hash}`
3. Append issue to `.agent/issues/high.md`:
   ```yaml
   ## BUG-NNNN@HHHHHH — New test failure: UserService.login

   id: BUG-NNNN@HHHHHH
   type: BUG
   status: todo
   priority: high
   description: Regression detected during validation

   ### Log
   - YYYY-MM-DD: Created from validation failure
   ```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| Create regression issue | `aoc issues create --type BUG --priority high --title "..."` |
| Update issue status | `aoc issues update <ID> --status done` |
| List blocking issues | `aoc issues list --status blocked` |

## API Detection

**Before running validation, check if project contains APIs:**

```yaml
api_indicators:
  - OpenAPI/Swagger spec (openapi.yaml, swagger.json, openapi.json)
  - API framework patterns (FastAPI, Flask, Express, ASP.NET controllers)
  - Route decorators (@app.route, @router.get, [HttpGet], etc.)
```

**If API detected during Tier 3 validation:**
1. Note: "API endpoints detected"
2. After standard validation, invoke `agent-ops-api-review` for contract alignment check
3. Include API review findings in validation report

## When to Use

- Before any git commit
- Before declaring a task complete
- Before critical review
- After recovery actions
- On explicit user request

## Preconditions

- `.agent/constitution.md` exists with confirmed commands
- `.agent/baseline.md` exists for comparison

## Validation Tiers

### Tier 1: Fast Checks (always run)

Run duration: < 30 seconds

1. **Syntax validation**: Files parse without errors
2. **Lint (fast mode)**: Style and obvious issues
3. **Type check** (if applicable): Static type errors
4. **Format check**: Code formatting consistent

### Tier 2: Standard Checks (before commit)

Run duration: < 5 minutes

1. All Tier 1 checks
2. **Unit tests**: Fast, isolated tests
3. **Build**: Project compiles/builds successfully
4. **Lint (full)**: Complete lint analysis

### Tier 3: Comprehensive Checks (before merge/complete)

Run duration: varies (can be slow)

1. All Tier 2 checks
2. **Integration tests**: Component interaction tests
3. **Coverage check**: Ensure coverage thresholds met
4. **Security scan** (if configured): Vulnerability detection
5. **Documentation**: Verify docs are updated

## Procedure

### Quick Validation (Tier 1)

```
1. Run lint command (fast mode if available)
2. Run type check command (if applicable)
3. Check for syntax errors in changed files
4. Report: PASS / FAIL with details
```

### Standard Validation (Tier 2)

```
1. Run Tier 1 checks
2. Run build command from constitution
3. Run unit test command from constitution
4. Compare results to baseline
5. Report: PASS / FAIL / REGRESSION
```

### Comprehensive Validation (Tier 3)

```
1. Run Tier 2 checks
2. Run full test suite
3. Run coverage analysis
4. Run security checks (if configured)
5. Verify documentation updated
6. Compare all results to baseline
7. Report: PASS / FAIL / REGRESSION with full details
```

## Validation Report Format

```markdown
## Validation Report - [timestamp]

### Summary
- Tier: [1|2|3]
- Result: [PASS|FAIL|REGRESSION]
- Duration: [time]

### Checks Performed

| Check | Status | Details |
|-------|--------|---------|
| Lint | ✅ PASS | 0 errors, 2 warnings (baseline: 2) |
| Build | ✅ PASS | Exit code 0 |
| Tests | ⚠️ REGRESSION | 1 new failure (see below) |

### Failures (if any)

#### Test Failure: test_feature_x
- File: tests/test_feature.py:42
- Error: AssertionError: expected X, got Y
- Baseline: PASS (new regression)

### Warnings (if any)

- lint: unused variable 'foo' in file.py:10 (pre-existing)

### Recommendation

[PROCEED | FIX REQUIRED | INVESTIGATE]
```

## Baseline Comparison Rules

### New Finding Categories

| Category | Action |
|----------|--------|
| New error | **BLOCK** - must fix before proceeding |
| New warning | **INVESTIGATE** - fix or document why acceptable |
| New test failure | **BLOCK** - must fix or prove pre-existing |
| Improved (fewer issues) | **PASS** - note improvement |
| Same as baseline | **PASS** - no change |

### Handling Regressions

1. Identify if regression is from agent's changes
2. If yes: fix before proceeding
3. If no (pre-existing): document and escalate as task
4. Never ignore regressions silently

## Integration Points

### With agent-ops-git

Before committing:
```
1. Run Tier 2 validation
2. If PASS: proceed with commit
3. If FAIL: abort commit, report issues
```

### With agent-ops-critical-review

During review:
```
1. Run Tier 3 validation
2. Include validation report in review
3. Block completion if FAIL or REGRESSION
```

### With agent-ops-implementation

After each step:
```
1. Run Tier 1 validation (fast feedback)
2. After final step: run Tier 2 validation
```

## Quality Gate Configuration

### Confidence-Based Coverage Thresholds

**Coverage requirements vary by confidence level:**

| Confidence | Line Coverage | Branch Coverage | Gate Type |
|------------|---------------|-----------------|----------|
| LOW | ≥90% on changed code | ≥85% on changed code | HARD (blocks) |
| NORMAL | ≥80% on changed code | ≥70% on changed code | SOFT (warning) |
| HIGH | Tests pass | N/A | None |

**During Tier 3 validation, check coverage against confidence threshold:**

```
🎯 COVERAGE VALIDATION — {CONFIDENCE} Confidence

| Metric | Required | Actual | Status |
|--------|----------|--------|--------|
| Line coverage | ≥{threshold}% | {actual}% | {PASS/FAIL} |
| Branch coverage | ≥{threshold}% | {actual}% | {PASS/FAIL} |

{If FAIL for LOW confidence:}
⛔ COVERAGE THRESHOLD NOT MET — Cannot proceed

Options:
1. Add more tests to reach threshold
2. Document why threshold is unachievable (requires justification)
```

### Constitution-Based Configuration

Read from `.agent/constitution.md`:

```markdown
## Quality gates
- lint_must_pass: true | false
- build_must_pass: true
- tests_must_pass: true
- coverage_threshold: 80% | none
- allow_warnings: true | false
- security_scan: true | false
```

If not configured, defaults:
- lint_must_pass: true
- build_must_pass: true  
- tests_must_pass: true
- coverage_threshold: none
- allow_warnings: true
- security_scan: false

## Commands

All validation commands MUST come from constitution. Never guess or assume commands.

```markdown
## From constitution:
- build: [constitution build command]
- lint: [constitution lint command]
- test: [constitution test command]
- format: [constitution format command]
```

## Output

Update `.agent/focus.md` with validation results:
```markdown
## Just did
- Ran Tier 2 validation: PASS
  - lint: 0 errors, 2 warnings (baseline match)
  - build: success
  - tests: 45 pass, 0 fail
```

## Issue Discovery After Validation

**After validation, invoke `agent-ops-tasks` discovery procedure for new findings:**

1) **Collect regressions and new issues:**
   - New test failures → `BUG` (high/critical)
   - New lint errors → `BUG` (medium)
   - New warnings → `CHORE` (low)
   - Coverage drops → `TEST` (medium)
   - Security findings → `SEC` (high/critical)

2) **Present to user:**
   ```
   📋 Validation found {N} new issues vs baseline:
   
   Critical:
   - [BUG] New test failure: UserService.login
   
   High:
   - [SEC] New security warning from npm audit
   
   Medium:
   - [BUG] 2 new lint errors in PaymentController
   
   Create issues to track these? [A]ll / [S]elect / [N]one
   
   Note: These MUST be fixed before commit/merge.
   ```

3) **After creating issues:**
   ```
   Created {N} issues. These block commit/merge.
   
   1. Start fixing highest priority (BUG-0024@abc123)
   2. View all blocking issues
   3. Abort current work
   ```

```

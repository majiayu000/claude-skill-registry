---
name: quality-capture-baseline
description: |
  Captures quality metrics baseline (tests, coverage, type errors, linting, dead code) by running
  quality gates and storing results in memory for regression detection. Use at feature start,
  before refactor work, or after major changes to establish baseline. Triggers on "capture baseline",
  "establish baseline", or PROACTIVELY at start of any feature/refactor work. Works with pytest
  output, pyright errors, ruff warnings, vulture results, and memory MCP server for baseline storage.
allowed-tools:
  - Bash
  - Read
  - mcp__memory__create_entities
  - mcp__memory__add_observations
---

# Capture Quality Baseline

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Baseline establishment for regression detection
- [Quick Start](#quick-start) - When to invoke and basic usage
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Prepare Context](#step-1-prepare-context) - Feature name, git commit, timestamp
  - [Step 2: Run Quality Checks](#step-2-run-quality-checks) - Primary and fallback methods
  - [Step 3: Parse Metrics](#step-3-parse-metrics) - Extract tests, coverage, type errors, linting, dead code
  - [Step 4: Create Memory Entity](#step-4-create-memory-entity) - Store baseline in memory system
  - [Step 5: Return Baseline Reference](#step-5-return-baseline-reference) - Success output format
- [Agent Integration](#agent-integration) - @planner, @implementer, @statuser workflows
- [Edge Cases](#edge-cases) - Quality check failures, no git, missing scripts, memory unavailable
- [Anti-Patterns](#anti-patterns) - What to avoid and what to do instead
- [Integration with Other Skills](#integration-with-other-skills) - run-quality-gates, validate-refactor-adr, manage-refactor-markers, manage-todo
- [Examples](#examples) - Comprehensive scenarios reference
- [Reference](#reference) - Parsing, lifecycle, quality gates documentation
- [Success Criteria](#success-criteria) - Validation checklist
- [Troubleshooting](#troubleshooting) - Common problems and solutions

## Purpose

Establish a quality metrics baseline at the start of a feature or refactor so that subsequent quality gate runs can detect regressions. This skill is a critical component of the project's regression detection strategy.

## When to Use

Use this skill when:
- Starting any new feature (before writing code)
- Beginning refactor work (to document pre-state)
- After major changes (dependency upgrades, architecture shifts)
- When @planner creates a new todo.md
- When @implementer starts task 0 of a feature
- User asks to "capture baseline" or "establish baseline metrics"
- Before major architectural changes to track impact

## Quick Start

**When to invoke this skill:**
- ✅ At the START of any new feature (before writing code)
- ✅ Before beginning refactor work (to document pre-state)
- ✅ After major changes (dependency upgrades, architecture shifts)
- ❌ NOT after you've already started coding (too late)

**Basic usage:**
```
1. Run quality checks: ./scripts/check_all.sh
2. Parse metrics (tests, coverage, type errors, linting, dead code)
3. Create memory entity: baseline_{feature}_{date}
4. Return baseline reference for future comparison
```

## Instructions

### Step 1: Prepare Context

**Before running quality checks, gather:**
- Feature name or refactor identifier (e.g., "auth", "service-result-migration")
- Current git commit hash: `git rev-parse HEAD`
- Current timestamp: `date +"%Y-%m-%d %H:%M:%S"`

**Example:**
```bash
FEATURE="user_profile"
GIT_COMMIT=$(git rev-parse HEAD)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +"%Y-%m-%d")
```

### Step 2: Run Quality Checks

**Primary method (recommended):**
```bash
./scripts/check_all.sh
```

**Fallback (if check_all.sh fails):**
```bash
# Run individual checks
uv run pytest tests/ -v --cov=src --cov-report=term-missing
uv run pyright src/
uv run ruff check src/
uv run vulture src/
```

**Capture output:**
- Store stdout and stderr
- Measure execution time
- Note any failures (document them, don't skip)

### Step 3: Parse Metrics

Use the parsing patterns from `references/parsing.md`. Quick reference:

**Tests:**
```bash
# Pattern: "X passed" or "X failed" or "X skipped"
PASSED=$(grep -oE "[0-9]+ passed" output.txt | grep -oE "[0-9]+")
FAILED=$(grep -oE "[0-9]+ failed" output.txt | grep -oE "[0-9]+")
SKIPPED=$(grep -oE "[0-9]+ skipped" output.txt | grep -oE "[0-9]+")
```

**Coverage:**
```bash
# Pattern: "TOTAL ... X%"
COVERAGE=$(grep "TOTAL" output.txt | grep -oE "[0-9]+%" | tail -1)
```

**Type Errors:**
```bash
# Pattern: "X errors, Y warnings" or "0 errors"
TYPE_ERRORS=$(grep -oE "[0-9]+ error" output.txt | grep -oE "[0-9]+" | head -1)
```

**Linting:**
```bash
# Pattern: "Found X errors"
LINTING_ERRORS=$(grep -oE "Found [0-9]+ error" output.txt | grep -oE "[0-9]+")
```

**Dead Code:**
```bash
# Pattern: Count vulture output lines or "X% unused"
DEAD_CODE=$(vulture src/ 2>&1 | grep -v "^$" | wc -l | xargs)
```

**Execution Time:**
```bash
# Measure with time command or calculate from timestamps
EXEC_TIME=$(echo "scale=1; $END_TIME - $START_TIME" | bc)
```

### Step 4: Create Memory Entity

**Entity structure:**
```yaml
name: quality-capture-baseline
type: quality_baseline
observations:
  - "Tests: {passed} passed, {failed} failed, {skipped} skipped"
  - "Coverage: {coverage}%"
  - "Type errors: {type_errors}"
  - "Linting errors: {linting_errors}"
  - "Dead code: {dead_code} items"
  - "Execution time: {exec_time}s"
  - "Git commit: {git_hash}"
  - "Timestamp: {timestamp}"
  - "Feature: {feature_name}"
```

**Example:**
```python
mcp__memory__create_entities({
    "entities": [{
        "name": f"baseline_{feature}_{date}",
        "type": "quality_baseline",
        "observations": [
            f"Tests: {passed} passed, {failed} failed, {skipped} skipped",
            f"Coverage: {coverage}%",
            f"Type errors: {type_errors}",
            f"Linting errors: {linting_errors}",
            f"Dead code: {dead_code} items",
            f"Execution time: {exec_time}s",
            f"Git commit: {git_commit}",
            f"Timestamp: {timestamp}",
            f"Feature: {feature}"
        ]
    }]
})
```

**If pre-existing issues exist:**
Add additional observation:
```
"Pre-existing issues: 3 type errors in legacy code (documented, will not be fixed)"
```

### Step 5: Return Baseline Reference

**Success output format:**
```
✅ Baseline captured: baseline_{feature}_{date}

Metrics:
- Tests: {passed} passed ({coverage}% coverage)
- Type safety: {status} ({type_errors} errors)
- Code quality: {status} ({linting_errors} linting, {dead_code} dead code items)
- Execution: {exec_time}s
- Git: {git_hash}

Use this baseline for regression detection.
```

**With pre-existing issues:**
```
✅ Baseline captured: baseline_{feature}_{date}

Metrics:
- Tests: 152 passed (89% coverage)
- Type safety: 3 errors (pre-existing, documented)
- Code quality: Clean
- Git: abc123f

⚠️  Note: 3 pre-existing type errors documented, will not cause regression failures.

Use this baseline for regression detection.
```

## Agent Integration

### @planner Usage

**When:** At plan creation, BEFORE creating todo.md

**Workflow:**
1. Receive feature request from user
2. Analyze requirements
3. **→ Invoke capture-quality-baseline**
4. Receive baseline reference
5. Create todo.md with baseline in header
6. Create memory entities linking to baseline

**Example:**
```markdown
# Todo: User Profile Feature
Baseline: baseline_user_profile_2025-10-16
Created: 2025-10-16

## Tasks
- [ ] Task 1 (references baseline for quality gates)
...
```

### @implementer Usage

**When:** At feature start (task 0) or before refactor work

**Workflow:**
1. Validate ADR (if refactor) using validate-refactor-adr
2. **→ Invoke capture-quality-baseline**
3. Receive baseline reference
4. Reference baseline in quality gate runs
5. Compare final metrics against baseline

**Example:**
```
User: "Start implementing authentication"

@implementer:
1. Invoke capture-quality-baseline
2. Receives: baseline_auth_2025-10-16
3. Begin task 1 implementation
4. After each task: Run quality gates, compare to baseline
5. Report: "All metrics maintained or improved from baseline"
```

### @statuser Usage

**When:** User requests baseline recapture or progress check

**Workflow:**
1. Receive progress check request
2. If major changes detected: **→ Invoke capture-quality-baseline**
3. Compare new baseline to original
4. Report delta and recommend re-baseline if appropriate

**Example:**
```
User: "Check progress after dependency upgrade"

@statuser:
1. Detects major change (dependency upgrade)
2. Invokes capture-quality-baseline
3. Receives: baseline_post_upgrade_2025-10-16
4. Compares to original baseline
5. Reports: "2 tests removed (deprecated APIs), coverage maintained, type errors resolved"
```

## Edge Cases

### Quality Checks Fail

**Scenario:** Some checks fail during baseline capture

**Handling:**
1. Still capture the baseline (document failures)
2. Add observation: "Baseline captured WITH failures"
3. Flag in output: "⚠️ Baseline has failures - must fix before feature work"
4. Return baseline reference (still usable for comparison)

**Example:**
```
✅ Baseline captured: baseline_auth_2025-10-16

⚠️  WARNING: Baseline has failures

Metrics:
- Tests: 140 passed, 5 FAILED, 2 skipped
- Type safety: 2 errors
- Code quality: 3 linting errors

🛑 FIX these failures before starting feature work.
```

### No Git Repository

**Scenario:** Not in a git repository (or git not available)

**Handling:**
1. Skip git commit capture
2. Continue with other metrics
3. Add observation: "No git commit (not in repository)"
4. Note in output: "Git: Not available"

### Script Not Found

**Scenario:** `./scripts/check_all.sh` doesn't exist

**Handling:**
1. Try individual checks (pytest, pyright, ruff, vulture)
2. If any work: Use those results
3. If none work: Report error and abort

**Error message:**
```
❌ Cannot capture baseline: Quality check scripts not found

Tried:
- ./scripts/check_all.sh (not found)
- uv run pytest (not found)
- uv run pyright (not found)

Cannot establish baseline without quality checks.
```

### Memory Service Unavailable

**Scenario:** Cannot create memory entity (MCP server down)

**Handling:**
1. Store baseline in local file: `.quality-baseline-{feature}-{date}.json`
2. Return file path as reference
3. Note in output: "Baseline stored locally (memory unavailable)"

**Fallback file format:**
```json
{
  "baseline_name": "baseline_auth_2025-10-16",
  "metrics": {
    "tests": {"passed": 145, "failed": 0, "skipped": 2},
    "coverage": 87,
    "type_errors": 0,
    "linting_errors": 0,
    "dead_code": 3,
    "execution_time": 8.3,
    "git_commit": "abc123f",
    "timestamp": "2025-10-16 10:30:00"
  }
}
```

## Anti-Patterns

❌ **DON'T:**
- Skip baseline capture (regression detection requires it)
- Reuse old baselines for new features (each feature needs its own)
- Capture baseline after starting work (too late)
- Ignore failing checks in baseline (document them)
- Forget to reference baseline in todo.md

✅ **DO:**
- Capture baseline BEFORE any feature work
- Create unique baseline per feature
- Document pre-existing issues in baseline
- Reference baseline in todo.md and memory
- Re-baseline after major changes (upgrades, migrations)

## Integration with Other Skills

**Skill: run-quality-gates**
- capture-quality-baseline: Establishes the reference point
- run-quality-gates: Compares current metrics against baseline

**Skill: validate-refactor-adr**
- validate-refactor-adr: Validates ADR completeness
- capture-quality-baseline: Documents pre-refactor state

**Skill: manage-refactor-markers**
- capture-quality-baseline: Establishes pre-refactor metrics
- manage-refactor-markers: Tracks refactor progress

**Skill: manage-todo**
- capture-quality-baseline: Provides baseline reference
- manage-todo: Stores baseline name in todo.md header

## Examples

See `examples.md` for comprehensive scenarios:
1. Feature start baseline (clean state)
2. Refactor start baseline (with pre-existing issues)
3. Re-baseline after major change
4. Baseline with failures
5. Agent auto-invocation patterns
6. Cross-agent baseline sharing
7. Baseline comparison workflows
8. Recovery from failed baseline capture

## Reference

- **Metrics parsing:** See `references/parsing.md` for detailed parsing logic
- **Baseline lifecycle:** See `references/lifecycle.md` for management best practices
- **Quality gates:** See project's `../run-quality-gates/references/shared-quality-gates.md` for gate definitions

## Success Criteria

- [ ] Quality checks execute successfully (or failures documented)
- [ ] All 5 metrics extracted (tests, coverage, type errors, linting, dead code)
- [ ] Memory entity created with baseline data
- [ ] Baseline name returned for reference
- [ ] Execution time < 30 seconds (typically ~8s)
- [ ] Git commit captured (if available)
- [ ] Timestamp recorded
- [ ] Pre-existing issues documented (if any)

## Troubleshooting

**Problem:** Metrics parsing fails (empty values)

**Solution:**
1. Check quality check output format (may have changed)
2. Review parsing patterns in `references/parsing.md`
3. Update regex patterns if needed
4. Fallback: Manually parse critical metrics

**Problem:** Baseline creation succeeds but can't be found later

**Solution:**
1. Verify memory entity name format: `baseline_{feature}_{date}`
2. Search memory: `mcp__memory__search_memories(query="baseline")`
3. Check fallback file: `.quality-baseline-*.json`

**Problem:** Quality checks take too long (> 30s)

**Solution:**
1. Check if Neo4j is running (connection timeout)
2. Skip slow tests: `pytest -m "not slow"`
3. Run checks in parallel (check_all.sh does this)
4. Report timing issue to user

---

**Last Updated:** 2025-10-16
**Priority:** High (critical for regression detection)
**Dependencies:** Quality gate scripts, memory MCP server

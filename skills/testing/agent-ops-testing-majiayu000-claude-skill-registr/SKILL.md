---
name: agent-ops-testing
description: "Test strategy, execution, and coverage analysis. Use when designing tests, running test suites, or analyzing test results beyond baseline checks."
category: core
invokes: [agent-ops-state, agent-ops-tasks, agent-ops-debugging]
invoked_by: [agent-ops-planning, agent-ops-implementation, agent-ops-critical-review]
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Testing Workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Purpose

Provide structured guidance for test design, execution, and analysis that goes beyond baseline capture. This skill covers test strategy during planning, incremental testing during implementation, and coverage analysis.

## Test Commands (from constitution)

```bash
# Python (uv/pytest)
uv run pytest                           # Run all tests
uv run pytest tests/ -v                 # Verbose output
uv run pytest tests/ -m "not slow"      # Skip slow tests
uv run pytest tests/ --tb=short -q      # Quick summary
uv run pytest --cov=src --cov-report=html  # Coverage report

# TypeScript/Node (vitest/jest)
npm run test                            # Run all tests
npm run test -- --coverage              # With coverage

# .NET (dotnet test)
dotnet test                             # Run all tests
dotnet test --collect:"XPlat Code Coverage"  # With coverage
```

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create test issue | Append to `.agent/issues/medium.md` with type `TEST` |
| Create bug from failure | Append to `.agent/issues/high.md` with type `BUG` |
| Log test results | Edit issue's `### Log` section in priority file |

### Example: Post-Test Issue Creation (File-Based)

1. Increment `.agent/issues/.counter`
2. Append issue to appropriate priority file
3. Add log entry with test run results

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Create test issue | `aoc issues create --type TEST --title "Add tests for..."` |
| Create bug from failure | `aoc issues create --type BUG --priority high --title "Test failure: ..."` |
| Log test results | `aoc issues update <ID> --log "Tests: 45 pass, 2 fail"` |

## Test Isolation (MANDATORY)

**Tests must NEVER create, modify, or delete files in the project folder.**

### Unit Tests
- Use mocks/patches for ALL file system operations
- Use in-memory data structures where possible
- NEVER call real file I/O against project paths
- Use `unittest.mock.patch` for `Path`, `open()`, file operations

### Integration Tests  
- ALWAYS use `pytest` `tmp_path` fixture (auto-cleaned)
- Use Docker containers for service dependencies (API, DB, etc.)
- Fixtures MUST handle cleanup on both success AND failure
- Test data lives ONLY in temp directories

### Forbidden Patterns
```python
# ❌ NEVER do this - pollutes project
Path(".agent/test.md").write_text("test")
Path("src/data/fixture.json").write_text("{}")
open("tests/output.log", "w").write("log")

# ✅ Always use tmp_path
def test_example(tmp_path):
    test_file = tmp_path / "test.md"
    test_file.write_text("test")  # Auto-cleaned
```

### Review Checklist (before approving tests)
- [ ] No hardcoded paths to project directories
- [ ] All file operations use `tmp_path` or mocks
- [ ] Integration tests use fixtures with cleanup
- [ ] Docker fixtures auto-remove containers

## When to Use

- During planning: designing test strategy for new features
- During implementation: running incremental tests
- During review: analyzing coverage and gaps
- On demand: investigating test failures, improving test suite

## Preconditions

- `.agent/constitution.md` exists with confirmed test command
- `.agent/baseline.md` exists (for comparison)

## Test Strategy Design

### For New Features

1. **Identify test levels needed**:
   - Unit tests: isolated function/method behavior
   - Integration tests: component interaction
   - E2E tests: user-facing workflows (if applicable)

2. **Define test cases from requirements**:
   - Happy path: expected inputs → expected outputs
   - Edge cases: boundary values, empty inputs, max values
   - Error cases: invalid inputs, failure scenarios
   - Regression cases: ensure existing behavior unchanged

3. **Document in task/plan**:
   ```markdown
   ## Test Strategy
   - Unit: [list of unit test cases]
   - Integration: [list of integration scenarios]
   - Edge cases: [specific edge cases to cover]
   - Not testing: [explicitly excluded with rationale]
   ```

### For Bug Fixes

1. Write failing test FIRST (reproduces the bug)
2. Fix the bug
3. Verify test passes
4. Check for related regression tests needed

## Test Execution

### Incremental Testing (during implementation)

After each implementation step:
1. Run the smallest reliable test subset covering changed code
2. If tests fail: stop, diagnose, fix before proceeding
3. Log test results in focus.md

### Full Test Suite (end of implementation)

1. Run complete test command from constitution
2. Compare results to baseline
3. Investigate ANY new failures (even in unrelated areas)

### Test Command Patterns

```bash
# Run specific test file
<test-runner> path/to/test_file.py

# Run tests matching pattern
<test-runner> -k "test_feature_name"

# Run with coverage
<test-runner> --coverage

# Run failed tests only (re-run)
<test-runner> --failed
```

Actual commands must come from constitution.

## Coverage Analysis

### Confidence-Based Coverage Thresholds (MANDATORY)

**Coverage requirements scale with confidence level:**

| Confidence | Line Coverage | Branch Coverage | Enforcement |
|------------|---------------|-----------------|-------------|
| LOW | ≥90% on changed code | ≥85% on changed code | HARD — blocks completion |
| NORMAL | ≥80% on changed code | ≥70% on changed code | SOFT — warning if missed |
| HIGH | Tests pass | N/A | MINIMAL — existing tests only |

**Rationale:**
- LOW confidence = more unknowns = more code paths to verify
- HIGH confidence = well-understood = existing tests sufficient

**Enforcement:**
```
🎯 COVERAGE CHECK — {CONFIDENCE} Confidence

Required: ≥{line_threshold}% line, ≥{branch_threshold}% branch
Actual:   {actual_line}% line, {actual_branch}% branch

[PASS] Coverage meets threshold
— OR —
[FAIL] Coverage below threshold — must add tests before completion
```

**For LOW confidence failures:**
- Coverage failure is a HARD BLOCK
- Cannot proceed until threshold is met
- Document why if threshold is truly unachievable (rare)

### When to Analyze Coverage

- After completing a feature (before critical review)
- When investigating untested code paths
- During improvement discovery

### Coverage Metrics to Track

| Metric | Target | Notes |
|--------|--------|-------|
| Line coverage | ≥80% for new code | Not a hard rule; quality over quantity |
| Branch coverage | Critical paths covered | Focus on decision points |
| Uncovered lines | Document rationale | Some code legitimately untestable |

### Coverage Gaps to Flag

- New code with 0% coverage → **must address**
- Error handling paths untested → **should address**
- Complex logic untested → **investigate**
- Generated/boilerplate untested → **acceptable**

## Test Quality Checklist

### Good Tests

- [ ] Test behavior, not implementation
- [ ] Independent (no test order dependencies)
- [ ] Deterministic (same result every run)
- [ ] Fast (< 1 second per unit test)
- [ ] Readable (test name describes scenario)
- [ ] Minimal mocking (only external dependencies)

### Anti-Patterns to Avoid

- ❌ Testing implementation details (breaks on refactor)
- ❌ Excessive mocking (tests mock, not real code)
- ❌ Flaky tests (intermittent failures)
- ❌ Slow tests without justification
- ❌ Tests that require manual setup
- ❌ Commented-out tests

## Failure Investigation

When tests fail unexpectedly, **invoke `agent-ops-debugging`**:

1. **Apply systematic debugging process**:
   - Isolate: Run failing test alone
   - Reproduce: Confirm failure is consistent
   - Form hypothesis: What might cause this?
   - Test hypothesis: Add logging, inspect state

2. **Categorize the failure**:
   | Category | Evidence | Action |
   |----------|----------|--------|
   | Agent's change | Test passed in baseline | Fix the change |
   | Pre-existing | Test failed in baseline | Document, create issue |
   | Flaky | Intermittent, no code change | Fix test or document |
   | Environment | Works elsewhere | Check constitution assumptions |

3. **Handoff decision**:
   ```
   🔍 Test failure analysis:
   
   - Test: {test_name}
   - Category: {agent_change | pre_existing | flaky | environment}
   - Root cause: {diagnosis}
   
   Next steps:
   1. Fix and re-run (if agent's change)
   2. Create issue and continue (if pre-existing)
   3. Deep dive with /agent-debug (if unclear)
   ```

## Output

After test activities, update:
- `.agent/focus.md`: test results summary
- `.agent/baseline.md`: if establishing new baseline

## Issue Discovery After Testing

**After test analysis, invoke `agent-ops-tasks` discovery procedure:**

1) **Collect test-related findings:**
   - Failing tests → `BUG` (high)
   - Missing test coverage → `TEST` (medium)
   - Flaky tests identified → `CHORE` (medium)
   - Test anti-patterns found → `REFAC` (low)
   - Missing edge case tests → `TEST` (medium)

2) **Present to user:**
   ```
   📋 Test analysis found {N} items:
   
   High:
   - [BUG] Flaky test: PaymentService.processAsync (failed 2/10 runs)
   
   Medium:
   - [TEST] Missing coverage for error handling in UserController
   - [TEST] No edge case tests for empty input scenarios
   
   Low:
   - [REFAC] Tests have excessive mocking in OrderService.test.ts
   
   Create issues for these? [A]ll / [S]elect / [N]one
   ```

3) **After creating issues:**
   ```
   Created {N} test-related issues. What's next?
   
   1. Start fixing highest priority (BUG-0024@abc123 - flaky test)
   2. Continue with current work
   3. Review test coverage report
   ```

```

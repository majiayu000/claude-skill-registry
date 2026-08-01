---
name: skill-quality-gates
description: Complete pre-PR validation combining linting, testing, and quality checks.
  Ensures all changes meet project standards before opening a pull request.
---

---
name: quality-gates
description: Complete pre-PR quality gates combining linting and testing. Use before opening a pull request, after completing a task, or when comprehensive validation is needed. Sequentially runs: lint → unit tests → integration tests → E2E tests. Triggers on "quality gates", "pre-pr check", "before PR", "validate changes", "run all checks".
---

# Quality Gates

## Purpose

Complete pre-PR validation combining linting, testing, and quality checks. Ensures all changes meet project standards before opening a pull request.

**Workflow:** Lint → Unit Test → Integration Test → E2E Test → ✅ PR Ready

## When to Use

- Before opening a pull request
- After completing a development task
- When comprehensive validation is needed
- Final check before merging
- CI/CD pipeline validation

**When NOT to use:**
- Quick development iteration (use individual skills)
- Exploration phase (use skill-testing-workflow)
- Single tool check (use specific skill)

## Quick Start

```bash
# Run complete quality gates
1. Linting (skill-linting-complete)
2. Unit tests (skill-testing-workflow)
3. Integration tests (skill-testing-workflow)
4. E2E tests (skill-testsprite-pre-pr)
5. Final validation
```

## Quality Gates Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY GATES PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GATE 1: LINTING                                                │
│  ├─> Run: skill-linting-complete                               │
│  ├─> Check: No errors in modified files                        │
│  ├─> Check: Formatting consistent                              │
│  └─> Status: ✅ PASS / ❌ FAIL                                  │
│       │                                                         │
│       ▼ (if pass)                                               │
│                                                                 │
│  GATE 2: UNIT TESTS                                             │
│  ├─> Run: npm test / pytest / cargo test                       │
│  ├─> Check: All tests pass                                     │
│  ├─> Check: Coverage > 80%                                     │
│  └─> Status: ✅ PASS / ❌ FAIL                                  │
│       │                                                         │
│       ▼ (if pass)                                               │
│                                                                 │
│  GATE 3: INTEGRATION TESTS                                      │
│  ├─> Run: Integration test suite                               │
│  ├─> Check: API contracts valid                                │
│  ├─> Check: Database operations work                           │
│  └─> Status: ✅ PASS / ❌ FAIL                                  │
│       │                                                         │
│       ▼ (if pass)                                               │
│                                                                 │
│  GATE 4: E2E TESTS                                              │
│  ├─> Run: skill-testsprite-pre-pr                              │
│  ├─> Check: Critical user flows work                           │
│  ├─> Check: No regressions                                     │
│  └─> Status: ✅ PASS / ❌ FAIL                                  │
│       │                                                         │
│       ▼ (if pass)                                               │
│                                                                 │
│  ✅ ALL GATES PASSED - OK TO OPEN PR                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Gate 1: Linting

### Execute

```bash
# Use skill-linting-complete
# Or manually:

# Detect changed files
CHANGED_FILES=$(git diff --name-only --diff-filter=ACMRTUXB main | grep -E '\.(ts|tsx|js|jsx|py|kt)$')

# Run lint on changed files
npm run lint -- $CHANGED_FILES
# or
ruff check $CHANGED_FILES
```

### Validation Criteria

- ✅ No errors in modified files
- ✅ No warnings OR warnings justified with comments
- ✅ Formatting consistent
- ✅ No secrets/credentials exposed

### On Failure

```markdown
❌ GATE 1 FAILED: Linting issues found

Action Required:
1. Run: npm run lint:fix (auto-fix)
2. Manually fix remaining issues
3. Re-run quality gates

Do NOT proceed to next gate until linting passes.
```

## Gate 2: Unit Tests

### Execute

```bash
# TypeScript/JavaScript
npm test -- --coverage

# Python
pytest --cov=src --cov-report=term-missing

# Rust
cargo test
```

### Validation Criteria

- ✅ All unit tests pass
- ✅ Coverage ≥ 80% for new code
- ✅ No test failures
- ✅ No test errors

### Coverage Check

```bash
# Check coverage threshold
# Example output:
# Name              Stmts   Miss  Cover
# -------------------------------------
# src/auth.py          45      2    96%
# src/utils.py         30      5    83%
# -------------------------------------
# TOTAL               150     15    90%
```

### On Failure

```markdown
❌ GATE 2 FAILED: Unit tests failed

Action Required:
1. Review failing tests
2. Fix code or update tests
3. Ensure coverage ≥ 80%
4. Re-run quality gates

Common issues:
- Missing test for new function
- Breaking change not reflected in tests
- Flaky test (run again to verify)
```

## Gate 3: Integration Tests

### Execute

```bash
# TypeScript/JavaScript
npm run test:integration
# or
npx jest --config jest.integration.config.js

# Python
pytest tests/integration/

# Start dependencies if needed
docker-compose -f docker-compose.test.yml up -d
npm run test:integration
docker-compose -f docker-compose.test.yml down
```

### Validation Criteria

- ✅ All integration tests pass
- ✅ API contracts work correctly
- ✅ Database operations succeed
- ✅ External services mocked/stubbed properly

### On Failure

```markdown
❌ GATE 3 FAILED: Integration tests failed

Action Required:
1. Check test environment (DB, services)
2. Verify API contracts
3. Check for race conditions
4. Re-run quality gates
```

## Gate 4: E2E Tests

### Execute

Use `skill-testsprite-pre-pr` for comprehensive E2E testing:

```markdown
"Run pre-PR testing with TestSprite"
```

Or manually:

```bash
# TestSprite MCP workflow
1. testsprite_bootstrap_tests
2. testsprite_generate_tests
3. testsprite_run_tests
4. testsprite_analyze_results
```

### Validation Criteria

- ✅ All E2E tests pass
- ✅ Critical user flows work
- ✅ No visual regressions
- ✅ Performance acceptable

### HITL Checkpoints

TestSprite includes human checkpoints:
1. Review test plan
2. Confirm scope (diff/codebase, backend/frontend)
3. Approve/reject failures

### On Failure

```markdown
❌ GATE 4 FAILED: E2E tests failed

Action Required:
1. Review TestSprite report
2. Fix issues or document known failures
3. Re-run TestSprite
4. Re-run quality gates
```

## Fast Mode vs Full Mode

### Fast Mode (Development)

Skip E2E for quick iteration:

```bash
# Run only first 3 gates
1. Linting ✅
2. Unit Tests ✅
3. Integration Tests ✅
# Skip: E2E (run manually before PR)
```

Use when:
- Rapid iteration
- E2E takes too long
- Confident in changes

### Full Mode (Pre-PR)

Run all gates:

```bash
# All 4 gates
1. Linting ✅
2. Unit Tests ✅
3. Integration Tests ✅
4. E2E Tests ✅
```

Required before:
- Opening PR
- Merging to main
- Release

## Environment-Specific Workflows

### Codespace / VS Code Web

```markdown
## Quality Gates (Codespace)

1. Linting
   - Use: skill-linting-complete

2. Unit Tests
   - Use: Wallaby MCP or npm test

3. Integration Tests
   - Use: npm run test:integration

4. E2E Tests
   - Use: TestSprite MCP (skill-testsprite-pre-pr)

Note: Agent Browser CLI not available in codespace
```

### Local Development

```markdown
## Quality Gates (Local)

1. Linting
   - Use: skill-linting-complete

2. Unit Tests
   - Use: Wallaby MCP (live feedback)

3. Integration Tests
   - Use: npm test:integration

4. E2E Tests
   - Quick: Agent Browser CLI (exploration)
   - Full: TestSprite MCP (regression)
```

### CI/CD Pipeline

```markdown
## Quality Gates (CI)

All gates run automatically:

1. Linting
   - npm run lint

2. Unit Tests
   - npm test -- --coverage

3. Integration Tests
   - npm run test:integration

4. E2E Tests
   - TestSprite MCP in headless mode

Fail fast: Stop at first failing gate
```

## Quality Gates Report

### Generate Report

```markdown
# Quality Gates Report

## Summary
Date: 2025-01-28
Branch: feature/new-auth
Commit: abc123

## Results

| Gate | Status | Details |
|------|--------|---------|
| Linting | ✅ PASS | 0 errors, 0 warnings |
| Unit Tests | ✅ PASS | 45/45 tests, 87% coverage |
| Integration | ✅ PASS | 12/12 tests |
| E2E Tests | ✅ PASS | 15/15 tests |

## Changed Files
- src/auth.ts (modified)
- src/utils.ts (modified)
- tests/auth.test.ts (added)

## Notes
- All gates passed
- Ready to open PR
```

### Failed Report

```markdown
# Quality Gates Report

## Summary
Date: 2025-01-28
Branch: feature/new-auth
Commit: abc123

## Results

| Gate | Status | Details |
|------|--------|---------|
| Linting | ❌ FAIL | 3 errors in src/auth.ts |
| Unit Tests | ⏭️ SKIP | Previous gate failed |
| Integration | ⏭️ SKIP | Previous gate failed |
| E2E Tests | ⏭️ SKIP | Previous gate failed |

## Action Required
Fix linting errors in src/auth.ts:
1. Line 45: Unused variable 'token'
2. Line 67: Missing return type
3. Line 89: Console statement

## Next Steps
1. Fix linting issues
2. Re-run quality gates
```

## Integration with Other Skills

| Skill | Role in Quality Gates |
|-------|----------------------|
| skill-linting-complete | Gate 1: Linting |
| skill-testing-workflow | Gates 2-3: Testing |
| skill-testsprite-pre-pr | Gate 4: E2E |
| skill-test-setup | Initial configuration |

## Best Practices

### Run Frequently

```bash
# After every significant change
quality-gates --fast    # Skip E2E

# Before PR
quality-gates --full    # All gates
```

### Don't Skip Gates

❌ Bad:
```
"Linting has warnings but tests pass, I'll skip fixing"
```

✅ Good:
```
"Fix all warnings or justify with comments before proceeding"
```

### Document Exceptions

If a gate must be skipped:

```markdown
## Quality Gates Exception

Gate: E2E Tests
Reason: TestSprite sandbox unavailable
Approved by: [Name]
Date: 2025-01-28

Alternative: Manual testing performed
- Tested login flow
- Tested payment flow
- All critical paths verified
```

## Troubleshooting

### Gate Takes Too Long

```bash
# Run only specific gate
quality-gates --gate=linting
quality-gates --gate=unit
```

### Flaky Tests

```bash
# Re-run specific gate
quality-gates --gate=e2e --retry=3
```

### Environment Issues

```bash
# Check environment
quality-gates --verify-env

# Reset and re-run
quality-gates --reset
```

## Output Confirmation

```
╔════════════════════════════════════════════════════════════╗
║              QUALITY GATES COMPLETE                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ✅ Gate 1: Linting - PASS                                 ║
║  ✅ Gate 2: Unit Tests - PASS                              ║
║  ✅ Gate 3: Integration Tests - PASS                       ║
║  ✅ Gate 4: E2E Tests - PASS                               ║
║                                                            ║
║  🎉 ALL GATES PASSED                                       ║
║                                                            ║
║  You may proceed to open PR                                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## Version

v1.0.0 (2025-01-28) - Complete quality gates pipeline
---
name: validate
description: Pre-commit validation ensuring lint and tests pass
---

# /validate - Pre-Commit Validation

## Purpose

Enforces the "Definition of Done" mandate by running all quality checks before work is marked complete. This skill ensures that no code is considered "done" until it compiles, lints, and tests successfully.

**Critical Rule:** NO IMPLEMENTATION IS COMPLETE UNTIL THIS SKILL REPORTS PASS.

## Usage

```
/validate           # Run lint + quick tests (default)
/validate --full    # Run lint + full test suite with coverage
```

## Workflow

### 1. Swift Lint Check
```bash
./scripts/lint.sh
```
- SwiftLint strict mode must pass
- Zero violations required
- If violations found, report them with file:line and stop

### 2. Python Lint Check (if Python files changed)
```bash
./scripts/lint-python.sh
```
- ruff linter must pass
- bandit security scan (medium+ severity)
- Matches CI Python lint behavior

### 3. Test Execution

**Default (quick):**
```bash
./scripts/test-quick.sh
```
- Unit tests only
- Faster validation for routine checks

**Full suite (--full):**
```bash
./scripts/test-all.sh
```
- Complete test suite (unit + integration)
- Includes code coverage with **80% threshold enforcement**
- Matches CI behavior exactly
- Use for significant changes and before PR

### 3. Report Results
- Summary of lint status (pass/fail, violation count)
- Test results (pass/fail count)
- Clear PASS or FAIL verdict
- Specific failure details if any

## Success Criteria

- **PASS:** Lint clean + all tests green + (for --full) coverage >= 80%
- **FAIL:** Any lint violation OR any test failure OR (for --full) coverage below 80%

Exit codes:
- `0` = All checks passed
- `1` = One or more checks failed

## When to Run

- Before marking any task "complete"
- Before staging changes for commit
- After making code modifications
- When the pre-commit hook runs (automatic)

## Examples

**Successful validation:**
```
User: /validate
Claude: Running pre-commit validation...

Lint Check: PASSED (0 violations)
Tests: PASSED (47/47 tests)

VALIDATION PASSED - Ready for commit
```

**Failed validation (lint):**
```
User: /validate
Claude: Running pre-commit validation...

Lint Check: FAILED (2 violations)
- UnaMentis/Services/AudioEngine.swift:42: Line length exceeds 120 characters
- UnaMentis/Views/SessionView.swift:18: Unused import 'Foundation'

VALIDATION FAILED - Fix lint violations before proceeding
```

**Failed validation (tests):**
```
User: /validate
Claude: Running pre-commit validation...

Lint Check: PASSED (0 violations)
Tests: FAILED (45/47 tests passed, 2 failed)

Failed tests:
- SessionManagerTests.testSessionTimeout
- AudioEngineTests.testBufferOverflow

VALIDATION FAILED - Fix failing tests before proceeding
```

## CI Parity

The validation is designed to catch issues locally that would fail in CI:

- **Swift Strict Concurrency**: Test scripts use `SWIFT_STRICT_CONCURRENCY=complete` to catch Sendable violations
- **Python Security**: bandit catches common security issues (though not as comprehensive as CodeQL)
- **Linting**: Both Swift and Python linting match CI checks

If CI fails with an issue that local validation missed, investigate and add the check to local validation.

## Integration

This skill replaces `.claude/commands/pre-commit.md` and complements the pre-commit hook in `.claude/hooks/pre-commit-check.sh`.

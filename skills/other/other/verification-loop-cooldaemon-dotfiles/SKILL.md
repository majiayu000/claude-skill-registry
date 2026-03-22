---
name: verification-loop
description: Pre-PR verification checklist. Use after completing features, before creating PRs, or after refactoring. Do NOT use for writing code, designing features, or making architectural decisions -- this is for running verification checks only.
durability: encoded-preference
---

# Verification Loop

## When to Use

- After completing a feature or significant code change
- Before creating a PR
- After refactoring

## Verification Principles

**Follow `makefile-first` skill for all command execution.**

### Build First
Check if the project builds. If build fails, STOP and fix before continuing.

### Type Safety
Run type checking. Zero type errors before proceeding.

### Lint Clean
Run linters. Zero errors required; review warnings.

### Tests Pass
Run test suite with coverage. All tests must pass. Coverage must meet project threshold.

### Security Scan
Run secrets detection and dependency vulnerability checks.

### Diff Review
Review `git diff` for:
- Unintended changes
- Missing error handling
- Potential edge cases

## Output Format

```
VERIFICATION REPORT
==================
Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
```

## Checklist

- [ ] Build passes
- [ ] No type errors
- [ ] No lint errors (warnings reviewed)
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] No security issues
- [ ] Diff reviewed for unintended changes

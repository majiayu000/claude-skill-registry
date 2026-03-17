---
name: quality-strict
description: Quality (Strict) skill for the ikigai project
---

# Quality (Strict)

## Description
Strict testing, coverage, and quality requirements for coverage phase. 90% is mandatory.

## Pre-Commit Requirements

BEFORE creating ANY commit (mandatory, no exceptions):

1. `make fmt` - Format code
2. `make check` - ALL tests pass (100%)
3. `make lint` - ALL complexity/file size checks pass
4. `make check-coverage` - ALL metrics (lines, functions, branches) at 90.0%
5. `make check-dynamic` - ALL sanitizer checks pass (ASan, UBSan, TSan)

If ANY check fails: fix ALL issues, re-run ALL checks, repeat until everything passes.

Never commit with ANY known issue - even "pre-existing" or "in another file".

## Test Execution

**By Default**: Tests run in parallel, with 24 parallel tests on this machine.
- `MAKE_JOBS=24` - up to 24 concurrent tests
- `PARALLEL=1` - all 4 check-dynamic subtargets in parallel

**When you need clear debug output** (serialize execution):
```bash
PARALLEL=0 MAKE_JOBS=1 make check
PARALLEL=0 MAKE_JOBS=1 make check-valgrind
```

**Best practice**: Test individual files during development, run full suite before commits.

Example:
```bash
make build/tests/unit/array/basic_test && ./build/tests/unit/array/basic_test
```

## Build Modes

```bash
make BUILD={debug|release|sanitize|tsan|coverage}
```

- `debug` - Development builds with symbols
- `release` - Optimized production builds
- `sanitize` - Address and undefined behavior sanitizers
- `tsan` - Thread sanitizer
- `coverage` - Code coverage analysis

## Quality Gates

- Use `make check` to verify tests while working on code changes
- Use `make lint && make check-coverage` before commits - **90% coverage is MANDATORY**
- **CRITICAL**: Never run multiple `make` commands simultaneously. Different targets use incompatible compiler flags and will corrupt the build.

## Coverage Phase Mindset

- Every uncovered line is a bug waiting to happen
- Every untested branch is a failure mode you haven't verified
- LCOV exclusions are a last resort, not a shortcut
- Zero tolerance for coverage gaps

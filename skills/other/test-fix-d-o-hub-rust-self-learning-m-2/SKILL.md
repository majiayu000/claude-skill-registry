---
name: test-fix
description: Systematic approach to diagnosing and fixing failing tests in Rust projects. Use when tests fail and you need to diagnose root causes, fix async/await issues, handle race conditions, or resolve database connection problems.
---

# Test Fix

Systematic approach to diagnosing and fixing failing tests.

## Process

### Step 1: Identify Failing Tests
```bash
cargo test --all
cargo test test_name -- --exact --nocapture
```

### Step 2: Reproduce Locally
```bash
# With debug logging
RUST_LOG=debug cargo test test_name

# Force single-threaded for race conditions
cargo test test_name -- --test-threads=1
```

### Step 3: Diagnose Root Cause

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Async/Await | "future cannot be sent" | Add `.await`, use Arc<Mutex> |
| Database | "connection refused" | Check env vars, use test DB |
| Race | Intermittent assertion failure | Add Mutex, sequential execution |
| Type | "expected X, found Y" | Update signatures, add conversions |
| Lifetime | "borrowed value" | Clone data, adjust lifetimes |

### Step 4: Verify Fix
```bash
# Run multiple times
for i in {1..10}; do cargo test test_name -- --exact || break; done

# Run full suite
cargo test --all
```

### Step 5: Regression Prevention
Add test for the specific bug that was fixed.

## Debugging Checklist

- [ ] Run failing test in isolation
- [ ] Check environment variables
- [ ] Review recent changes
- [ ] Check for missing `.await`
- [ ] Verify database connections
- [ ] Look for race conditions
- [ ] Check type compatibility

## Tools

```bash
# Debug logging
RUST_LOG=debug cargo test

# Full backtrace
RUST_BACKTRACE=full cargo test

# Specific module
RUST_LOG=memory_core=debug cargo test
```

## When to Skip vs Fix

**Skip** (temporarily):
- External service down
- Platform-specific issue
- Known upstream bug

**Fix** immediately:
- Logic error
- Incorrect assertion
- Missing error handling

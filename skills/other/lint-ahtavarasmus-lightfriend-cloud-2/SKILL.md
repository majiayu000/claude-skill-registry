---
name: lint
description: Run formatting and linting checks on the codebase
---

# Quick Lint Check

Run all code quality checks without committing.

## Process

### Step 1: Check Formatting

```bash
cd backend && cargo fmt --check
```

Report pass/fail status.

### Step 2: Run Clippy

```bash
cd backend && cargo clippy --workspace --all-targets --all-features -- -D warnings
```

Report any warnings or errors.

### Step 3: Summary

Report overall status:
- Formatting: PASS/FAIL
- Clippy: PASS/FAIL (with count of issues if any)

## Auto-Fix Option

If formatting fails, offer to auto-fix:

```bash
cd backend && cargo fmt
```

For clippy issues, some can be auto-fixed:

```bash
cd backend && cargo clippy --fix --allow-dirty --allow-staged
```

Note: Not all clippy issues are auto-fixable. Manual fixes may be required.

## Quick Reference

```bash
# Check only
cd backend && cargo fmt --check && cargo clippy --workspace --all-targets --all-features -- -D warnings

# Auto-fix formatting
cd backend && cargo fmt

# Auto-fix clippy (where possible)
cd backend && cargo clippy --fix --allow-dirty --allow-staged
```

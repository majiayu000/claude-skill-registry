---
name: verify
description: Run the full verification pipeline — tests, types, and quality checks
---

Run the complete verification pipeline.

## Step 1: Tests
Run the test command (see project config).
- ALL tests must pass
- Report total count and any failures with full error output

## Step 2: Type Checking
Run the type-check command (see project config).
- Must pass with zero errors
- Report any type violations with file:line references

## Step 3: Quick Sanity Checks
Verify these project invariants:
- `from __future__ import annotations` present in every `.py` file under the source root
- No `print()` statements in source root (use `logging` instead)
- No `Any` type in the models/schemas file
- Fail-safe operation called in both startup and shutdown paths in the app factory

## Output
```
Tests:      PASS (X passed) / FAIL (X passed, Y failed)
Types:      PASS (X files) / FAIL (list errors)
Invariants: PASS / FAIL (list violations)
```

If everything passes: "Ready to commit."
If anything fails: list each failure with file:line and suggested fix.
---
name: cleanup
description: Remove dead code, unused imports, stale files, and fix code quality issues found by /audit
disable-model-invocation: true
---

Clean up the codebase: $ARGUMENTS

Unlike `/audit` (which finds issues), `/cleanup` actively removes and fixes them.

## Step 1 — Run Audit First
If not already done, run `/audit` to identify all issues. Otherwise, work from the provided audit findings.

## Step 2 — Remove Dead Code

### Unused imports:
- Search every source file for imports that are never referenced
- Remove them
- Run the type-check command after each batch to catch anything that was actually needed

### Unused functions/methods:
- For each function identified as unused, search the entire codebase for callers
- If zero callers: remove the function
- If only called in tests: keep it (it's being tested)

### Commented-out code:
- Remove blocks of 3+ consecutive commented lines
- If the code might be needed, it's in git history — don't keep it commented

### Empty files:
- Check all `__init__.py` files — if they're empty and not needed for package structure, keep them but don't add unnecessary exports

## Step 3 — Fix Import Order
Ensure imports follow this order in every file:
Follow the language-standard import ordering convention.
If the project uses a future annotations pattern (see stack concepts), it goes first.

## Step 4 — Remove Stale Configuration
- Check env example file for settings not in the config file
- Check config file for settings not documented in the env example file
- Remove any that don't belong

## Step 5 — Clean Test Files
- Remove empty test classes
- Remove skipped tests without linked issues
- Remove unused test fixtures from conftest
- Verify all test imports are used

## Step 6 — Verify Nothing Broke
Run the test and type-check commands (see project config).
Both MUST pass. If anything breaks, the removed code was actually needed — restore it.

## Step 7 — Summary
Report what was cleaned:
```
CLEANUP RESULTS
═══════════════
Unused imports removed:     X (across Y files)
Dead functions removed:     X
Commented code removed:     X blocks
Stale config entries:       X
Test cleanup:               X items

Files modified:  X
Lines removed:   X
Tests: PASS
Types: PASS
```

## Rules
- NEVER remove something without verifying it's unused (grep the full codebase)
- ALWAYS run tests after each batch of removals
- If in doubt, leave it — false positives are worse than leftover dead code
- Commit after each logical batch (imports, functions, config) — not all at once
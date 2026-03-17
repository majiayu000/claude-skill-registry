---
name: hourly-monitor
description: Check Hive test progress, update documentation, and commit with standardized message.
argument-hint: "[--no-commit]"
---

# Hourly Test Monitor

Check Hive test progress, update documentation, and commit changes with a standardized message format.

## Arguments

- `--no-commit`: Update docs but don't commit (for review first)
- (no args): Update docs and commit automatically

## What This Skill Does

1. Checks progress of running Hive tests (core-geth, besu-etc, etc.)
2. Updates **SITREP.md only** with current progress (single source of truth)
3. Commits changes with message format: `Docs: hourly update (HH:MM UTC)`

**Note:** Only SITREP.md is updated with progress. TODO.md is for future plans only.

## Workflow

### Step 1: Check for Running Tests

```bash
# Check if Hive is running
ps aux | grep -E 'hive.*--sim' | grep -v grep

# Find recent logs
/bin/ls -lt /workspaces/etc-nexus/hive/workspace/logs/details/ | head -5
```

### Step 2: Gather Progress for Each Test Suite

For each active test run:

```bash
# Count completed tests
grep -c '^-- ' <log-file>

# Get pass/fail counts
grep -c 'pass' <log-file>
grep -c 'fail' <log-file>
```

Calculate:
- Percentage: `completed / total * 100`
- Rate: ~70 tests/min typical for this machine
- ETA: `remaining_tests / rate / 60` hours

### Step 3: Update Documentation

**SITREP.md only** - Update test progress sections:
```
### core-geth: `legacy-cancun` suite

| Metric | Value |
|--------|-------|
| Progress | X / Y (Z%) |
| Rate | ~N tests/min |
| ETA | ~H hours |
| Status | Running / Completed / Interrupted |
```

Also update baseline test results table if any tests completed.

**Do NOT update TODO.md** - It's for future plans only, not current progress.

### Step 4: Commit (unless --no-commit)

```bash
git add SITREP.md
git commit -m "$(cat <<'EOF'
Docs: hourly update (HH:MM UTC)

Test progress:
- core-geth: legacy-cancun X.X% (N/M) ~Xh ETA
- besu-etc: legacy X.X% (N/M) ~Xh ETA

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

## Test Suite Reference

| Suite | Total Tests | Notes |
|-------|-------------|-------|
| `legacy` | 32,616 | Constantinople and earlier |
| `legacy-cancun` | 111,983 | Istanbul through Cancun |
| `consensus` | 1,148 | Cancun only |

## Commit Message Format

```
Docs: hourly update (HH:MM UTC)

Test progress:
- <client>: <suite> X.X% (N/M) ~Xh ETA

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Example Output

```
=== Hourly Update (12:00 UTC) ===

Checking Hive test progress...

core-geth: legacy-cancun
  Progress: 45,231 / 111,983 (40.4%)
  Rate: ~68 tests/min
  ETA: ~16.4 hours

besu-etc: legacy
  Progress: 15,432 / 32,616 (47.3%)
  Rate: ~52 tests/min
  ETA: ~5.5 hours

Updating documentation...
Committed: "Docs: hourly update (12:00 UTC)"
```

## If No Tests Running

Report current state and commit with:
```
Docs: hourly update (HH:MM UTC) - no active tests
```

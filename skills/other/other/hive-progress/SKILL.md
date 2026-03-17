---
name: hive-progress
description: Check progress of running Hive tests and update documentation with estimates.
argument-hint: "[--update]"
---

# Check Hive Test Progress

Monitor the progress of a running Hive consensus test suite and optionally update documentation.

## Arguments

- `--update`: Automatically update SITREP.md and TODO.md without asking
- (no args): Show progress, then ask user if they want to update docs

## What This Skill Does

1. Finds the active Hive test run by checking recent simulator logs
2. Counts completed tests from the details log
3. Analyzes client log timestamps to calculate actual running time (excluding hibernation gaps)
4. Estimates remaining time based on test rate
5. Displays progress summary
6. If `--update` passed: automatically updates **SITREP.md only**
7. If no args: asks user "Would you like me to update SITREP.md with this progress?"

**Note:** Only SITREP.md is updated. TODO.md is for future plans only.

## How to Find Test Progress

### 1. Find the Active Simulator Log

```bash
# Find the most recent simulator details log
/bin/ls -lt /workspaces/etc-nexus/hive/workspace/logs/details/ | head -5
```

The active log will be the most recently modified file matching `*-simulator-*-0.log`.

### 2. Count Completed Tests

```bash
# Count test entries (each test starts with "-- ")
grep -c "^-- " /workspaces/etc-nexus/hive/workspace/logs/details/<log-file>
```

### 3. Analyze Timestamps for Hibernation Gaps

Check client log distribution to find gaps (hibernation periods):

```bash
# Get timestamp distribution of client logs
/bin/ls -lt /workspaces/etc-nexus/hive/workspace/logs/core-geth/ | awk '{print $6, $7, $8}' | sort | uniq -c
```

Look for gaps >30 minutes between consecutive timestamps - these indicate hibernation.

### 4. Calculate Test Rate

```
rate = completed_tests / active_minutes (excluding hibernation)
```

Typical rate on this machine: ~70 tests/minute

### 5. Estimate Remaining Time

```
remaining_tests = total_tests - completed_tests
remaining_time = remaining_tests / rate
```

## Test Suite Totals (Reference)

| Suite | Total Tests | Command |
|-------|-------------|---------|
| `legacy` | 32,615 | `--sim.limit legacy` |
| `legacy-cancun` | 111,983 | `--sim.limit legacy-cancun` |
| `consensus` | 1,148 | `--sim.limit consensus` |

## Update Documentation

After displaying progress:
- If `--update` flag was passed: automatically update SITREP.md
- Otherwise: ask the user "Would you like me to update SITREP.md with this progress?"

### SITREP.md (Only File to Update)

Update the test progress section with:
- Progress: X / Y tests (Z%)
- Rate: ~N tests/minute
- Estimated time remaining: ~H hours
- Status: Running / Completed / Interrupted

**Do NOT update TODO.md** - It's for future plans only.

## Example Output

```
=== Hive Test Progress ===
Suite: legacy (LegacyTests/Constantinople/BlockchainTests)
Progress: 17,468 / 32,615 (54%)
Rate: ~70 tests/minute
Estimated remaining: ~3.6 hours
Estimated total: ~7.8 hours

Note: Hibernation gap detected 15:21-22:36 UTC (excluded from estimates)
```

## Troubleshooting

- If no active log found, check if hive is running: `ps aux | grep hive`
- If timestamps show no recent activity, the test may have completed or stalled
- Check `hive.json` for run metadata: `cat /workspaces/etc-nexus/hive/workspace/logs/hive.json`

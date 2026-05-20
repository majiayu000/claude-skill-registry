---
name: sync-docs
description: Synchronize documentation with current project state. Updates SITREP.md (status) and TODO.md (future plans).
argument-hint: "[--commit]"
---

# Sync Documentation

Update project documentation to reflect the current state and future plans. SITREP.md is the single source of truth for current status; TODO.md contains only future work.

## Arguments

- `--commit`: Automatically commit changes after syncing (optional)
- (no args): Sync docs but ask before committing

## Documentation Pattern

**SITREP.md** is the **single source of truth** for current status and progress:
- Current test runs and progress
- What's working / what's broken
- Recent changes and updates
- Baseline test results

**TODO.md** focuses on **future work only**:
- Planned next steps
- Future features/improvements
- Known issues to address later
- NO current progress, NO resolved items

**Operation Log** at end of SITREP.md:
- Reverse chronological log of completed work
- When a task is completed, remove from TODO.md and add entry to Operation Log
- Format: Date, status, brief description, reference links

**README.md** links to both:
- Brief overview only
- Links to SITREP.md for status
- Links to TODO.md for plans

## Files Updated

| File | Purpose | What to Update |
|------|---------|----------------|
| `SITREP.md` | Current status (ONLY source of truth) | Test progress, running tests, recent changes, what's working |
| `TODO.md` | Future plans only | Add/remove planned tasks, update future work items |

## Workflow

### Step 1: Check for Running Tests

Look for active Hive test runs:

```bash
# Check if hive is running
ps aux | grep -E "hive.*--sim" | grep -v grep

# Find active test log
/bin/ls -lt /workspaces/etc-nexus/hive/workspace/logs/details/ | head -3
```

If tests are running, get current progress:

```bash
# Count completed tests
grep -c "^-- " /workspaces/etc-nexus/hive/workspace/logs/details/<latest-log>
```

### Step 2: Gather Current State

Collect information about:
- **Test progress**: If running, what % complete? What's the rate/ETA?
- **Git status**: Any uncommitted changes? What branch?
- **Recent commits**: What was done recently?

```bash
git status --short
git log --oneline -5
```

### Step 3: Update SITREP.md (Single Source of Truth)

Update with ALL current status information:
- **Cloud Deployment status** (if running tests interrupted)
- **Test progress** for all active runs (X/Y tests, Z% complete, rate, ETA)
- **Baseline test results** table
- **What's Working** section if status has changed
- **Recent session summary** with any new work done

### Step 4: Update TODO.md (Future Work Only)

Update ONLY future-focused content:
- Add new planned tasks discovered during work
- Remove tasks that are now completed (don't track progress here)
- Update "Immediate Actions" if priorities changed
- NO test progress, NO current status

### Step 5: Review Changes

Show a summary of what was updated:

```
Docs synced:
- SITREP.md: Updated test progress to X/Y (Z%)
- TODO.md: Added new planned task for <feature>

Changes ready to commit. Proceed? (or use --commit to auto-commit)
```

### Step 6: Commit (if requested)

If `--commit` flag or user confirms:

```bash
git add SITREP.md TODO.md
git commit -m "Docs: sync with current state

- SITREP: Test progress X/Y (Z%)
- TODO: Updated future plans

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Reference: Test Suite Totals

| Suite | Total Tests |
|-------|-------------|
| `legacy` | 32,615 |
| `legacy-cancun` | 111,983 |
| `consensus` | 1,148 |

## Tips

- Run this before `/handoff` to ensure docs are current
- Run periodically during long test runs to track progress
- The skill will detect if no tests are running and skip test-related updates

---
name: beads-session-workflow
description: Session start/end protocols, syncing with git, and daily workflow integration
triggers:
  - start session
  - end session
  - sync issues
  - session workflow
  - bd sync
  - bd ready
  - bd stats
  - bd prime
---

# Beads Session Workflow

Daily workflow protocols for managing work sessions with Beads issue tracking and git integration.

## Overview

Beads integrates seamlessly with git-based workflows, enabling:

- **Automatic sync**: Commit, pull, push issue changes
- **Session context**: Prime AI agents with current work state
- **Work discovery**: Find ready tasks at session start
- **Progress tracking**: Review stats at session end
- **Multi-device support**: Sync issues across clones via git branches

The session workflow ensures issues stay synchronized, agents stay informed, and work stays focused.

## Canonical Sources

**Command Reference**:
```bash
bd sync --help      # Git synchronization
bd ready --help     # Finding unblocked work
bd stats --help     # Database statistics
bd status --help    # Overview of issue database
bd prime --help     # AI workflow context
bd daemon --help    # Background sync daemon
```

**Session Commands** (if available in `.claude/commands/`):
- `bd prime` for AI session context
- Git hooks for automatic sync on commit

## Patterns

### Session Start Protocol

```bash
# 1. Sync issues from remote
cd /path/to/project
bd sync

# 2. Review database status
bd status

# Output:
# Total Issues:      622
# Open:              245
# In Progress:       3
# Blocked:           53
# Ready to Work:     192

# 3. Find unblocked work
bd ready --limit 10 --sort hybrid

# 4. (Optional) Prime AI agent with workflow context
bd prime

# 5. Start work on selected issue
bd update tmnl-abc --status in_progress
```

### During Session: Incremental Sync

```bash
# Create issues as work progresses
bd create "Implement feature X" --type task --priority P1

# Update status as you work
bd update tmnl-abc --status in_progress

# Sync changes to remote (squash mode for fewer commits)
bd sync --squash

# Continue working...

# When ready to commit all accumulated changes
bd sync --message "Session progress: completed 3 tasks"
```

### Session End Protocol

```bash
# 1. Update issue status
bd update tmnl-abc --status closed --notes "Completed and tested"
bd update tmnl-xyz --status in_progress --notes "WIP: need to finish tests"

# 2. Review session statistics
bd stats

# Output shows counts by type, status, priority

# 3. Final sync to remote
bd sync --message "End of session: closed tmnl-abc, WIP tmnl-xyz"

# 4. (Optional) Review what's ready for next session
bd ready --limit 5
```

### Git Integration Workflow

```bash
# Standard git workflow with beads sync
git checkout -b feat/new-feature

# Work on code
bd update tmnl-abc --status in_progress

# Sync issues alongside code changes
git add .
git commit -m "Implement feature X"
bd sync  # Auto-commit issues, pull, push

# Continue iterating
# ...

# When feature complete
bd close tmnl-abc --reason "Feature implemented"
git push origin feat/new-feature
bd sync  # Push issue updates
```

### Sync Modes

```bash
# Full sync: export, commit, pull, push
bd sync

# Custom commit message
bd sync --message "Daily standup: closed 2 bugs, created 1 epic"

# Dry run (preview without changes)
bd sync --dry-run

# Squash mode: accumulate changes without committing
bd sync --squash  # Run multiple times during session
bd sync           # Final commit when ready

# Flush only: export to JSONL without git ops
bd sync --flush-only

# Import only: load from JSONL after manual git pull
git pull origin master
bd sync --import-only

# No push: sync locally without pushing to remote
bd sync --no-push

# No pull: skip pulling from remote
bd sync --no-pull

# One-way sync from main (for ephemeral branches)
bd sync --from-main
```

### Daemon Mode (Background Sync)

```bash
# Start background sync daemon
bd daemon start

# Daemon auto-syncs on CRUD operations
bd create "Task"  # Auto-synced in background

# Check daemon status
bd daemon status

# Stop daemon
bd daemon stop

# View daemon logs
tail -f .beads/daemon.log
```

### Work Discovery Patterns

```bash
# Find high-priority unblocked work
bd ready --priority 0 --limit 5

# Find unassigned work
bd ready --unassigned --limit 10

# Find work by label
bd ready --label frontend --limit 10

# Sort by oldest first (tackle stale issues)
bd ready --sort oldest --limit 5

# Sort by priority
bd ready --sort priority --limit 10

# Hybrid sort (balances priority + age)
bd ready --sort hybrid --limit 10
```

### Issue Status Tracking

```bash
# Show current work in progress
bd list --status in_progress

# Show blocked work (needs unblocking)
bd blocked

# Show recently closed issues
bd list --status closed --closed-after 2025-12-19

# Show stale issues (not updated recently)
bd stale --days 30
```

## Examples

### Example 1: Morning Session Start

```bash
# 1. Pull latest changes from remote
cd ~/projects/tmnl
git pull origin master

# 2. Sync issues
bd sync

# 3. Check overall status
bd status

# 4. Find ready work
bd ready --limit 10

# Output:
# 📋 Ready work (10 issues):
# 1. [P0] tmnl-abc: Fix authentication bug
# 2. [P0] tmnl-xyz: Implement search indexing
# 3. [P1] tmnl-def: Add profile UI component
# ...

# 5. Select and start task
bd update tmnl-abc --status in_progress --assignee val

# 6. Prime AI agent (if using Claude Code)
bd prime

# Output:
# Beads Workflow Context for AI:
# - Use `bd create` to track new issues
# - Use `bd ready` to find unblocked work
# - Use `bd sync` to synchronize with git
# ...
```

### Example 2: Mid-Session Progress Sync

```bash
# Working on feature, discover subtasks
bd create "Add validation logic" --type task --priority P1
bd create "Write unit tests" --type task --priority P1

# Squash sync (accumulate changes)
bd sync --squash

# Continue working...

# Discover a bug
bd create "Fix null pointer in validator" \
  --type bug \
  --priority P0 \
  --deps "discovered-from:tmnl-validation"

# Squash sync again
bd sync --squash

# Eventually, commit all accumulated changes
bd sync --message "Feature development: validation + tests + bugfix"
```

### Example 3: Evening Session Close

```bash
# 1. Update status of in-progress work
bd update tmnl-abc --notes "Completed core logic, tests pending"

# 2. Close completed issues
bd close tmnl-xyz --reason "Implemented and tested"

# 3. Review session stats
bd stats

# Output:
# Issue Statistics:
# By Status:
#   Open:           240 (38.6%)
#   In Progress:    4 (0.6%)
#   Blocked:        53 (8.5%)
#   Closed:         375 (60.3%)
#
# By Type:
#   Task:           450 (72.3%)
#   Bug:            80 (12.9%)
#   Feature:        60 (9.6%)
#   Epic:           20 (3.2%)
#   Chore:          12 (1.9%)
#
# By Priority:
#   P0:             25 (4.0%)
#   P1:             80 (12.9%)
#   P2:             400 (64.3%)
#   P3:             100 (16.1%)
#   P4:             17 (2.7%)

# 4. Final sync
bd sync --message "Session close: completed tmnl-xyz, WIP tmnl-abc"

# 5. Preview next session's work
bd ready --limit 5 --sort priority
```

### Example 4: Multi-Device Sync

```bash
# Device 1 (laptop)
bd create "Add feature X" --type task --priority P1
bd sync  # Push to remote

# Device 2 (desktop)
git pull origin master
bd sync  # Import new issue
bd update tmnl-feature-x --status in_progress
bd sync  # Push status update

# Device 1 (laptop)
bd sync  # Pull status update
bd show tmnl-feature-x
# Output: Status: in_progress (updated from Device 2)
```

### Example 5: Git Hook Integration

```bash
# Install git hooks for auto-sync (if supported)
bd hooks install

# Now git commit auto-triggers bd sync --flush-only
git add .
git commit -m "Implement feature"
# (Beads issues auto-exported to .beads/issues.jsonl)

# Manual sync for pull/push
bd sync

# Uninstall hooks if needed
bd hooks uninstall
```

### Example 6: Session Recovery After Conflict

```bash
# Sync fails due to merge conflict
bd sync

# Output:
# Error: Merge conflict in .beads/issues.jsonl

# Resolve manually or use bd merge driver
git status
git mergetool  # Uses bd merge driver if configured

# After resolving conflict
git add .beads/issues.jsonl
git commit -m "Merge beads issues"
bd sync --import-only  # Reload from JSONL

# Verify database consistency
bd validate
```

## Anti-Patterns

### DON'T: Skip syncing before session start

```bash
# WRONG - start work without syncing
bd ready  # Shows stale data
bd update tmnl-abc --status in_progress  # May conflict with remote

# CORRECT - always sync first
bd sync
bd ready
bd update tmnl-abc --status in_progress
```

### DON'T: Forget to sync at session end

```bash
# WRONG - leave changes unsynced
bd create "Task"
bd update tmnl-abc --status closed
# (Exit session without syncing)

# CORRECT - always sync before ending
bd create "Task"
bd update tmnl-abc --status closed
bd sync --message "Session close"
```

### DON'T: Work on stale issue data

```bash
# WRONG - skip checking if data is stale
bd list --status open  # Shows stale data from days ago

# CORRECT - sync first
bd sync  # Pull latest
bd list --status open  # Fresh data
```

### DON'T: Use conflicting sync flags

```bash
# WRONG - contradictory flags
bd sync --flush-only --import-only  # Can't do both!

# CORRECT - use one mode at a time
bd sync --flush-only  # Export only
# OR
bd sync --import-only  # Import only
```

### DON'T: Ignore daemon errors

```bash
# WRONG - daemon fails silently, manual sync needed
bd daemon status
# Output: Daemon not running (crashed)

# (Continue working without syncing)

# CORRECT - restart daemon or use manual sync
bd daemon start
# OR
bd sync  # Manual sync as fallback
```

### DON'T: Create excessive commit noise

```bash
# WRONG - sync after every tiny change
bd create "Task 1"
bd sync  # Commit 1
bd create "Task 2"
bd sync  # Commit 2
bd update tmnl-abc --status in_progress
bd sync  # Commit 3

# CORRECT - use squash mode
bd create "Task 1"
bd sync --squash
bd create "Task 2"
bd sync --squash
bd update tmnl-abc --status in_progress
bd sync --message "Batch: created 2 tasks, started work on tmnl-abc"
```

## Quick Reference Card

| Task | Command |
|------|---------|
| Start session | `bd sync && bd ready --limit 10` |
| End session | `bd stats && bd sync` |
| Full sync | `bd sync` |
| Squash mode | `bd sync --squash` |
| Dry run | `bd sync --dry-run` |
| Custom commit | `bd sync --message "Session work"` |
| Find ready work | `bd ready --limit 10` |
| Review stats | `bd stats` |
| Database status | `bd status` |
| Prime AI | `bd prime` |
| Start daemon | `bd daemon start` |
| Check daemon | `bd daemon status` |

## Session Checklist

### Morning Start
- [ ] `cd` to project directory
- [ ] `git pull origin master`
- [ ] `bd sync` to import latest issues
- [ ] `bd status` to review database
- [ ] `bd ready --limit 10` to find unblocked work
- [ ] `bd update [id] --status in_progress` to start work
- [ ] `bd prime` to brief AI agent (if applicable)

### During Session
- [ ] `bd create` to track new issues as discovered
- [ ] `bd update` to track progress on active issues
- [ ] `bd sync --squash` for incremental sync (optional)
- [ ] `bd ready` to check for new unblocked work

### Evening Close
- [ ] `bd update` to finalize status of in-progress work
- [ ] `bd close` for completed issues with `--reason`
- [ ] `bd stats` to review session productivity
- [ ] `bd sync --message "Session summary"` to push changes
- [ ] `bd ready --limit 5` to preview next session's work

## Integration Points

- **Git workflow**: Issues committed alongside code changes
- **AI agents**: Use `bd prime` to provide workflow context
- **Issue management**: Use `bd ready` and `bd blocked` (see beads-issue-management skill)
- **Dependencies**: Sync preserves dependency relationships (see beads-dependency-tracking skill)
- **Templates**: Session-specific templates via `bd template`
- **Daemon**: Background auto-sync for seamless workflow

## Sync Branch Workflow

Beads supports multi-clone setups via dedicated sync branches:

```bash
# Initialize sync branch workflow
bd migrate-sync

# Sync uses dedicated branch (e.g., beads-sync)
bd sync  # Auto-commits to sync branch, not main

# View sync branch status
bd sync --status

# Merge sync branch to main when ready
bd sync --merge

# One-way sync from main (for ephemeral feature branches)
bd sync --from-main
```

## Troubleshooting

### Sync conflicts
```bash
# If merge conflict occurs
bd sync  # Reports conflict
git status  # Check conflicted files
git mergetool  # Resolve with bd merge driver
git commit -m "Merge beads issues"
bd sync --import-only  # Reload
```

### Stale data warnings
```bash
# If bd warns about stale data
bd sync --allow-stale  # Override check (use cautiously)
# Better: sync first
bd sync  # Update to latest
```

### Daemon issues
```bash
# Daemon not responding
bd daemon status  # Check status
bd daemon stop && bd daemon start  # Restart
tail -f .beads/daemon.log  # Check logs
```

### Database corruption
```bash
# Run health check
bd validate

# Repair orphaned dependencies
bd repair-deps

# If severe, re-import from JSONL
mv .beads/beads.db .beads/beads.db.backup
bd sync --import-only  # Rebuild from JSONL
```

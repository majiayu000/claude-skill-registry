---
name: beads-issue-management
description: Creating, updating, and closing Beads issues with proper types, priorities, and metadata
triggers:
  - create issue
  - new issue
  - close issue
  - update issue
  - bd create
  - bd close
  - bd update
---

# Beads Issue Management

Comprehensive workflow for creating, updating, and closing issues in the Beads issue tracker.

## Overview

Beads is a dependency-first issue tracker optimized for AI-assisted development. Issues are stored in `.beads/issues.jsonl` and synchronized via git. The system supports:

- **5 issue types**: task, bug, feature, epic, chore
- **5 priority levels**: P0 (highest) through P4 (lowest)
- **4 status states**: open, in_progress, blocked, closed
- **Rich metadata**: assignees, labels, estimates, external refs
- **First-class dependencies**: blocks, related, parent-child, discovered-from

## Canonical Sources

**Command Reference**:
```bash
bd create --help   # Creating issues
bd update --help   # Updating issues
bd close --help    # Closing issues
bd list --help     # Listing/filtering issues
bd show [id]       # Viewing issue details
```

**File Locations**:
- Issue database: `.beads/beads.db`
- JSONL export: `.beads/issues.jsonl`
- Config: `.beads/config.yaml`

## Patterns

### Creating a Single Issue

```bash
# Basic task (default type)
bd create "Implement feature X"

# With full metadata
bd create "Fix authentication bug" \
  --type bug \
  --priority P0 \
  --assignee getbygenius \
  --labels auth,security \
  --estimate 120 \
  --description "Users cannot log in after password reset"

# With dependencies (inline)
bd create "Wire up UI component" \
  --type task \
  --deps "blocks:tmnl-abc,related:tmnl-xyz"

# From template
bd create "Epic: Search System" \
  --from-template epic \
  --priority P0
```

### Creating Multiple Issues (Batch)

```bash
# From markdown file with multiple issues
bd create --file issues.md

# Example issues.md format:
# ## [P0] Implement search indexing
# type: task
# labels: search, backend
# ---
# ## [P1] Add search UI
# type: feature
# labels: search, ui
```

### Parallel Issue Creation Pattern

When decomposing a large task, create independent issues in parallel:

```bash
# Create infrastructure issues
bd create "Setup PostgreSQL schema" --type task --priority P1 &
bd create "Setup Redis cache" --type task --priority P1 &
bd create "Configure NATS JetStream" --type task --priority P1 &
wait

# Then create dependent integration task
bd create "Wire services together" \
  --type task \
  --priority P2 \
  --deps "blocks:tmnl-[id1],blocks:tmnl-[id2],blocks:tmnl-[id3]"
```

### Updating Issues

```bash
# Change status
bd update tmnl-abc --status in_progress
bd update tmnl-abc --status blocked

# Update metadata
bd update tmnl-abc \
  --priority P0 \
  --assignee val \
  --add-label urgent \
  --estimate 240

# Bulk update (multiple IDs)
bd update tmnl-abc tmnl-xyz tmnl-def --status closed

# Update description or notes
bd update tmnl-abc --description "New description here"
bd update tmnl-abc --notes "Additional context or findings"
```

### Closing Issues

```bash
# Simple close
bd close tmnl-abc

# With reason
bd close tmnl-abc --reason "Completed implementation and tests"

# Bulk close
bd close tmnl-abc tmnl-xyz tmnl-def --reason "Obsoleted by new architecture"
```

### Listing and Filtering

```bash
# Show all open issues
bd list --status open

# Filter by type and priority
bd list --type bug --priority P0

# Filter by labels (AND logic)
bd list --label search --label backend

# Filter by assignee
bd list --assignee val --status in_progress

# Date-based filtering
bd list --created-after 2025-12-01 --status open

# Limit results
bd list --limit 10 --sort priority

# Detailed output
bd list --status open --long
```

### Viewing Issue Details

```bash
# Show full issue details
bd show tmnl-abc

# Output includes:
# - Title, status, priority, type
# - Created/updated timestamps
# - Description, notes, design
# - Dependencies (what blocks this, what this blocks)
# - Comments history
```

## Examples

### Example 1: Feature Development Workflow

```bash
# 1. Create feature issue
FEATURE_ID=$(bd create "Add user profile page" \
  --type feature \
  --priority P1 \
  --labels ui,profile \
  --description "User-facing profile with avatar, bio, settings" \
  --json | jq -r '.id')

# 2. Create subtasks with dependency
bd create "Design profile schema" \
  --type task \
  --priority P1 \
  --deps "blocks:$FEATURE_ID"

bd create "Build profile UI component" \
  --type task \
  --priority P1 \
  --deps "blocks:$FEATURE_ID"

bd create "Add profile API endpoint" \
  --type task \
  --priority P1 \
  --deps "blocks:$FEATURE_ID"

# 3. Start work
bd update $FEATURE_ID --status in_progress

# 4. Close when complete
bd close $FEATURE_ID --reason "Feature shipped to production"
```

### Example 2: Bug Triage Workflow

```bash
# 1. Create bug from user report
bd create "Login fails with 2FA enabled" \
  --type bug \
  --priority P0 \
  --labels auth,2fa,production \
  --description "Users with 2FA cannot complete login flow" \
  --external-ref "gh-1234"

# 2. Investigate and update with findings
bd update tmnl-abc --notes "Root cause: token expiry not handled in 2FA flow"

# 3. Create fix task
bd create "Fix 2FA token expiry handling" \
  --type task \
  --priority P0 \
  --deps "discovered-from:tmnl-abc"

# 4. Close bug when fixed
bd close tmnl-abc --reason "Fixed in tmnl-xyz"
```

### Example 3: Epic Decomposition

```bash
# 1. Create epic
EPIC_ID=$(bd create "Search System v2" \
  --from-template epic \
  --priority P0 \
  --description "Replace legacy search with Effect-based indexed search" \
  --json | jq -r '.id')

# 2. Create phases as child issues
bd create "Phase 1: Index infrastructure" \
  --type task \
  --priority P0 \
  --parent $EPIC_ID

bd create "Phase 2: Query engine" \
  --type task \
  --priority P0 \
  --parent $EPIC_ID

bd create "Phase 3: UI integration" \
  --type task \
  --priority P1 \
  --parent $EPIC_ID

# 3. Track epic progress
bd show $EPIC_ID  # Shows child issue status
```

## Anti-Patterns

### DON'T: Create issues without type/priority

```bash
# WRONG - defaults to task/P2, loses intent
bd create "Do something important"

# CORRECT - explicit metadata
bd create "Implement critical auth fix" \
  --type bug \
  --priority P0 \
  --labels security,auth
```

### DON'T: Use vague titles

```bash
# WRONG - what needs fixing?
bd create "Fix bug"
bd create "Update code"

# CORRECT - specific, actionable
bd create "Fix null pointer in authentication handler"
bd create "Update user schema to include email verification field"
```

### DON'T: Skip descriptions for complex issues

```bash
# WRONG - no context for future reference
bd create "Refactor search system" --type task --priority P1

# CORRECT - provides context
bd create "Refactor search system" \
  --type task \
  --priority P1 \
  --description "Replace FlexSearch with Effect-based index. Preserve API compatibility."
```

### DON'T: Forget to close completed issues

```bash
# WRONG - leaves stale issues open
git commit -m "Implemented feature X"
# (issue still shows as in_progress)

# CORRECT - close when done
git commit -m "Implemented feature X"
bd close tmnl-abc --reason "Feature complete, tests passing"
```

### DON'T: Update status without checking dependencies

```bash
# WRONG - marking as in_progress when blocked
bd update tmnl-abc --status in_progress
# (tmnl-abc has open blocking dependencies)

# CORRECT - check blockers first
bd show tmnl-abc  # Review dependencies
bd blocked        # See what's blocked
bd ready          # Find unblocked work
bd update tmnl-xyz --status in_progress  # Start unblocked work
```

### DON'T: Use sequential IDs manually

```bash
# WRONG - bd generates hash-based IDs automatically
bd create "Task" --id bd-123

# CORRECT - let bd assign IDs
bd create "Task"  # Gets ID like tmnl-a3f8
```

### DON'T: Batch operations without verification

```bash
# WRONG - close without checking
bd close tmnl-* --reason "Cleanup"

# CORRECT - list first, then close explicitly
bd list --status open --assignee nobody
bd close tmnl-abc tmnl-xyz --reason "Obsolete, removing from backlog"
```

## Quick Reference Card

| Task | Command |
|------|---------|
| Create task | `bd create "Title" --type task --priority P1` |
| Create bug | `bd create "Title" --type bug --priority P0 --labels bug` |
| Create epic | `bd create "Title" --from-template epic --priority P0` |
| Start work | `bd update [id] --status in_progress` |
| Mark blocked | `bd update [id] --status blocked` |
| Close issue | `bd close [id] --reason "Done"` |
| View details | `bd show [id]` |
| List open | `bd list --status open` |
| Filter by type | `bd list --type bug --status open` |
| Batch update | `bd update [id1] [id2] [id3] --status closed` |

## Integration Points

- **Git workflow**: Issues synced via `bd sync` (see beads-session-workflow skill)
- **Dependencies**: Use `bd dep` commands (see beads-dependency-tracking skill)
- **AI context**: Use `bd prime` for workflow reminders in AI sessions
- **Templates**: Use `bd template list` to see available templates

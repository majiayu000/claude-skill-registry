---
name: beads-dependency-tracking
description: Managing issue dependencies, viewing blocked work, and navigating dependency graphs
triggers:
  - add dependency
  - show dependencies
  - dependency tree
  - blocked issues
  - unblock
  - bd dep
  - bd blocked
---

# Beads Dependency Tracking

First-class dependency management for issue tracking with visual graphs and blocking detection.

## Overview

Beads treats dependencies as a core primitive, not an afterthought. The system supports:

- **4 dependency types**: blocks, related, parent-child, discovered-from
- **Bidirectional tracking**: What blocks this issue, what this issue blocks
- **Cycle detection**: Prevents circular dependency chains
- **Visual trees**: ASCII and Mermaid.js graph outputs
- **Blocking analysis**: Find issues that can't proceed due to dependencies

Dependencies are the key to intelligent work prioritization and unblocking workflows.

## Canonical Sources

**Command Reference**:
```bash
bd dep --help          # Dependency management overview
bd dep add --help      # Adding dependencies
bd dep remove --help   # Removing dependencies
bd dep tree --help     # Viewing dependency trees
bd dep cycles --help   # Detecting cycles
bd blocked --help      # Showing blocked issues
bd ready --help        # Showing unblocked work
```

**Dependency Types**:
- **blocks**: This issue must be completed before the dependent can start
- **related**: Informational link, no blocking semantics
- **parent-child**: Hierarchical relationship (epics → tasks)
- **discovered-from**: Tracks issue discovery context (bugs found during work)

## Patterns

### Adding Dependencies

```bash
# Simple blocking dependency
bd dep add tmnl-abc tmnl-xyz
# Meaning: tmnl-abc is blocked by tmnl-xyz (xyz must complete first)

# Explicit type
bd dep add tmnl-abc tmnl-xyz --type blocks

# Related (non-blocking) dependency
bd dep add tmnl-abc tmnl-xyz --type related

# Parent-child relationship
bd dep add tmnl-child tmnl-parent --type parent-child

# Discovery context
bd dep add tmnl-bug tmnl-feature --type discovered-from
# Meaning: bug was discovered while working on feature
```

### Adding Dependencies During Creation

```bash
# Inline dependency specification
bd create "Wire UI to backend" \
  --type task \
  --deps "blocks:tmnl-api,blocks:tmnl-ui,related:tmnl-docs"

# Multiple dependencies with different types
bd create "Fix integration bug" \
  --type bug \
  --deps "discovered-from:tmnl-feature,blocks:tmnl-infra"
```

### Removing Dependencies

```bash
# Remove specific dependency
bd dep remove tmnl-abc tmnl-xyz

# Remove all dependencies of an issue
bd dep remove tmnl-abc --all  # (if supported)
```

### Viewing Dependency Trees

```bash
# Show what blocks this issue (dependencies, down direction)
bd dep tree tmnl-abc
bd dep tree tmnl-abc --direction down

# Show what this issue blocks (dependents, up direction)
bd dep tree tmnl-abc --direction up

# Show full bidirectional graph
bd dep tree tmnl-abc --direction both

# Filter by status (only open issues)
bd dep tree tmnl-abc --status open

# Limit depth
bd dep tree tmnl-abc --max-depth 3

# Mermaid.js output for visualization
bd dep tree tmnl-abc --format mermaid > graph.mmd
```

### Finding Blocked Issues

```bash
# Show all blocked issues
bd blocked

# Filter blocked issues by priority
bd blocked | grep "\[P0\]"

# Show blocking dependencies for a specific issue
bd show tmnl-abc  # Lists dependencies at bottom
```

### Finding Ready Work

```bash
# Show unblocked issues (no open dependencies)
bd ready

# Filter ready work by priority
bd ready --priority 0  # P0 only

# Filter by assignee
bd ready --assignee val

# Show unassigned ready work
bd ready --unassigned

# Limit results
bd ready --limit 5

# Sort by priority (default), oldest, or hybrid
bd ready --sort priority
bd ready --sort oldest
bd ready --sort hybrid  # Balances priority + age
```

### Detecting Dependency Cycles

```bash
# Check for circular dependencies
bd dep cycles

# Example output if cycle detected:
# Cycle detected: tmnl-a → tmnl-b → tmnl-c → tmnl-a
```

## Examples

### Example 1: Feature Implementation Chain

```bash
# 1. Create foundation tasks
API_ID=$(bd create "Build API endpoint" --type task --priority P1 --json | jq -r '.id')
SCHEMA_ID=$(bd create "Design data schema" --type task --priority P1 --json | jq -r '.id')
UI_ID=$(bd create "Build UI component" --type task --priority P1 --json | jq -r '.id')

# 2. Add blocking dependencies
bd dep add $API_ID $SCHEMA_ID      # API blocked by schema
bd dep add $UI_ID $API_ID          # UI blocked by API

# 3. View dependency chain
bd dep tree $UI_ID

# Output:
# tmnl-ui: Build UI component
#   └─ tmnl-api: Build API endpoint
#      └─ tmnl-schema: Design data schema

# 4. Find what's ready to start
bd ready --limit 5

# Output shows tmnl-schema as unblocked, ready to work
```

### Example 2: Unblocking Workflow

```bash
# 1. Check blocked work
bd blocked

# Output:
# [P0] tmnl-integration: Wire services together
#   Blocked by 3 open dependencies: [tmnl-api, tmnl-db, tmnl-cache]

# 2. View dependency tree
bd dep tree tmnl-integration

# 3. Start work on blocking issues
bd update tmnl-api --status in_progress

# 4. Close completed blockers
bd close tmnl-api --reason "Endpoint implemented and tested"

# 5. Check if integration is now unblocked
bd show tmnl-integration  # Shows remaining 2 blockers
bd blocked                # No longer shows tmnl-integration when all blockers closed
```

### Example 3: Epic Decomposition with Dependencies

```bash
# 1. Create epic
EPIC_ID=$(bd create "Search System v2" --from-template epic --priority P0 --json | jq -r '.id')

# 2. Create phases with parent relationship
PHASE1=$(bd create "Phase 1: Infrastructure" --type task --priority P0 --parent $EPIC_ID --json | jq -r '.id')
PHASE2=$(bd create "Phase 2: Indexing" --type task --priority P0 --parent $EPIC_ID --json | jq -r '.id')
PHASE3=$(bd create "Phase 3: UI" --type task --priority P1 --parent $EPIC_ID --json | jq -r '.id')

# 3. Add sequential blocking
bd dep add $PHASE2 $PHASE1  # Phase 2 blocked by Phase 1
bd dep add $PHASE3 $PHASE2  # Phase 3 blocked by Phase 2

# 4. Create subtasks for Phase 1
TASK1=$(bd create "Setup PostgreSQL FTS" --type task --priority P0 --json | jq -r '.id')
TASK2=$(bd create "Setup Redis cache" --type task --priority P0 --json | jq -r '.id')

bd dep add $PHASE1 $TASK1  # Phase 1 blocked by Task 1
bd dep add $PHASE1 $TASK2  # Phase 1 blocked by Task 2

# 5. View full dependency graph
bd dep tree $EPIC_ID --direction down

# Output shows waterfall structure:
# epic → phase1 → [task1, task2]
#     → phase2 (blocked by phase1)
#     → phase3 (blocked by phase2)

# 6. Find ready work
bd ready --limit 10
# Shows task1 and task2 as ready (no blockers)
```

### Example 4: Bug Discovery Chain

```bash
# 1. During feature work, discover a bug
FEATURE_ID=$(bd show tmnl-feature-123 --json | jq -r '.id')

# 2. Create bug with discovery context
BUG_ID=$(bd create "Null pointer in auth handler" \
  --type bug \
  --priority P0 \
  --deps "discovered-from:$FEATURE_ID" \
  --json | jq -r '.id')

# 3. Bug blocks feature completion
bd dep add $FEATURE_ID $BUG_ID --type blocks

# 4. View feature's dependency tree
bd dep tree $FEATURE_ID

# Output:
# tmnl-feature-123: Implement user profile
#   └─ tmnl-bug-456: Null pointer in auth handler
#      └─ (discovered-from) tmnl-feature-123

# 5. Close bug, unblocking feature
bd close $BUG_ID --reason "Fixed NPE with null check"
bd ready --limit 5  # Now shows tmnl-feature-123 as ready
```

### Example 5: Parallel Work Identification

```bash
# 1. Find all unblocked work
bd ready --limit 20 --sort priority

# 2. Filter to specific labels
bd ready --label backend --limit 10

# 3. Assign parallel work to team members
bd update tmnl-abc --assignee alice --status in_progress
bd update tmnl-xyz --assignee bob --status in_progress
bd update tmnl-def --assignee val --status in_progress

# 4. Check blocked work that will become ready soon
bd blocked | grep "\[P0\]"
# Shows high-priority blocked issues

# 5. View dependency trees for blocked work
bd dep tree tmnl-blocked-issue
# Identify which blockers to prioritize
```

## Anti-Patterns

### DON'T: Create circular dependencies

```bash
# WRONG - creates cycle
bd dep add tmnl-a tmnl-b  # a blocked by b
bd dep add tmnl-b tmnl-c  # b blocked by c
bd dep add tmnl-c tmnl-a  # c blocked by a (CYCLE!)

# System will reject or warn. Fix by breaking cycle:
bd dep remove tmnl-c tmnl-a  # Remove problematic link
```

### DON'T: Start work on blocked issues

```bash
# WRONG - working on blocked issue
bd blocked | grep tmnl-abc
# Output: tmnl-abc has 3 open blockers
bd update tmnl-abc --status in_progress  # BAD!

# CORRECT - work on unblocked issues
bd ready --limit 10
bd update tmnl-xyz --status in_progress  # Good, no blockers
```

### DON'T: Forget to remove dependencies when requirements change

```bash
# WRONG - leaving stale dependencies
# (Original plan: UI blocked by API)
bd dep add tmnl-ui tmnl-api

# (Plan changes: UI can use mock data, doesn't need real API)
# But dependency is still there, blocking UI work!

# CORRECT - remove stale dependency
bd dep remove tmnl-ui tmnl-api
bd ready  # Now tmnl-ui shows as ready
```

### DON'T: Use wrong dependency type

```bash
# WRONG - using "blocks" for informational links
bd dep add tmnl-ui tmnl-docs --type blocks
# (UI doesn't actually need docs to be complete)

# CORRECT - use "related" for informational links
bd dep add tmnl-ui tmnl-docs --type related
```

### DON'T: Create deep dependency chains without reviewing

```bash
# WRONG - creating long chain without visualization
bd dep add tmnl-a tmnl-b
bd dep add tmnl-b tmnl-c
bd dep add tmnl-c tmnl-d
bd dep add tmnl-d tmnl-e
# (Creates 5-level waterfall, may be inefficient)

# CORRECT - visualize and refactor if needed
bd dep tree tmnl-a
# Review if some tasks can be parallelized
bd dep remove tmnl-c tmnl-d  # Break chain if possible
```

### DON'T: Ignore blocked issue warnings

```bash
# WRONG - closing issue with open dependents
bd close tmnl-api  # (tmnl-ui depends on this)
# This orphans tmnl-ui's dependency, may cause confusion

# CORRECT - check reverse dependencies first
bd dep tree tmnl-api --direction up  # See what depends on this
# If closing, update or remove dependents
bd dep remove tmnl-ui tmnl-api  # If dependency no longer valid
bd close tmnl-api --reason "Obsolete, replaced by new endpoint"
```

## Quick Reference Card

| Task | Command |
|------|---------|
| Add blocking dependency | `bd dep add [issue] [blocker]` |
| Add related link | `bd dep add [issue] [related] --type related` |
| Remove dependency | `bd dep remove [issue] [blocker]` |
| View dependency tree | `bd dep tree [issue]` |
| View reverse tree (dependents) | `bd dep tree [issue] --direction up` |
| Show blocked issues | `bd blocked` |
| Show ready work | `bd ready --limit 10` |
| Detect cycles | `bd dep cycles` |
| Mermaid graph | `bd dep tree [issue] --format mermaid` |
| Filter ready by priority | `bd ready --priority 0` |

## Dependency Types Reference

| Type | Semantics | Example |
|------|-----------|---------|
| **blocks** | Hard blocker, dependent cannot start | API must exist before UI can call it |
| **related** | Soft link, informational only | UI relates to docs, but can proceed independently |
| **parent-child** | Hierarchical relationship | Epic contains multiple child tasks |
| **discovered-from** | Discovery context | Bug found while implementing feature |

## Workflow Tips

1. **Start with `bd ready`**: Always check unblocked work before starting new tasks
2. **Review `bd blocked`**: Identify bottlenecks and prioritize unblocking work
3. **Use `bd dep tree`**: Visualize complex dependency chains before starting work
4. **Check reverse dependencies**: Before closing, verify what depends on the issue
5. **Detect cycles early**: Run `bd dep cycles` after adding complex dependency chains
6. **Prefer parallel over sequential**: Only use blocking deps when truly necessary

## Integration Points

- **Issue creation**: Use `--deps` flag (see beads-issue-management skill)
- **Session workflow**: `bd ready` and `bd blocked` inform daily work (see beads-session-workflow skill)
- **Git workflow**: Dependencies preserved across `bd sync` operations
- **AI context**: Dependency graphs help AI understand project structure

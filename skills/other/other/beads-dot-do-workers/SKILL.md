---
name: beads
description: "Track work with beads issue tracker using TDD workflow. Create issues for RED (failing tests), GREEN (implementation), and REFACTOR phases."
---

# Beads Issue Tracking with TDD Workflow

## Overview

Beads (bd) is a git-native issue tracker that lives in your repository. Use it to track multi-session work with dependency graphs. For TDD workflows, create separate issues for each phase: RED, GREEN, REFACTOR.

## When to Use Beads vs TodoWrite

| Use Beads | Use TodoWrite |
|-----------|---------------|
| Multi-session work | Single session tasks |
| Complex dependencies | Linear task lists |
| Needs persistent context | Ephemeral tracking |
| TDD phase tracking | Simple checklists |
| Collaborative work | Solo quick tasks |

## TDD Workflow with Beads

### Phase 1: RED (Failing Tests)

Create an issue for writing the failing test:

```bash
bd create --title="RED: [Feature] tests" --type=task --priority=0 --labels="tdd-red,[feature-area]"
```

**Issue content should include:**
- What behavior the test should verify
- Expected inputs and outputs
- Edge cases to cover

**Mark in_progress when starting:**
```bash
bd update [issue-id] --status=in_progress
```

**Close when test is written and failing:**
```bash
bd close [issue-id] --reason="Test written, failing as expected"
```

### Phase 2: GREEN (Minimal Implementation)

Create an issue for the implementation (depends on RED):

```bash
bd create --title="GREEN: Implement [Feature]" --type=task --priority=0 --labels="tdd-green,[feature-area]"
bd dep add [green-id] [red-id]  # GREEN depends on RED
```

**Issue content should include:**
- Link to the RED issue
- Minimal approach to make tests pass
- No extra features (YAGNI)

**Close when tests pass:**
```bash
bd close [issue-id] --reason="Tests passing"
```

### Phase 3: REFACTOR (Clean Up)

Create an issue for refactoring (depends on GREEN):

```bash
bd create --title="REFACTOR: Clean up [Feature]" --type=task --priority=1 --labels="tdd-refactor,[feature-area]"
bd dep add [refactor-id] [green-id]  # REFACTOR depends on GREEN
```

**Issue content should include:**
- What needs cleaning (duplication, naming, extraction)
- Keep tests green throughout

**Close when refactoring complete:**
```bash
bd close [issue-id] --reason="Refactored, tests still green"
```

## Essential Commands

### Finding Work
```bash
bd ready                    # Show issues with no blockers
bd list --status=open       # All open issues
bd list --status=in_progress # Active work
bd blocked                  # See what's blocked and why
```

### Creating Issues
```bash
bd create --title="..." --type=task|bug|feature|epic --priority=0-4
# Priority: 0=critical, 1=high, 2=medium, 3=low, 4=backlog
```

### Managing Dependencies
```bash
bd dep add [issue] [depends-on]  # issue is blocked by depends-on
bd show [issue]                   # See dependencies and dependents
```

### Updating Status
```bash
bd update [id] --status=in_progress  # Claim work
bd update [id] --status=blocked      # Mark blocked
bd close [id]                        # Complete work
bd close [id1] [id2] [id3]          # Close multiple at once
```

### Syncing
```bash
bd sync --from-main    # Pull beads updates from main branch
bd sync --status       # Check sync status
```

## TDD Labels Convention

Use these labels consistently:

| Label | Phase | Description |
|-------|-------|-------------|
| `tdd-red` | RED | Writing failing tests |
| `tdd-green` | GREEN | Implementing to pass tests |
| `tdd-refactor` | REFACTOR | Cleaning up while green |

Plus feature-area labels like: `auth`, `api`, `ui`, `database`, etc.

## Example: Adding User Authentication

```bash
# 1. Create RED issue
bd create --title="RED: User authentication tests" \
  --type=task --priority=0 \
  --labels="tdd-red,auth" \
  --description="Write tests for login, logout, session management"

# 2. Create GREEN issue (blocked by RED)
bd create --title="GREEN: Implement user authentication" \
  --type=task --priority=0 \
  --labels="tdd-green,auth"
bd dep add workers-xxxx workers-yyyy  # GREEN blocked by RED

# 3. Create REFACTOR issue (blocked by GREEN)
bd create --title="REFACTOR: Clean up auth module" \
  --type=task --priority=1 \
  --labels="tdd-refactor,auth"
bd dep add workers-zzzz workers-xxxx  # REFACTOR blocked by GREEN

# 4. Work through in order
bd update workers-yyyy --status=in_progress  # Start RED
# ... write tests ...
bd close workers-yyyy --reason="Tests written, failing"

bd update workers-xxxx --status=in_progress  # Start GREEN
# ... implement ...
bd close workers-xxxx --reason="Tests passing"

bd update workers-zzzz --status=in_progress  # Start REFACTOR
# ... refactor ...
bd close workers-zzzz --reason="Refactored, tests green"
```

## Parallel TDD with Subagents

For large features, use parallel subagents to create TDD issue chains:

```
Launch parallel agents to create beads issues for each module:
- Agent 1: Create RED/GREEN/REFACTOR chain for Module A
- Agent 2: Create RED/GREEN/REFACTOR chain for Module B
- Agent 3: Create RED/GREEN/REFACTOR chain for Module C

Each agent creates 3 issues with proper dependencies.
```

## Session Management

### Starting a Session
```bash
bd ready                    # Find available work
bd show [id]               # Review issue details
bd update [id] --status=in_progress
```

### Ending a Session
```bash
bd close [completed-ids]   # Close finished work
bd sync --from-main        # Pull latest from main
git add . && git commit    # Commit changes
```

## Key Principles

1. **One issue per TDD phase** - Don't combine RED/GREEN/REFACTOR
2. **Dependencies enforce order** - GREEN blocked by RED, REFACTOR blocked by GREEN
3. **Close immediately** - Mark done as soon as phase completes
4. **Labels for filtering** - Use `tdd-*` labels to find phase-specific work
5. **Sync regularly** - Keep beads in sync with main branch

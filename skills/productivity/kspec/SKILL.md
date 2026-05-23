---
name: kspec
description: Use kspec CLI for task and spec management. Invoke when working with tasks, tracking work, capturing ideas, checking session status, or managing specs in this project.
---

# Kspec - Task & Spec Management

Kspec is the task and specification management system for this project. **Always use CLI commands, never manually edit YAML files.**

## Quick Start

```bash
# Session context (run first!)
kspec session start

# Task workflow
kspec task start @task-slug
kspec task note @task-slug "What you did..."
kspec task complete @task-slug --reason "Summary"

# View tasks
kspec tasks ready          # What can be worked on
kspec task get @task-slug  # Full details

# Capture ideas (not yet tasks)
kspec inbox add "idea or thought"
kspec inbox promote @ref --title "Task title"

# Create task directly
kspec task add --title "Title" --priority 2
```

## Session Context

### Setting Focus

When starting work on a specific area:

```bash
# Set focus
kspec meta focus "working on CLI improvements"

# Check current focus
kspec meta focus

# Clear when done
kspec meta focus --clear
```

### Managing Threads

Track parallel work streams:

```bash
# Add thread
kspec meta thread --add "debugging test failures"

# List threads
kspec meta thread --list

# Remove when done (0-indexed)
kspec meta thread --remove 0
```

### Open Questions

Track questions that need answers:

```bash
# Add question
kspec meta question --add "Should we validate on parse or execute?"

# List questions
kspec meta question --list

# Remove when answered
kspec meta question --remove 0
```

## Task Lifecycle

### Start -> Note -> Complete

The standard workflow:

```bash
# 1. Start the task
kspec task start @task-slug

# 2. Add notes as you work (not just at the end)
kspec task note @task-slug "Exploring approach X..."
kspec task note @task-slug "Decided to use Y because Z"

# 3. Complete with summary
kspec task complete @task-slug --reason "Implemented X with approach Y"
```

### Blocking and Unblocking

When external dependencies appear:

```bash
# Block with reason
kspec task block @task-slug --reason "Waiting on API spec"

# Work on other tasks...

# Unblock when ready
kspec task unblock @task-slug
```

**In loop mode:** Block only for genuine external blockers (human decision needed, spec gap, external dependency). Complexity and difficulty are NOT blockers — push through. You MUST verify by running `kspec tasks ready --eligible` before stopping — its output is authoritative. Do not infer task eligibility; the command is the source of truth. See `/task-work` for detailed loop mode guidance.

### Cancellation

When a task is no longer needed:

```bash
kspec task cancel @task-slug --reason "Superseded by @other-task"
```

### Deletion

Permanent removal (use sparingly):

```bash
# Preview first
kspec task delete @task-slug --dry-run

# Delete
kspec task delete @task-slug --force
```

## Finding Work

### Ready Tasks

Tasks that can be started now (no blockers, dependencies met):

```bash
kspec tasks ready
kspec tasks ready -v        # More details
kspec tasks ready --full    # Full details including notes
```

### Blocked Tasks

Tasks waiting on dependencies:

```bash
kspec tasks blocked
```

### Active Work

Tasks currently in progress (should be 0-1):

```bash
kspec tasks in-progress
# or
kspec tasks active
```

### Next Task

Highest priority ready task:

```bash
kspec tasks next
```

### Filtered Queries

Find specific tasks:

```bash
# By status
kspec tasks list --status pending
kspec tasks list --status completed

# By tag
kspec tasks list --tag mvp
kspec tasks list --tag bug

# By type
kspec tasks list --type bug
kspec tasks list --type spike

# Combined filters
kspec tasks list --status pending --tag mvp

# Search in content
kspec tasks list --grep "authentication"
```

## Inbox Workflow

### Quick Capture

For ideas without clear scope:

```bash
kspec inbox add "maybe we need better error handling"
kspec inbox add "refactor auth flow" --tag auth --tag refactor
```

### Triage

List oldest first (encourages processing):

```bash
kspec inbox list

# Filter by tag
kspec inbox list --tag refactor

# Newest first
kspec inbox list --newest
```

### Promotion

Convert to task when scope is clear:

```bash
# Basic
kspec inbox promote @ref --title "Improve error handling"

# With full context
kspec inbox promote @ref \
  --title "Add retry logic to API client" \
  --priority 2 \
  --spec-ref @api-client \
  --tag reliability
```

### Deletion

Remove if no longer relevant:

```bash
kspec inbox delete @ref
```

### Convert to Observation

If it's a friction point rather than a task:

```bash
kspec meta observe --from-inbox @ref
```

## Spec Operations

### Viewing Specs

```bash
# Get specific item
kspec item get @spec-slug

# List with filters
kspec item list --type feature
kspec item list --tag cli
kspec item list --status implemented

# Search
kspec search "validation"
```

### Updating Specs

```bash
# Update fields
kspec item set @spec-slug --description "Updated description"
kspec item set @spec-slug --status implemented
kspec item set @spec-slug --tag new-tag

# JSON patch for complex updates
kspec item patch @spec-slug --data '{"priority": "high"}'

# Preview changes
kspec item patch @spec-slug --data '{"priority": "high"}' --dry-run
```

### Acceptance Criteria

```bash
# List AC
kspec item ac list @spec-slug

# Add AC
kspec item ac add @spec-slug \
  --given "User runs command with --json" \
  --when "Command succeeds" \
  --then "Output is valid JSON"

# Update AC
kspec item ac set @spec-slug ac-1 --then "Output includes error field"

# Remove AC
kspec item ac remove @spec-slug ac-1 --force
```

### Creating Specs

```bash
# Add under parent
kspec item add \
  --under @parent-slug \
  --title "New Feature" \
  --type feature \
  --slug new-feature

# Add requirement under feature
kspec item add \
  --under @new-feature \
  --title "Specific Requirement" \
  --type requirement
```

### Deriving Tasks

Create implementation tasks from specs:

```bash
# Preview first (recommended)
kspec derive @spec-slug --dry-run

# Recursive (default) - includes children
kspec derive @spec-slug

# Flat - only this spec
kspec derive @spec-slug --flat

# All specs without tasks
kspec derive --all
```

## Task Updates

### Setting Fields

```bash
# Update title
kspec task set @task-slug --title "New title"

# Update priority
kspec task set @task-slug --priority 1

# Add tags
kspec task set @task-slug --tag urgent --tag bug

# Add dependency
kspec task set @task-slug --depends-on @other-task

# Link to spec
kspec task set @task-slug --spec-ref @spec-item
```

### JSON Patch

For complex updates:

```bash
# Single update
kspec task patch @task-slug --data '{"priority": 1, "tags": ["urgent"]}'

# Preview
kspec task patch @task-slug --data '{"priority": 1}' --dry-run
```

## Creating Tasks

### Minimal

```bash
kspec task add --title "Fix the bug"
```

### Full

```bash
kspec task add \
  --title "Implement feature X" \
  --spec-ref @spec-item \
  --priority 2 \
  --slug feature-x \
  --tag feature --tag mvp
```

### With Dependencies

```bash
kspec task add \
  --title "Build on previous work" \
  --depends-on @prerequisite-task
```

## Validation

```bash
# Full validation
kspec validate

# References only
kspec validate --refs

# Schema only
kspec validate --schema

# Auto-fix issues
kspec validate --fix
```

## Key Principles

1. **Use CLI, not manual YAML** - Commands maintain consistency
2. **Add notes liberally** - Future context depends on it
3. **Track your work** - Start tasks before working, complete when done
4. **Spec is source of truth** - Code implements what spec defines
5. **Inbox for unclear scope** - Promote to task when ready

## Running kspec

**For normal usage** (after `npm link`):
```bash
kspec session start
kspec tasks ready
```

**For testing source changes** (no build needed):
```bash
npm run dev -- session start
npm run dev -- tasks ready
```

Use `kspec` for day-to-day work. Use `npm run dev` when modifying the CLI itself and testing changes before building.

After source changes, run `npm run build` to update the `kspec` command.

## Environment

- `KSPEC_AUTHOR` - Attribution for notes (e.g., @claude)
- Run `kspec setup` to configure automatically

## Related Skills

- **`/meta`** - Session context management (focus, threads, questions, observations)
- **`/triage`** - Systematic inbox processing
- **`/spec-plan`** - Translate plans to specs
- **`/reflect`** - Session reflection and learning capture

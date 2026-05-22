---
name: beads
description: "Git-backed persistent task tracking with dependencies. Use when user says 'beads', 'ready tasks', 'dependencies', 'blockers', or needs cross-session memory."
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Beads Task Tracker

You are an expert at using beads for persistent, git-backed task management with dependency tracking.

## When To Use

- User says "beads", "ready tasks", "what's next", "next task"
- User needs cross-session task persistence
- User wants dependency tracking between tasks
- Multi-agent coordination is needed
- Before/after handoffs to sync persistent state
- User says "blockers", "blocked by", "dependencies"

## Inputs

- Task descriptions and priorities
- Dependency relationships between tasks
- Status updates (open, in_progress, closed)

## Outputs

- Persisted tasks in `.beads/` directory
- Ready task lists (unblocked work)
- Dependency graphs
- Synced state with git

## Why Beads (Not Just TODO.md)

| Aspect | TODO.md | Beads |
|--------|---------|-------|
| Persistence | Session | Git-backed |
| Dependencies | None | Full graph |
| Multi-agent | Conflicts | Hash IDs |
| Ready detection | Manual | `bd ready` |
| Survives /clear | No | Yes |
| Survives session | No | Yes |

**Rule**: Use TODO.md for immediate visibility. Use beads for persistent state.

## Workflow

### 1. Session Start

```bash
# Pull latest state
bd sync

# See what's ready (no blockers)
bd ready --json

# Pick highest priority task
bd update <id> --status in_progress --json
```

Update TODO.md with current task for visibility.

### 2. During Work

**Create new tasks discovered during work:**
```bash
bd create "Task title" -p 1 -t task --json
```

**Add dependencies when tasks block each other:**
```bash
bd dep add <child-id> <parent-id> --type blocks
```

**Complete tasks:**
```bash
bd close <id> --reason "Completed" --json
```

### 3. Session End

```bash
# CRITICAL: Push all changes before ending
bd sync
```

Create handoff if needed - beads state persists regardless.

## Core Commands

### Check Ready Tasks
```bash
bd ready --json
```
Returns tasks with no open blockers. Start here each session.

### Create Tasks
```bash
bd create "Task title" -p 1 -t task --json
bd create "Bug description" -p 0 -t bug --json
bd create "Feature request" -p 2 -t feature --json
bd create "Epic name" -t epic --json
```

Priority: 0=critical, 1=high, 2=normal, 3=low, 4=backlog

### Manage Dependencies
```bash
# Child blocked until parent closes
bd dep add <child-id> <parent-id> --type blocks

# View dependency tree
bd dep tree <id>
```

### Update Status
```bash
bd update <id> --status in_progress --json
bd update <id> --status open --json
bd close <id> --reason "Completed" --json
```

### View Tasks
```bash
bd show <id> --json
bd list --status open --json
bd list --status in_progress --json
```

### Sync (Critical!)
```bash
bd sync
```
Forces immediate export/commit/push. ALWAYS run before session end.

## Integration with TODO.md

Keep TODO.md in sync for immediate visibility:

```markdown
# TODO

## From Beads (bd ready)
- [ ] bd-a1b2: Implement auth endpoint (p1)
- [ ] bd-f4c3: Add login tests (p2)

## Session Tasks
- [ ] Current step: Write login handler
```

## Multi-Agent Coordination

Beads prevents conflicts via hash-based IDs (bd-xxxx format).

### Task Claiming
```bash
# Agent claims a task
bd update <id> --status in_progress --json
bd sync  # Others see the claim immediately
```

### Parallel Work
```bash
# Agent A creates bd-a1b2
# Agent B creates bd-f4c3
# No collision - different hash IDs
```

### Discovery Pattern
```bash
# Found sub-task during implementation
bd create "Sub-task" --deps parent:<parent-id> -p 2 --json
bd sync
```

### Agent Handover
```bash
# Agent A ending
bd close <id> --reason "Completed auth endpoint"
bd sync

# Agent B starting
bd sync
bd ready --json
```

## Handoff Integration

### Before create-handoff
```bash
bd sync  # Push all changes
```

Include in handoff document:
- In-progress tasks
- Ready tasks
- Blocked tasks with blockers

### After resume-handoff
```bash
bd sync  # Pull latest
bd ready --json  # See available work
```

## Background Agent Tracking

Beads can track background agents across sessions for result retrieval.

### New Fields for Background Tasks

When creating tasks that spawn background agents:

```bash
# Create task with agent tracking
bd create "Run security audit" -t agent_task --json --meta '{"agent_id": "abc123", "agent_type": "security-auditor", "poll_status": "running"}'
```

**Meta fields for agent tasks:**
- `agent_id`: Background agent/task ID (from Task tool response)
- `agent_type`: Type of agent spawned (security-auditor, background-worker, etc.)
- `poll_status`: pending | running | completed | failed
- `started_at`: ISO timestamp when spawned
- `completed_at`: ISO timestamp when finished

### Agent Task Workflow

```bash
# 1. Spawn background agent and record in beads
bd create "Security audit before PR" -t agent_task --json \
  --meta '{"agent_id": "sec_xyz", "agent_type": "security-auditor", "poll_status": "running"}'
# Returns bd-f1a2

# 2. Check agent status (updates poll_status)
bd poll bd-f1a2
# Uses TaskOutput internally, returns: "running" or "completed: [summary]"

# 3. Get full results
bd results bd-f1a2
# Returns full agent output, updates poll_status to "completed"

# 4. Close task with findings
bd close bd-f1a2 --reason "Security audit passed, no issues"
```

### Polling Multiple Agents

```bash
# List all running agent tasks
bd list --type agent_task --meta-filter 'poll_status=running' --json

# Poll all running agents
bd poll-all --json
# Returns: [{"id": "bd-f1a2", "status": "completed"}, {"id": "bd-g3h4", "status": "running"}]
```

### Cross-Session Agent Resumption

Agent IDs persist across sessions:

```bash
# Session 1: Start long security audit
bd create "Deep security scan" -t agent_task --meta '{"agent_id": "deep_sec_123"}'
bd sync
# Session ends

# Session 2: Check on agent
bd sync
bd poll bd-f1a2  # Agent still running or completed
bd results bd-f1a2  # Get findings
```

## Common Patterns

### Breaking Down Work
```bash
# Create epic
bd create "User Authentication" -t epic --json
# Returns bd-a1b2

# Create child tasks
bd create "Login endpoint" --deps parent:bd-a1b2 -p 1 --json
bd create "Logout endpoint" --deps parent:bd-a1b2 -p 1 --json
bd create "Password reset" --deps parent:bd-a1b2 -p 2 --json
```

### Tracking Blockers
```bash
# Found a blocker
bd create "Need API key from user" -t blocker -p 0 --json
# Returns bd-x1y2

# Link current task as blocked
bd dep add <current-task> bd-x1y2 --type blocks
```

### Initialize in New Project
```bash
bd init --stealth  # Keeps .beads/ local to you
```

## Aggressive Persistence (Disconnect-Proof)

**NEW in v7.4**: Sync state aggressively to survive terminal disconnection.

### Sync Triggers (ALWAYS sync on these)

| Event | Action |
|-------|--------|
| Task started | `bd update --status in_progress && bd sync` |
| Task completed | `bd close && bd sync` |
| File committed | `bd sync` (after git commit) |
| Every 5 minutes | Background checkpoint sync |
| Before risky operation | `bd sync` |
| On any error | `bd sync` (preserve state before crash) |

### Resilient Workflow

```bash
# Start task (sync immediately)
bd update $ID --status in_progress --json
bd sync

# Do work...

# Complete task (sync immediately)
bd close $ID --reason "commit: xyz" --json
bd sync  # Don't wait, sync now!

# If error occurs
bd sync  # Save state before handling error
```

### Recovery After Disconnect

```bash
# 1. Pull latest state
bd sync

# 2. See where we left off
bd list --status in_progress --json  # What was in progress?
bd ready --json                       # What's next?

# 3. Check what was completed
bd list --status closed --json | tail -5

# 4. Resume
# If task was in_progress but not complete, continue it
# If task was closed, move to next ready task
```

### Background Auto-Sync

When running in resilient mode, beads syncs automatically:

```bash
# Add to your session (done automatically by resilient-executor)
( while true; do sleep 300; bd sync 2>/dev/null || true; done ) &
```

## Anti-Patterns

- Creating beads issues for trivial tasks (use TODO.md instead)
- Forgetting `bd sync` before session end
- Not using `--json` flag for structured output
- Creating dependencies on closed issues
- Over-engineering dependency graphs for simple work
- **NEW**: Waiting to batch syncs (sync immediately after each action)
- **NEW**: Assuming terminal will stay connected (always use resilient mode)

## Beads vs Handoffs

| Need | Use |
|------|-----|
| Save session context | `create-handoff` |
| Track persistent tasks | `beads` |
| Resume after /clear | `resume-handoff` + `bd sync` |
| Multi-agent task handoff | `beads` with sync |

## Installation

Beads is optional but required for persistent features:

```bash
npm install -g @beads/bd
# or
brew install steveyegge/beads/bd
# or
go install github.com/steveyegge/beads/cmd/bd@latest
```

## Skill Testing Framework

**NEW**: Test ONE_SHOT skills with scenarios to verify they work correctly.

### Test Commands

```bash
# Test a specific skill
bd test <skill-name>

# Test all skills
bd test --all

# Run tests with coverage report
bd test --coverage

# List test scenarios
bd test --list

# Run specific test scenario
bd test <skill-name> --scenario <scenario-name>
```

### Test Scenario Format

Each skill can have test scenarios in `.claude/skills/<skill-name>/TESTS.md`:

```markdown
# Test Scenarios: <skill-name>

## Scenario 1: Basic Functionality
**Input:** User says "test message"
**Expected:** Skill loads correctly, provides expected output
**Steps:**
1. Verify skill loads from disk
2. Parse frontmatter metadata
3. Return correct triggers
**Status:** PASS | FAIL

## Test Scenarios

```bash
# Test a specific skill
bd test <skill-name>

# Test coverage report
bd test --coverage

# Health score
bd test --health
```
4. Run `bd test --coverage` to ensure overall health

---

## Keywords

beads, tasks, ready, dependencies, blockers, persistent, cross-session, bd ready, bd create, bd sync, bd close, bd update, bd dep, multi-agent, bd test, skill testing, test coverage

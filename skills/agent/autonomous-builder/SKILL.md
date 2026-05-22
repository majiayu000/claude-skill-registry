---
name: autonomous-builder
description: "Run headless implementation from idea to artifact. Use when user says 'build in background', 'autonomous', 'headless', or wants hands-off execution."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

# Autonomous Builder

Build from idea to working artifact with minimal supervision.

## When To Use

- User says "build this in background"
- User says "autonomous", "headless", "overnight"
- User provides idea and wants hands-off execution
- User says "just build it" or "come back with something working"

## Core Philosophy

> "Tell it an idea, come back with the thing built."

Like a capable underling: takes an idea, uses best judgment at every step, and returns with something tangible (50-99% complete).

---

## Quick Start

```bash
# From project directory (runs in resilient tmux session):
oneshot-build "A CLI tool that converts markdown to PDF"

# Monitor progress:
tail -f .agent/STATUS.md

# Attach to running session:
tmux attach -t oneshot-build

# Check tasks:
bd list --json
```

**Resilient by default**: All builds run in tmux. Survives terminal disconnect.

---

## How It Works

### Phase 1: Planning (Automatic)
1. Uses front-door skill to analyze idea
2. Creates structured plan with create-plan
3. Parses plan into beads tasks with dependencies
4. Commits plan file

### Phase 2: Building (Loop)
```
while tasks remain:
  1. bd ready --json → pick next task
  2. bd update <id> --status in_progress
  3. Implement the task
  4. git commit after each file
  5. bd close <id> --reason "commit: hash"
  6. Check for stuck condition
```

### Phase 3: Completion
- All beads tasks closed
- Final status written to .agent/STATUS.md
- Git history contains all work

---

## .agent/ Directory

Created automatically for each build:

```
.agent/
├── STATUS.md        # Real-time progress log
├── ITERATIONS.md    # Current iteration count
├── LAST_STATE.md    # Beads state hash (for stuck detection)
├── LAST_ERROR.md    # Last error if any
└── SCRATCHPAD.md    # Working notes
```

---

## Loop Detection

Prevents infinite loops via:

| Check | Threshold | Action |
|-------|-----------|--------|
| Max iterations | 100 | Stop |
| Same beads state | 5 iterations | Stop (stuck) |
| Consecutive errors | 3 | Stop |

When stuck, writes to `.agent/LAST_ERROR.md` and stops gracefully.

---

## Configuration

Environment variables:

```bash
MAX_ITERATIONS=100      # Maximum build iterations
STUCK_THRESHOLD=5       # Iterations without progress
CLAUDE_CMD=claude       # Claude CLI command
```

---

## Manual Mode

If you want more control, run phases manually:

```bash
# Phase 1: Plan only
claude -p "Use front-door, then create-plan for: [idea]. Create beads tasks, then stop."

# Phase 2: Build one task at a time
claude -p "Run bd ready, implement one task, commit, close task, stop."

# Repeat Phase 2 until done
```

---

## Decision Making

The autonomous builder uses these principles:

1. **Prefer simple** - Choose straightforward solutions
2. **Commit often** - Every file edit gets committed
3. **Use existing** - Leverage ONE_SHOT patterns and skills
4. **Best effort** - 50% working is better than 0% perfect
5. **Stop gracefully** - When stuck, save state and stop

---

## Resilient Execution (v7.4)

**All builds run in tmux by default** - survives terminal disconnect, SSH drops, etc.

### How It Works

```
oneshot-build "idea"
  ├─ Creates tmux session: oneshot-build-{timestamp}
  ├─ Starts heartbeat (every 30s)
  ├─ Starts checkpointer (every 5 min)
  ├─ Runs Claude with aggressive sync rules
  └─ Logs everything to .agent/session.log
```

### Aggressive State Persistence

During build, state is saved:
- **Before** each task: `bd update && bd sync`
- **After** each task: `bd close && bd sync`
- **Every commit**: `bd sync`
- **Every 5 minutes**: checkpoint commit + `bd sync`
- **On any error**: `bd sync` (preserve before crash)

### If Terminal Disconnects

The build continues! When you reconnect:

```bash
# 1. Check if session running
tmux list-sessions | grep oneshot

# 2. Reattach
tmux attach -t oneshot-build

# 3. If session died, check beads
bd sync && bd ready --json

# 4. Resume from state
claude -p "Resume from beads"
```

## Recovery

If the builder stops unexpectedly:

```bash
# Check what happened
cat .agent/STATUS.md
cat .agent/LAST_ERROR.md
cat .agent/HEARTBEAT | tail -5  # When did it die?

# See remaining tasks
bd sync
bd ready --json

# Check session log
less .agent/session.log

# Continue manually or restart
oneshot-build "same idea"  # Will pick up from beads state
```

---

## Integration with ONE_SHOT

The builder uses these skills internally:
- `front-door` - Initial interview and spec
- `create-plan` - Structured planning
- `implement-plan` - Task execution
- `beads` - Persistent task tracking
- `failure-recovery` - Loop detection

---

## Example Session

```bash
$ oneshot-build "A Python CLI that fetches weather data and displays it nicely"

=== ONE_SHOT Autonomous Builder ===
Idea: A Python CLI that fetches weather data...
Max iterations: 100

Initialized .agent/ directory
Phase 1: Planning
- Created epic: weather-cli
- Created 8 tasks in 3 groups
- Plan saved: thoughts/shared/plans/2025-01-03-weather-cli.md
Planning complete

Phase 2: Building
Iteration 1: Building
- Implementing: Create project structure
- Committed: feat(setup): create project structure
Iteration 2: Building
- Implementing: Add API client
- Committed: feat(api): add weather API client
...
Iteration 8: Building
- Implementing: Add CLI interface
- Committed: feat(cli): add rich CLI display

All tasks complete!

=== Build Complete ===
Check .agent/STATUS.md for details
```

---

## Keywords

autonomous, headless, background, overnight, build it, just do it, hands-off, come back with

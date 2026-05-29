---
name: resilient-executor
description: "Execute work that survives terminal disconnection. Uses tmux for persistence, aggressive state saving, and recovery. Use when user says 'keep running', 'survive disconnect', or for any long-running work."
allowed-tools: Bash, Read, Write, Edit, Task
---

# Resilient Executor

Execute work that continues even if the terminal disconnects.

## Quick Start - The `oneshot` Command

**You never need to touch tmux directly.** Use the `oneshot` command:

```bash
# Build something autonomously
oneshot build "A Python CLI that fetches weather data"

# Run any prompt resiliently
oneshot run "implement the auth feature"

# Check what's happening
oneshot status

# Watch the work
oneshot attach

# Stop and save state
oneshot stop

# Resume later
oneshot resume
```

All sessions are managed automatically. Survives disconnect.

---

## All Commands

```
oneshot build <idea>     Build something autonomously
oneshot run <prompt>     Run prompt in resilient session
oneshot attach           Connect to running session
oneshot status           Show current status
oneshot log              View full session log
oneshot follow           Follow log live
oneshot stop             Stop current session (saves state)
oneshot resume           Resume from beads state
oneshot list             List all sessions
oneshot killall          Stop all sessions
oneshot update           Update ONE_SHOT from GitHub
```

---

## When To Use

**Auto-Trigger:**
- Any implementation task estimated >5 minutes
- User says "keep running", "don't stop", "survive disconnect"
- User says "I might disconnect", "run in background"
- Running autonomous-builder mode
- Long-running tests or builds

## Core Principle

> **If terminal dies, work continues. If work dies, state is recoverable.**

---

## How It Works (Automatic - You Don't Manage This)

### What Happens Behind the Scenes

When you run `oneshot build` or `oneshot run`:

1. **Creates tmux session** - Runs Claude in isolated terminal
2. **Starts heartbeat** - Writes every 30s to prove it's alive
3. **Starts checkpointer** - Commits + syncs every 5 minutes
4. **Logs everything** - Full transcript in `.agent/session.log`

When you disconnect:
- Session keeps running
- State keeps syncing
- When you reconnect, just `oneshot attach`

When something crashes:
- Beads state is synced
- `oneshot resume` picks up where it left off

### Layer 2: Aggressive State Persistence

Save state BEFORE every action, not just after:

```
Before each task:
  1. bd sync                    # Push beads state
  2. git add -A && git stash   # Save any uncommitted work
  3. echo "$(date): Starting $TASK" >> .agent/STATUS.md

After each task:
  1. git commit                 # Commit work
  2. bd close $ID               # Close task
  3. bd sync                    # Push immediately
```

### Layer 3: Heartbeat & Recovery

```bash
# Write heartbeat every 30 seconds
while true; do
  echo "$(date): alive" >> .agent/HEARTBEAT
  sleep 30
done &

# Recovery check on start
if [ -f .agent/HEARTBEAT ]; then
  LAST=$(tail -1 .agent/HEARTBEAT)
  echo "Last activity: $LAST"
  echo "Resuming from beads state..."
fi
```

---

## Execution Patterns

### Pattern 1: Resilient Single Command

```bash
# Wrap any command in tmux
resilient-run() {
  local SESSION="oneshot-$$"
  local CMD="$@"

  # Start in tmux
  tmux new-session -d -s "$SESSION" "$CMD"

  echo "Started in tmux session: $SESSION"
  echo "Attach with: tmux attach -t $SESSION"
  echo "Session will survive disconnect."
}

# Usage
resilient-run "pytest tests/ -v"
resilient-run "npm run build"
```

### Pattern 2: Resilient Claude Session

```bash
# oneshot-resilient - Run Claude in disconnect-proof session
#!/bin/bash

SESSION="oneshot-$(date +%s)"
PROJECT_DIR="${PWD}"

# Create the command
CLAUDE_CMD="cd $PROJECT_DIR && claude -p '$1'"

# Start in tmux with logging
tmux new-session -d -s "$SESSION" \
  "script -f .agent/session.log -c \"$CLAUDE_CMD\""

echo "=== Resilient ONE_SHOT Session ==="
echo "Session: $SESSION"
echo "Log: .agent/session.log"
echo ""
echo "Commands:"
echo "  Attach:  tmux attach -t $SESSION"
echo "  Detach:  Ctrl+B, D"
echo "  Kill:    tmux kill-session -t $SESSION"
echo ""
echo "Session will continue if you disconnect."
```

### Pattern 3: Checkpoint-and-Continue

For work that's already running, checkpoint frequently:

```
Every 5 minutes OR after each file edit:
  1. git add -A
  2. git commit -m "WIP: checkpoint $(date +%H%M)"
  3. bd sync
  4. echo "Checkpoint at $(date)" >> .agent/CHECKPOINTS.md
```

---

## State Files

The resilient executor maintains these files:

```
.agent/
├── STATUS.md        # Current status, last action
├── HEARTBEAT        # Heartbeat timestamps (for recovery detection)
├── CHECKPOINTS.md   # Checkpoint history
├── session.log      # Full session transcript (via script command)
├── LAST_STATE.md    # Beads state hash
└── RECOVERY.md      # Instructions if disconnected
```

---

## Recovery After Disconnect

If you disconnect and reconnect:

```bash
# 1. Check if tmux session is still running
tmux list-sessions

# 2. If running, reattach
tmux attach -t oneshot-work

# 3. If not running, check beads state
bd sync
bd ready --json

# 4. Check what was last done
cat .agent/STATUS.md
cat .agent/HEARTBEAT | tail -5
git log --oneline -5

# 5. Resume from where it stopped
claude -p "Resume from beads. Run bd ready and continue."
```

---

## Integration with autonomous-builder

The autonomous builder should ALWAYS use resilient mode:

```bash
# Enhanced oneshot-build script
oneshot-build() {
  local IDEA="$1"
  local SESSION="oneshot-build-$(date +%s)"

  # Initialize .agent/ directory
  mkdir -p .agent
  echo "Started: $(date)" > .agent/STATUS.md
  echo "Idea: $IDEA" >> .agent/STATUS.md

  # Create recovery instructions
  cat > .agent/RECOVERY.md << 'EOF'
# Recovery Instructions

If disconnected:
1. tmux attach -t $SESSION
2. If session dead: bd sync && bd ready
3. Resume: claude -p "Continue from beads"

Check progress:
- cat .agent/STATUS.md
- bd list --json
- git log --oneline -10
EOF

  # Run in resilient tmux session
  tmux new-session -d -s "$SESSION" \
    "script -f .agent/session.log -c 'claude --dangerously-skip-permissions -p \"
      You are running in autonomous mode. Build: $IDEA

      CRITICAL: Save state frequently:
      - bd sync after EVERY task close
      - git commit after EVERY file change
      - Update .agent/STATUS.md regularly

      If you detect issues, stop gracefully and bd sync.
    \"'"

  echo "=== Resilient Autonomous Build ==="
  echo "Session: $SESSION"
  echo "Attach: tmux attach -t $SESSION"
  echo "Progress: tail -f .agent/STATUS.md"
}
```

---

## Aggressive Sync Rules

**ALWAYS sync state in these situations:**

| Trigger | Action |
|---------|--------|
| Before starting any task | `bd sync` |
| After completing any task | `bd close && bd sync` |
| After any file edit | `git commit` |
| Every 5 minutes | Checkpoint commit |
| Before any risky operation | `git stash && bd sync` |
| On any error | `bd sync && echo error >> STATUS.md` |

---

## Commands

```bash
# Start resilient session
oneshot-resilient "implement the auth feature"

# Check if session running
tmux list-sessions | grep oneshot

# Attach to running session
tmux attach -t oneshot-work

# Force checkpoint now
bd sync && git add -A && git commit -m "checkpoint"

# Check heartbeat
tail -5 .agent/HEARTBEAT

# View full session log
less .agent/session.log
```

---

## Configuration

```bash
# In your shell profile
export ONESHOT_RESILIENT=true          # Always use resilient mode
export ONESHOT_CHECKPOINT_INTERVAL=300 # Checkpoint every 5 min
export ONESHOT_TMUX_SESSION="oneshot"  # Default session name
```

---

## Anti-Patterns

- Running long tasks without tmux
- Forgetting to `bd sync` after task completion
- Not committing work frequently
- Assuming terminal will stay connected
- Not checking `.agent/STATUS.md` before resuming

---

## Keywords

resilient, persistent, survive, disconnect, tmux, screen, background, nohup, checkpoint, recovery, reconnect, terminal, ssh

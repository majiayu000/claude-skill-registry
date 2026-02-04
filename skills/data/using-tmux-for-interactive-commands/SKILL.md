---
name: running-interactive-commands-with-tmux
description: Controls interactive CLI tools (vim, git rebase -i, REPLs) through tmux detached sessions and send-keys. Use when running tools requiring terminal interaction, programmatic editor control, or orchestrating Claude Code sessions. Triggers include "interactive command", "vim", "REPL", "tmux", or "git rebase -i".
---

# Using tmux for Interactive Commands

## Overview

Interactive CLI tools (vim, interactive git rebase, REPLs, etc.) cannot be controlled through standard bash because they require a real terminal. tmux provides detached sessions that can be controlled programmatically via `send-keys` and `capture-pane`.

## When to Use

**Use tmux when:**
- Running vim, nano, or other text editors programmatically
- Controlling interactive REPLs (Python, Node, etc.)
- Handling interactive git commands (`git rebase -i`, `git add -p`)
- Working with full-screen terminal apps (htop, etc.)
- Commands that require terminal control codes or readline

**Don't use for:**
- Simple non-interactive commands (use regular Bash tool)
- Commands that accept input via stdin redirection
- One-shot commands that don't need interaction

## Quick Reference

| Task | Command |
|------|---------|
| Start session | `tmux new-session -d -s <name> <command>` |
| Send input | `tmux send-keys -t <name> 'text' Enter` |
| Capture output | `tmux capture-pane -t <name> -p` |
| Stop session | `tmux kill-session -t <name>` |
| List sessions | `tmux list-sessions` |

## Core Pattern

### Before (Won't Work)
```bash
# This hangs because vim expects interactive terminal
bash -c "vim file.txt"
```

### After (Works)
```bash
# Create detached tmux session
tmux new-session -d -s edit_session vim file.txt

# Send commands (Enter, Escape are tmux key names)
tmux send-keys -t edit_session 'i' 'Hello World' Escape ':wq' Enter

# Capture what's on screen
tmux capture-pane -t edit_session -p

# Clean up
tmux kill-session -t edit_session
```

## Implementation

### Basic Workflow

1. **Create detached session** with the interactive command
2. **Wait briefly** for initialization (100-500ms depending on command)
3. **Send input** using `send-keys` (can send special keys like Enter, Escape)
4. **Capture output** using `capture-pane -p` to see current screen state
5. **Repeat** steps 3-4 as needed
6. **Terminate** session when done

### Special Keys

Common tmux key names:
- `Enter` - Return/newline
- `Escape` - ESC key
- `C-c` - Ctrl+C
- `C-x` - Ctrl+X
- `Up`, `Down`, `Left`, `Right` - Arrow keys
- `Space` - Space bar
- `BSpace` - Backspace

### Working Directory

Specify working directory when creating session:
```bash
tmux new-session -d -s git_session -c /path/to/repo git rebase -i HEAD~3
```

### Helper Wrapper

For easier use, see `/home/jesse/git/interactive-command/tmux-wrapper.sh`:
```bash
# Start session
/path/to/tmux-wrapper.sh start <session-name> <command> [args...]

# Send input
/path/to/tmux-wrapper.sh send <session-name> 'text' Enter

# Capture current state
/path/to/tmux-wrapper.sh capture <session-name>

# Stop
/path/to/tmux-wrapper.sh stop <session-name>
```

## Common Patterns

### Python REPL
```bash
tmux new-session -d -s python python3 -i
tmux send-keys -t python 'import math' Enter
tmux send-keys -t python 'print(math.pi)' Enter
tmux capture-pane -t python -p  # See output
tmux kill-session -t python
```

### Vim Editing
```bash
tmux new-session -d -s vim vim /tmp/file.txt
sleep 0.3  # Wait for vim to start
tmux send-keys -t vim 'i' 'New content' Escape ':wq' Enter
# File is now saved
```

### Interactive Git Rebase
```bash
tmux new-session -d -s rebase -c /repo/path git rebase -i HEAD~3
sleep 0.5
tmux capture-pane -t rebase -p  # See rebase editor
# Send commands to modify rebase instructions
tmux send-keys -t rebase 'Down' 'Home' 'squash' Escape
tmux send-keys -t rebase ':wq' Enter
```

## Common Mistakes

### Not Waiting After Session Start
**Problem:** Capturing immediately after `new-session` shows blank screen

**Fix:** Add brief sleep (100-500ms) before first capture
```bash
tmux new-session -d -s sess command
sleep 0.3  # Let command initialize
tmux capture-pane -t sess -p
```

### Forgetting Enter Key
**Problem:** Commands typed but not executed

**Fix:** Explicitly send Enter
```bash
tmux send-keys -t sess 'print("hello")' Enter  # Note: Enter is separate argument
```

### Using Wrong Key Names
**Problem:** `tmux send-keys -t sess '\n'` doesn't work

**Fix:** Use tmux key names: `Enter`, not `\n`
```bash
tmux send-keys -t sess 'text' Enter  # ✓
tmux send-keys -t sess 'text\n'      # ✗
```

### Not Cleaning Up Sessions
**Problem:** Orphaned tmux sessions accumulate

**Fix:** Always kill sessions when done
```bash
tmux kill-session -t session_name
# Or check for existing: tmux has-session -t name 2>/dev/null
```

## Progressive Details

For advanced patterns including Claude Code orchestration and remote monitoring protocols, see sections below.

<!-- progressive: advanced-tmux-patterns -->

## Controlling Claude Code Sessions in tmux

### The Two-Step Pattern (CRITICAL)

Claude Code running in tmux requires a **two-step command pattern**:

1. **Queue the command**: Send command with C-m (appears in prompt but doesn't execute)
2. **Execute the command**: Send C-m again (executes the queued command)

**Example - Sending a Command to Claude Code**:
```bash
# Step 1: Queue the command in the Claude Code prompt
tmux send-keys -t csv-import 'date -u +"%Y-%m-%d %H:%M:%S UTC"' C-m

# Step 2: Send Return to execute the queued command
tmux send-keys -t csv-import C-m

# Step 3: Monitor output after brief wait
sleep 3 && tmux capture-pane -t csv-import -p | tail -15
```

### Launching Claude Code in tmux

Create a detached tmux session running Claude Code:

```bash
# Create tmux session with Claude Code
tmux new-session -d -s csv-import -c /path/to/project

# Send the Claude Code launch command (two steps)
tmux send-keys -t csv-import 'claude -p "your prompt here"' C-m
tmux send-keys -t csv-import C-m

# Monitor session startup
sleep 5 && tmux capture-pane -t csv-import -p | tail -30
```

### Common Operations

**Execute a prompt**:
```bash
# Queue the command
tmux send-keys -t csv-import 'claude -p "analyze the codebase"' C-m

# Execute it
tmux send-keys -t csv-import C-m

# Monitor progress
sleep 2 && tmux capture-pane -t csv-import -p | tail -40
```

**Send multi-line prompts** (use heredoc in file, reference in command):
```bash
# Create prompt file first
cat > /tmp/prompt.txt <<'EOF'
Your detailed prompt here
with multiple lines
EOF

# Send command referencing file
tmux send-keys -t csv-import 'claude -p "$(cat /tmp/prompt.txt)"' C-m
tmux send-keys -t csv-import C-m
```

**Monitor ongoing execution**:
```bash
# Continuous monitoring (every 30 seconds)
while true; do
  echo "=== Status at $(date -u +"%H:%M:%S") ==="
  tmux capture-pane -t csv-import -p | tail -25
  sleep 30
done
```

**Check if Claude Code is still active**:
```bash
# Capture current state
tmux capture-pane -t csv-import -p | tail -20

# Look for indicators:
# - "Garnishing..." = processing
# - Fresh prompt = ready for next command
# - Error messages = needs attention
```

### Critical Mistakes with Claude Code

**❌ WRONG - Single C-m (command queued but not executed)**:
```bash
tmux send-keys -t csv-import 'date' C-m
# Command appears in prompt but doesn't run!
```

**✅ CORRECT - Two-step pattern**:
```bash
tmux send-keys -t csv-import 'date' C-m  # Queue
tmux send-keys -t csv-import C-m         # Execute
```

**❌ WRONG - Using Enter instead of C-m**:
```bash
tmux send-keys -t csv-import 'command' Enter Enter
# May not work consistently with Claude Code
```

**✅ CORRECT - Use C-m for Return**:
```bash
tmux send-keys -t csv-import 'command' C-m  # Queue
tmux send-keys -t csv-import C-m            # Execute
```

### Workflow Example: CSV Processing Pipeline

```bash
# 1. Launch Claude Code session
tmux new-session -d -s csv-import -c /path/to/project
tmux send-keys -t csv-import 'claude' C-m
tmux send-keys -t csv-import C-m
sleep 5

# 2. Send initial processing command
tmux send-keys -t csv-import 'claude -p "Extract CSV rows 2-401"' C-m
tmux send-keys -t csv-import C-m

# 3. Monitor progress
sleep 30 && tmux capture-pane -t csv-import -p | tail -30

# 4. Send next step after completion
tmux send-keys -t csv-import 'claude -p "Transform to JSON"' C-m
tmux send-keys -t csv-import C-m

# 5. Continue monitoring
while tmux capture-pane -t csv-import -p | grep -q "Garnishing"; do
  echo "Still processing..."
  sleep 15
done
echo "Processing complete"
```

### Troubleshooting Claude Code in tmux

**Symptom**: Command appears in prompt but doesn't execute
- **Cause**: Forgot second C-m
- **Fix**: Send additional `tmux send-keys -t session-name C-m`

**Symptom**: Can't see what's happening
- **Cause**: Capture timing issue
- **Fix**: Add sleep before capture, increase tail lines
```bash
sleep 3 && tmux capture-pane -t csv-import -p | tail -40
```

**Symptom**: Session becomes unresponsive
- **Cause**: Claude Code waiting for input or error state
- **Fix**: Capture full pane to see error, send C-c to interrupt
```bash
tmux capture-pane -t csv-import -p
tmux send-keys -t csv-import C-c  # Interrupt
```

## Remote Orchestration Protocol for Claude Code Sessions

### Overview

When orchestrating a Claude Code session running in tmux from another Claude Code instance, you need a systematic approach to monitor progress, detect issues, and guide execution.

### Session State Detection

**Parse capture-pane output to determine state:**

| Indicator | State | Action |
|-----------|-------|--------|
| `> ` at bottom with no activity | **IDLE** | Ready for new command |
| `⏺` bullet points updating | **ACTIVE** | Processing, monitor |
| `Garnishing...` | **PROCESSING** | Wait for completion |
| `Context left until auto-compact: X%` | **LOW_CONTEXT** | May need `/clear` soon |
| `API Error` or `Error:` | **ERROR** | Needs intervention |
| `Todos` with checkboxes | **PROGRESS** | Check task status |
| `☐` unchecked boxes | **PENDING** | Tasks remaining |
| `☒` or `☑` checked boxes | **COMPLETED** | Tasks done |

### Monitoring Cycle Protocol

**Every monitoring cycle should:**

1. **Capture current state**:
```bash
tmux capture-pane -t SESSION -p | tail -60
```

2. **Detect session state** from indicators above

3. **Log to scratch pad** with timestamp and findings

4. **Take action based on state**:
   - IDLE + pending tasks → Send nudge command
   - ERROR → Analyze and send recovery command
   - ACTIVE → Continue monitoring
   - LOW_CONTEXT → Prepare for context reset

### Intervention Commands

**Nudge idle session to continue:**
```bash
# Simple continuation nudge
tmux send-keys -t SESSION 'continue with the next task in the plan' C-m
sleep 0.5
tmux send-keys -t SESSION C-m
```

**Recovery from API error:**
```bash
# Acknowledge error and retry
tmux send-keys -t SESSION 'The previous operation encountered an API error. Please retry the last step.' C-m
sleep 0.5
tmux send-keys -t SESSION C-m
```

**Context compaction trigger:**
```bash
# Tell session to compact and continue
tmux send-keys -t SESSION '/clear' C-m
sleep 2
tmux send-keys -t SESSION 'Resume execution of docs/plans/2025-11-25-full-csv-transformation.md from where we left off' C-m
sleep 0.5
tmux send-keys -t SESSION C-m
```

**Progress check request:**
```bash
# Ask for status update
tmux send-keys -t SESSION 'What is the current progress? Which batch/task are you on?' C-m
sleep 0.5
tmux send-keys -t SESSION C-m
```

### Orchestrator Decision Tree

```
START MONITORING CYCLE
        │
        ▼
┌───────────────────┐
│ Capture pane      │
│ (last 60 lines)   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     ┌─────────────────┐
│ Is session IDLE?  │─YES─▶│ Check pending   │
│ ("> " at bottom)  │      │ tasks in output │
└─────────┬─────────┘      └────────┬────────┘
          │NO                       │
          ▼                         ▼
┌───────────────────┐     ┌─────────────────┐
│ Is there ERROR?   │─YES─▶│ Send recovery   │
│ (API/tool error)  │      │ command         │
└─────────┬─────────┘      └────────┬────────┘
          │NO                       │
          ▼                         │
┌───────────────────┐               │
│ Is context LOW?   │─YES─▶ Log warning, prepare /clear
│ (<15% remaining)  │               │
└─────────┬─────────┘               │
          │NO                       │
          ▼                         │
┌───────────────────┐               │
│ Session ACTIVE    │               │
│ Continue monitor  │◀──────────────┘
└───────────────────┘
          │
          ▼
    SLEEP 30-60s
          │
          ▼
    NEXT CYCLE
```

### Long-Running Orchestration Pattern

For multi-hour workflows like CSV transformation:

```bash
# Orchestration scratch pad file
SCRATCH_PAD="/tmp/orchestration-$(date +%Y%m%d).md"
SESSION="eddy-csv-transform"

# Initialize scratch pad
echo "# Orchestration Log - $(date -u +"%Y-%m-%d %H:%M:%S UTC")" > $SCRATCH_PAD

# Monitoring loop
while true; do
  TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
  OUTPUT=$(tmux capture-pane -t $SESSION -p | tail -60)

  # Log to scratch pad
  echo "" >> $SCRATCH_PAD
  echo "## Check: $TIMESTAMP" >> $SCRATCH_PAD
  echo '```' >> $SCRATCH_PAD
  echo "$OUTPUT" | tail -20 >> $SCRATCH_PAD
  echo '```' >> $SCRATCH_PAD

  # State detection
  if echo "$OUTPUT" | grep -q "API Error\|Error:"; then
    echo "**STATUS**: ERROR detected" >> $SCRATCH_PAD
    # Send recovery command
    tmux send-keys -t $SESSION 'retry the last operation that failed' C-m
    sleep 0.5
    tmux send-keys -t $SESSION C-m
    echo "**ACTION**: Sent retry command" >> $SCRATCH_PAD

  elif echo "$OUTPUT" | grep -q "^> $" | tail -1; then
    # Check if truly idle (prompt visible, no activity)
    if echo "$OUTPUT" | grep -q "☐"; then
      echo "**STATUS**: IDLE with pending tasks" >> $SCRATCH_PAD
      tmux send-keys -t $SESSION 'continue with the next pending task' C-m
      sleep 0.5
      tmux send-keys -t $SESSION C-m
      echo "**ACTION**: Sent continuation nudge" >> $SCRATCH_PAD
    fi

  elif echo "$OUTPUT" | grep -q "Context left.*[0-9]%"; then
    CONTEXT_PCT=$(echo "$OUTPUT" | grep -o "Context left.*[0-9]*%" | grep -o "[0-9]*")
    if [ "$CONTEXT_PCT" -lt 15 ]; then
      echo "**STATUS**: LOW CONTEXT ($CONTEXT_PCT%)" >> $SCRATCH_PAD
      echo "**WARNING**: May need /clear soon" >> $SCRATCH_PAD
    fi
  else
    echo "**STATUS**: ACTIVE/PROCESSING" >> $SCRATCH_PAD
  fi

  # Sleep before next check
  sleep 45
done
```

### Sub-Agent Orchestration Pattern

When using a sub-agent to monitor remotely:

```python
Task(
    description="Monitor and orchestrate CSV transformation",
    prompt="""You are orchestrating a Claude Code session running in tmux session 'eddy-csv-transform'.

**YOUR MISSION**: Continuously monitor the session and guide it to completion of the full CSV transformation plan.

**MONITORING PROTOCOL**:
1. Capture current state: `tmux capture-pane -t eddy-csv-transform -p | tail -60`
2. Analyze state indicators (IDLE, ACTIVE, ERROR, LOW_CONTEXT)
3. Log findings to your scratch pad
4. Take appropriate action if needed
5. Sleep 45 seconds
6. REPEAT until all 20 batches complete

**STATE INDICATORS**:
- `> ` with no activity = IDLE, may need nudge
- `☐` unchecked = pending tasks
- `☒` checked = completed tasks
- `API Error` = needs recovery
- `Context left: X%` where X<15 = needs /clear

**INTERVENTION COMMANDS**:
- Nudge: `tmux send-keys -t eddy-csv-transform 'continue' C-m && sleep 0.5 && tmux send-keys -t eddy-csv-transform C-m`
- Recovery: `tmux send-keys -t eddy-csv-transform 'retry' C-m && sleep 0.5 && tmux send-keys -t eddy-csv-transform C-m`

**SUCCESS CRITERIA**:
- All 20 batches transformed, QA'd, and imported
- 1,916 universities in database with v3.9 schema
- PROGRESS.md shows all batches complete

**NEVER STOP** monitoring until the mission is complete or user intervenes.""",
    subagent_type="general-purpose"
)
```

### Health Check Commands

**Quick status check:**
```bash
# One-liner status
tmux capture-pane -t SESSION -p | tail -5
```

**Full diagnostic:**
```bash
# Complete session dump
tmux capture-pane -t SESSION -p -S -1000 > /tmp/session-dump.txt
```

**Check if session exists:**
```bash
tmux has-session -t SESSION 2>/dev/null && echo "EXISTS" || echo "NOT FOUND"
```

### Recovery Scenarios

**Session crashed/closed:**
```bash
# Recreate session and resume
tmux new-session -d -s SESSION -c /path/to/project
tmux send-keys -t SESSION 'claude' C-m
sleep 3
tmux send-keys -t SESSION C-m
sleep 5
tmux send-keys -t SESSION 'Resume execution of the plan from where we left off' C-m
tmux send-keys -t SESSION C-m
```

**Session stuck on permission prompt:**
```bash
# Press 'y' to accept
tmux send-keys -t SESSION 'y' C-m
```

**Session needs user attention:**
```bash
# Check what it's asking for
tmux capture-pane -t SESSION -p | tail -20
# Respond accordingly
```

## Real-World Impact

- Enables programmatic control of vim/nano for file editing
- Allows automation of interactive git workflows (rebase, add -p)
- Makes REPL-based testing/debugging possible
- Unblocks any tool that requires terminal interaction
- **Enables orchestrating Claude Code sessions from another Claude Code instance**
- **Remote monitoring protocol for long-running multi-hour workflows**
- **Automatic error recovery and continuation nudging**
- No need to build custom PTY management - tmux handles it all

<!-- /progressive -->

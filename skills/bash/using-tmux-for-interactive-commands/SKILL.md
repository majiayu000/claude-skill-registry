---
name: using-tmux-for-interactive-commands
description: Use when you need to run interactive CLI tools (vim, git rebase -i, Python REPL, etc.) that require real-time input/output - provides tmux-based approach for controlling interactive sessions through detached sessions and send-keys
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

## Real-World Impact

- Enables programmatic control of vim/nano for file editing
- Allows automation of interactive git workflows (rebase, add -p)
- Makes REPL-based testing/debugging possible
- Unblocks any tool that requires terminal interaction
- No need to build custom PTY management - tmux handles it all

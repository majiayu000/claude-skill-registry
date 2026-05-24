---
name: tmux-tui
description: Interact with TUI applications via tmux. Consider using tuistory skill instead for better synchronization (waitForText vs sleep). Use tmux-tui when you need visual debugging via tmux attach, or when Bun is unavailable.
allowed-tools: Bash
---

# tmux TUI Interaction

Control and test interactive terminal applications by running them in tmux sessions, sending keystrokes, and capturing output for verification.

> **Note:** For most TUI automation, prefer the **tuistory** skill which has proper `waitForText` synchronization instead of `sleep` hacks. Use tmux-tui when you need to visually attach to the session for debugging (`tmux attach -t name`) or when Bun is not available.

## Prerequisites

- tmux must be installed (`brew install tmux` on macOS)
- The TUI application must be runnable from command line

## Core Commands

| Command | Purpose |
|---------|---------|
| `tmux new-session -d -s NAME` | Create detached session |
| `tmux send-keys -t NAME "text" Enter` | Send keystrokes |
| `tmux capture-pane -t NAME -p` | Get current screen content |
| `tmux capture-pane -t NAME -p -e` | Get content with ANSI colors |
| `tmux kill-session -t NAME` | Clean up session |
| `tmux list-sessions` | List active sessions |

## Workflow

### 1. Start TUI in Detached Session

```bash
# Create session and run command inside it
tmux new-session -d -s tui-test
tmux send-keys -t tui-test "your-cli-command" Enter

# Wait for startup
sleep 2
```

### 2. Capture Current State

```bash
OUTPUT=$(tmux capture-pane -t tui-test -p)
echo "$OUTPUT"
```

### 3. Send Input

```bash
# Send single key
tmux send-keys -t tui-test "1"

# Send key + Enter
tmux send-keys -t tui-test "1" Enter

# Send special keys
tmux send-keys -t tui-test Enter      # Enter key
tmux send-keys -t tui-test Escape     # Escape key
tmux send-keys -t tui-test Tab        # Tab key
tmux send-keys -t tui-test Up Down    # Arrow keys
tmux send-keys -t tui-test C-c        # Ctrl+C
tmux send-keys -t tui-test C-m        # Same as Enter

# Send text followed by Enter
tmux send-keys -t tui-test "hello world" Enter
```

### 4. Wait and Capture Again

```bash
sleep 0.5  # Allow time for TUI to update
OUTPUT=$(tmux capture-pane -t tui-test -p)
```

### 5. Assert on Output

```bash
# Check for expected text
if echo "$OUTPUT" | grep -q "expected text"; then
    echo "PASS"
else
    echo "FAIL"
fi

# Multiple assertions
echo "$OUTPUT" | grep -q "Menu loaded" && echo "✓ Menu"
echo "$OUTPUT" | grep -q "Option selected" && echo "✓ Selection"
```

### 6. Clean Up

```bash
tmux kill-session -t tui-test
```

## Complete Example

```bash
#!/bin/bash
SESSION="cli-test-$$"

# Start CLI
tmux new-session -d -s "$SESSION"
tmux send-keys -t "$SESSION" "uv run my-cli-app" Enter
sleep 2

# Verify startup
OUTPUT=$(tmux capture-pane -t "$SESSION" -p)
if ! echo "$OUTPUT" | grep -q "Main Menu"; then
    echo "FAIL: CLI didn't start"
    tmux kill-session -t "$SESSION"
    exit 1
fi

# Navigate menu
tmux send-keys -t "$SESSION" "1" Enter
sleep 0.5

# Check result
OUTPUT=$(tmux capture-pane -t "$SESSION" -p)
echo "$OUTPUT" | grep -q "Success" && echo "✓ PASS"

# Quit and cleanup
tmux send-keys -t "$SESSION" "q" Enter
sleep 0.3
tmux kill-session -t "$SESSION"
```

## Special Keys Reference

| Key | tmux syntax |
|-----|-------------|
| Enter | `Enter` or `C-m` |
| Escape | `Escape` |
| Tab | `Tab` |
| Backspace | `BSpace` |
| Arrow keys | `Up`, `Down`, `Left`, `Right` |
| Ctrl+C | `C-c` |
| Ctrl+D | `C-d` |
| Page Up/Down | `PPage`, `NPage` |
| Home/End | `Home`, `End` |
| Function keys | `F1` through `F12` |

## Tips

- **Use unique session names**: Include `$$` (PID) to avoid conflicts: `SESSION="test-$$"`
- **Always clean up**: Use `tmux kill-session` even on test failure
- **Adjust sleep times**: Complex TUIs may need longer waits (1-2s)
- **Capture scrollback**: Use `tmux capture-pane -S -` for full history
- **Debug visually**: Attach to session with `tmux attach -t NAME` to see what's happening

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `can't find session` | Session ended or never started | Check if command crashed |
| `no server running` | tmux server not started | First `new-session` starts it |
| Empty capture | TUI hasn't rendered yet | Increase sleep time |
| Wrong output | Timing issue | Add `sleep` after `send-keys` |

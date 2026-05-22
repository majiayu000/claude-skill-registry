---
name: TUI Puppeteering with tmux
description: Use when automating or testing TUI/CLI applications - provides isolated tmux sessions with scripts for input, output capture, and state verification
---

# TUI Puppeteering

<required>
**CRITICAL**: Use ONLY the bundled scripts in `/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/` to interact with tmux.
Direct tmux commands risk destroying user sessions. The bundled scripts enforce isolation automatically.
</required>

## Workflow

<required>
Add to TodoWrite before ANY interaction:

1. Write a **Test Plan** (required before execution)
2. Start session with `tui-start`
3. **Assert-Act-Assert loop**: verify state, send input, verify result
4. Cleanup with `tui-stop`
</required>

## Test Plan (Mandatory)

Before running any commands, output a plan block:

<bad-example>
"Let me try pressing enter then quiting"
</bad-example>

<good-example>
**Plan:** Start `./my-app`, expect "Welcome". Press Enter, expect "Menu". Press 'q' to exit.
</good-example>

## Scripts

All scripts use hardcoded socket `nori-agent-sock` for isolation.

### tui-start

```bash
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-start <session-name> "<command>"
```

Creates isolated session with 120x40 geometry, runs command, disables status bar.

### tui-assert

```bash
# Fixed string match (default)
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-assert <session> "<text>" [timeout]

# Regex match
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-assert <session> -E "<pattern>" [timeout]
```

Default timeout: 5s. On failure, writes `<session>_failure.log`.

<bad-example>
`sleep 2`  # Never blindly sleep
</bad-example>

<good-example>
`tui-assert "mytest" "Ready>" 10`
`tui-assert "mytest" -E "Error:.*code [0-9]+" 5`
</good-example>

### tui-send

```bash
# Literal text (no Enter)
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-send <session> "<text>"

# Special keys
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-send <session> --keys "Enter"
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-send <session> --keys "C-c"
```

Use `--keys` for: Enter, Escape, Tab, Space, BSpace, Up, Down, Left, Right, C-a to C-z, F1-F12.

<warning>
**Escape key timing**: Sending `Escape` immediately followed by another key may be interpreted as Alt+key.
```bash
# BAD: May become Alt+j
$SCRIPTS/tui-send "$SESSION" --keys "Escape"
$SCRIPTS/tui-send "$SESSION" --keys "j"

# GOOD: Add delay after Escape
$SCRIPTS/tui-send "$SESSION" --keys "Escape"
sleep 0.2
$SCRIPTS/tui-send "$SESSION" --keys "j"
```
</warning>

### tui-capture

```bash
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-capture <session>
```

Returns current screen content. Use for debugging mid-flow.

**Optional flags** (rarely needed):

| Flag | Use Case |
|------|----------|
| `-e` | Preserve ANSI color codes (for testing colored output) |
| `-S N` | Include N lines of scrollback history |
| `-a` | Capture inactive buffer instead of active |

<warning>
These flags are rarely needed. The default captures what the user sees.
- `-e`: Only if explicitly testing colors
- `-S`: Only if output scrolled off screen
- `-a`: Only if app uses altscreen AND you need the hidden buffer
</warning>

### tui-stop

```bash
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tui-stop <session>
```

Kills session and cleans up. **Always call when done, even on failure.**

### tmux-isolated

For any direct tmux commands (cleanup, advanced usage):

```bash
/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/tmux-isolated <tmux-args>
```

## Assert-Act-Assert Loop

```bash
SCRIPTS="/home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux"
SESSION="test-feature"

# Start
$SCRIPTS/tui-start "$SESSION" "./my-app"

# ASSERT initial state
$SCRIPTS/tui-assert "$SESSION" "Welcome" 10

# ACT
$SCRIPTS/tui-send "$SESSION" "hello"
$SCRIPTS/tui-send "$SESSION" --keys "Enter"

# ASSERT result
$SCRIPTS/tui-assert "$SESSION" "Response:" 10

# Cleanup
$SCRIPTS/tui-stop "$SESSION"
```

## Debugging Failures

On assertion failure, check the auto-generated log:

```bash
cat <session-name>_failure.log
```

For manual inspection mid-test:

```bash
$SCRIPTS/tui-capture "$SESSION"
```

## Safety

<warning>
**NEVER** use `tmux kill-server` without the isolated socket—it destroys ALL user sessions.
Only use `tui-stop` or `tmux-isolated kill-session -t <session>`.
</warning>

## Verification

Run the test suite to verify scripts work:

```bash
bash /home/clifford/Documents/source/nori/skills/tui-puppeteering-with-tmux/test_tui_scripts.sh
```

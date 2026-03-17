---
name: automating-tmux-windows
description: Automates terminal sessions in tmux windows using MCP tools. Use when launching background processes, monitoring builds/servers, sending commands to debuggers (pdb/gdb), interacting with CLI prompts, using interactive commands or commands that require sudo, or orchestrating parallel tasks across multiple terminal sessions.
triggers: tmux, terminal automation, background process, interactive commands, sudo, debugger, pdb, gdb, long-running process, server monitoring
---

# Automating tmux Windows

Control tmux windows programmatically: create windows, send commands, capture output, and manage processes. Each window gets full screen space for easier output tracking.

> **Note**: These tools are provided by the **orchestrator** MCP server, which also includes AI CLI tools (see ai-orchestration skill).

## Recommended: Use Subagent for Context Efficiency

**To save context in the main conversation**, delegate tmux operations to the `tmux-runner` subagent:

```python
# Instead of calling tmux tools directly, use Task tool:
Task(
    subagent_type="tmux-runner",
    description="Run npm build",
    prompt="Run 'npm run build' in the project directory. Return success/failure and any errors.",
    model="haiku"  # Fast and cheap for simple commands
)
```

**When to use subagent:**
- Simple build/test commands
- Any command where you just need pass/fail + output
- Commands that don't need real-time monitoring

**When to use direct tmux tools:**
- Long-running servers you need to monitor over time
- Complex interactive debugging sessions
- When you need the window to persist across multiple operations

## Quick Reference

| Tool                                   | Purpose                               |
| -------------------------------------- | ------------------------------------- |
| `mcp__orchestrator__tmux_new_window`   | Create new window with command        |
| `mcp__orchestrator__tmux_send`         | Send text/keys to window              |
| `mcp__orchestrator__tmux_capture`      | Get window output                     |
| `mcp__orchestrator__tmux_list`         | List windows (JSON)                   |
| `mcp__orchestrator__tmux_kill`         | Close window                          |
| `mcp__orchestrator__tmux_interrupt`    | Send Ctrl+C                           |
| `mcp__orchestrator__tmux_wait_idle`    | Wait for idle (no output changes)     |
| `mcp__orchestrator__tmux_select`       | Switch to window (bring to front)     |
| `mcp__orchestrator__tmux_run_and_read` | Run command, wait, return file output |

## Window Identifiers

**Always use the window ID returned by `tmux_new_window`** (e.g., `"@3"`). These IDs:

- Never change when other windows are created or killed
- Persist until the window itself is destroyed
- Are the only reliable way to reference windows across operations

Window names are visible in the tmux status bar for easy identification.

## Standard Workflow

```python
# 1. Create window - SAVE THE RETURNED ID
# Can pass any command directly - non-shell commands are auto-wrapped in a shell
window_id = mcp__orchestrator__tmux_new_window(command="npm run build", name="build")  # Returns "@3"

# 2. Wait for completion
mcp__orchestrator__tmux_wait_idle(target=window_id, idle_seconds=2.0)  # Returns "idle" or "timeout"

# 3. Get output
output = mcp__orchestrator__tmux_capture(target=window_id, lines=50)

# 4. Optionally switch to window to view it
mcp__orchestrator__tmux_select(target=window_id)

# 5. Cleanup
mcp__orchestrator__tmux_kill(target=window_id)
```

## File-Based Output Workflow

For commands that write to a file (cleaner than capturing pane output):

```python
# Single call: run command, wait for completion, return file contents
# Use __OUTPUT_FILE__ placeholder - it gets replaced with a random /tmp path
result = mcp__orchestrator__tmux_run_and_read(
    command="my-tool --output __OUTPUT_FILE__",
    name="my-task",
    timeout=300
)
```

**Key differences from `tmux_new_window`:**

- Does NOT spawn a shell wrapper (command runs directly)
- Waits for window to close (command exit) instead of idle detection
- Returns file contents instead of pane capture
- Auto-generates safe temp file path (replaces `__OUTPUT_FILE__` placeholder)
- Auto-cleans up window and output file

**Use cases:**

- CLI tools with `-o` or `--output` flags that accept a path argument
- Wrapper scripts that write results to a specified path

## Parallel Windows

Create multiple windows for parallel tasks:

```python
# Create named windows - commands run directly
logs_window = mcp__orchestrator__tmux_new_window(command="tail -f /var/log/app.log", name="logs")
work_window = mcp__orchestrator__tmux_new_window(command="cd ~/project && make", name="work")

# Capture from both
logs = mcp__orchestrator__tmux_capture(target=logs_window, lines=100)
output = mcp__orchestrator__tmux_capture(target=work_window, lines=50)
```

## Interactive Commands

For commands requiring input (sudo, prompts, debuggers):

```python
# Start interactive session
window_id = mcp__orchestrator__tmux_new_window(command="sudo apt update", name="sudo")

# Wait for password prompt
mcp__orchestrator__tmux_wait_idle(target=window_id, idle_seconds=1, timeout=10)

# Send password (if needed)
mcp__orchestrator__tmux_send(target=window_id, text="password")

# Wait for completion
mcp__orchestrator__tmux_wait_idle(target=window_id, idle_seconds=2, timeout=120)
```

## Window Navigation

- Use `tmux_select` to switch to a window programmatically
- User can navigate with Ctrl+b n (next) / Ctrl+b p (previous)
- Window names appear in tmux status bar

## Tool Parameters

### tmux_new_window

| Parameter | Type   | Default | Description                         |
| --------- | ------ | ------- | ----------------------------------- |
| `command` | string | "zsh"   | Command to run (auto shell-wrapped) |
| `name`    | string | ""      | Window name for status bar          |

### tmux_run_and_read

| Parameter | Type   | Default  | Description                                |
| --------- | ------ | -------- | ------------------------------------------ |
| `command` | string | required | Command with `__OUTPUT_FILE__` placeholder |
| `name`    | string | ""       | Window name for status bar                 |
| `timeout` | int    | 300      | Max seconds to wait                        |

The `__OUTPUT_FILE__` placeholder is replaced with an auto-generated `/tmp/tmux_output_<uuid>.txt` path.

### tmux_wait_idle

| Parameter      | Type   | Default  | Description                 |
| -------------- | ------ | -------- | --------------------------- |
| `target`       | string | required | Window ID (e.g., "@3")      |
| `idle_seconds` | float  | 2.0      | Seconds of no change = idle |
| `timeout`      | int    | 60       | Max seconds to wait         |

### tmux_capture

| Parameter | Type   | Default  | Description                   |
| --------- | ------ | -------- | ----------------------------- |
| `target`  | string | required | Window ID (e.g., "@3")        |
| `lines`   | int    | 100      | Lines to capture (max: 10000) |

## Safety

- Cannot kill own window (server prevents this)
- Use `mcp__orchestrator__tmux_interrupt` to stop runaway processes
- Check `is_claude` field in `mcp__orchestrator__tmux_list` to identify your window
- **Always store and reuse the window ID from `mcp__orchestrator__tmux_new_window`**
- Target validation prevents command injection via window IDs

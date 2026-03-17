---
name: tmux
description: Manage tmux sessions for interactive background processes
version: 1.0.0
license: MIT
compatibility: opencode
---

## Overview

CLI tools for managing tmux sessions, enabling agents to run and interact with background processes like database connections (psql, mysql), REPLs, log tailing, and other interactive commands.

## Prerequisites

- [bun](https://bun.sh) runtime installed
- [tmux](https://github.com/tmux/tmux) installed (`brew install tmux` or `apt install tmux`)

## Commands

### List Sessions

List all active tmux sessions.

```bash
bun .opencode/skill/tmux/list-sessions.js [options]
```

**Options:**
- `--json` - Output as JSON

**Examples:**
```bash
bun .opencode/skill/tmux/list-sessions.js
bun .opencode/skill/tmux/list-sessions.js --json
```

---

### Create Session

Create a new tmux session for running background processes.

```bash
bun .opencode/skill/tmux/create-session.js <name> [options]
```

**Arguments:**
- `name` - Session name (required)

**Options:**
- `--command <cmd>` - Initial command to run in the session
- `--workdir <path>` - Working directory for the session
- `--window <name>` - Name for the initial window
- `--json` - Output as JSON

**Examples:**
```bash
# Create a session for psql
bun .opencode/skill/tmux/create-session.js db-session --command "psql -h localhost -U postgres mydb"

# Create a session for tailing logs
bun .opencode/skill/tmux/create-session.js logs --command "tail -f /var/log/app.log"

# Create a session in a specific directory
bun .opencode/skill/tmux/create-session.js dev --workdir ~/projects/myapp
```

---

### Send Command

Send a command to a tmux session (types the command and presses Enter).

```bash
bun .opencode/skill/tmux/send-command.js <session> <command> [options]
```

**Arguments:**
- `session` - Session name (or session:window or session:window.pane)
- `command` - Command to send

**Options:**
- `--no-enter` - Send keys without pressing Enter
- `--literal` - Send keys literally (no special key interpretation)
- `--json` - Output as JSON

**Examples:**
```bash
# Run a SQL query in a psql session
bun .opencode/skill/tmux/send-command.js db-session "SELECT * FROM users LIMIT 10;"

# Send Ctrl+C to interrupt a process
bun .opencode/skill/tmux/send-command.js logs "C-c" --no-enter

# Type text without executing
bun .opencode/skill/tmux/send-command.js dev "echo hello" --no-enter
```

---

### Capture Output

Capture and read the current output from a tmux session pane.

```bash
bun .opencode/skill/tmux/capture-output.js <session> [options]
```

**Arguments:**
- `session` - Session name (or session:window or session:window.pane)

**Options:**
- `--lines <n>` - Number of lines of scrollback to capture (default: 100)
- `--wait <pattern>` - Wait for output matching this pattern before capturing
- `--timeout <ms>` - Timeout for --wait in milliseconds (default: 30000)
- `--json` - Output as JSON

**Examples:**
```bash
# Capture recent output from a session
bun .opencode/skill/tmux/capture-output.js db-session

# Capture more scrollback history
bun .opencode/skill/tmux/capture-output.js logs --lines 500

# Wait for a specific prompt before capturing
bun .opencode/skill/tmux/capture-output.js db-session --wait "postgres=#" --timeout 5000
```

---

### Kill Session

Terminate a tmux session.

```bash
bun .opencode/skill/tmux/kill-session.js <name> [options]
```

**Arguments:**
- `name` - Session name to kill

**Options:**
- `--json` - Output as JSON

**Examples:**
```bash
bun .opencode/skill/tmux/kill-session.js db-session
```

---

## Common Workflows

### Database Session (psql)

```bash
# Create a psql session
bun .opencode/skill/tmux/create-session.js psql --command "psql -h localhost -U postgres mydb"

# Wait for connection, then run queries
bun .opencode/skill/tmux/capture-output.js psql --wait "postgres=#"
bun .opencode/skill/tmux/send-command.js psql "SELECT COUNT(*) FROM users;"

# Capture the query results
bun .opencode/skill/tmux/capture-output.js psql --lines 50

# Clean up when done
bun .opencode/skill/tmux/kill-session.js psql
```

### Log Monitoring

```bash
# Start tailing logs
bun .opencode/skill/tmux/create-session.js logs --command "tail -f /var/log/app.log"

# Check for errors periodically
bun .opencode/skill/tmux/capture-output.js logs --lines 200

# Stop monitoring
bun .opencode/skill/tmux/kill-session.js logs
```

### Interactive REPL (Python, Node, etc.)

```bash
# Start a Python REPL
bun .opencode/skill/tmux/create-session.js python --command "python3"

# Run Python commands
bun .opencode/skill/tmux/send-command.js python "import pandas as pd"
bun .opencode/skill/tmux/send-command.js python "df = pd.read_csv('data.csv')"
bun .opencode/skill/tmux/send-command.js python "df.describe()"

# Capture output
bun .opencode/skill/tmux/capture-output.js python
```

---

## Output Behavior

- Command output is displayed directly to the user in the terminal
- **Do not re-summarize or reformat output** - the user can already see it
- When capturing output, the raw terminal content is returned (may include ANSI codes)
- Use `--json` for structured output when parsing programmatically

## Notes

- Session names should be descriptive and unique (e.g., `psql-mydb`, `logs-app`)
- Target format: `session` or `session:window` or `session:window.pane`
- Special keys: `C-c` (Ctrl+C), `C-d` (Ctrl+D), `C-m` (Enter), `C-l` (clear)
- Sessions persist until explicitly killed or system restart

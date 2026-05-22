---
name: tmux
description: "Remote control tmux sessions for interactive CLIs, background tasks, and services. Supports sub-tasks, long-running processes, and service management with session persistence and automatic cleanup."
license: MIT
---

# tmux Skill

Use tmux as a programmable terminal multiplexer for interactive work, background tasks, and service management. Works on Linux and macOS with stock tmux; uses a private socket to avoid interfering with your personal tmux configuration.

## Quickstart (isolated socket)

```bash
# Create a new session
bun ~/.pi/agent/skills/tmux/lib.ts create my-task "echo 'Hello World'" task

# List all sessions
bun ~/.pi/agent/skills/tmux/lib.ts list

# Capture output
bun ~/.pi/agent/skills/tmux/lib.ts capture pi-task-my-task-20250107-123456

# Kill a session
bun ~/.pi/agent/skills/tmux/lib.ts kill pi-task-my-task-20250107-123456
```

## Socket Convention

- **Socket Directory**: `${TMPDIR:-/tmp}/pi-tmux-sockets`
- **Default Socket**: `/tmp/pi-tmux-sockets/pi.sock`
- **Environment Variable**: `PI_TMUX_SOCKET_DIR` (optional override)

All Agent sessions use a private socket to avoid conflicts with your personal tmux configuration.

## Session Naming

Sessions are named using the pattern: `pi-{category}-{name}-{timestamp}`

- **Categories**:
  - `task`: Temporary sub-tasks (compilation, testing)
  - `service`: Long-running services (dev servers, databases)
  - `agent`: Agent-specific tasks (training, data processing)

- **Examples**:
  - `pi-task-compile-20250107-123456`
  - `pi-service-dev-server-20250107-123456`
  - `pi-agent-training-20250107-123456`

## CLI Commands

### Create Session
```bash
bun ~/.pi/agent/skills/tmux/lib.ts create <name> <command> [category]
```

Creates a new tmux session and automatically prints the monitoring command.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts create compile "make clean && make all" task
```

### List Sessions
```bash
bun ~/.pi/agent/skills/tmux/lib.ts list [filter]
```

Lists all sessions with status and last activity time.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts list
bun ~/.pi/agent/skills/tmux/lib.ts list service
```

### Session Status
```bash
bun ~/.pi/agent/skills/tmux/lib.ts status <id>
```

Shows detailed information about a session.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts status pi-task-compile-20250107-123456
```

### Send Keys
```bash
bun ~/.pi/agent/skills/tmux/lib.ts send <id> <keys>
```

Sends keystrokes to a session. Uses literal mode to avoid shell escaping.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts send pi-task-python-20250107-123456 "print('Hello')"
```

### Capture Output
```bash
bun ~/.pi/agent/skills/tmux/lib.ts capture <id> [lines]
```

Captures pane output (default: 200 lines).

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts capture pi-task-compile-20250107-123456 500
```

### Kill Session
```bash
bun ~/.pi/agent/skills/tmux/lib.ts kill <id>
```

Terminates a tmux session.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts kill pi-task-compile-20250107-123456
```

### Cleanup Old Sessions
```bash
bun ~/.pi/agent/skills/tmux/lib.ts cleanup [hours]
```

Removes inactive sessions older than the specified age (default: 24 hours).

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts cleanup
bun ~/.pi/agent/skills/tmux/lib.ts cleanup 48
```

### Attach to Session
```bash
bun ~/.pi/agent/skills/tmux/lib.ts attach <id>
```

Prints the command to attach to a session interactively.

**Example**:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts attach pi-task-python-20250107-123456
# Output: tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t pi-task-python-20250107-123456
```

### Sync Sessions
```bash
bun ~/.pi/agent/skills/tmux/lib.ts sync
```

Synchronizes session status with tmux actual state.

## Session Persistence

Session information is stored in `${TMPDIR:-/tmp}/pi-tmux-sessions.json`. This allows:
- Cross-session recovery
- State tracking across Agent restarts
- Automatic cleanup of stale sessions

**Storage Format**:
```json
{
  "sessions": {
    "pi-task-compile-20250107-123456": {
      "id": "pi-task-compile-20250107-123456",
      "name": "compile",
      "category": "task",
      "socket": "/tmp/pi-tmux-sockets/pi.sock",
      "target": "pi-task-compile-20250107-123456:0.0",
      "command": "make clean && make all",
      "status": "running",
      "createdAt": "2025-01-07T12:34:56Z",
      "lastActivityAt": "2025-01-07T12:35:00Z"
    }
  },
  "lastSync": "2025-01-07T12:35:00Z"
}
```

## Use Cases

### Sub-task Execution
Execute temporary tasks that require monitoring:

```bash
# Start compilation
bun ~/.pi/agent/skills/tmux/lib.ts create compile "make all" task

# Wait for completion (in script)
bun ~/.pi/agent/skills/tmux/lib.ts capture pi-task-compile-20250107-123456 | grep "Build successful"

# Get result
bun ~/.pi/agent/skills/tmux/lib.ts capture pi-task-compile-20250107-123456

# Cleanup
bun ~/.pi/agent/skills/tmux/lib.ts kill pi-task-compile-20250107-123456
```

### Long-running Tasks
Run tasks in the background and check progress later:

```bash
# Start training
bun ~/.pi/agent/skills/tmux/lib.ts create training "python train.py --epochs 100" task

# Check progress later
bun ~/.pi/agent/skills/tmux/lib.ts list
bun ~/.pi/agent/skills/tmux/lib.ts capture pi-task-training-20250107-123456
```

### Service Management
Start development servers or services:

```bash
# Start dev server
bun ~/.pi/agent/skills/tmux/lib.ts create dev-server "npm run dev" service

# Monitor logs
tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t pi-service-dev-server-20250107-123456

# Stop when done
bun ~/.pi/agent/skills/tmux/lib.ts kill pi-service-dev-server-20250107-123456
```

### Interactive Tools
Use interactive tools like Python REPL, gdb, or databases:

```bash
# Python REPL (always use PYTHON_BASIC_REPL=1)
bun ~/.pi/agent/skills/tmux/lib.ts create python "PYTHON_BASIC_REPL=1 python3 -q" task

# Send commands
bun ~/.pi/agent/skills/tmux/lib.ts send pi-task-python-20250107-123456 "print('Hello')"
bun ~/.pi/agent/skills/tmux/lib.ts send pi-task-python-20250107-123456 "2 + 2"
```

## Status Detection

Sessions have three possible states:
- **running**: Process is active with recent output
- **idle**: Process exists but no recent output
- **exited**: Process has terminated

Status is automatically synced with tmux actual state.

## Automatic Cleanup

By default, sessions inactive for more than 24 hours are automatically cleaned up. You can:

- Trigger manual cleanup:
  ```bash
  bun ~/.pi/agent/skills/tmux/lib.ts cleanup [hours]
  ```

- Disable auto-cleanup in code:
  ```typescript
  const tmux = new TmuxManager({ autoCleanup: false });
  ```

## Helper Scripts

### wait-for-text.sh
Polls a pane for a regex pattern with timeout.

```bash
./scripts/wait-for-text.sh -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-t/--target`: Pane target (required)
- `-p/--pattern`: Regex to match (required); add `-F` for fixed string
- `-T`: Timeout in seconds (default: 15)
- `-i`: Poll interval in seconds (default: 0.5)
- `-l`: History lines to search (default: 1000)

### find-sessions.sh
Lists tmux sessions with metadata.

```bash
./scripts/find-sessions.sh -S "$SOCKET"
./scripts/find-sessions.sh --all  # Scan all sockets
```

## Examples

See the `examples/` directory for complete examples:
- `python-repl.ts`: Interactive Python REPL
- `long-task.ts`: Long-running task with progress
- `start-service.ts`: Service management

## TypeScript API

You can also use the TypeScript API directly:

```typescript
import { TmuxManager } from "~/.pi/agent/skills/tmux/lib.ts";

const tmux = new TmuxManager();

// Create session
const session = await tmux.createSession('compile', 'make all', 'task');

// Wait for output
const success = await tmux.waitForText(session.target, 'Build successful', { timeout: 60 });

// Capture output
const output = await tmux.capturePane(session.target, 200);

// Cleanup
await tmux.killSession(session.id);
```

## Monitoring Sessions

After creating a session, ALWAYS tell the user how to monitor it:

```
To monitor this session yourself:
  tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t pi-task-compile-20250107-123456

Or to capture the output once:
  tmux -S /tmp/pi-tmux-sockets/pi.sock capture-pane -p -J -t pi-task-compile-20250107-123456:0.0 -S -200
```

This must be printed immediately after session creation and at the end of the tool loop.

## Security Considerations

- Uses private socket path to avoid conflicts
- Sends keys in literal mode (`-l`) to prevent shell injection
- Checks tmux actual state before cleanup
- Requires explicit confirmation for destructive operations

## Troubleshooting

### Session not found
Run sync to update session state:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts sync
```

### Cannot attach to session
Ensure tmux is installed and the socket path is correct:
```bash
tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t <session-id>
```

### Sessions not cleaning up
Manually trigger cleanup:
```bash
bun ~/.pi/agent/skills/tmux/lib.ts cleanup
```

### Permission denied on socket
Check socket directory permissions:
```bash
ls -la /tmp/pi-tmux-sockets/
```

## Requirements

- tmux (Linux/macOS)
- Bun runtime
- Bash (for helper scripts)
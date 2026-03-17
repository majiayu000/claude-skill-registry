---
name: tmux
description: "Remote control tmux sessions for interactive CLIs, background tasks, and services."
license: MIT
---

# tmux Skill

## Core Concepts

**Socket**: `/tmp/pi-tmux-sockets/pi.sock` (private, no conflicts with personal tmux)

**Session Naming**: `pi-{category}-{name}-{timestamp}`
- Categories: `task` (temporary), `service` (long-running), `agent` (agent-specific)

**Session States**: `running` | `idle` | `exited`

**Persistence**: `/tmp/pi-tmux-sessions.json`

**Auto-cleanup**: Inactive sessions > 24h removed (configurable)

## CLI Commands

```bash
bun ~/.pi/agent/skills/tmux/lib.ts <command>

create <name> <command> [category]    # Create session, prints monitoring command
list [filter]                         # List sessions with status
status <id>                           # Session details
send <id> <keys>                      # Send keystrokes (literal mode, safe)
capture <id> [lines]                  # Capture pane output (default: 200)
kill <id>                             # Terminate session
cleanup [hours]                       # Remove old sessions (default: 24h)
attach <id>                           # Print attach command
sync                                  # Sync session state with tmux
```

**TUI**: `bun ~/.pi/agent/skills/tmux/tui.ts` (visual management, shortcuts: r/n/c/s/a/k/q)

## TypeScript API

```typescript
import { TmuxManager } from "~/.pi/agent/skills/tmux/lib.ts";

const tmux = new TmuxManager({ autoCleanup: false }); // optional config

// Session lifecycle
const session = await tmux.createSession(name, command, category);
await tmux.killSession(session.id);

// Output handling
const output = await tmux.capturePane(target, lines);
const success = await tmux.waitForText(target, pattern, { timeout: 60 });

// State management
const sessions = await tmux.listSessions(filter);
const status = await tmux.getSessionStatus(id);
await tmux.sync();
await tmux.cleanup(hours);
```

## Key Rules

1. **Always print monitoring command** after session creation:
   ```
   tmux -S /tmp/pi-tmux-sockets/pi.sock attach -t {session-id}
   ```

2. **Use `send` for interactive tools** (Python REPL, gdb, databases):
   ```bash
   # Python REPL: always use PYTHON_BASIC_REPL=1
   bun ~/.pi/agent/skills/tmux/lib.ts create python "PYTHON_BASIC_REPL=1 python3 -q" task
   bun ~/.pi/agent/skills/tmux/lib.ts send pi-task-python-* "print('Hello')"
   ```

3. **Category selection**:
   - `task`: compilation, testing, temporary operations
   - `service`: dev servers, databases, persistent services
   - `agent`: training, data processing, agent-specific tasks

4. **Safe key injection**: `send` uses literal mode (`-l`), no shell escaping needed

5. **Session recovery**: Run `sync` if session not found

## Helper Scripts

```bash
# Wait for text pattern with timeout
./scripts/wait-for-text.sh -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]

# List sessions with metadata
./scripts/find-sessions.sh -S "$SOCKET"
./scripts/find-sessions.sh --all
```

## Requirements

- tmux (Linux/macOS)
- Bun runtime
- Bash (helper scripts)
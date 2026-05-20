---
name: dry-run
description: "Simulates command execution in dry-run mode without file modifications. Sets dry_run flag, executes command with read-only constraint, then resets flag. Useful for testing workflows safely. Triggers on keywords: dry run, simulate, test command, preview changes, safe mode, no write"
project-agnostic: true
allowed-tools:
  - Bash
  - Write
  - Read
---

# Dry Run Skill

Executes any command or skill in simulation mode, preventing all file modifications except session state.

## Usage

```
/dry-run <any command or prompt>
```

Examples:
- `/dry-run /mux-ospec path/to/spec.md` - Preview full spec workflow
- `/dry-run /spec IMPLEMENT path/to/spec.md` - Test implementation without changes
- `/dry-run why did you implement X this way?` - Normal chat (no files affected)

## Workflow

### Step 1: Initialize Session Status

Resolve the Claude Code PID using process-tree tracing (same logic as the dry-run hook), then create the session directory:

```bash
CLAUDE_PID=$(python3 - <<'PY'
import os
import subprocess

pid = os.getpid()
for _ in range(10):
    result = subprocess.run(
        ["ps", "-o", "pid=,ppid=,comm=", "-p", str(pid)],
        capture_output=True,
        text=True,
    )
    line = result.stdout.strip()
    if not line:
        break

    parts = line.split()
    if len(parts) >= 3:
        current_pid, ppid, comm = int(parts[0]), int(parts[1]), parts[2]
        if "claude" in comm.lower():
            print(current_pid)
            break
        pid = ppid
    else:
        break
else:
    print("shared")
PY
)

[ -n "$CLAUDE_PID" ] || CLAUDE_PID="shared"
mkdir -p "outputs/session/${CLAUDE_PID}"
```

Check if `outputs/session/<CLAUDE_PID>/status.yml` exists. If not, create with initial schema:

```yaml
dry_run: false
```

### Step 2: Set Dry-Run Mode

Update `outputs/session/<CLAUDE_PID>/status.yml`:

```yaml
dry_run: true
```

This signals to THIS session's file operations that writes are prohibited.
Other Claude sessions (different PIDs) are not affected.

### Step 3: Execute Delegated Command

Execute the provided command/prompt EXACTLY as given. All behavior remains normal EXCEPT:

CRITICAL CONSTRAINTS:
- NO file modifications allowed (Read, Grep, Glob, LSP, Bash read-only commands OK)
- ONLY exception: `outputs/session/<CLAUDE_PID>/status.yml` can be modified
- If command requires file writes, DESCRIBE what WOULD be changed instead
- For chat-only prompts (no file operations needed), respond normally

### Step 4: Reset Dry-Run Mode

After execution completes (success or failure), reset state in `outputs/session/<CLAUDE_PID>/status.yml`:

```yaml
dry_run: false
```

### Step 5: Report Results

Provide summary:
- What was executed
- What file changes WOULD have occurred (if any)
- Verification that dry_run mode is reset

## Implementation Notes

The skill acts as a wrapper:
1. It does NOT interpret or execute the delegated work itself
2. It sets the flag, then lets normal AI behavior handle the prompt
3. The dry_run flag is checked by pretooluse hook (hard enforcement at tool level)
4. After completion, it ensures cleanup

## State Schema

`outputs/session/<claude_pid>/status.yml`:
```yaml
dry_run: bool  # true = prevent file writes, false = normal mode
```

Session isolation by Claude PID ensures parallel agents don't interfere with each other.
Future extensions may add additional session state fields.

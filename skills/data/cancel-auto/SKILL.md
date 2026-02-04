---
name: cancel-auto
description: EMERGENCY ONLY - Manually cancel running auto session. Generates summary report and releases lock. Activates for: cancel auto, stop auto, emergency cancel.
---

# Cancel Auto Command

**⚠️ EMERGENCY USE ONLY - Manually cancel the running auto session.**

> **Note**: Auto mode is designed to run until completion. In most cases, just close the Claude Code session and resume later with `/sw:do`. Only use this command in true emergencies.

## Usage

```bash
/sw:cancel-auto [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Cancel without confirmation |

## Examples

```bash
# Interactive cancel (asks for confirmation)
/sw:cancel-auto

# Force cancel without confirmation (emergency)
/sw:cancel-auto --force
```

## What It Does

1. Checks if auto session is active
2. Shows current session status
3. Asks for confirmation (unless --force)
4. Updates session status to "cancelled"
5. Releases session lock
6. Generates summary report

## Output Example

```
📊 Current Session

Session ID: auto-2025-12-29-abc123
Status: running
Iteration: 47
Current Increment: 0001-user-auth
Increments Completed: 2
Duration: 2h 15m

Cancel this session? [y/N] y

✅ Session cancelled

Summary: .specweave/logs/auto-2025-12-29-abc123-summary.md

💡 To resume work later, just run /sw:do
```

## Execution

When this command is invoked:

```bash
bash plugins/specweave/scripts/cancel-auto.sh [args]
```

## Notes

- **This command should rarely be needed** - auto mode is designed to run until completion
- **Preferred approach**: Just close the Claude Code session to pause, resume later with `/sw:do`
- Cancelling doesn't undo completed work
- tasks.md progress is preserved
- You can resume anytime with `/sw:do`
- Use Claude Code's `/resume` to restore full conversation context

## When to Use

**Use cancel-auto only for:**
- True emergencies (system resources, critical bugs)
- Need to force-stop a runaway session

**DON'T use for:**
- Normal pause/resume (just close Claude Code)
- Switching contexts (close tab, resume later)
- Profile switches (not supported - wrong concept)

---
name: cc-hooks
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Configure Claude Code hooks for PreToolUse, PostToolUse, Stop, Notification.
  Use when blocking commands, auto-formatting, custom permissions, or writing hooks.
practices:
- pragmatic-programmer
---
# Claude Code Hooks

Shell commands that fire at specific points in Claude Code's lifecycle.

<!-- TOC: Quick Start | Events | Blocking | Writing Hooks | Anti-Patterns | References -->

## Quick Start

Add to `~/.claude/settings.json` (user) or `.claude/settings.json` (project):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "my-validator.sh" }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | When | Blocks? | Common Use |
|-------|------|---------|------------|
| `PreToolUse` | Before tool runs | Yes | Block/modify commands |
| `PostToolUse` | After tool succeeds | Feedback | Auto-format, lint |
| `PermissionRequest` | Permission dialog | Yes | Auto-approve/deny |
| `UserPromptSubmit` | Prompt submitted | Yes | Add context, validate |
| `Stop` | Claude finishes | Yes | Force continue |
| `SessionStart` | Session begins | No | Load context, set env |
| `Notification` | Notifications | No | Desktop alerts |

Full schemas: [HOOK-EVENTS.md](references/HOOK-EVENTS.md)

## Matchers

```
"Bash"              → exact match
"Edit|Write"        → regex OR
"mcp__.*__write"    → MCP tools
"*" or ""           → all tools
```

Tools: `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Task`, `WebFetch`, `WebSearch`

## Exit Codes

| Code | Effect |
|------|--------|
| 0 | Success - JSON parsed from stdout |
| 2 | **Block** - stderr fed to Claude |
| Other | Non-blocking error |

## Blocking a Tool

**Simple (exit 2):**
```bash
echo "Blocked: reason" >&2 && exit 2
```

**JSON (exit 0):**
```json
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked"}}
```

Decisions: `"allow"` (auto-approve), `"deny"` (block), `"ask"` (show dialog)

## Modifying Input

```json
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow",
  "updatedInput":{"command":"modified-command"}}}
```

## Real-World: DCG + RCH

```json
{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[
  {"type":"command","command":"dcg"},
  {"type":"command","command":"rch"}
]}]}}
```

- **DCG**: Blocks `git reset --hard`, `rm -rf`, `git push --force`
- **RCH**: Routes builds to remote workers

Details: [DCG-RCH.md](references/DCG-RCH.md)

## Writing Your Own Hook

**Minimal Python:**
```python
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
cmd = data.get('tool_input', {}).get('command', '')

if 'dangerous' in cmd:
    print("Blocked: dangerous", file=sys.stderr)
    sys.exit(2)

sys.exit(0)  # Allow
```

**Hook input (stdin):**
```json
{"tool_name":"Bash","tool_input":{"command":"npm test"},"session_id":"...","cwd":"..."}
```

## Environment Variables

| Variable | Scope | Purpose |
|----------|-------|---------|
| `CLAUDE_PROJECT_DIR` | All | Project root |
| `CLAUDE_ENV_FILE` | SessionStart/Setup | Persist env vars |

## Stop Hook (Force Continue)

```json
{"decision":"block","reason":"Tests failing. Fix before stopping."}
```

**Critical:** Check `stop_hook_active` to prevent infinite loops.

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Old object format | Array format with `matcher` |
| Unquoted `$VAR` | `"$VAR"` |
| Exit 2 with JSON | Exit 2 uses stderr only |
| Skip `stop_hook_active` check | Always check in Stop hooks |

## Debugging

```bash
claude --debug  # Hook execution details
/hooks          # View/edit in REPL
```

## References

- [HOOK-EVENTS.md](references/HOOK-EVENTS.md) - All events with full schemas
- [DCG-RCH.md](references/DCG-RCH.md) - Production examples (dcg, rch)
- [PATTERNS.md](references/PATTERNS.md) - Auto-format, logging, notifications
- [JSON-OUTPUT.md](references/JSON-OUTPUT.md) - Response schemas

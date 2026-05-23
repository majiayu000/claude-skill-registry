---
name: hooks-manager
description: Manage Claude Code lifecycle hooks for automation (secrets scan, auto-format, audit log, session context).
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash
metadata: {"oneshot":{"emoji":"🪝","requires":{"bins":["bash"]}}}
---

# Hooks Manager

Manage Claude Code lifecycle hooks for automation.

## When To Use

- User says "setup hooks", "add hooks", "configure hooks"
- User says "secrets scan", "auto-format", "audit log"
- User wants automation on tool execution or session events

## Available Hooks

| Hook | Trigger | Use Case |
|------|---------|----------|
| `secrets-scan` | PreToolUse (Write/Edit) | Block commits containing secrets |
| `auto-format` | PostToolUse (Write/Edit) | Format code after writing |
| `audit-log` | PostToolUse (*) | Log all tool executions |
| `session-context` | SessionStart | Inject project context |

## Workflow

### 1. Check Current Hooks

```bash
# In Claude Code
/hooks
```

### 2. Install Hook Scripts

Copy to project:
```bash
mkdir -p .claude/hooks
cp ~/.claude/skills/oneshot/hooks/*.sh .claude/hooks/
chmod +x .claude/hooks/*.sh
```

### 3. Configure settings.json

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/secrets-scan.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-format.sh",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-log.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-context.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Hook Scripts Reference

### secrets-scan.sh
Blocks writes containing potential secrets (API keys, tokens, passwords).

**Exit codes:**
- 0: No secrets found
- 2: Secrets detected (blocks the write)

### auto-format.sh
Runs project formatter (prettier, black, gofmt) after file writes.

**Supports:** .js, .ts, .py, .go, .rs, .json, .yaml, .md

### audit-log.sh
Appends tool executions to `.claude/audit.log`.

**Format:** `TIMESTAMP | TOOL | FILE_PATH`

### session-context.sh
Injects project context on session start (reads LLM-OVERVIEW.md, TODO.md).

## Minimal Setup (Secrets Only)

For just secrets scanning:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/secrets-scan.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Inputs

- User request for hook configuration
- Existing `.claude/settings.json` (if any)

## Outputs

- Hook scripts in `.claude/hooks/`
- Updated `.claude/settings.json`
- Verification that hooks are registered (`/hooks`)

## Keywords

hooks, automation, secrets scan, auto-format, audit log, pre-tool, post-tool, session start

---
name: kit-hooks
description: (ePost) This skill should be used when the user asks to "create a hook", "add a hook", "write a PreToolUse hook", "implement a SessionStart hook", "block tool access", "validate tool use", "add automation on stop", or mentions hook events (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification). Provides guidance for creating hooks in the epost_agent_kit package system.
user-invocable: false
  connections:
    enhances: [kit-agents]
---

# Hook Development for epost_agent_kit

## Overview

Hooks are event-driven automation scripts that execute in response to Claude Code events. Use hooks to validate operations, enforce policies, add context, and integrate external tools.

## Hook Types

### Command Hooks (Deterministic)

Execute bash/node scripts for fast, deterministic checks:

```json
{
  "type": "command",
  "command": "node .claude/hooks/my-hook.cjs",
  "timeout": 60
}
```

### Prompt Hooks (LLM-Driven)

Use Claude for context-aware validation:

```json
{
  "type": "prompt",
  "prompt": "Validate this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

Supported events: Stop, SubagentStop, UserPromptSubmit, PreToolUse

## Hook Events

| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool runs | Validation, blocking, modification |
| `PostToolUse` | After tool completes | Feedback, logging, lint/build |
| `UserPromptSubmit` | User sends prompt | Context injection, rules reminder |
| `Stop` | Agent stopping | Completeness check, notification |
| `SubagentStop` | Subagent done | Task validation |
| `SessionStart` | Session begins | Project detection, env setup |
| `SessionEnd` | Session ends | Cleanup, logging |
| `PreCompact` | Before compaction | Preserve critical context |
| `Notification` | User notified | Reactions |

## Hook Configuration in settings.json

Hooks are configured in `packages/core/settings.json` under the `hooks` key:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Glob|Grep|Read|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node .claude/hooks/scout-block.cjs",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Matchers

- Exact: `"matcher": "Write"`
- Multiple: `"matcher": "Read|Write|Edit"`
- Wildcard: `"matcher": "*"`
- Regex: `"matcher": "mcp__.*__delete.*"`

## Input/Output Contract

### Input (JSON via stdin)

```json
{
  "session_id": "abc123",
  "cwd": "/project/dir",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path" }
}
```

### Output (JSON via stdout)

**PreToolUse decisions:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask"
  },
  "systemMessage": "Explanation for Claude"
}
```

**Exit codes:** 0 = success, 2 = blocking error (stderr → Claude)

## epost_agent_kit Hook Architecture

Hooks live in `packages/core/hooks/` and are generated to `.claude/hooks/`:

```
packages/core/hooks/
├── session-init.cjs            # SessionStart: project detection, env vars, plan resolution
├── subagent-init.cjs           # SubagentStart: compact context injection to Task agents
├── context-reminder.cjs        # UserPromptSubmit: session context + rules (deduplicated)
├── scout-block.cjs             # PreToolUse: block node_modules/dist/.git per .epost-ignore
├── privacy-block.cjs           # PreToolUse: block .env/secrets unless APPROVED: prefix
├── subagent-stop-reminder.cjs  # SubagentStop: post-agent reminders (planner → /cook)
├── session-metrics.cjs         # Stop: record session duration/git stats → .epost-data/
├── lesson-capture.cjs          # Stop: evaluate significance, prompt knowledge capture
└── notifications/
    └── notify.cjs              # Stop: Discord/Telegram notification

packages/kit/hooks/
├── kit-session-check.cjs       # SessionStart: check skill-index.json staleness
├── kit-write-guard.cjs         # PreToolUse: block writes to .claude/ in kit-repo context
└── kit-post-edit-reminder.cjs  # PostToolUse: skill index + re-init + stale ref scan
```

Configuration files:
- `.epost-kit.json` — Hook config (plan naming, project type, hook toggles, validation rules)
- `.epost-ignore` — Scout-block patterns (gitignore-spec format)

## Creating a New Hook

1. Create hook script in `packages/{package}/hooks/{hook-name}.cjs`
2. Wire into `packages/core/settings.json` under appropriate event
3. Add to `packages/{package}/package.yaml` files mapping if needed
4. Run `epost-kit init --fresh` to regenerate

## Additional Resources

For detailed patterns, security practices, and advanced techniques:
- **`references/hook-patterns.md`** — Common patterns, testing, debugging

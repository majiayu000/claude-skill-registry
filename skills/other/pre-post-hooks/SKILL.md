---
name: pre-post-hooks
description: >
  Guide for configuring PreToolUse, PostToolUse, and Stop hooks in Claude Code.
  Use when the user asks about hooks, wants to run commands before/after tool calls,
  needs auto-formatting, auto-linting, validation gates, or mentions settings.json hook config.
---

# Pre/Post Hooks

Claude Code hooks are shell commands that execute automatically in response to tool events. They enable validation, formatting, and guardrails without manual intervention.

## When to Use
- User wants to run a command before or after a tool executes
- User asks about PreToolUse, PostToolUse, or Stop hooks
- User wants to add validation gates or blockers
- User needs to configure hooks in settings.json
- User mentions auto-running commands on file edit, git push, or session end

## Core Patterns

### Hook Types and Lifecycle

```
PreToolUse  --> Tool Executes --> PostToolUse
                                       |
                                  (session ends)
                                       |
                                     Stop
```

- **PreToolUse**: Runs before a tool call. Can block execution by returning a non-zero exit code.
- **PostToolUse**: Runs after a tool call completes. Used for side effects like formatting or checks.
- **Stop**: Runs when the agent session ends. Used for final audits or cleanup.

### Hook Configuration in settings.json

Hooks live in `~/.claude/settings.json` under the `hooks` key:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "echo 'About to write a file'",
        "description": "Log before file writes"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\"",
        "description": "Auto-format after editing JS/TS files"
      }
    ],
    "Stop": [
      {
        "command": "echo 'Session ended'",
        "description": "Log session end"
      }
    ]
  }
}
```

### Matcher Patterns

The `matcher` field filters which tool triggers the hook. It matches against tool names:

```json
{
  "matcher": "Edit",
  "command": "..."
}
```

Common tool names to match:
- `Write` — file creation
- `Edit` — file modification
- `Bash` — shell command execution
- `Read` — file reading
- `Glob` — file search
- `Grep` — content search

Use pipe `|` for multiple matchers:

```json
{
  "matcher": "Write|Edit",
  "command": "npx prettier --write \"$CLAUDE_FILE_PATH\""
}
```

Omit `matcher` entirely to match ALL tool calls (useful for Stop hooks).

### Environment Variables in Hooks

Hooks receive context via environment variables:

| Variable | Description |
|----------|-------------|
| `CLAUDE_FILE_PATH` | The file path being operated on |
| `CLAUDE_TOOL_NAME` | Name of the tool being called |
| `CLAUDE_SESSION_ID` | Current session identifier |

### Blocking with PreToolUse

A PreToolUse hook that exits non-zero blocks the tool from executing:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "echo \"$CLAUDE_FILE_PATH\" | grep -qv '\\.md$' || (echo 'BLOCKED: Do not create markdown files' && exit 1)",
        "description": "Block creation of .md files"
      }
    ]
  }
}
```

### PostToolUse Side Effects

Run checks or formatting after tool execution without blocking:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -q '\\.ts$'; then npx tsc --noEmit \"$CLAUDE_FILE_PATH\" 2>&1 | head -20; fi",
        "description": "Type-check TypeScript files after edit"
      }
    ]
  }
}
```

### Stop Hook for Final Audit

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "git diff --cached --name-only | xargs grep -l 'console.log' 2>/dev/null && echo 'WARNING: console.log found in staged files'",
        "description": "Audit staged files for console.log before session ends"
      }
    ]
  }
}
```

## Anti-Patterns

- **Slow hooks on hot paths**: Do not run expensive commands (full test suite, large builds) in PostToolUse on every Edit. It blocks the agent loop. Use targeted, fast checks instead.
- **Blocking reads**: Do not use PreToolUse to block Read or Grep calls. These are non-destructive and blocking them disrupts exploration.
- **Missing error handling**: Hook commands that fail silently hide problems. Always include meaningful error messages in blocking hooks.
- **Hardcoded paths**: Use `$CLAUDE_FILE_PATH` instead of hardcoding file paths. Hooks should be project-agnostic.
- **Too many hooks**: Each hook adds latency to every matching tool call. Keep the hook list focused on high-value checks.

## Quick Reference

| Hook Type | Timing | Can Block? | Use Case |
|-----------|--------|------------|----------|
| PreToolUse | Before tool | Yes (exit 1) | Validation, gates, warnings |
| PostToolUse | After tool | No | Formatting, type-checking, linting |
| Stop | Session end | No | Final audits, cleanup |

**Config location**: `~/.claude/settings.json` > `hooks`
**Matcher syntax**: Tool name string, pipe-separated for multiple
**Blocking**: Only PreToolUse can block (non-zero exit code)

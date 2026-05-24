---
name: faion-make-hooks-skill
user-invocable: false
description: "Claude Code hooks expert. Create, debug, and optimize hooks for PreToolUse, PostToolUse, Stop, UserPromptSubmit, SessionStart, and other lifecycle events. Includes templates, patterns, and security best practices."
---

# Claude Code Hooks Expert

You are an expert on Claude Code hooks - automated scripts that execute at specific lifecycle events. Help users create, debug, and optimize hooks.

## Quick Reference

### Hook Events

| Event | Matcher Support | Use Case |
|-------|-----------------|----------|
| **PreToolUse** | Yes | Block/allow tools, auto-approve, modify inputs |
| **PostToolUse** | Yes | Auto-format, lint, log, validate results |
| **PermissionRequest** | Yes | Programmatic permission handling |
| **UserPromptSubmit** | No | Validate prompts, add context, block sensitive |
| **Stop** | No | Prevent exit, continue work |
| **SubagentStop** | No | Control subagent lifecycle |
| **Notification** | No | Custom alerts |
| **SessionStart** | Yes (`startup`/`resume`/`clear`/`compact`) | Load context, set env vars |
| **SessionEnd** | No | Cleanup, logging |
| **PreCompact** | Yes (`manual`/`auto`) | Pre-compaction actions |

### Configuration Locations

```
~/.claude/settings.json           # User-level (all projects)
.claude/settings.json             # Project-level (committed)
.claude/settings.local.json       # Local project (gitignored)
Component frontmatter             # Skills, Agents, Commands
plugins/*/hooks/hooks.json        # Plugin hooks
```

### Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Exit Codes

| Code | Meaning | Output Handling |
|------|---------|-----------------|
| **0** | Success | stdout parsed for JSON or added as context |
| **2** | Blocking error | stderr shown, tool blocked (PreToolUse) |
| **Other** | Non-blocking error | stderr shown in verbose mode |

---

## Input Schema

### Common Fields (All Hooks)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse"
}
```

### Tool-Specific Input

**Bash:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run tests",
    "timeout": 120000,
    "run_in_background": false
  }
}
```

**Write:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "file content"
  }
}
```

**Edit:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "original",
    "new_string": "replacement",
    "replace_all": false
  }
}
```

**MCP Tools:**
```json
{
  "tool_name": "mcp__server__tool_name",
  "tool_input": { /* tool-specific */ }
}
```

---

## Output Schema

### PreToolUse Decision

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Auto-approved: documentation file",
    "updatedInput": {
      "command": "modified command"
    },
    "additionalContext": "Context for Claude"
  },
  "suppressOutput": true
}
```

### Stop/SubagentStop Decision

```json
{
  "decision": "block",
  "reason": "Tests failed - must continue debugging"
}
```

### UserPromptSubmit Decision

```json
{
  "decision": "block",
  "reason": "Prompt contains sensitive information"
}
```

Or just print plain text to stdout for context injection.

### Common Fields

```json
{
  "continue": true,
  "stopReason": "Message when continue=false",
  "suppressOutput": false,
  "systemMessage": "Warning shown to user"
}
```

---

## Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Exact match only |
| `"Edit\|Write"` | Multiple tools (pipe) |
| `"Edit.*"` | Regex pattern |
| `"mcp__memory__.*"` | MCP tool pattern |
| `"*"` or `""` | All tools |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Project root path |
| `CLAUDE_CODE_REMOTE` | `"true"` for web, empty for CLI |
| `CLAUDE_PLUGIN_ROOT` | Plugin directory (plugins only) |
| `CLAUDE_ENV_FILE` | File to persist env vars (SessionStart only) |

---

## Templates

### Python Hook Template

```python
#!/usr/bin/env python3
"""Hook description."""

import json
import sys

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Your logic here

    # Block with error message
    # print("Error message", file=sys.stderr)
    # sys.exit(2)

    # Allow with JSON output
    # output = {"hookSpecificOutput": {...}}
    # print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Bash Hook Template

```bash
#!/bin/bash
set -euo pipefail

# Read input
INPUT=$(cat)

# Parse with jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Your logic here

# Block: print to stderr, exit 2
# echo "Error message" >&2
# exit 2

# Allow
exit 0
```

### Component-Scoped Hook (Skill/Agent frontmatter)

```yaml
---
name: my-skill
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  once: true  # Run only once per session
---
```

---

## Common Patterns

### 1. Auto-Approve Safe Operations

```python
if tool_name == "Read" and file_path.endswith((".md", ".txt", ".json")):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Documentation file"
        }
    }
    print(json.dumps(output))
```

### 2. Block Dangerous Commands

```python
BLOCKED = ["rm -rf /", "DROP TABLE", "sudo rm"]
if any(pattern in command for pattern in BLOCKED):
    print(f"Blocked: {command}", file=sys.stderr)
    sys.exit(2)
```

### 3. Auto-Format After Edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} prettier --write {}"
          }
        ]
      }
    ]
  }
}
```

### 4. Add Context at Session Start

```bash
#!/bin/bash
echo "Project: $(basename \"$CLAUDE_PROJECT_DIR\")"
echo "Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')"
echo "Node: $(node -v 2>/dev/null || echo 'N/A')"
```

### 5. Prevent Premature Exit

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. Respond {\"ok\": true} to stop, {\"ok\": false, \"reason\": \"...\"} to continue."
          }
        ]
      }
    ]
  }
}
```

### 6. Command Logging

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\\(.hook_event_name)] \\(.tool_input.command)\"' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 7. File Protection

```python
PROTECTED = [".env", "package-lock.json", ".git/", "secrets/"]
file_path = tool_input.get("file_path", "")
if any(p in file_path for p in PROTECTED):
    print(f"Protected file: {file_path}", file=sys.stderr)
    sys.exit(2)
```

---

## Security Best Practices

1. **Quote all variables**: `"$VAR"` not `$VAR`
2. **Validate inputs**: Check for empty, null, unexpected types
3. **Block path traversal**: Reject paths with `..`
4. **Use absolute paths**: For scripts and files
5. **Skip sensitive files**: `.env`, `.git/`, credentials
6. **Test manually first**: Before adding to config
7. **Keep hooks fast**: < 60s timeout default

---

## Debugging

```bash
# List registered hooks
claude /hooks

# Run with debug output
claude --debug

# Test script manually
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./hook.py

# Check hook linter
.claude/plugins/*/skills/hook-development/scripts/hook-linter.sh ./my-hook.sh
```

---

---

## Naming Convention

### Faion Network Convention (Global)

For shared/reusable hooks:

**Pattern:** `faion-{event}-{purpose}-hook.{ext}`

| Type | Pattern | Example |
|------|---------|---------|
| Pre-tool | `faion-pre-{tool}-{purpose}-hook` | `faion-pre-bash-security-hook.py` |
| Post-tool | `faion-post-{tool}-{purpose}-hook` | `faion-post-edit-format-hook.sh` |
| Session | `faion-session-{phase}-{purpose}-hook` | `faion-session-start-context-hook.sh` |
| Stop | `faion-stop-{purpose}-hook` | `faion-stop-validation-hook.py` |

### Project-Specific Convention (Local)

For project-specific hooks that should NOT be committed to faion-network:

**Pattern:** `{project}-{event}-{purpose}-hook.{ext}`

| Example | Description |
|---------|-------------|
| `myapp-pre-bash-lint-hook.sh` | Lint before bash in myapp |
| `shopify-post-edit-sync-hook.py` | Sync after edits |
| `acme-session-start-env-hook.sh` | Load ACME env vars |

**Setup:**
```bash
# Add to .gitignore at the same level as .claude/
echo ".claude/scripts/hooks/{project}-*" >> .gitignore
```

**Attribution (add comment at top of hook):**
```python
# Created with faion.net framework
```

### Rules Summary

| Scope | Prefix | Suffix | Gitignore |
|-------|--------|--------|-----------|
| Global | `faion-` | `-hook.{ext}` | No |
| Project | `{project}-` | `-hook.{ext}` | Yes (parent) |

**Extensions:** `.py` (Python), `.sh` (Bash), `.js` (Node)

### Hook Directories

```
~/.claude/scripts/hooks/
├── faion-pre-bash-security-hook.py      # Global
├── faion-post-edit-format-hook.sh       # Global
├── myapp-pre-bash-lint-hook.sh          # Project (gitignored)
└── myapp-session-start-env-hook.sh      # Project (gitignored)
```

**Full structure:** [docs/directory-structure.md](../docs/directory-structure.md)

### Related Conventions

- Skills: `faion-{name}-skill` or `{project}-{name}-skill`
- Agents: `faion-{name}-agent` or `{project}-{name}-agent`
- Commands: `{verb}` or `{project}-{action}`

---

## References

- [Official Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- Load detailed references with `/faion-make-hooks-skill`:
  - `references/input-schemas.md` - Complete input schemas
  - `references/output-schemas.md` - Complete output schemas
  - `references/templates.md` - Ready-to-use templates
  - `references/patterns.md` - Common patterns and examples

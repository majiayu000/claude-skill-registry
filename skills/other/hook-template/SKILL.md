---
name: hook-template
description: Generate hook script from template
user-invocable: true
---

# Hook Template Generator

Generate a hook script and configuration based on requirements.

**Usage**: `/hook-template [hook-type] [purpose]`

---

## Hook Types

| Type | When it Runs | Use Case |
|------|--------------|----------|
| `PreToolUse` | Before a tool runs | Block, validate, add context |
| `PostToolUse` | After a tool completes | Log, notify, react |
| `UserPromptSubmit` | User submits a prompt | Context injection, validation |
| `Stop` | Main agent stopping | Completeness check, continue loops |
| `SubagentStop` | Subagent finishes | Task validation |
| `SessionStart` | Session begins | Context loading, env setup |
| `SessionEnd` | Session ends | Cleanup, logging |
| `PreCompact` | Before context compaction | Preserve critical context |
| `PostCompact` | After compaction completes | Context recovery |
| `Notification` | User is notified | External alerts (Slack, etc.) |
| `Elicitation` | MCP server requests input | Override elicitation |
| `ElicitationResult` | Elicitation result available | Post-process |

---

## Hook Config Fields

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `type` | String | Yes | - | `"command"` or `"prompt"` |
| `command` | String | If type=command | - | Shell command to execute |
| `prompt` | String | If type=prompt | - | Natural language prompt for LLM |
| `timeout` | Integer | No | 60s (command), 30s (prompt) | Seconds |
| `once` | Boolean | No | false | Run hook only once per session |

---

## Hook Input (stdin JSON)

All hooks receive JSON on stdin with these fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path/to/file" }
}
```

---

## Process

1. **Gather Requirements**
   - Hook type
   - Purpose
   - Matcher (for Pre/PostToolUse: tool name, regex, or `*`)

2. **Generate Script** at `.claude/hooks/[name].sh`

3. **Update settings.json** with hook config

4. **Make Executable**: `chmod +x`

5. **Validate** with `/hooks-check`

---

## Templates

### PreToolUse (Blocker)
```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block edits to specific files
if [[ "$FILE" == *"package-lock.json"* ]]; then
    echo "BLOCKED: Do not edit lockfiles directly" >&2
    exit 2
fi
exit 0  # Allow (no output needed)
```

### PreToolUse (Context Adding)
```bash
#!/bin/bash
cat > /dev/null  # Consume stdin
INFO="This file requires careful review"
jq -n --arg ctx "$INFO" '{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": $ctx
    }
}'
exit 0
```

### PostToolUse (Logger)
```bash
#!/bin/bash
INPUT=$(cat)
# Process and log... (no stdout needed)
exit 0
```

### Stop (Auto-Loop)
```bash
#!/bin/bash
CHECKPOINT=".auto-loop/checkpoint.json"
if [[ ! -f "$CHECKPOINT" ]]; then
    exit 0  # Allow stop
fi
# Block stop to continue loop
jq -n --arg reason "Continuing iteration" \
    '{"decision": "block", "reason": $reason}'
exit 0
```

### SessionStart (Context Load)
```bash
#!/bin/bash
cat > /dev/null
echo "Loading project context..." >&2
exit 0
```

### Prompt Hook (LLM-based)

Instead of a bash script, use `type: "prompt"` in settings.json:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the work done. Return 'approve' if complete, or 'block' with reason.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## Settings.json Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/load-context.sh",
            "once": true
          }
        ]
      }
    ]
  }
}
```

---

## Example

```
/hook-template PreToolUse "block edits to package-lock.json"

Creates:
- .claude/hooks/protect-lockfile.sh
- Updates .claude/settings.json
```

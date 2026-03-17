---
name: hooks-reference
description: >-
  Use this skill when asked about "hooks", "PreToolUse", "PostToolUse",
  "SessionStart", "hook events", "validate tool use", "block commands",
  "add context on session start", or implementing event-driven automation.
---

# Hooks Reference Skill

This skill provides comprehensive guidance for implementing Claude Code hooks - event handlers that automate validation, context loading, and workflow enforcement.

## Hook Events Overview

| Event | When Triggered | Use Cases |
|-------|----------------|-----------|
| `PreToolUse` | Before tool executes | Validate, block, modify |
| `PostToolUse` | After tool completes | Audit, react, verify |
| `PermissionRequest` | Permission dialog shown | Auto-allow, auto-deny |
| `Stop` | Claude finishes | Force continue, verify |
| `SubagentStop` | Subagent finishes | Verify task complete |
| `SessionStart` | Session begins | Load context, setup |
| `SessionEnd` | Session ends | Cleanup, save state |
| `UserPromptSubmit` | Prompt submitted | Validate, add context |
| `PreCompact` | Before compaction | Preserve info |
| `Notification` | Notification sent | Alert, log |

## hooks.json Structure

Basic structure:
```json
{
  "description": "What these hooks do",
  "hooks": {
    "EventName": [
      {
        "matcher": "Pattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/handler.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

For tool events (PreToolUse, PostToolUse, PermissionRequest):
- `"Write"` - Match exact tool name
- `"Write|Edit"` - Match multiple tools (regex)
- `"Notebook.*"` - Regex pattern
- `"*"` or `""` - Match all tools

For SessionStart:
- `"startup"` - Initial startup
- `"resume"` - From --resume, --continue, /resume
- `"clear"` - From /clear
- `"compact"` - From auto/manual compact

For Notification:
- `"permission_prompt"` - Permission requests
- `"idle_prompt"` - Claude waiting for input

## Hook Types

### Command Hooks (type: "command")
Execute a bash script:
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 30
}
```

### Prompt Hooks (type: "prompt")
LLM-based evaluation (Stop, SubagentStop only):
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

## Exit Codes

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| 0 | Success | Action proceeds, stdout to user (verbose) |
| 2 | Block | Action blocked, stderr shown to Claude |
| Other | Error | Non-blocking, stderr to user (verbose) |

## Hook Input (stdin JSON)

Common fields:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

PreToolUse specific:
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_use_id": "toolu_01ABC..."
}
```

SessionStart specific:
```json
{
  "source": "startup"
}
```

Stop specific:
```json
{
  "stop_hook_active": false
}
```

## Advanced JSON Output

Return structured decisions via stdout (exit code 0):

### PreToolUse Decision Control
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved documentation file",
    "updatedInput": {
      "field_to_modify": "new value"
    }
  }
}
```

Decision values: `"allow"`, `"deny"`, `"ask"`

### Stop Decision Control
```json
{
  "decision": "block",
  "reason": "Not all tasks complete - still need to run tests"
}
```

### UserPromptSubmit Context
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Current time: 2024-01-15 10:30:00"
  }
}
```

### SessionStart Context
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project context loaded..."
  }
}
```

## Example Hooks

### 1. Validate File Writes (PreToolUse)

hooks/hooks.json:
```json
{
  "description": "Validate file write operations",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-write.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

scripts/validate-write.sh:
```bash
#!/usr/bin/env bash

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# Block writes to sensitive files
if [[ "$FILE_PATH" == *.env* ]] || [[ "$FILE_PATH" == *secret* ]]; then
  echo "Cannot write to sensitive files: $FILE_PATH" >&2
  exit 2
fi

# Block writes outside project
if [[ ! "$FILE_PATH" == "$CLAUDE_PROJECT_DIR"* ]]; then
  echo "Cannot write outside project directory" >&2
  exit 2
fi

exit 0
```

### 2. Block Dangerous Commands (PreToolUse)

hooks/hooks.json:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

scripts/validate-bash.sh:
```bash
#!/usr/bin/env bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block destructive commands
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  ":(){ :|:& };:"
  "> /dev/sda"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "Blocked dangerous command pattern: $pattern" >&2
    exit 2
  fi
done

exit 0
```

### 3. Load Project Context (SessionStart)

hooks/hooks.json:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

scripts/load-context.sh:
```bash
#!/usr/bin/env bash

CONTEXT=""

# Load CLAUDE.md if exists
if [ -f "$CLAUDE_PROJECT_DIR/CLAUDE.md" ]; then
  CONTEXT+="Project instructions from CLAUDE.md have been loaded.\n"
fi

# Add git status
if [ -d "$CLAUDE_PROJECT_DIR/.git" ]; then
  BRANCH=$(git -C "$CLAUDE_PROJECT_DIR" branch --show-current 2>/dev/null)
  CONTEXT+="Current git branch: $BRANCH\n"
fi

# Output as JSON for structured context
cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "$CONTEXT"
  }
}
EOF

exit 0
```

### 4. Verify Before Stop (Stop)

Using prompt-based hook:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop. Context: $ARGUMENTS\n\nCheck if:\n1. All requested tasks are complete\n2. No errors need addressing\n3. No tests need running\n\nRespond with: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

### 5. Add Timestamp to Prompts (UserPromptSubmit)

hooks/hooks.json:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/add-timestamp.sh"
          }
        ]
      }
    ]
  }
}
```

scripts/add-timestamp.sh:
```bash
#!/usr/bin/env bash

# Plain text stdout is added as context
echo "Current time: $(date '+%Y-%m-%d %H:%M:%S %Z')"

exit 0
```

## Environment Variables

Available in hooks:
- `${CLAUDE_PLUGIN_ROOT}` - Absolute path to plugin directory
- `$CLAUDE_PROJECT_DIR` - Project root directory
- `$CLAUDE_ENV_FILE` - (SessionStart only) File to persist env vars
- `$CLAUDE_CODE_REMOTE` - "true" if running in web environment

## Persisting Environment (SessionStart)

```bash
#!/usr/bin/env bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export API_URL=http://localhost:3000' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

## Best Practices

1. **Always quote variables**: Use `"$VAR"` not `$VAR`
2. **Validate input**: Never trust stdin blindly
3. **Use portable paths**: `${CLAUDE_PLUGIN_ROOT}` for plugin files
4. **Set timeouts**: Prevent hanging hooks
5. **Handle errors**: Check for missing fields with `// empty`
6. **Keep hooks fast**: Target <1 second execution
7. **Use jq for JSON**: Safer than string parsing

## Debugging

Enable debug mode:
```bash
claude --debug
```

Test hook manually:
```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | \
  ./scripts/validate-write.sh
echo $?  # Check exit code
```

## References

- Hooks documentation: https://code.claude.com/docs/en/hooks
- Hooks guide: https://code.claude.com/docs/en/hooks-guide
- Example hooks: https://github.com/anthropics/claude-code/tree/main/examples/hooks

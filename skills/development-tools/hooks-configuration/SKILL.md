---
model: haiku
name: hooks-configuration
description: |
  Claude Code hooks configuration and development. Covers hook lifecycle events,
  configuration patterns, input/output schemas, and common automation use cases.
  Use when user mentions hooks, automation, PreToolUse, PostToolUse, SessionStart,
  SubagentStart, or needs to enforce consistent behavior in Claude Code workflows.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, TodoWrite
---

# Claude Code Hooks Configuration

Expert knowledge for configuring and developing Claude Code hooks to automate workflows and enforce best practices.

## Core Concepts

**What Are Hooks?**
Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. Unlike relying on Claude to "decide" to run something, hooks provide **deterministic, guaranteed execution**.

**Why Use Hooks?**
- Enforce code formatting automatically
- Block dangerous commands before execution
- Inject context at session start
- Log commands for audit trails
- Send notifications when tasks complete

## Hook Lifecycle Events

| Event | When It Fires | Key Use Cases |
|-------|---------------|---------------|
| **SessionStart** | Session begins/resumes | Environment setup, context loading |
| **UserPromptSubmit** | User submits prompt | Input validation, context injection |
| **PreToolUse** | Before tool execution | Permission control, blocking dangerous ops |
| **PostToolUse** | After tool completes | Auto-formatting, logging, validation |
| **Stop** | Agent finishes | Notifications, git reminders |
| **SubagentStart** | Subagent is about to start | Input modification, context injection |
| **SubagentStop** | Subagent finishes | Task completion evaluation |
| **PreCompact** | Before context compaction | Transcript backup |
| **Notification** | Claude sends notification | Custom alerts |
| **SessionEnd** | Session terminates | Cleanup, state persistence |

## Configuration

### File Locations

Hooks are configured in settings files:

- **`~/.claude/settings.json`** - User-level (applies everywhere)
- **`.claude/settings.json`** - Project-level (committed to repo)
- **`.claude/settings.local.json`** - Local project (not committed)

Claude Code merges all matching hooks from all files.

### Frontmatter Hooks (Skills and Commands)

Hooks can also be defined directly in skill and command frontmatter using the `hooks` field:

```yaml
---
name: my-skill
description: A skill with hooks
allowed-tools: Bash, Read
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo 'Pre-tool hook from skill'"
          timeout: 10
---
```

This allows skills and commands to define their own hooks that are active only when that skill/command is in use.

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
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns

- **Exact match**: `"Bash"` - matches exactly "Bash" tool
- **Regex patterns**: `"Edit|Write"` - matches either tool
- **Wildcards**: `"Notebook.*"` - matches tools starting with "Notebook"
- **All tools**: `"*"` - matches everything
- **MCP tools**: `"mcp__server__tool"` - targets MCP server tools

## Input Schema

Hooks receive JSON via stdin with these common fields:

```json
{
  "session_id": "unique-session-id",
  "transcript_path": "/path/to/conversation.json",
  "cwd": "/current/working/directory",
  "permission_mode": "mode",
  "hook_event_name": "PreToolUse"
}
```

**PreToolUse additional fields:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

**PostToolUse additional fields:**
```json
{
  "tool_name": "Bash",
  "tool_input": { ... },
  "tool_response": { ... }
}
```

**SubagentStart additional fields:**
```json
{
  "subagent_type": "Explore",
  "subagent_prompt": "original prompt text",
  "subagent_model": "claude-sonnet-4-20250514"
}
```

## Output Schema

### Exit Codes

- **0**: Success (command allowed)
- **2**: Blocking error (stderr shown to Claude, operation blocked)
- **Other**: Non-blocking error (logged in verbose mode)

### JSON Response (optional)

**PreToolUse:**
```json
{
  "permissionDecision": "allow|deny|ask",
  "permissionDecisionReason": "explanation",
  "updatedInput": { "modified": "input" }
}
```

**Stop/SubagentStop:**
```json
{
  "decision": "block",
  "reason": "required explanation for continuing"
}
```

**SubagentStart (input modification):**
```json
{
  "updatedPrompt": "modified prompt text to inject context or modify behavior"
}
```

**SessionStart:**
```json
{
  "additionalContext": "Information to inject into session"
}
```

## Common Hook Patterns

### Block Dangerous Commands (PreToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block rm -rf /
if echo "$COMMAND" | grep -Eq 'rm\s+(-rf|-fr)\s+/'; then
    echo "BLOCKED: Refusing to run destructive command on root" >&2
    exit 2
fi

exit 0
```

### Auto-Format After Edits (PostToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$FILE" == *.py ]]; then
    ruff format "$FILE" 2>/dev/null
    ruff check --fix "$FILE" 2>/dev/null
elif [[ "$FILE" == *.ts ]] || [[ "$FILE" == *.tsx ]]; then
    prettier --write "$FILE" 2>/dev/null
fi

exit 0
```

### Remind About Built-in Tools (PreToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -Eq '^\s*cat\s+[^|><]'; then
    echo "REMINDER: Use the Read tool instead of 'cat'" >&2
    exit 2
fi

exit 0
```

### Load Context at Session Start (SessionStart)

```bash
#!/bin/bash
GIT_STATUS=$(git status --short 2>/dev/null | head -5)
BRANCH=$(git branch --show-current 2>/dev/null)

cat << EOF
{
  "additionalContext": "Current branch: $BRANCH\nPending changes:\n$GIT_STATUS"
}
EOF
```

### Inject Context for Subagents (SubagentStart)

```bash
#!/bin/bash
INPUT=$(cat)
SUBAGENT_TYPE=$(echo "$INPUT" | jq -r '.subagent_type // empty')
ORIGINAL_PROMPT=$(echo "$INPUT" | jq -r '.subagent_prompt // empty')

# Add project context to Explore agents
if [ "$SUBAGENT_TYPE" = "Explore" ]; then
    PROJECT_INFO="Project uses TypeScript with Bun. Main source in src/."
    cat << EOF
{
  "updatedPrompt": "$PROJECT_INFO\n\n$ORIGINAL_PROMPT"
}
EOF
fi

exit 0
```

### Desktop Notification on Stop (Stop)

```bash
#!/bin/bash
# Linux
notify-send "Claude Code" "Task completed" 2>/dev/null

# macOS
osascript -e 'display notification "Task completed" with title "Claude Code"' 2>/dev/null

exit 0
```

### Audit Logging (PostToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // "N/A"')

echo "$(date -Iseconds) | $TOOL | $COMMAND" >> ~/.claude/audit.log
exit 0
```

## Configuration Examples

### Anti-Pattern Detection

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/hooks-plugin/hooks/bash-antipatterns.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Auto-Format Python Files

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'FILE=$(cat | jq -r \".tool_input.file_path\"); [[ \"$FILE\" == *.py ]] && ruff format \"$FILE\"'"
          }
        ]
      }
    ]
  }
}
```

### Git Reminder on Stop

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'changes=$(git status --porcelain | wc -l); [ $changes -gt 0 ] && echo \"Reminder: $changes uncommitted changes\"'"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

**Script Development:**
1. Always read input from stdin with `cat`
2. Use `jq` for JSON parsing
3. Quote all variables to prevent injection
4. Exit with code 2 to block, 0 to allow
5. Write blocking messages to stderr
6. Keep hooks fast (< 5 seconds)

**Configuration:**
1. Use `$CLAUDE_PROJECT_DIR` for portable paths
2. Set appropriate timeouts (default: 60s)
3. Use specific matchers over wildcards
4. Test hooks manually before enabling

**Security:**
1. Validate all inputs
2. Use absolute paths
3. Avoid touching `.env` or `.git/` directly
4. Review hook code before deployment

## Debugging

**Verify hook registration:**
```
/hooks
```

**Enable debug logging:**
```bash
claude --debug
```

**Test hooks manually:**
```bash
echo '{"tool_input": {"command": "cat file.txt"}}' | bash your-hook.sh
echo $?  # Check exit code
```

## Available Hooks in This Plugin

- **bash-antipatterns.sh**: Detects when Claude uses shell commands instead of built-in tools (cat, grep, sed, timeout, etc.)

See `hooks/README.md` for full documentation.

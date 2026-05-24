---
name: create-hook
description: Create Claude Code hooks with proper patterns, security best practices, and configuration. Use this skill when building PreToolUse, PostToolUse, SessionStart, or other hook types for plugins.
---

# Hook Development Guide

This skill provides comprehensive guidance for creating Claude Code hooks. Hooks intercept events in the Claude Code lifecycle and can validate, modify, or block operations.

## Hook Types

### 1. Command Hooks (Recommended)

Execute a script for deterministic checks. Best for pattern matching, validation, and blocking.

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.py",
  "timeout": 10
}
```

### 2. Prompt Hooks

Use LLM reasoning for context-aware decisions. More expensive but can understand intent.

```json
{
  "type": "prompt",
  "prompt": "Check if this operation is safe given the project context..."
}
```

### 3. Agent Hooks (v2.1.0+)

Leverage agent capabilities for complex workflows requiring multiple steps.

## Hook Events

| Event | Trigger | Common Uses |
|-------|---------|-------------|
| `PreToolUse` | Before any tool executes | Block dangerous commands, validate inputs |
| `PostToolUse` | After tool completes | Format code, run linters, log results |
| `SessionStart` | When session begins | Check environment, load config |
| `SessionEnd` | When session ends | Cleanup, save state |
| `Stop` | When agent stops | Verify task completion |
| `SubagentStop` | When subagent stops | Validate subagent work |
| `UserPromptSubmit` | When user sends message | Process user input |
| `PreCompact` | Before context compression | Preserve critical info |
| `Notification` | System notifications | React to events |
| `PermissionRequest` | Permission dialogs (v2.1.0) | Custom permission handling |

## Configuration Structure

### Plugin hooks.json Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/check-bash.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/format-on-save.py",
            "timeout": 30
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
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/init.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Matchers

- `"Bash"` - Match specific tool by name
- `"Edit"` - Match Edit tool
- `"Read"` - Match Read tool
- `"*"` - Match all tools/events
- Tool names are case-sensitive

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_PLUGIN_ROOT` | Plugin directory (use for portable paths) |
| `CLAUDE_PROJECT_DIR` | Current project root |
| `CLAUDE_ENV_FILE` | Persist variables from SessionStart |

**Critical:** Always use `${CLAUDE_PLUGIN_ROOT}` in hook commands for portability.

## Writing Command Hooks (Python)

### Basic Structure

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["cchooks"]
# ///
"""Hook description."""

from cchooks import PreToolUseContext, create_context

c = create_context()
assert isinstance(c, PreToolUseContext)

# Check if this is the right tool
if c.tool_name != "Bash":
    c.output.exit_success()

# Get tool input
command = c.tool_input.get("command", "")

# Your validation logic here
if is_dangerous(command):
    c.output.exit_block("Reason for blocking")

c.output.exit_success()
```

### Context Types

- `PreToolUseContext` - Before tool execution
- `PostToolUseContext` - After tool execution
- Other contexts follow same pattern

### Exit Methods

```python
# Allow operation to proceed
c.output.exit_success()

# Block operation with message
c.output.exit_block("Descriptive reason for blocking")

# Modify tool input (PreToolUse only)
c.output.exit_modify({"command": modified_command})
```

## Best Practices

### Security

1. **Quote all bash variables** to prevent injection
2. **Validate inputs** before processing
3. **Use safe patterns** with allowlists before blocklists
4. **Set reasonable timeouts** to prevent hangs

### Performance

1. **Exit early** when hook doesn't apply (`if c.tool_name != "X": exit_success()`)
2. **Use compiled regex** for pattern matching
3. **Keep hooks focused** - one responsibility per hook

### Patterns

#### Safe Patterns First

```python
# Check safe patterns before blocking
SAFE_PATTERNS = [
    r"rm\s+-rf\s+/tmp/",
]

BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+", "rm -rf is destructive"),
]

for pattern in SAFE_PATTERNS:
    if re.search(pattern, command):
        c.output.exit_success()

for pattern, reason in BLOCKED_PATTERNS:
    if re.search(pattern, command):
        c.output.exit_block(reason)
```

#### Informative Block Messages

```python
c.output.exit_block(
    f"BLOCKED: {reason}\n"
    f"Command: {command}\n"
    "If this operation is truly needed, ask the user for permission."
)
```

## Templates

Ready-to-use templates are available:

- `templates/pretooluse-bash.py` - PreToolUse hook for Bash commands
- `templates/pretooluse-read.py` - PreToolUse hook for file reads
- `templates/posttooluse-edit.py` - PostToolUse hook for formatting
- `templates/sessionstart.sh` - SessionStart initialization

Copy and customize for your plugin:

```bash
cp ${CLAUDE_PLUGIN_ROOT}/skills/create-hook/templates/pretooluse-bash.py \
   your-plugin/hooks/your-hook.py
```

## Creating a New Hook Plugin

### 1. Create Directory Structure

```bash
mkdir -p plugins/my-hook/.claude-plugin
mkdir -p plugins/my-hook/hooks
```

### 2. Create plugin.json

```json
{
  "name": "my-hook",
  "version": "1.0.0",
  "description": "What this hook does"
}
```

### 3. Create hooks/hooks.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### 4. Create Hook Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["cchooks"]
# ///
"""My hook description."""

from cchooks import PreToolUseContext, create_context

c = create_context()
assert isinstance(c, PreToolUseContext)

if c.tool_name != "Bash":
    c.output.exit_success()

command = c.tool_input.get("command", "")

# Add your logic here

c.output.exit_success()
```

### 5. Make Executable

```bash
chmod +x plugins/my-hook/hooks/my-hook.py
```

### 6. Validate

```bash
claude plugin validate .
```

## Common Hook Patterns

### Block Destructive Commands

See `plugins/safety-guard/hooks/safety_guard_bash.py`

### Enforce Coding Standards

See `plugins/conventional-commits/hooks/conventional_commits.py`

### Format on Save

See `plugins/python-format/hooks/format_python.py`

### Protect Sensitive Files

See `plugins/protect-env/hooks/protect_env.py`

## Debugging Hooks

### Test Hook Directly

```bash
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | \
  python plugins/my-hook/hooks/my-hook.py
```

### Check Hook Output

Hooks should output JSON. Check stdout/stderr for errors.

### Validate JSON

```bash
cat plugins/my-hook/hooks/hooks.json | jq .
```

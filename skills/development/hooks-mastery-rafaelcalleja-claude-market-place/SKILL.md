---
name: hooks-mastery
description: This skill should be used when the user asks to "create a hook", "configure hooks", "validate hook configuration", "add a PreToolUse hook", "add a PostToolUse hook", "add a SessionStart hook", mentions hook events (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, UserPromptSubmit, PermissionRequest, Notification, PreCompact, SessionEnd), or needs help with Claude Code hooks protocol. Provides comprehensive guidance for creating, configuring, and validating hooks following the official protocol specification.
version: 1.0.0
---

# Claude Code Hooks Mastery

## Overview

Claude Code hooks are event-driven extensions that execute commands or LLM evaluations at specific lifecycle points. This skill provides guidance for creating production-ready hooks following the official protocol specification.

## Core Concepts

### Hook Types

**Command Hooks**: Execute bash scripts with JSON input via stdin
```json
{
  "type": "command",
  "command": "python3 /path/to/script.py",
  "timeout": 60
}
```

**Prompt-Based Hooks**: Use LLM (Haiku) for intelligent evaluation
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS",
  "timeout": 30
}
```

### Hook Events

| Event | Matcher | Purpose | Common Use Cases |
|-------|---------|---------|------------------|
| PreToolUse | Yes | Before tool execution | Validation, modification, blocking |
| PermissionRequest | Yes | Permission dialog | Auto-approve/deny |
| PostToolUse | Yes | After tool execution | Formatting, validation |
| UserPromptSubmit | No | Before prompt processing | Context injection, validation |
| Stop/SubagentStop | No | Agent finishing | Determine if work complete |
| SessionStart | Yes | Session start/resume | Environment setup, context loading |
| SessionEnd | No | Session end | Cleanup, logging |
| Notification | Yes | Notifications sent | External alerting |
| PreCompact | Yes | Before compact | Validation, logging |

### Configuration Structure

Hooks are configured in settings files (user, project, or local scope):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validator.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Creating Hooks

### Step 1: Choose Hook Event

Identify which lifecycle point to hook into:
- **Validation before action**: PreToolUse, PermissionRequest
- **Processing after action**: PostToolUse
- **Context enhancement**: UserPromptSubmit, SessionStart
- **Flow control**: Stop, SubagentStop

### Step 2: Write Hook Script

**Input Protocol**: Hooks receive JSON via stdin with these common fields:
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|bypassPermissions",
  "hook_event_name": "EventName",
  // Event-specific fields...
}
```

**Output Protocol**: Respond via exit codes and stdout:

Exit Code 0 (Success):
- stdout: Plain text or JSON for structured control
- JSON enables advanced decisions

Exit Code 2 (Blocking):
- stderr: Error message fed to Claude
- Blocks the action (behavior varies by event)

Exit Code 1+ (Non-blocking):
- stderr: Logged to verbose mode
- Execution continues

### Step 3: Configure Hook

Add to appropriate settings file:
- `~/.claude/settings.json` - User-level
- `.claude/settings.json` - Project-level (team-shared)
- `.claude/settings.local.json` - Local (git-ignored)

### Step 4: Test Hook

Enable debug mode to see hook execution:
```bash
claude --debug
```

Use verbose mode (Ctrl+O) during session to see hook output.

## Common Patterns

### Pattern 1: Validation Hook (PreToolUse)

Validate and potentially block tool calls:

```python
#!/usr/bin/env python3
import json
import sys

# Read input
input_data = json.load(sys.stdin)

# Validate
if should_block(input_data):
    print("Validation failed: reason", file=sys.stderr)
    sys.exit(2)  # Block execution

# Allow with optional modification
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {
            "modified_field": "new_value"
        }
    }
}
print(json.dumps(output))
sys.exit(0)
```

### Pattern 2: Context Enrichment (UserPromptSubmit)

Add context before Claude processes prompt:

```python
#!/usr/bin/env python3
import json
import sys
import datetime

input_data = json.load(sys.stdin)

# Add context (plain text stdout with exit 0)
context = f"Current time: {datetime.datetime.now()}\n"
context += f"Current directory: {input_data['cwd']}"
print(context)

sys.exit(0)
```

### Pattern 3: Environment Setup (SessionStart)

Initialize environment variables and context:

```bash
#!/bin/bash

# Setup environment
source ~/.nvm/nvm.sh
nvm use 20

# Persist variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

# Add context
echo "Environment initialized: Node $(node --version)"

exit 0
```

### Pattern 4: Intelligent Decision (Stop Hook)

Use LLM for context-aware decisions:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Context: $ARGUMENTS\n\nDetermine if all tasks are complete. Check for:\n1. All user requests fulfilled\n2. No errors requiring fixes\n3. Tests passing\n\nRespond: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

Matchers determine when hooks execute (PreToolUse, PostToolUse, PermissionRequest, Notification, PreCompact, SessionStart):

**Exact match**: `"matcher": "Write"` - Only Write tool
**Regex**: `"matcher": "Edit|Write"` - Multiple tools
**All tools**: `"matcher": "*"` or `"matcher": ""`
**MCP tools**: `"matcher": "mcp__github__.*"` - All GitHub server tools

## Environment Variables

Available in all hooks:
- `CLAUDE_PROJECT_DIR` - Project root directory
- `CLAUDE_CODE_REMOTE` - `"true"` if web environment

SessionStart hooks only:
- `CLAUDE_ENV_FILE` - File path for persisting environment variables

Plugin hooks only:
- `CLAUDE_PLUGIN_ROOT` - Plugin directory

## Security Considerations

**Input Validation**: Always validate and sanitize inputs
```python
if '..' in file_path or file_path.startswith('/'):
    print("Path traversal detected", file=sys.stderr)
    sys.exit(2)
```

**Shell Safety**: Quote all variables
```bash
command="$CLAUDE_PROJECT_DIR/script.sh"
```

**Sensitive Files**: Skip .env, .git/, keys, etc.
```python
sensitive = ['.env', '.git/', 'id_rsa', '*.pem']
if any(p in file_path for p in sensitive):
    sys.exit(2)
```

## Troubleshooting

**Hook not executing**:
- Check configuration with `/hooks` command
- Verify matcher pattern matches tool name
- Enable debug mode: `claude --debug`

**Hook timing out**:
- Increase timeout in configuration
- Default: 60s for command, 30s for prompt
- Individual timeout doesn't affect other hooks

**JSON parsing errors**:
- Validate JSON output with `jq`
- Check exit code is 0 for JSON processing
- Exit code 2 ignores stdout JSON

**Permission denied**:
- Make scripts executable: `chmod +x script.sh`
- Check file paths are absolute or use `$CLAUDE_PROJECT_DIR`

## Quick Reference

### Decision Control by Event

| Event | Allow Action | Block Action | Modify Input |
|-------|--------------|--------------|--------------|
| PreToolUse | `permissionDecision: "allow"` | `permissionDecision: "deny"` | `updatedInput: {}` |
| PermissionRequest | `behavior: "allow"` | `behavior: "deny"` | `updatedInput: {}` |
| PostToolUse | - | `decision: "block"` | - |
| UserPromptSubmit | - | `decision: "block"` | - |
| Stop/SubagentStop | - | `decision: "block"` | - |

### Exit Code Behavior

| Code | stdout | stderr | Continues |
|------|--------|--------|-----------|
| 0 | Parsed as JSON/text | Ignored | Yes |
| 2 | Ignored | Fed to Claude/User | Depends |
| Other | Ignored | Logged | Yes |

## Additional Resources

For detailed protocol specifications:
- **`references/protocol-specification.md`** - Complete protocol documentation
- **`references/event-reference.md`** - Detailed event specifications

For working examples:
- **`examples/pretooluse-validator/`** - Bash command validation
- **`examples/userprompt-enricher/`** - Context injection
- **`examples/sessionstart-setup/`** - Environment initialization
- **`examples/stop-evaluator/`** - Prompt-based decision making

For validation and testing:
- **`scripts/validate-hook-config.py`** - Validate hooks.json against schema
- **`scripts/test-hook-io.py`** - Test hook input/output locally
- **`scripts/generate-hook-template.sh`** - Generate hook boilerplate

For schema validation:
- **`assets/hooks-schema.json`** - JSON schema for hooks configuration

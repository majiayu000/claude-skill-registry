---
name: hooks
description: Create and manage Claude Code hooks for automating workflows, validating inputs, and customizing behavior. Use when users request to create hooks, set up automation for tool usage (PreToolUse, PostToolUse), add session context (SessionStart), validate prompts (UserPromptSubmit), control stopping behavior (Stop, SubagentStop), or configure permission handling (PermissionRequest).
---

# Claude Code Hooks

## Overview

Create and configure Claude Code hooks to automate workflows, validate inputs, add context, and customize behavior across different events in the Claude Code lifecycle.

## When to Use This Skill

Use this skill when users request:
- Creating hooks for any event (PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, SessionStart, SessionEnd, PreCompact, Notification, PermissionRequest)
- Setting up automation for tool usage validation or formatting
- Adding session context at startup
- Validating or blocking prompts
- Controlling when Claude should continue or stop
- Auto-approving or denying permissions
- Setting up notifications

## Pre-requisite: Fetch Latest Documentation

**MANDATORY FIRST STEP:** Before creating any hook, fetch the latest hooks documentation:

```
WebFetch: https://code.claude.com/docs/en/hooks
Prompt: "Extract the complete hooks reference documentation including all hook events, input/output formats, configuration structure, and examples."
```

This ensures access to the most current hook events, JSON schemas, and best practices.

## Hook Creation Workflow

### 1. Understand User Requirements

Ask clarifying questions:
- **What event** should trigger the hook? (PreToolUse, PostToolUse, UserPromptSubmit, etc.)
- **What tools** should be matched? (Bash, Write, Edit, specific MCP tools, etc.)
- **What action** should the hook perform? (Validate, format, add context, block, etc.)
- **Where** should the hook be configured? (User settings `~/.claude/settings.json` or project settings `.claude/settings.json`)

### 2. Determine Hook Type

**Command-based hooks (`type: "command"`):**
- Fast, deterministic validation
- File operations, linting, formatting
- Simple rule-based decisions
- Examples: Bash command validation, code formatting, git checks

**Prompt-based hooks (`type: "prompt"`):**
- Context-aware, intelligent decisions using LLM
- Complex evaluation requiring natural language understanding
- Supported for: Stop, SubagentStop, UserPromptSubmit, PreToolUse
- Examples: Task completion checking, security policy evaluation

### 3. Create Hook Script or Prompt

For **command-based hooks**, create a script that:
1. Reads JSON input from stdin
2. Validates/processes the input
3. Returns appropriate exit code:
   - `0` = Success (stdout shown to user, or added to context for UserPromptSubmit/SessionStart)
   - `2` = Blocking error (stderr fed back to Claude)
   - Other = Non-blocking error (stderr shown to user)
4. Optionally returns JSON for advanced control

For **prompt-based hooks**, craft a prompt that:
1. Uses `$ARGUMENTS` placeholder for hook input
2. Clearly states evaluation criteria
3. Expects JSON response: `{"decision": "approve"|"block", "reason": "..."}`

### 4. Configure in Settings

Add hook configuration to appropriate settings file:
- User-wide: `~/.claude/settings.json`
- Project-specific: `.claude/settings.json`
- Local (not committed): `.claude/settings.local.json`

### 5. Test and Iterate

1. Verify hook registration with `/hooks` command
2. Test with relevant tool calls or prompts
3. Use `claude --debug` to see execution details
4. Refine based on results

## Common Hook Patterns

### PreToolUse: Bash Command Validation

**Use case:** Enforce best practices for bash commands (use `rg` instead of `grep`, `fd` instead of `find`)

**Script:** Reference `scripts/bash_command_validator.py` and customize validation rules.

**Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash_validator.py"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse: Code Formatting

**Use case:** Automatically format code after file edits

**Script:** Reference `scripts/code_formatter.py` and customize for project formatters.

**Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### SessionStart: Load Development Context

**Use case:** Add git status, recent commits, and environment setup at session start

**Script:** Reference `scripts/session_context_loader.sh` and customize for project needs.

**Configuration:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/load_context.sh"
          }
        ]
      }
    ]
  }
}
```

### UserPromptSubmit: Validate and Add Context

**Use case:** Block prompts with secrets, add current timestamp

**Script:** Reference `scripts/prompt_validator.py` and customize validation patterns.

**Configuration:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_prompt.py"
          }
        ]
      }
    ]
  }
}
```

### Stop: Intelligent Continuation (Prompt-based)

**Use case:** Use LLM to decide if Claude should continue working

**Configuration:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS\n\nCheck if:\n1. All user tasks are complete\n2. Any errors need addressing\n3. Follow-up work is needed\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### PermissionRequest: Auto-Approve Safe Operations

**Use case:** Automatically approve read operations for documentation files

**Script example:**
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name == "Read" and file_path.endswith((".md", ".txt", ".json")):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "allow"
            }
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# Let normal permission flow proceed
sys.exit(0)
```

## Hook Input/Output Reference

### Common Input Fields (All Hooks)
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "string"
}
```

### Event-Specific Fields

Consult the fetched documentation for complete schemas for each event type (PreToolUse, PostToolUse, UserPromptSubmit, etc.).

### JSON Output Schema

**Common fields:**
```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "systemMessage": "string"
}
```

**Event-specific `hookSpecificOutput`:** See fetched documentation for each event type.

## Working with MCP Tools

MCP tools follow the pattern `mcp__<server>__<tool>`:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

**Example matcher:** `"matcher": "mcp__memory__.*"` to match all memory server tools.

## Security Best Practices

1. **Validate inputs:** Never trust hook input data blindly
2. **Quote variables:** Use `"$VAR"` not `$VAR` in shell scripts
3. **Block path traversal:** Check for `..` in file paths
4. **Use absolute paths:** Reference scripts with `$CLAUDE_PROJECT_DIR`
5. **Skip sensitive files:** Avoid processing `.env`, `.git/`, keys, credentials
6. **Set timeouts:** Prevent hooks from hanging indefinitely
7. **Test in safe environment:** Verify hooks before production use

## Environment Variables

- `$CLAUDE_PROJECT_DIR` - Project root directory (all hooks)
- `$CLAUDE_ENV_FILE` - File for persisting env vars (SessionStart only)
- `$CLAUDE_CODE_REMOTE` - "true" in web environment, empty in CLI

## Debugging Hooks

1. **Check registration:** Run `/hooks` command
2. **Verify syntax:** Ensure JSON is valid
3. **Test commands manually:** Run hook scripts directly with sample input
4. **Check permissions:** Ensure scripts are executable (`chmod +x`)
5. **Review logs:** Use `claude --debug` for detailed execution info
6. **Validate JSON schemas:** Test input/output with sample data

## Resources

### scripts/

Example hook scripts to customize:
- `bash_command_validator.py` - Validate and suggest better bash commands
- `code_formatter.py` - Format code after file edits
- `session_context_loader.sh` - Load git context and environment at session start
- `prompt_validator.py` - Validate prompts and add timestamp context

### assets/

Template configurations to adapt:
- `pretooluse_template.json` - PreToolUse hook examples
- `posttooluse_template.json` - PostToolUse hook examples
- `sessionstart_template.json` - SessionStart hook examples
- `stop_hook_template.json` - Prompt-based Stop hook example
- `userpromptsubmit_template.json` - UserPromptSubmit hook example

## Implementation Steps

When implementing a hook for a user:

1. **Fetch latest docs** from https://code.claude.com/docs/en/hooks
2. **Clarify requirements** - event type, matcher, action
3. **Choose hook type** - command-based or prompt-based
4. **Create script or prompt** using examples as templates
5. **Make executable** if command-based: `chmod +x script.py`
6. **Add configuration** to appropriate settings.json
7. **Test** with `/hooks` and `claude --debug`
8. **Document** the hook's purpose and usage for the user

---
name: hook-creator
description: >
  This skill should be used when the user asks to "create a hook", "write hook config", "add
  hooks.json", "configure event hooks", "create PreToolUse hook", "add SessionStart hook",
  "implement hook validation", "set up event-driven automation", needs guidance on hooks.json
  structure, hook events (PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd,
  UserPromptSubmit), or wants to automate workflows and implement event-driven behavior in Claude
  Code plugins.
---

# Hook Creator

## Overview

Creates hook configurations that respond to Claude Code events automatically. Hooks
enable automation like formatting on save, running tests after edits, or custom session
initialization.

**When to use:** User wants to automate workflows, needs event-driven behavior, or requests hooks for their plugin.

**References:** Consult
`plugins/meta/claude-docs/skills/claude-docs/reference/plugins-reference.md` for hook specifications and available
events.

## Hook Structure Requirements

Hooks are defined in `hooks/hooks.json` with:

1. **Event type** (SessionStart, PostToolUse, etc.)
2. **Matcher** (optional, for filtering which tool uses trigger hook)
3. **Hook actions** (command, validation, notification)
4. **Proper use of** `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths

## Available Events

From official documentation:

- `PreToolUse` - Before Claude uses any tool
- `PostToolUse` - After Claude uses any tool
- `UserPromptSubmit` - When user submits a prompt
- `Notification` - When Claude Code sends notifications
- `Stop` - When Claude attempts to stop
- `SubagentStop` - When subagent attempts to stop
- `SessionStart` - At session beginning
- `SessionEnd` - At session end
- `PreCompact` - Before conversation history compaction

## Creation Process

### Step 1: Identify Event and Purpose

Ask the user:

- What should happen automatically?
- When should it happen (which event)?
- What tool uses should trigger it (if PostToolUse)?

### Step 2: Choose Hook Type

Three hook types:

- **command**: Execute shell commands/scripts
- **validation**: Validate file contents or project state
- **notification**: Send alerts or status updates

### Step 3: Write Hook Configuration

Structure for `hooks/hooks.json`:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName1|ToolName2",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/script.sh"
          }
        ]
      }
    ]
  }
}
```

### Step 4: Create Associated Scripts

If using command hooks:

1. Create script in plugin's `scripts/` directory
2. Make executable: `chmod +x scripts/script.sh`
3. Use `${CLAUDE_PLUGIN_ROOT}` for paths

### Step 5: Verify Against Official Docs

Check
`plugins/meta/claude-docs/skills/claude-docs/reference/plugins-reference.md` for:

- Current event names
- Hook configuration schema
- Environment variable usage

## Key Principles

- **Event Selection**: Choose most specific event for the need
- **Matcher Precision**: Use matchers to avoid unnecessary executions
- **Script Paths**: Always use `${CLAUDE_PLUGIN_ROOT}` for portability
- **Error Handling**: Scripts should handle errors gracefully

## Examples

### Example 1: Code Formatting Hook

User: "Auto-format code after I edit files"

Hook configuration:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Creates `scripts/format-code.sh` that runs formatter on modified files.

### Example 2: Session Welcome Message

User: "Show a message when Claude starts"

Hook configuration:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Welcome! Plugin loaded successfully.'"
          }
        ]
      }
    ]
  }
}
```

Simple command hook, no external script needed.

### Example 3: Test Runner Hook

User: "Run tests after I modify test files"

Hook configuration:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh"
          }
        ]
      }
    ]
  }
}
```

Creates `scripts/run-tests.sh` that detects test file changes and runs relevant tests.

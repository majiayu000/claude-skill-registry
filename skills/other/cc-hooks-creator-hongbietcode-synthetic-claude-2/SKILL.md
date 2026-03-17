---
name: cc-hooks-creator
description: This skill should be used when users want to create, configure, or debug Claude Code hooks. Hooks are shell commands that execute at various points in Claude Code's lifecycle (PreToolUse, PostToolUse, Stop, SessionStart, etc.). Use this skill when users ask to create custom automation, file protection, code formatting hooks, notifications, or any lifecycle-based triggers for Claude Code.
---

# Claude Code Hooks Creator

## Overview

This skill provides guidance for creating effective Claude Code hooks - shell commands that execute automatically at specific points in Claude Code's lifecycle. Hooks enable deterministic control over Claude's behavior, ensuring certain actions always happen rather than relying on the LLM to choose them.

## When to Use This Skill

- User wants to create a new hook for Claude Code
- User needs to automate actions before/after tool execution
- User wants file protection, code formatting, or notification hooks
- User needs to debug or fix existing hooks
- User wants to understand hook configuration and lifecycle events

## Hook Creation Workflow

### Phase 1: Understand Requirements

Before creating a hook, gather information:

1. **What action should happen?** (log, format, block, notify, validate)
2. **When should it trigger?** (before/after tool, on stop, session start/end)
3. **Which tools should it affect?** (Bash, Write, Edit, Read, all tools)
4. **What conditions apply?** (file types, patterns, always)

### Phase 2: Select Hook Event

Choose the appropriate hook event based on timing needs:

| Event | When It Runs | Common Use Cases |
|-------|--------------|------------------|
| `PreToolUse` | Before tool executes | Block operations, validate inputs, auto-approve |
| `PostToolUse` | After tool completes | Format files, log operations, validate output |
| `Stop` | When Claude finishes | Remind to store learnings, validate completion |
| `SubagentStop` | When subagent completes | Validate subagent output |
| `UserPromptSubmit` | When user submits prompt | Add context, validate prompts |
| `Notification` | On notifications | Custom notifications |
| `SessionStart` | Session begins | Load context, set environment |
| `SessionEnd` | Session ends | Cleanup, logging |
| `PreCompact` | Before context compact | Save important context |

### Phase 3: Design Hook Logic

#### Input Format (JSON via stdin)

All hooks receive JSON input with common fields:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "EventName",
  // Event-specific fields...
}
```

#### Output Format

**Simple: Exit Codes**
- Exit 0: Success (stdout shown in verbose mode)
- Exit 2: Blocking error (stderr shown to Claude)
- Other: Non-blocking error (stderr logged)

**Advanced: JSON Output** (exit code 0)
```json
{
  "decision": "block",
  "reason": "Explanation for Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra info for Claude"
  }
}
```

### Phase 4: Implement the Hook

#### Option A: Inline Command (Simple)

For simple operations, use inline bash/jq:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

#### Option B: Python Script (Complex)

For complex logic, create a Python script:

```python
#!/usr/bin/env python3
"""Hook script template for Claude Code."""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract common fields
    hook_event = input_data.get("hook_event_name", "")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Your logic here...

    # Option 1: Allow (exit 0, no output)
    sys.exit(0)

    # Option 2: Block with message to Claude (exit 2)
    # print("Error message for Claude", file=sys.stderr)
    # sys.exit(2)

    # Option 3: JSON output for advanced control
    # output = {"decision": "block", "reason": "My reason"}
    # print(json.dumps(output))
    # sys.exit(0)

if __name__ == "__main__":
    main()
```

### Phase 5: Configure Hook in Settings

Add hook to `~/.claude/settings.json` (user) or `.claude/settings.json` (project):

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook-script.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Matcher patterns:**
- Exact match: `"Write"` matches only Write tool
- Regex: `"Edit|Write"` matches Edit or Write
- All tools: `"*"` or `""`

### Phase 6: Test and Debug

1. Make script executable: `chmod +x /path/to/hook.py`
2. Test manually: `echo '{"tool_name":"Write"}' | /path/to/hook.py`
3. Run with debug: `claude --debug`
4. Check verbose output: `Ctrl+O` in Claude Code

## Common Hook Patterns

### File Protection Hook (PreToolUse)

Block edits to sensitive files:

```python
#!/usr/bin/env python3
import json
import sys

PROTECTED_PATTERNS = ['.env', 'package-lock.json', '.git/', 'credentials']

input_data = json.load(sys.stdin)
file_path = input_data.get('tool_input', {}).get('file_path', '')

if any(p in file_path for p in PROTECTED_PATTERNS):
    print(f"Protected file: {file_path}", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

### Code Formatter Hook (PostToolUse)

Auto-format files after editing:

```python
#!/usr/bin/env python3
import json
import sys
import subprocess

input_data = json.load(sys.stdin)
file_path = input_data.get('tool_input', {}).get('file_path', '')

if file_path.endswith('.py'):
    subprocess.run(['black', file_path], capture_output=True)
elif file_path.endswith(('.ts', '.tsx', '.js', '.jsx')):
    subprocess.run(['npx', 'prettier', '--write', file_path], capture_output=True)

sys.exit(0)
```

### Stop Reminder Hook (Stop)

Remind to store learnings:

```python
#!/usr/bin/env python3
import json
import sys
import random

input_data = json.load(sys.stdin)

# Prevent infinite loops
if input_data.get('stop_hook_active'):
    sys.exit(0)

# Trigger 30% of the time
if random.random() < 0.3:
    output = {
        "decision": "block",
        "reason": "Consider storing any valuable learnings from this session using --store"
    }
    print(json.dumps(output))

sys.exit(0)
```

### Context Loader Hook (SessionStart)

Load context at session start:

```python
#!/usr/bin/env python3
import json
import sys
import os

# Read recent git changes
result = os.popen('git log --oneline -5 2>/dev/null').read()

output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": f"Recent commits:\\n{result}"
    }
}
print(json.dumps(output))
sys.exit(0)
```

## Decision Control Reference

### PreToolUse Decisions

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason shown to user/Claude",
    "updatedInput": {"field": "modified_value"}
  }
}
```

### PostToolUse Decisions

```json
{
  "decision": "block",
  "reason": "Reason shown to Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra context for Claude"
  }
}
```

### Stop/SubagentStop Decisions

```json
{
  "decision": "block",
  "reason": "Must continue because..."
}
```

## State Management Pattern

For hooks that need to track state across invocations:

```python
#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

STATE_FILE = os.path.expanduser("~/.claude/hook_state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"invocations": 0, "last_run": None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

state = load_state()
state["invocations"] += 1
state["last_run"] = datetime.now().isoformat()
save_state(state)

# Use state in hook logic...
```

## Production-Ready Examples

This skill includes **real working hooks** from production use. Read these files for complete, battle-tested implementations.

### examples/memory_store_reminder.py (Stop Hook)

A sophisticated Stop hook that reminds Claude to store learnings after completing tasks.

**Key Features:**
- Probability-based execution (33% trigger rate)
- State persistence across sessions
- Cooldown management (configurable, disabled for multi-session workflows)
- Multiple infinite loop prevention mechanisms
- Session tracking

**Configuration:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/memory_store_reminder.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Test command:**
```bash
echo '{"session_id": "test", "stop_hook_active": false}' | ./examples/memory_store_reminder.py
```

### examples/todowrite_first_call.py (PostToolUse Hook)

A PostToolUse hook that detects the first TodoWrite call for each new task and triggers memory recall.

**Key Features:**
- Detects first call by checking if `oldTodos` is empty
- State persistence with cooldown support
- Structured JSON output with `hookSpecificOutput`
- Debug logging to stderr

**Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/todowrite_first_call.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Test command:**
```bash
echo '{"tool_input": {"todos": [{"status": "pending"}]}, "tool_response": {"oldTodos": []}}' | ./examples/todowrite_first_call.py
```

### examples/hooks_readme.md

Documentation explaining the workflow these hooks support, configuration details, and troubleshooting tips.

## Resources

### references/

Complete Claude Code hooks documentation:

- `cc_hooks_getting_started.md` - Quickstart guide with practical examples
- `cc_hooks_ref.md` - Complete reference documentation with all hook events, input/output formats, and advanced patterns

To get detailed information about specific hook events or patterns, read these reference files.

### examples/

Production-ready hook implementations:

- `memory_store_reminder.py` - Stop hook with probability execution and state management
- `todowrite_first_call.py` - PostToolUse hook with first-call detection
- `hooks_readme.md` - Documentation for the example hooks

These examples demonstrate advanced patterns like state persistence, cooldowns, probability-based execution, and structured JSON output.

## Security Considerations

- Hooks run with your user permissions - they can access any files you can
- Always validate and sanitize input data
- Quote shell variables: use `"$VAR"` not `$VAR`
- Block path traversal by checking for `..` in paths
- Skip sensitive files like `.env`, credentials, keys
- Use absolute paths for scripts
- Test hooks in safe environments before production use

---
name: hook-writer
description: "Expert assistant for authoring Claude Code hooks. Creates Python hooks with correct JSON output schema, validates against PreToolUse/PostToolUse/UserPromptSubmit formats, and applies fail-open principles. Triggers on keywords: writing hooks, creating hooks, hook authoring, pretooluse hook, posttooluse hook, new hook, hook template, hook validation, hook schema"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Claude Code Hook Writer

Creates Python hooks for Claude Code with correct JSON output schemas and fail-open patterns.

## Hook Types

| Event | Trigger | Use Case |
|-------|---------|----------|
| PreToolUse | Before tool execution | Block dangerous commands, validate inputs |
| PostToolUse | After tool execution | Log results, trigger follow-up actions |
| UserPromptSubmit | Before prompt processing | Validate/transform user input |
| Stop | Session ends | Cleanup, summary generation |
| SubagentStop | Subagent completes | Aggregate results, status reporting |

## JSON Output Schema

### PreToolUse/PostToolUse (Permission Decisions)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Optional explanation"
  }
}
```

| Field | Values | Required |
|-------|--------|----------|
| `hookEventName` | `"PreToolUse"` or `"PostToolUse"` | Yes |
| `permissionDecision` | `"allow"`, `"deny"`, `"ask"` | Yes |
| `permissionDecisionReason` | String explanation | No (recommended for deny) |

**DEPRECATED FORMAT (DO NOT USE):**
```json
{"decision": "allow", "message": null}
```

### UserPromptSubmit

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "modifiedPrompt": "Transformed user prompt"
  }
}
```

### Stop/SubagentStop

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Stop"
  }
}
```

## Python TypedDict Templates

### PreToolUse/PostToolUse

```python
from typing import TypedDict


class HookSpecificOutput(TypedDict, total=False):
    """Inner hook output structure."""
    hookEventName: str
    permissionDecision: str  # "allow" | "deny" | "ask"
    permissionDecisionReason: str


class HookOutput(TypedDict):
    """JSON output returned via stdout."""
    hookSpecificOutput: HookSpecificOutput
```

### UserPromptSubmit

```python
from typing import TypedDict


class HookSpecificOutput(TypedDict, total=False):
    """Inner hook output structure."""
    hookEventName: str
    modifiedPrompt: str


class HookOutput(TypedDict):
    """JSON output returned via stdout."""
    hookSpecificOutput: HookSpecificOutput
```

## Hook Input Schema

Hooks receive JSON via stdin:

```python
class ToolInput(TypedDict, total=False):
    """Tool parameters from Claude Code."""
    command: str      # Bash commands
    file_path: str    # Write/Edit/Read targets
    content: str      # Write content
    old_string: str   # Edit source
    new_string: str   # Edit replacement


class HookInput(TypedDict):
    """JSON input received via stdin."""
    tool_name: str    # "Bash", "Write", "Edit", "Read", etc.
    tool_input: ToolInput
```

## Complete Hook Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Pretooluse hook for Claude Code that [PURPOSE].

[DETAILED DESCRIPTION]
Fail-open principle: allow operations if hook encounters errors.
"""

import json
import sys
from typing import TypedDict


class ToolInput(TypedDict, total=False):
    """Tool parameters from Claude Code."""
    command: str


class HookInput(TypedDict):
    """JSON input received via stdin."""
    tool_name: str
    tool_input: ToolInput


class HookSpecificOutput(TypedDict, total=False):
    """Inner hook output structure."""
    hookEventName: str
    permissionDecision: str  # "allow" | "deny"
    permissionDecisionReason: str


class HookOutput(TypedDict):
    """JSON output returned via stdout."""
    hookSpecificOutput: HookSpecificOutput


def should_block_tool(tool_name: str, tool_input: ToolInput) -> tuple[bool, str | None]:
    """
    Determine if tool should be blocked.

    Returns:
        (should_block, message): Tuple of block decision and optional message
    """
    # Only inspect specific tools
    if tool_name != "Bash":
        return False, None

    command = tool_input.get("command", "")

    # Add detection logic here
    if "dangerous_pattern" in command:
        return True, "Blocked: explanation of why this is blocked."

    return False, None


def main() -> None:
    """Main hook execution."""
    try:
        # Read input from stdin
        input_data: HookInput = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Determine if should block
        should_block, message = should_block_tool(tool_name, tool_input)

        # Return decision in Claude Code hook format
        hook_output: HookSpecificOutput = {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny" if should_block else "allow",
        }
        if message:
            hook_output["permissionDecisionReason"] = message

        output: HookOutput = {"hookSpecificOutput": hook_output}
        print(json.dumps(output))

    except Exception as e:
        # Fail-open: if hook crashes, allow the operation
        output: HookOutput = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            }
        }
        print(json.dumps(output))
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
```

## settings.json Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "uv run --no-project --script /path/to/hook.py"
      }
    ]
  }
}
```

### Matcher Options

| Matcher | Matches |
|---------|---------|
| `"Bash"` | Bash tool only |
| `"Write"` | Write tool only |
| `"*"` | All tools |
| `["Bash", "Write"]` | Multiple specific tools |

## Fail-Open Principle

Hooks MUST fail-open to prevent blocking legitimate operations due to hook errors:

1. **Wrap main logic in try/except**
2. **Exception handler outputs `"permissionDecision": "allow"`**
3. **Log error to stderr (optional)**
4. **Exit with 0 (not error code)**

```python
except Exception as e:
    # Fail-open: if hook crashes, allow the operation
    output: HookOutput = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }
    print(json.dumps(output))
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Exit cleanly even on error
```

## Reference Implementations

| Hook | Purpose | Bundled In |
|------|---------|------------|
| dry-run-guard.py | Block file-writing in dry-run mode | `dry-run` skill |
| git-commit-guard.py | Block --no-verify flag | project `.claude/hooks/` |
| gsuite-public-asset-guard.py | Block public asset creation | `gsuite` skill |
| mux-orchestrator-guard.py | Block forbidden tools in MUX orchestrator | `mux` skill |
| mux-subagent-guard.py | Block TaskOutput for MUX subagents | `mux-subagent` skill |

Hooks are bundled within their respective skill directories under `hooks/` subdirectory.
For standalone hooks not tied to a skill, see the project's `.claude/hooks/` directory.

## Workflow

1. **Identify** the tool(s) to monitor
2. **Define** blocking conditions (patterns, state checks)
3. **Create** hook using template above
4. **Test** manually: `echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | python hook.py`
5. **Configure** in settings.json
6. **Verify** hook triggers on actual tool use

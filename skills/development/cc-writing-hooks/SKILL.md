---
name: cc-writing-hooks
description: Use when creating or modifying Claude Code hooks in settings.json. Triggers on "add hook", "create hook", "PostToolUse", "PreToolUse", "hook not working", "hook not firing".
---

# Writing Claude Code Hooks

Create and configure hooks in `.claude/settings.json`.

## CRITICAL

### Matcher Syntax

**Matchers match TOOL NAMES only, not file paths.**

```json
// ✅ CORRECT - tool name regex
"matcher": "Write|Edit"

// ❌ WRONG - glob patterns don't work
"matcher": "Edit(**/*.md)"
"matcher": "Write(docs/*.ts)"
```

File path filtering must happen **inside your hook script** by parsing `tool_input.file_path`.

### Absolute Paths

Tools pass **absolute paths** in `tool_input.file_path`. Your script must handle this:

```bash
# Strip project dir to get relative path
rel_path="${file_path#$CLAUDE_PROJECT_DIR/}"

# Now match against relative path
if [[ "$rel_path" =~ ^docs/.*\.md$ ]]; then
  # ...
fi
```

## Hook Structure

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/my-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | When | Common Use |
|-------|------|------------|
| `PreToolUse` | Before tool runs | Validate, block |
| `PostToolUse` | After tool succeeds | Format, lint |
| `UserPromptSubmit` | User sends prompt | Add context |
| `SessionStart` | Session begins | Load context |
| `Stop` | Agent finishes | Cleanup |

## Hook Input (stdin JSON)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/absolute/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

## Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Continue, stdout shown in transcript (Ctrl-R) |
| 2 | Block | Stop tool, stderr shown to Claude |
| Other | Error | Continue, stderr shown to user |

## Script Template

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Convert absolute to relative
rel_path="${file_path#$CLAUDE_PROJECT_DIR/}"

# Filter by extension/path
if [[ -z "$rel_path" || ! "$rel_path" =~ \.(ts|tsx|md)$ ]]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"
# Your logic here

exit 0
```

## Notes

- **Changes require restart** — Hook edits don't take effect until CC restarts
- **Parallel execution** — Multiple matching hooks run in parallel
- **60s default timeout** — Override with `"timeout": <seconds>`
- **Debug mode** — `claude --debug` shows hook execution details

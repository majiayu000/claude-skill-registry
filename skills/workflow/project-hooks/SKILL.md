---
name: project-hooks
description: Create and manage project-specific Claude Code hooks
impact: HIGH
version: 1.0.0
---

# Project Hooks

Create project-specific hooks that only run in a specific workspace.

## Quick Setup

```bash
# 1. Create hooks directory
mkdir -p .claude/hooks

# 2. Create settings.json with hook config (see templates below)
```

## Hook Locations

| Location | Scope |
|----------|-------|
| `~/.claude/hooks/` | Global (all projects) |
| `<project>/.claude/hooks/` | Project-specific |

## settings.json Structure

Create `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "command": ".claude/hooks/pre-tool.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "command": ".claude/hooks/post-tool.sh"
      }
    ],
    "UserPromptSubmit": [
      {
        "command": ".claude/hooks/on-prompt.sh"
      }
    ]
  }
}
```

## Hook Events

| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool runs | Validation, blocking |
| `PostToolUse` | After tool runs | Logging, notifications |
| `UserPromptSubmit` | When user sends message | Context injection |
| `Notification` | On notifications | Alerts |

## Matcher Patterns

- `"*"` - Match all tools
- `"Bash"` - Match specific tool
- `"Bash|Edit|Write"` - Match multiple tools (OR)
- `"mcp__playwright__*"` - Wildcard patterns

## Hook Input/Output

### Input (stdin)
```json
{
  "event": "PreToolUse",
  "tool": "Bash",
  "input": {"command": "ls -la"},
  "session_id": "abc123"
}
```

### Output (stdout)
```json
{
  "decision": "allow",
  "message": "Optional message to show"
}
```

### Decisions
- `"allow"` - Proceed normally
- `"block"` - Stop the action
- `"modify"` - Change the input (with `modifiedInput`)

---

## Templates

### Template 1: Lint on Save (TypeScript)

**`.claude/settings.json`**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": ".claude/hooks/lint-on-save.sh"
      }
    ]
  }
}
```

**`.claude/hooks/lint-on-save.sh`**:
```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

if [[ "$FILE" == *.ts || "$FILE" == *.tsx ]]; then
  npx eslint --fix "$FILE" 2>/dev/null
fi

echo '{"continue": true}'
```

### Template 2: Block Dangerous Commands

**`.claude/hooks/block-dangerous.sh`**:
```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.input.command // empty')

# Block rm -rf /
if echo "$CMD" | grep -qE 'rm\s+-rf\s+/[^/]'; then
  echo '{"decision": "block", "message": "Blocked dangerous rm command"}'
  exit 0
fi

echo '{"decision": "allow"}'
```

### Template 3: Auto-Format Python

**`.claude/hooks/format-python.sh`**:
```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

if [[ "$FILE" == *.py ]]; then
  black "$FILE" 2>/dev/null
  ruff check --fix "$FILE" 2>/dev/null
fi

echo '{"continue": true}'
```

### Template 4: Project Context Injection

**`.claude/hooks/inject-context.sh`**:
```bash
#!/bin/bash
# Inject project-specific context into every prompt
echo '{"message": "Project: MyApp | Stack: React + Supabase"}'
```

### Template 5: Run Tests After Changes

**`.claude/hooks/run-tests.sh`**:
```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')

# Run tests for changed file
if [[ "$FILE" == *.ts && "$FILE" != *.test.ts ]]; then
  TEST_FILE="${FILE%.ts}.test.ts"
  if [[ -f "$TEST_FILE" ]]; then
    npm test -- "$TEST_FILE" 2>/dev/null &
  fi
fi

echo '{"continue": true}'
```

---

## Scaffold Command

Run this to scaffold hooks for any project:

```bash
mkdir -p .claude/hooks && echo '{"hooks":{}}' > .claude/settings.json
```

---

## Debugging Hooks

### Test hook manually
```bash
echo '{"event":"PreToolUse","tool":"Bash","input":{"command":"ls"}}' | .claude/hooks/my-hook.sh
```

### Add logging
```bash
echo "[$(date)] $INPUT" >> /tmp/hook-debug.log
```

---

## Best Practices

1. **Keep hooks fast** - Slow hooks delay every action
2. **Always output valid JSON** - Invalid JSON = hook failure
3. **Use `#!/bin/bash`** - Explicit shebang
4. **Make executable** - `chmod +x .claude/hooks/*.sh`
5. **Handle missing tools** - Check if eslint/black exist before running

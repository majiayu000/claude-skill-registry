---
name: claude-code-hooks
description: Create event-driven hooks for Claude Code automation. Configure hook events in settings or frontmatter, parse stdin JSON inputs, return decision-control JSON, and implement secure hook scripts.
---

# Claude Code Hooks — Meta Reference

This skill provides the definitive reference for creating Claude Code hooks. Use this when building automation that triggers on Claude Code events.

---

## When to Use This Skill

- Building event-driven automation for Claude Code
- Creating PreToolUse guards to block dangerous commands
- Implementing PostToolUse formatters, linters, or auditors
- Adding Stop hooks for testing or notifications
- Setting up SessionStart/SessionEnd for environment management
- Integrating Claude Code with CI/CD pipelines (headless mode)

---

## Quick Reference

| Event | Trigger | Use Case |
|-------|---------|----------|
| `SessionStart` | Session begins/resumes | Initialize environment |
| `UserPromptSubmit` | User submits prompt | Preprocess/validate input |
| `PreToolUse` | Before tool execution | Validate, block dangerous commands |
| `PermissionRequest` | Permission dialog shown | Auto-allow/deny permissions |
| `PostToolUse` | After tool succeeds | Format, audit, notify |
| `PostToolUseFailure` | After tool fails | Capture failures, add guidance |
| `SubagentStart` | Subagent spawns | Inspect subagent metadata |
| `Stop` | When Claude finishes | Run tests, summarize |
| `SubagentStop` | Subagent finishes | Verify subagent completion |
| `Notification` | On notifications | Alert integrations |
| `PreCompact` | Before context compaction | Preserve critical context |
| `Setup` | `--init`/`--maintenance` | Initialize repo/env |
| `SessionEnd` | Session ends | Cleanup, save state |
## Hook Structure

```text
.claude/hooks/
├── pre-tool-validate.sh
├── post-tool-format.sh
├── post-tool-audit.sh
├── stop-run-tests.sh
└── session-start-init.sh
```
---

## Configuration

### settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-format.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-validate.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-run-tests.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Execution Model (Jan 2026)

- Hooks receive a JSON payload via stdin (treat it as untrusted input) and run with your user permissions (outside the Bash tool sandbox).
- Default timeout is 60s per hook command; all matching hooks run in parallel; identical commands are deduplicated.

### Hook Input (stdin)

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la"
  }
}
```

### Environment Variables (shell)

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Absolute project root where Claude Code started |
| `CLAUDE_PLUGIN_ROOT` | Plugin root (plugin hooks only) |
| `CLAUDE_CODE_REMOTE` | `"true"` in remote/web environments; empty/local otherwise |
| `CLAUDE_ENV_FILE` | File path to persist `export ...` lines (available in SessionStart; check docs for Setup support) |

---

## Exit Codes

| Code | Meaning | Notes |
|------|---------|------|
| `0` | Success | JSON written to stdout is parsed for structured control |
| `2` | Blocking error | `stderr` becomes the message; JSON in stdout is ignored |
| Other | Non-blocking error | Execution continues; `stderr` is visible in verbose mode |

Stdout injection note: for `UserPromptSubmit`, `SessionStart`, and `Setup`, non-JSON stdout (exit 0) is injected into Claude’s context; most other events show stdout only in verbose mode.

---

## Decision Control + Input Modification (v2.0.10+)

PreToolUse hooks can allow/deny/ask and optionally modify the tool input via `updatedInput`.

### Hook Output Schema

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Reason shown to user (and to Claude on deny)",
    "updatedInput": { "command": "echo 'modified'" },
    "additionalContext": "Extra context added before tool runs"
  }
}
```

Note: older `decision`/`reason` fields are deprecated; prefer the `hookSpecificOutput.*` fields.

### Example: Redirect Sensitive File Edits

```bash
#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')"

# Redirect package-lock.json edits to /dev/null
if [[ "$FILE_PATH" == *"package-lock.json" ]]; then
  UPDATED_INPUT="$(echo "$INPUT" | jq -c '.tool_input | .file_path = "/dev/null"')"
  jq -cn --argjson updatedInput "$UPDATED_INPUT" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      permissionDecisionReason: "Redirected write to /dev/null",
      updatedInput: $updatedInput
    }
  }'
  exit 0
fi

echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
```

### Example: Strip Sensitive Files from Git Add

```bash
#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.tool_name')"
CMD="$(echo "$INPUT" | jq -r '.tool_input.command // empty')"

if [[ "$TOOL_NAME" == "Bash" && "$CMD" =~ ^git[[:space:]]+add ]]; then
  # Remove .env files from staging
  SAFE_CMD="$(echo "$CMD" | sed 's/\.env[^ ]*//g')"
  if [[ "$SAFE_CMD" != "$CMD" ]]; then
    echo '{}' | jq -cn --arg cmd "$SAFE_CMD" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow",
        permissionDecisionReason: "Removed .env from git add",
        updatedInput: { command: $cmd }
      }
    }'
    exit 0
  fi
fi

echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
```

---

## Prompt-Based Hooks

For complex decisions, use LLM-evaluated hooks (`type: "prompt"`) instead of bash scripts. They are most useful for `Stop` and `SubagentStop` decisions.

### Configuration

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate whether Claude should stop. Context JSON: $ARGUMENTS. Return {\"ok\": true} if all tasks are complete, otherwise {\"ok\": false, \"reason\": \"what remains\"}.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Response Schema

- Allow: `{"ok": true}`
- Block: `{"ok": false, "reason": "Explanation shown to Claude"}`

### Combining Command and Prompt Hooks

Use command hooks for fast, deterministic checks. Use prompt hooks for nuanced decisions:

```json
{
  "Stop": [
    {
      "hooks": [
        { "type": "command", "command": ".claude/hooks/quick-check.sh" },
        { "type": "prompt", "prompt": "Verify code quality meets standards" }
      ]
    }
  ]
}
```

---

## Hook Templates

### Pre-Tool Validation

```bash
#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.tool_name')"
CMD="$(echo "$INPUT" | jq -r '.tool_input.command // empty')"

if [[ "$TOOL_NAME" == "Bash" ]]; then
  # Block rm -rf /
  if echo "$CMD" | grep -qE 'rm\s+-rf\s+/'; then
    echo '{}' | jq -cn '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Dangerous rm command detected"
      }
    }'
    exit 0
  fi

  # Block force push to main
  if echo "$CMD" | grep -qE 'git\s+push.*--force.*(main|master)'; then
    echo '{}' | jq -cn '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Force push to main/master not allowed"
      }
    }'
    exit 0
  fi

  # Soft-warning: possible credential exposure
  if echo "$CMD" | grep -qE '(password|secret|api_key)\s*='; then
    echo '{}' | jq -cn '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: "Possible credential exposure in command",
        additionalContext: "Command may include a secret. Confirm intent and avoid committing secrets."
      }
    }'
    exit 0
  fi
fi

exit 0
```

### Post-Tool Formatting

```bash
#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.tool_name')"
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')"

if [[ "$TOOL_NAME" =~ ^(Edit|Write)$ && -n "$FILE_PATH" && -f "$FILE_PATH" ]]; then
  case "$FILE_PATH" in
    *.js|*.ts|*.jsx|*.tsx|*.json|*.md)
      npx prettier --write "$FILE_PATH" 2>/dev/null || true
      ;;
    *.py)
      ruff format "$FILE_PATH" 2>/dev/null || true
      ;;
    *.go)
      gofmt -w "$FILE_PATH" 2>/dev/null || true
      ;;
    *.rs)
      rustfmt "$FILE_PATH" 2>/dev/null || true
      ;;
  esac
fi

exit 0
```

### Post-Tool Security Audit

```bash
#!/bin/bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.tool_name')"
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')"

if [[ "$TOOL_NAME" =~ ^(Edit|Write)$ && -n "$FILE_PATH" && -f "$FILE_PATH" ]]; then
  # Check for hardcoded secrets
  if grep -qE '(password|secret|api_key|token)\s*[:=]\s*["\x27][^"\x27]+["\x27]' "$FILE_PATH"; then
    echo "WARNING: Possible hardcoded secret in $FILE_PATH" >&2
  fi

  # Check for console.log in production code
  if [[ "$FILE_PATH" =~ \.(ts|js|tsx|jsx)$ ]] && grep -q 'console.log' "$FILE_PATH"; then
    echo "NOTE: console.log found in $FILE_PATH" >&2
  fi
fi

exit 0
```

### Stop Hook (Run Tests)

```bash
#!/bin/bash
set -euo pipefail

# Run tests after Claude finishes
cd "$CLAUDE_PROJECT_DIR"

# Detect test framework
if [[ -f "package.json" ]]; then
  if grep -q '"vitest"' package.json; then
    npm run test 2>&1 | head -50
  elif grep -q '"jest"' package.json; then
    npm test 2>&1 | head -50
  fi
elif [[ -f "pytest.ini" ]] || [[ -f "pyproject.toml" ]]; then
  pytest --tb=short 2>&1 | head -50
fi

exit 0
```

### Session Start

```bash
#!/bin/bash
set -euo pipefail

cd "$CLAUDE_PROJECT_DIR"

# Check git status
echo "=== Git Status ==="
git status --short

# Check for uncommitted changes
if ! git diff --quiet; then
  echo "WARNING: Uncommitted changes detected"
fi

# Verify dependencies
if [[ -f "package.json" ]]; then
  if [[ ! -d "node_modules" ]]; then
    echo "NOTE: node_modules missing, run npm install"
  fi
fi

exit 0
```

---

## Matchers

Matchers filter which tool triggers the hook:

- Exact match: `Write` matches only the Write tool
- Regex: `Edit|Write` or `Notebook.*`
- Match all: `*` (also works with `""` or omitted matcher)

---

## Security Best Practices

```text
HOOK SECURITY CHECKLIST

[ ] Validate all inputs with regex
[ ] Quote all variables: "$VAR" not $VAR
[ ] Use absolute paths
[ ] No eval with untrusted input
[ ] Set -euo pipefail at top
[ ] Keep hooks fast (<1 second)
[ ] Log actions for audit
[ ] Test manually before deploying
```

---

## Hook Composition

### Multiple Hooks on Same Event

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        { "type": "command", "command": ".claude/hooks/format.sh" },
        { "type": "command", "command": ".claude/hooks/audit.sh" },
        { "type": "command", "command": ".claude/hooks/notify.sh" }
      ]
    }
  ]
}
```

All matching hooks run in parallel. If you need strict ordering (format → lint → test), make one wrapper script that runs them sequentially.

---

## Debugging Hooks

```bash
# Test a PostToolUse hook manually (stdin JSON)
export CLAUDE_PROJECT_DIR="$(pwd)"
echo '{"hook_event_name":"PostToolUse","tool_name":"Edit","tool_input":{"file_path":"'"$(pwd)"'/src/app.ts"}}' \
  | bash .claude/hooks/post-tool-format.sh

# Check exit code
echo $?
```

---

## Navigation

### Resources

- [references/hook-patterns.md](references/hook-patterns.md) — Common patterns
- [references/hook-security.md](references/hook-security.md) — Security guide
- [data/sources.json](data/sources.json) — Documentation links

### Related Skills

- [../claude-code-commands/SKILL.md](../claude-code-commands/SKILL.md) — Command creation
- [../claude-code-agents/SKILL.md](../claude-code-agents/SKILL.md) — Agent creation
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — CI/CD integration

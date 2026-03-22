---
name: automation-triggers
description: >
  Patterns for auto-format on save, auto-lint, auto-test on file change, and CI triggers
  within Claude Code. Use when the user wants automated reactions to file changes,
  wants to set up continuous feedback loops, or asks about triggering actions automatically.
---

# Automation Triggers

Automation triggers create feedback loops that run formatting, linting, testing, or CI actions in response to file changes. They reduce manual intervention and catch issues immediately.

## When to Use
- User wants files auto-formatted after every edit
- User asks about auto-linting or auto-testing on save
- User needs continuous feedback during development
- User wants to trigger CI checks or deploy previews automatically
- User mentions "run X every time I change Y"

## Core Patterns

### Auto-Format on Edit

Use a PostToolUse hook to format files immediately after modification:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(js|ts|jsx|tsx|css|json)$'; then npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi",
        "description": "Auto-format JS/TS/CSS/JSON files with Prettier"
      }
    ]
  }
}
```

For Python projects, use Black or Ruff:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.py$'; then ruff format \"$CLAUDE_FILE_PATH\" 2>/dev/null && ruff check --fix \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi",
  "description": "Auto-format and fix Python files with Ruff"
}
```

For Go projects:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.go$'; then gofmt -w \"$CLAUDE_FILE_PATH\" && goimports -w \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi",
  "description": "Auto-format Go files with gofmt and goimports"
}
```

### Auto-Lint After Edit

Run linters as PostToolUse hooks to surface issues immediately:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(ts|tsx)$'; then npx eslint --no-warn-ignored \"$CLAUDE_FILE_PATH\" 2>&1 | head -30; fi",
  "description": "Auto-lint TypeScript files with ESLint"
}
```

### Auto Type-Check

For TypeScript, run incremental type-checking after edits:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.tsx?$'; then npx tsc --noEmit --pretty 2>&1 | tail -20; fi",
  "description": "Type-check TypeScript after edit"
}
```

### Auto-Test on File Change

Run related tests when source files change. Keep the test scope narrow for speed:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(ts|tsx)$'; then TEST_FILE=$(echo \"$CLAUDE_FILE_PATH\" | sed 's/\\.ts/.test.ts/' | sed 's/\\.tsx/.test.tsx/'); if [ -f \"$TEST_FILE\" ]; then npx vitest run \"$TEST_FILE\" --reporter=verbose 2>&1 | tail -30; fi; fi",
  "description": "Run matching test file when source is edited"
}
```

For pytest:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.py$'; then TEST_FILE=$(echo \"$CLAUDE_FILE_PATH\" | sed 's|/\\([^/]*\\)\\.py$|/test_\\1.py|'); if [ -f \"$TEST_FILE\" ]; then python -m pytest \"$TEST_FILE\" -x --tb=short 2>&1 | tail -20; fi; fi",
  "description": "Run matching pytest file when Python source is edited"
}
```

### CI Trigger Patterns

Use Stop hooks or git push PreToolUse hooks to integrate with CI:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git push'; then echo 'Reminder: CI will run on push. Ensure tests pass locally first.'; fi",
        "description": "Remind about CI before git push"
      }
    ]
  }
}
```

### Chaining Multiple Triggers

Combine format + lint + type-check in a single hook with early exit on failure:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.tsx?$'; then npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null && npx eslint --fix \"$CLAUDE_FILE_PATH\" 2>/dev/null && npx tsc --noEmit --pretty 2>&1 | tail -10; fi",
  "description": "Format, lint, and type-check TypeScript files"
}
```

## Anti-Patterns

- **Running full test suites on every edit**: This is too slow. Only run the specific test file related to the changed source file. Full suites belong in CI or explicit user commands.
- **Formatting files you did not change**: Scope hooks to `$CLAUDE_FILE_PATH` only. Never run `prettier --write .` in a hook — it reformats the entire project on every edit.
- **Ignoring exit codes**: When chaining commands with `&&`, a failure in formatting stops linting. Use `; ` instead of `&&` if you want all steps to run regardless.
- **No output truncation**: Linter output can be huge. Always pipe through `head` or `tail` to limit output and prevent flooding the agent context.
- **Auto-testing without test isolation**: If tests modify shared state (database, filesystem), auto-running them in hooks can corrupt the development environment.

## Quick Reference

| Trigger | Tool Matcher | When | Speed Target |
|---------|-------------|------|--------------|
| Format | `Edit\|Write` | PostToolUse | < 1s |
| Lint | `Edit\|Write` | PostToolUse | < 3s |
| Type-check | `Edit\|Write` | PostToolUse | < 5s |
| Test (single) | `Edit\|Write` | PostToolUse | < 10s |
| CI reminder | `Bash` (git push) | PreToolUse | instant |

**Rule of thumb**: If a hook takes > 5 seconds, it should be opt-in, not automatic.
**Scope narrowly**: Always filter by file extension and limit output.

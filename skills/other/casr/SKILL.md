---
name: casr
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Cross Agent Session Resumer. Convert and resume sessions across Claude Code,
  Codex, Gemini, and other providers. Use when switching AI agent providers mid-session or migrating an active chat history to a new tool.
practices:
- pragmatic-programmer
---
# casr — Cross Agent Session Resumer

Use `casr` when you need to keep working on the same session but switch providers.

## Fast Path

```bash
casr list
casr info <session-id>
casr -cc <session-id>   # open in Claude Code
casr -cod <session-id>  # open in Codex
casr -gmi <session-id>  # open in Gemini
```

## Helpful Commands

```bash
casr providers
casr list --workspace "$(pwd)" --sort date --limit 20
casr cod resume <session-id> --source cc
casr info <session-id> --json
```

## Notes

- `casr list` is project-scoped to your current working directory by default.
- `-cc`, `-cod`, and `-gmi` auto-detect source provider from the session ID.
- Use `--json` output mode for automation.

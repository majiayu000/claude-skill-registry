---
name: health-check
description: Runs plugin health checks (venv packages and skill registration). Use when the user asks to check plugin health, verify setup, or troubleshoot missing skills.
model: claude-haiku-4-5-20251001
allowed-tools:
  - ToolSearch
  - bitwize-music-mcp
---

# Health Check

## Your Task

Run the `health_check` MCP tool and report results to the user.

## Workflow

**IMPORTANT: Do NOT use Bash for any step. Use only the tools listed below.**

1. Use the `ToolSearch` tool with query `select:mcp__plugin_bitwize-music_bitwize-music-mcp__health_check` to load the MCP tool schema
2. Call `mcp__plugin_bitwize-music_bitwize-music-mcp__health_check` (the MCP tool, not a CLI command)
3. Report results clearly using the format below

## Report Format

### All OK

```
HEALTH CHECK: OK
  Venv: N packages verified
  Skills: N skills registered
```

### Warnings

```
HEALTH CHECK: WARN

VENV [warn]
  N outdated: pkg1 (1.0 -> 1.1), pkg2 (2.0 -> 2.1)
  N missing: pkg3, pkg4
  Fix: ~/.bitwize-music/venv/bin/pip install -r .../requirements.txt

SKILLS [warn]
  N missing from Claude Code: skill-a, skill-b
  N ghost (deleted but cached): skill-c
  Fix: claude plugin update bitwize-music

For comprehensive diagnostics, run the `diagnose` MCP tool.
```

### Failure

```
HEALTH CHECK: FAIL

VENV [fail]
  Venv not found at ~/.bitwize-music/venv
  Fix: /bitwize-music:setup
```

## Remember

1. **Be concise** — this is a status report
2. **Show fix commands** — always include the fix command when status is not ok
3. **Suggest diagnose** — if warnings are found, mention `diagnose` MCP tool for deeper checks

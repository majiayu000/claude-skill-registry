---
name: clean
description: Remove temporary artifacts
allowed-tools: Bash, Glob
model: haiku
user-invocable: false
---

# Clean

Remove Claude Code artifacts.

## Process
1. Delete `.claude/screenshots/*.png`
2. Delete `.playwright-mcp/` folder
3. Delete any leftover v3 artifacts: `prd-backup-*.json`, `handoff-*.md`
4. Report files removed

Never touches source code, project-meta.json, or config.

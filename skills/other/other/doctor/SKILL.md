---
name: doctor
description: Run health checks on Claude Code configuration and sessions. Use when troubleshooting Claude Code issues.
allowed-tools: Bash(cozempic *)
---

Run cozempic health checks:

```bash
cozempic doctor
```

Checks for:
- **Trust dialog hang** — Windows resume bug where `.claude.json` trust entry causes hangs
- **Hooks trust flag** — missing `hasTrustDialogHooksAccepted` causing hooks to silently fail (v2.1.51+ bug)
- **Agent model mismatch** — spawned subagents not inheriting team lead's model causing 403 errors
- **Claude.json corruption** — truncated or invalid `.claude.json` from concurrent write races
- **Corrupted tool_use** — tool blocks with names >200 chars causing 400 API errors
- **Orphaned tool_results** — tool_result blocks missing matching tool_use causing 400 API errors
- **Zombie teams** — stale agent team directories accumulating on disk
- **Oversized sessions** — sessions that may trigger compaction issues
- **Stale backups** — old `.bak` files consuming disk space
- **Disk usage** — total Claude Code storage footprint

To auto-fix detected issues:
```bash
cozempic doctor --fix
```

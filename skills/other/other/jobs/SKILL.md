---
description: View and manage background jobs (cloning, imports, living-docs). Shows job status, progress, and logs. Use when saying "check jobs", "job status", or "background tasks".
argument-hint: "[--all] [--id job-id]"
---

# Background Jobs Monitor

## Project Overrides

!`s="jobs"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

Shows background job information including:
- **Clone jobs** — repository cloning progress and status
- **Import jobs** — issue/epic import from GitHub, JIRA, ADO
- **Living docs** — documentation builder progress
- **Brownfield analysis** — code-spec gap detection

## Hook Execution (Default)

This command is intercepted by the **UserPromptSubmit hook** for instant execution (<100ms). The hook runs `read-jobs.sh` or `jobs.js` directly.

**No action needed** — the hook output appears automatically in `<system-reminder>` tags.

## CLI Fallback

If hook output isn't displayed (rare), execute:

```bash
specweave jobs
```

## Arguments

- `/sw:jobs` — Show active and recent jobs
- `/sw:jobs --all` — Show all jobs including completed
- `/sw:jobs --id <job-id>` — Show details for specific job

## Data Shown

| Field | Description |
|-------|-------------|
| Job ID | Short UUID identifier |
| Type | clone-repos, import-issues, living-docs-builder, etc. |
| Status | pending, running, completed, completed_with_warnings, failed |
| Progress | `X/Y (Z%)` with progress bar |
| Duration | Elapsed time since job started |

## Related Commands

- `/sw:progress` — Increment task/AC completion
- `/sw-github:clone` — Trigger GitHub repo cloning
- `/sw-ado:clone` — Trigger ADO repo cloning

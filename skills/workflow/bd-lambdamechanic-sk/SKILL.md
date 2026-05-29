---
name: bd-workflow
description: How to use bd (beads) for issue tracking, ready work, status updates, and comments in this repo.
---

# bd (beads) Workflow Guide

This document expands the abbreviated rules in `AGENTS.md`. Read this whenever you interact with task tracking, planning docs, or MCP helpers.

## Why bd?

- **Dependency-aware**: track blockers, dependents, and discovered-from links.
- **Git-friendly**: bd auto-syncs to `.beads/issues.jsonl`, so repos capture task history.
- **Agent-optimized**: machine-readable JSON output (`--json`) plus "ready" filtering.
- **Single source of truth**: prevents duplicate trackers, markdown TODOs, or ad-hoc spreadsheets.

## Quick Start Commands

```bash
bd ready --json -n 0                    # find unblocked work
bd create "Issue title" -t task -p 2 --json
bd update bd-42 --status in_progress --json
bd close bd-42 --reason "Completed" --json
```

Always run bd with `--json`. Pipe/parse as needed.

## Issue Types & Priorities

- Types: `bug`, `feature`, `task`, `epic`, `chore`.
- Priorities: `0` (critical) through `4` (backlog). Respect existing priority unless the PM/user changes it.

## Workflow for AI Agents

1. **Check ready work** with `bd ready --json -n 0`. Do this before asking what to work on.
2. **Claim** the task: `bd update <id> --status in_progress --json` (add notes if relevant).
3. **Implement / test / document** the change.
4. **Discover new work?** Create a linked issue (e.g., `bd create "Fix follow-up" -p 1 --deps discovered-from:<parent> --json`).
5. **Complete** the task via `bd close <id> --reason "Completed" --json` when the PR merges.
6. **Commit `.beads/issues.jsonl` alongside code.** Never leave tracker changes uncommitted.

## Auto-Sync Behavior

- bd exports to `.beads/issues.jsonl` automatically (5s debounce) after changes.
- After `git pull`, bd imports newer JSONL back into the local state. No manual sync needed.

## MCP Integration (Optional)

- Install: `pip install beads-mcp`.
- Add to `~/.config/claude/config.json`:

```json
{
  "beads": {
    "command": "beads-mcp",
    "args": []
  }
}
```

- Use `mcp__beads__*` calls instead of the CLI if your client supports MCP.

## Planning Document Hygiene

AI-generated planning/design docs should live under `history/` (add it to `.gitignore` if desired). Keeping the repo root clean avoids confusing ephemeral plans with durable docs.

## Important Rules (Do & Don't)

- ✅ Use bd for **all** task tracking.
- ✅ Include discovered-from dependencies to show provenance.
- ✅ Keep `.beads/issues.jsonl` in every relevant commit.
- ✅ Store planning docs in `history/`.
- ❌ No markdown TODO lists or alternative trackers.
- ❌ No forgetting `--json`.
- ❌ No cluttering the repo root with temporary planning files.

## Need More Context?

See `README.md` / `QUICKSTART.md` for broader project background, but treat bd as the authoritative view of work.

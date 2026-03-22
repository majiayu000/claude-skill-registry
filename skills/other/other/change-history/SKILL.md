---
name: change-history
description: >
  Maintain a structured JSON history of project changes in .history/changes.json.
  Use this skill after making any medium-to-large changes to the codebase. This includes:
  new files, API changes, schema changes, dependency changes, config changes, refactors,
  Dockerfile changes, and significant bug fixes. Do NOT log formatting-only changes, typo
  fixes, or trivial single-line edits. When in doubt, log it.
---

# Change History

After making medium-to-large changes, update `.history/changes.json` with a new entry.

## Steps

1. Read the current `.history/changes.json` (create it if it doesn't exist)
2. Determine if the changes warrant a log entry
3. If yes, append a new entry to the `entries` array
4. Write the updated file back

## Entry Schema

Each entry must have:
- `id`: ISO timestamp + 6-char random hex suffix (e.g. `"2025-01-15T14:32:00Z-a1b2c3"`)
- `timestamp`: Current UTC time in ISO 8601
- `type`: One of `feature`, `bugfix`, `refactor`, `config`, `docs`, `test`, `infra`
- `scope`: One of `backend`, `infra`, `config`
- `summary`: One-line description (max 120 chars)
- `detail`: Multi-sentence explanation including WHY
- `files_changed`: Array of file paths
- `breaking`: Boolean
- `dependencies_added`: Array of `"package@version"` (optional)
- `dependencies_removed`: Array of `"package@version"` (optional)
- `related_entries`: Array of entry IDs (optional)
- `tags`: Freeform tags (optional)

## When to Log

**Always log:** New files, Dockerfile changes, docker-compose changes, process.py changes,
dependency changes, config changes, CI/CD pipeline changes, benchmark results.

**Never log:** Formatting-only, typo fixes, trivial edits.

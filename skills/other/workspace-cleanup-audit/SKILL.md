---
name: workspace-cleanup-audit
description: Read-only repository hygiene scanner for directories under ~/Workspace. Use when asked to audit cleanup chores, detect build or cache artifact buildup, find large transient files, or rank cleanup issues by severity with the repo and directory where each issue is found.
---

# Workspace Cleanup Audit

## Overview

Run a read-only scan over repositories in `~/Workspace` and report cleanup chores ranked by severity. Never delete, move, or modify files.

## Workflow

1. Run `scripts/scan_workspace_cleanup.py`.
2. Review top-ranked findings first.
3. Report findings with severity, repo, directory, category, size, and reason.
4. Suggest cleanup actions as text only.

## Commands

Use the default workspace scan:

```bash
python3 scripts/scan_workspace_cleanup.py
```

Scan a custom workspace root:

```bash
python3 scripts/scan_workspace_cleanup.py --workspace ~/Workspace
```

Return machine-readable output:

```bash
python3 scripts/scan_workspace_cleanup.py --json
```

Tune noise floor and stale threshold:

```bash
python3 scripts/scan_workspace_cleanup.py --min-mb 100 --stale-days 90
```

## Output Contract

Each finding includes:

- `severity`
- `repo`
- `directory`
- `category`
- `size_human`
- `score`
- `why_flagged`
- `suggested_cleanup`

The report also includes:

- Top findings sorted by severity then size
- Repo summary ranked by total flagged size

## Read-Only Rules

- Never run destructive commands.
- Never remove artifacts automatically.
- Never write into scanned repositories.
- Provide recommendations only.

## Automation Templates

Use `$workspace-cleanup-audit` inside automation prompts so Codex consistently loads this skill behavior.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including placeholders, safety defaults, and output handling, use:
- `references/automation-prompts.md`

## References

- Pattern and threshold notes: `references/patterns.md`
- Automation prompt templates: `references/automation-prompts.md`

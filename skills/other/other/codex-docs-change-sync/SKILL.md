---
name: codex-docs-change-sync
description: Map code changes to candidate documentation updates using git diff and mapping rules. Use during docs steps to report impacted docs in MVP without auto-editing documentation.
load_priority: lazy
---

## TL;DR
Map code changes to affected documentation via `map_changes_to_docs.py`. Report-only by default, no auto-edit. Scope: auto-detect staged -> unstaged -> last commit. Fallback: manual diff inspection.

# Codex Docs Change Sync

## Purpose

Identify documentation that is likely affected by code changes.

## Activation

1. Activate during workflow `docs` steps.
2. Activate on explicit `$codex-docs-change-sync`.

## Script Invocation

- Windows:
  `python "$env:USERPROFILE\.codex\skills\codex-docs-change-sync\scripts\map_changes_to_docs.py" --project-root <path> --diff-scope <scope>`
- macOS/Linux:
  `python "$HOME/.codex/skills/codex-docs-change-sync/scripts/map_changes_to_docs.py" --project-root <path> --diff-scope <scope>`

## Script Invocation Discipline

1. Always run `--help` before invoking `map_changes_to_docs.py`.
2. Treat the script as a black-box mapper and prefer direct execution over source inspection.
3. Read script source only when customization or bug fixing is required.

## Enhanced Diff Scope

If scope is not specified, use `auto` mode:

1. staged changes
2. unstaged changes
3. last commit

Report which scope was selected.

## Behavior

1. Run script and parse JSON output.
2. Report changed files and candidate docs with reason/confidence.
3. Keep MVP in report-only mode; do not auto-edit docs unless user requests it.

## Fallback

If script cannot run, inspect diffs manually and report likely docs:
`docs/`, `README.md`, `CHANGELOG.md`, and module-specific docs.

## Reference Files

- `references/docs-sync-spec.md`: script behavior, output format, and fallback protocol.

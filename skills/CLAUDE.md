# CLAUDE.md

This repository is the archive leg of a three-repo split:
- `claude-skill-registry-core`: source of truth for workflows, scripts, indexing, Pages, and publish orchestration
- `claude-skill-registry-data`: archived skill contents
- `claude-skill-registry`: merged publish artifact

## Before Editing
- If the task is about archive content, archive layout, or archive-local docs, this repo is the right place.
- If the task is about discovery, dedupe, registry generation, search-index generation, Pages, or sync/publish behavior, switch to `core`.
- If the task is about merged publish wiring in `main`, switch to `claude-skill-registry`.

## Layout Contract
- Canonical path shape: `<category>/<skill>/SKILL.md` + `<category>/<skill>/metadata.json`
- Category directories live at the repo root.
- Avoid case-only path conflicts and follow the suffix policy defined in `core/scripts/utils.py`.

## README Rule
- Do not write hardcoded archive counts or dates into `README.md`.
- Use live badges or values sourced from `core` `stats.json`.
- If displayed counts are stale, fix the `core` pipeline or rerun it instead of editing numbers here.

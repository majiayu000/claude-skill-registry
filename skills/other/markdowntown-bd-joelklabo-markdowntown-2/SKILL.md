---
name: markdowntown-bd
description: Beads (bd) issue workflow and repo operations for markdowntown. Use when creating bd tasks, updating status, adding dependencies, running required tests, committing, and pushing to main.
---

# markdowntown-bd

## Core workflow
1. Clear stale work: `node scripts/bd-reset-stale.mjs --hours 4`.
2. Pick work: `npx bd --no-daemon ready --json`.
3. Claim task: `npx bd --no-daemon update <id> --status in_progress --json`.
4. Read task: `npx bd --no-daemon show <id> --json`.
5. Implement changes and run required tests.
6. Commit and push to `main` after tests pass.
7. Close task: `npx bd --no-daemon close <id> --reason "Implemented" --json`.
8. Commit `.beads/issues.jsonl` updates with code changes.
9. At session end: `npx bd --no-daemon sync`.

## Guardrails
- Always use `--no-daemon` and `--json` with bd commands.
- Never leave tasks in `in_progress` if stopping work.
- Always run compile, lint, and unit tests before committing.
- Push to `main` after each completed task.
- Avoid destructive git commands unless explicitly requested.
- Never paste secrets (tokens, keys, credentials) into issues, commits, or logs.

## References
- docs/BEADS.md
- docs/DEV_ONBOARDING.md
- codex/skills/markdowntown-bd/references/beads.md
- codex/skills/markdowntown-bd/references/release.md

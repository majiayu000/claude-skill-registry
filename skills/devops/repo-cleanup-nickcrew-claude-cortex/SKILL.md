---
name: repo-cleanup
description: Use when a repository needs cleanup of dead code, build artifacts, unused dependencies, outdated docs, or stale tests - provides safe cleanup workflows, validation steps, and reporting templates for code, deps, docs, tests, and sprint archives.
---

# Repo Cleanup

## Overview
Establish a safe, repeatable cleanup workflow for code, dependencies, docs, tests, and sprint artifacts. Minimize risk by validating usage, archiving before deletion, and verifying with tests.

## When to Use
- Repository bloat (generated artifacts, caches, unused files)
- Dead code or unused dependencies suspected
- Docs drifted from actual behavior
- Tests are brittle, redundant, or mislocated
- Sprint closure needs structured archiving

Avoid when:
- Active incident response is ongoing
- The target area lacks owners or rollback coverage

## Quick Reference

| Task | Load reference |
| --- | --- |
| Code cleanup | `skills/repo-cleanup/references/code-cleanup.md` |
| Dependency cleanup | `skills/repo-cleanup/references/deps-cleanup.md` |
| Docs cleanup | `skills/repo-cleanup/references/docs-cleanup.md` |
| Test cleanup | `skills/repo-cleanup/references/test-cleanup.md` |
| Sprint archive | `skills/repo-cleanup/references/archive-sprint.md` |

## Workflow
1. Define scope and safety mode (safe vs aggressive).
2. Capture baseline state (git status, key tests, backups).
3. Load the relevant reference file(s) for the target area.
4. Execute cleanup steps with usage checks before removal.
5. Validate changes (tests, build, lint, or doc checks).
6. Report outcomes (actions taken, risks, follow-ups).

## Output
- Summary of actions and files touched
- Validation results and remaining risks
- Follow-up recommendations or backlog items

## Common Mistakes
- Deleting without confirming usage or regenerability
- Skipping baseline tests and rollback checkpoints
- Removing dependencies without updating build/test scripts
- Collapsing docs without preserving entry points

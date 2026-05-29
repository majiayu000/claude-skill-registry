---
created: 2026-01-18T17:30
title: Integrate PR skill into Kata system
area: tooling
files:
  - /Users/gannonhall/.claude/skills/working-with-pull-requests/SKILL.md
  - /Users/gannonhall/.claude/skills/working-with-pull-requests/creating-workflow.md
  - /Users/gannonhall/.claude/skills/working-with-pull-requests/reviewing-workflow.md
  - /Users/gannonhall/.claude/skills/working-with-pull-requests/merging-workflow.md
---

## Problem

There's an existing `working-with-pull-requests` skill that handles the complete PR lifecycle:
- **Creating**: branch → commit → push → `gh pr create`
- **Reviewing**: identify PR → run review agents → fix issues → update state
- **Merging**: CI checks → confirm ready → `gh pr merge` → checkout main

This skill should be integrated into Kata for seamless phase-level PR workflows (one PR per phase is already a Kata decision).

## Solution

Integrate the PR skill into Kata:
1. Port to `skills/kata-pull-requests/` or similar
2. Coordinate with phase completion (auto-create PR after phase execution?)
3. Connect to verification workflow (run review agents as part of `/kata:phase-verify`?)
4. Consider phase-level PR template with summary of plans executed

Key integration points:
- After `/kata:phase-execute` completes → suggest/create PR
- `/kata:phase-verify` could include PR review
- STATE.md could track PR state per phase

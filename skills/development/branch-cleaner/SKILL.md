---
name: branch-cleaner
description: Identify and clean up stale git branches locally and on remotes with safe, reversible steps. Use when asked to prune, list, or delete merged/old branches or audit branch hygiene.
---
# Branch cleaner

## Goal
Safely identify stale branches and provide explicit delete/prune commands.

## Inputs to confirm (ask if missing)
- Default branch (main/master/develop).
- Remote name (origin) and whether remote deletion is desired.
- Safety rules: keep patterns (release/*, hotfix/*), minimum age, merged-only.

## Workflow
1) Sync and inspect
   - Run `git fetch --prune`.
   - Check `git status` and note uncommitted changes.
2) Build candidate lists
   - Local merged into default: `git branch --merged <base>`
   - Local not merged (list only): `git branch --no-merged <base>`
   - Remote merged: `git branch -r --merged <base>`
   - Stale by date: `git for-each-ref --sort=committerdate refs/heads --format="%(committerdate:short) %(refname:short)"`
3) Exclude protected branches
   - Always keep `<base>`, current branch, and user-provided patterns.
4) Confirm with user
   - Present candidates grouped by local vs remote.
5) Provide delete commands
   - Delete branches approved for deletion by the user
   - 

## Optional GitHub CLI checks
- `gh pr list --state merged --base <base>` to correlate merged branches.
- `gh pr view <branch>` to verify status if needed.

## Deliverables
- Candidate lists and rationale.
- Warnings for unmerged or recently updated branches.
- Don't remove remote branches unless explicitly approved.
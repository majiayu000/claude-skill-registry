---
name: sync
description: Sync branch with remote and confirm a clean end-of-session state.
---

# Sync

Standardize the end-of-session push. Confirm nothing is left unpushed.

## Inputs

Optional: `-DryRun` (print actions only), `-AllowMain` (permit syncing on `main`).

## Workflow

1. Confirm current branch is not `main` (unless `-AllowMain`).
2. Confirm working tree is clean. If not, warn and stop.
3. Run `git pull --rebase`. If it fails, stop and report — do not force.
4. Run `git push`.
5. Run `git status -sb` and confirm branch is up to date.

## Output

Short summary including the final `git status -sb`.

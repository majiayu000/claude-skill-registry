---
name: atomic-commit-and-push
description: Run the atomic-commit workflow on the current changes, then publish the resulting commits to the remote. Use whenever the user says "commit and push", "ship these changes", "atomic commit and push", "publish my work", or wants atomic commits delivered to origin in one step. Prefers `git submit` (git-branchless); falls back to a named branch + `git push origin HEAD:refs/heads/<branch>`. Refuses force-push and direct push to protected branches without explicit authorization.
---
# Atomic Commit and Push

## Phase 1 — Atomic commit
Review staged + unstaged changes. Group by mechanism/file boundary.
Create one commit per logical change. Run repo-native type-checker and linter before each commit.
Do NOT bundle unrelated changes.

## Phase 2 — Publish
Prefer `git submit` when git-branchless is installed and the forge is supported.
Fallback: pick a descriptive branch name, then `git push origin HEAD:refs/heads/<branch>`.
Set upstream only when the user explicitly wants tracking.
Never `--force` or `--force-with-lease` without explicit user authorization.
Never push directly to protected branches (e.g., `main`, `master`, `release/*`).

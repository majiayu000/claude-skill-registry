---
name: worktree-clean
description: Use when removing a git worktree and cleaning up its associated local branch from the main repository.
argument-hint: [worktree-path]
allowed-tools: Bash
---
worktree_path = $ARGUMENTS

Clean up a local worktree and its local branch. If no argument is provided, list worktrees and ask the user which to remove.

## Local Only

This skill manages local git state — worktrees and local branches. Remote branches are out of scope because they carry invisible state: open MRs, CI pipelines, review comments, deployment triggers. Deleting a remote branch can auto-close an MR and destroy that context silently. Only the user decides when a remote branch goes.

## Submodules

Submodules initialized inside a worktree store their git state under `.git/worktrees/{name}/modules/{submodule}`. This is cleaned up automatically when the parent worktree is removed — no separate worktree removal needed for submodules. Just remove the parent worktree normally.

## When Removal Resists

`git worktree remove` fails on unclean state or unmerged branches. Investigate the actual state — `git status`, `git diff`, whether the branch was pushed or has a merged MR. Trivial leftovers (build artifacts, debug logs, already-pushed work) justify force-removing autonomously. Substantive uncommitted or unmerged work — describe what you found and let the user decide.

Always `git worktree prune` after removal to clean stale internal references.

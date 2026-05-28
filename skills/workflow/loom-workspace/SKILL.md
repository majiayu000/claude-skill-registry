---
name: loom-workspace
description: Use loom workspace to create/manage worktrees for isolated execution of tickets.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "git,workflow"
---

<!-- BEGIN:compound:skill-managed -->
## Worktree basics (repo model)

Ensure a worktree exists for a branch:

- `compound_workspace(argv=["repo", "worktree", "add", "<branch>"])`

List worktrees:

- `compound_workspace(argv=["repo", "worktree", "ls"])`

Remove a worktree:

- `compound_workspace(argv=["repo", "worktree", "rm", "<branch>"])`

Repo status:

- `compound_workspace(argv=["repo", "status"])`

## Branch naming

Recommended:

- `ticket-<ticket-id>-<short-slug>`

Example:

- `ticket-42-streaming-chunking`

## Practical note

OpenCode runs inside *one* working directory. Typically, this is the main branch worktree.
`loom workspace` creates the worktree path (usually under `.loom-repo/worktrees/<branch>`).
Do the code changes in that worktree.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._

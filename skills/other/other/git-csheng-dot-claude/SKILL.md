---
name: git
description: Execution-layer skill for git inspection and safe patching
---

## Commands

- git.status
- git.diff
- git.applyPatch

## Constraints

- Never run git commit, push, or destructive history operations.
- Primary focus is read-only inspection plus safe patch application.

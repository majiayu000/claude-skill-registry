---
name: merge-squashbase
description: "{{ 𝛀𝛀𝛀 }} Squash and rebase"
model: opus
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Read", "Glob", "Grep", "Edit"]
---

## Squash and Rebase onto Main

1. Check current branch name and confirm with user
2. Do NOT create a worktree - work in the current directory
3. Run `git fetch origin main`
4. Run `git rebase -i origin/main` — in the editor, squash or fixup commits as appropriate, leaving one clean commit (or a small number of logical commits) with a descriptive message
5. If conflicts exist, list them and resolve one at a time preserving our branch's intent, running `git rebase --continue` after each
6. Run tests to verify
7. Push with `git push --force-with-lease`

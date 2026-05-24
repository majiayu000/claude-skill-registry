---
name: git-what
description: Concise git workspace snapshot for the current directory. Use when asked to show current branch, cwd, repo root, whether the current directory is a worktree, local dirty status, or whether other worktrees have uncommitted changes.
---

# Git What

## Overview
Provide a short, formatted git status snapshot for the current working directory and any sibling worktrees.

## Quick start
- Run `scripts/gitwhat.sh` from the target directory.
- If not inside a git repo, report the cwd and exit.

## Output fields
- CWD
- Branch (or detached@<sha>)
- Repo root
- Worktree (yes/no + name or main)
- Status (clean/dirty with counts)
- Other worktrees (clean/dirty per worktree)

## Notes
- Keep output compact and use the script output as-is unless the user asks for more detail.
- Do not use network calls; rely on local git commands.

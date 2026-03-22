---
name: ait-git
description: Git commands for aitasks/aiplans directories — use ./ait git instead of plain git
user-invocable: false
---

## Git Operations on Task/Plan Files

When running git commands that operate on files in `aitasks/` or `aiplans/` directories, **always use `./ait git` instead of plain `git`**. This ensures correct branch targeting when task data lives on a separate `aitask-data` branch.

### Usage

```bash
./ait git add aitasks/t42_foo.md
./ait git commit -m "ait: Update task t42"
./ait git push
./ait git status
```

### How it works

- If `.aitask-data/` worktree exists (branch mode): `ait git` routes to `git -C .aitask-data`
- If no worktree (legacy mode): `ait git` passes through to plain `git`

### When to use

- Any `git add`, `git commit`, `git push`, `git rm` involving files under `aitasks/` or `aiplans/`
- When committing task metadata changes (status, assignment, etc.)
- When archiving or creating task files

### When NOT to use

- For code-related git operations (implementation commits go on the main branch as normal)
- For `git log`, `git diff` on code files
- The aitask shell scripts already use `task_git()` internally — no need to wrap script calls

---
name: worktree
description: Use when starting new feature work that should happen in an isolated git worktree on its own branch.
argument-hint: <task description or branch name>
allowed-tools: Bash
---
input = $ARGUMENTS

Create an isolated worktree for feature development.

## Branch Name

Derive from user input (or ask if not provided). Default format: `<type>/<kebab-description>` using conventional commit types (`feat` when ambiguous). **But check `git branch` first** — if the repo uses a different convention (e.g., `feature/JIRA-123-desc`), match it.

Show the derived name before proceeding.

## Worktree Location

- `{repo_root}/.claude/worktrees/{branch_slug}` where `branch_slug` replaces `/` with `-`
- `repo_root` = `git rev-parse --show-toplevel`
- Ensure `.claude/worktrees/` exists and is in `.gitignore`

## Base Branch

Always branch from the latest remote default branch, not from `HEAD`:

1. Detect default branch: `git symbolic-ref refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||'` (fallback: try `main`, then `master`)
2. Fetch latest: `git fetch origin {default_branch}`
3. Use `origin/{default_branch}` as the start point

Create: `git worktree add -b {branch} {directory} origin/{default_branch}`
If branch already exists: `git worktree add {directory} {branch}` (no `-b`).

After creation, symlink gitignored files so the worktree is immediately functional without reinstalling:
```
bash ~/.claude/skills/worktree/scripts/symlink-gitignored.sh {repo_root} {directory}
```

## Submodules

`git worktree add` on a parent repo does NOT automatically set up submodules. The submodule directories will be empty. But each worktree gets its own independent submodule git dir at `.git/worktrees/{name}/modules/{submodule}`, so submodules can be on different branches without conflicting with the original checkout.

**Setup after creating the parent worktree:**

1. Initialize and checkout submodules inside the worktree:
   ```
   cd {directory}
   git submodule update --init
   ```
2. If the submodule needs a specific branch (not just the commit pinned by the parent):
   ```
   git -C {directory}/{submodule} checkout {branch}
   ```
3. Symlink gitignored files for each submodule:
   ```
   bash ~/.claude/skills/worktree/scripts/symlink-gitignored.sh {repo_root}/{submodule} {directory}/{submodule}
   ```

**Scope determination** — before creating anything:
- **Single submodule only** — worktree in that submodule alone
- **Parent + submodule(s)** — parent worktree + submodule init inside it
- **Ambiguous** — ask

## Output

Show: worktree path, `claude --cwd {directory}` command, reminder to use `/worktree-clean` when done, and `git worktree list`.

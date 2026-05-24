---
name: worktree
description: Create a git worktree with Graphite tracking and local config setup for isolated feature work.
allowed-tools: Bash(git:*), Bash(gt:*), Bash(gh:*), Bash(ln:*), Bash(ls:*), Bash(pnpm:*), Bash(mkdir:*), Bash(test:*), Read
---

# Worktree Skill

Creates a git worktree with Graphite tracking, symlinked env files, and installed dependencies.

## Usage

Invoke with `/worktree <branch-name>` and optionally `--parent <branch>`.

- `/worktree my-feature` — new branch `my-feature`, tracked to `staging`
- `/worktree my-feature --parent main` — new branch tracked to `main`
- `/worktree existing-branch` — checks out existing branch into worktree (no `-b`)
- `/worktree` — prompts for branch name (only interactive step)

## Autonomous Execution

This skill runs **fully autonomously** without user interaction (except when no branch name is provided). When invoked:

- **Do NOT ask for user confirmation** at any step
- **Do NOT pause** between tasks or wait for approval
- **Proceed directly** through all workflow steps
- **Only stop** if a critical error occurs

## Workflow

### Step 1: Parse Arguments

Extract the branch name and optional `--parent` flag from the arguments.

- If no branch name is provided, prompt the user for one. This is the **only** interactive step.
- Default parent: `staging`

### Step 2: Validate Preconditions

Determine the repo root (all paths are relative to it):

```bash
git rev-parse --show-toplevel
```

Check if the worktree path already exists:

```bash
test -d .worktrees/<name>
```

If it exists, report an error with a removal hint and stop:

```
Error: .worktrees/<name> already exists.
To remove it: git worktree remove .worktrees/<name>
```

Check if the branch exists locally:

```bash
git branch --list <name>
```

If the branch exists, check it's not already checked out in another worktree:

```bash
git worktree list
```

If the branch is checked out elsewhere, report which worktree has it and stop.

For **new branches only**, check if a PR already exists for this branch name (to avoid reusing a name that has an existing PR):

```bash
gh pr list --head <name> --state all --json number,title,state --limit 1
```

If a PR is found, automatically append a numeric suffix to find a unique name. Try `<name>-v2`, then `<name>-v3`, etc., checking each with `gh pr list` until a name with no existing PR is found. Use the unique name as the branch name for all subsequent steps (worktree directory name stays as the original `<name>`). Report the rename:

```
Note: "<name>" already has PR #<number>. Using "<name>-v2" instead.
```

Skip this check for existing branches (they already have a PR association).

Ensure the `.worktrees` directory exists:

```bash
mkdir -p .worktrees
```

### Step 3: Create Worktree

Note: `<dir>` is the original name argument (worktree directory), `<branch>` is the final branch name (may differ if renamed due to PR conflict).

For a **new branch** (branch does not exist locally):

```bash
git worktree add .worktrees/<dir> -b <branch>
```

For an **existing branch**:

```bash
git worktree add .worktrees/<dir> <branch>
```

### Step 4: Track with Graphite (New Branches Only)

Only for newly created branches, track with Graphite:

```bash
cd .worktrees/<dir> && gt track --parent <parent>
```

If `gt track` fails, report a warning but continue — the worktree is still usable without Graphite tracking.

Skip this step entirely for existing branches (they already have tracking configured).

### Step 5: Symlink Local Configs

For each config file, check if the source exists and create a symlink if it does. Use **absolute paths** for symlink sources so they resolve from any CWD.

```bash
# Root .env
test -f <repo-root>/.env && ln -s <repo-root>/.env .worktrees/<name>/.env
```

If a source file doesn't exist, skip it silently.

### Step 6: Install Dependencies

```bash
cd .worktrees/<name> && pnpm install
```

If `pnpm install` fails, warn but report that the worktree was created successfully.

### Step 7: Report Success

Output a summary (show both directory and branch name if they differ):

```
Worktree created:
  Branch:   <branch>
  Parent:   <parent>
  Path:     .worktrees/<dir>

  Configs symlinked:
    .env                     symlinked | not found, skipped

  Dependencies: installed

  To start working:
    cd .worktrees/<dir>

  To remove later:
    git worktree remove .worktrees/<dir>
```

## Edge Cases

- **No branch name** — prompt user (only interactive step)
- **Worktree path exists** — error with `git worktree remove` hint
- **Branch already checked out elsewhere** — error with which worktree has it
- **Branch name has existing PR** — auto-rename branch to `<name>-v2` (or `-v3`, etc.), worktree directory keeps original name
- **Branch exists locally** — use without `-b`, skip `gt track`
- **`.env` doesn't exist** — skip silently
- **`gt track` fails** — warn but continue
- **`pnpm install` fails** — warn but report worktree was created

## Important Rules

- **Always use absolute paths** for symlink sources
- **Always check preconditions** before creating the worktree
- **New branches default to `staging` parent** unless `--parent` is specified
- **Existing branches skip `gt track`** — they already have tracking

---
version: 1.0.0
name: tool-worktree
description: Manage git bare + worktree repositories
---

# Git Worktree Management

Manage repositories that use the bare + worktree pattern. In this setup, each branch is a separate directory — you switch context by `cd`-ing, not by stashing and checking out.

## Repository Structure

```
~/Repository/my-project/
├── .bare/              ← bare clone (all git data)
├── .git                ← file pointing to .bare
├── main/               ← default branch (keep clean)
├── feature-auth/       ← active work
└── hotfix-fix-crash/   ← parallel work
```

## Detecting Worktree Repos

Before running any command, detect whether the current repo uses the bare + worktree pattern:

```bash
# Check if .git is a file (worktree pattern) vs directory (normal clone)
if [[ -f "$(git rev-parse --show-toplevel)/../.git" ]]; then
    # Bare + worktree pattern
    ROOT="$(cd "$(git rev-parse --show-toplevel)/.." && pwd)"
else
    # Normal clone — worktree commands won't work
fi
```

The repo root is the directory containing `.bare/` and `.git` (the file). Each subdirectory is a worktree.

## Commands Reference

These scripts live in `~/.local/bin/` and are available as git subcommands:

| Command | Purpose |
|---------|---------|
| `git wtc <url> [name]` | Clone repo as bare + worktree |
| `git wta <branch> [base]` | Add worktree (new branch or checkout existing remote) |
| `git wtd <branch>` | Remove worktree and delete branch |
| `git wtu [base]` | Rebase current branch on base (default: main) |
| `git wtl` | List all worktrees |
| `git wtmigrate` | Convert normal clone to bare + worktree |

## Operations

### List Worktrees

Show all worktrees with their branch and status:

```bash
git wtl
```

For richer status, iterate worktrees and show ahead/behind:

```bash
ROOT="<repo-root>"
cd "$ROOT"
git fetch --all --prune

for wt in $(git worktree list --porcelain | grep "^worktree " | awk '{print $2}'); do
    branch=$(git -C "$wt" symbolic-ref --short HEAD 2>/dev/null || echo "detached")
    status=$(git -C "$wt" status --porcelain | wc -l)
    ahead_behind=$(git -C "$wt" rev-list --left-right --count "origin/$branch...$branch" 2>/dev/null || echo "? ?")
    ahead=$(echo "$ahead_behind" | awk '{print $2}')
    behind=$(echo "$ahead_behind" | awk '{print $1}')
    echo "$branch: $status uncommitted, ↑$ahead ↓$behind"
done
```

### Clone a New Repo

```bash
git wtc <git-url> [folder-name]
```

This creates the bare + worktree structure and checks out the default branch.

### Add a Worktree

For a new feature branch:

```bash
cd "$ROOT"
git wta feature-name        # branches from main
git wta feature-name develop # branches from develop
```

For checking out an existing remote branch (e.g., a PR):

```bash
cd "$ROOT"
git wta their-branch-name   # detects it on origin, checks it out
```

### Remove a Worktree

```bash
cd "$ROOT"
git wtd feature-name   # removes worktree dir and deletes branch
```

Refuses to delete the default branch. Warns if branch has unmerged changes.

### Sync a Single Worktree with Main

Update the current branch by rebasing on main:

```bash
cd "$ROOT/<branch>"
git wtu           # pulls main, rebases current branch
git wtu develop   # rebase on develop instead
```

### Sync ALL Worktrees with Main

Pull main first, then merge/rebase main into every open worktree branch:

```bash
ROOT="<repo-root>"
default_branch=$(git -C "$ROOT" remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')
default_branch="${default_branch:-main}"

# Step 1: Update the default branch
echo "Updating $default_branch..."
git -C "$ROOT/$default_branch" pull --ff-only

# Step 2: Sync each worktree
for wt in $(git worktree list --porcelain | grep "^worktree " | awk '{print $2}'); do
    branch=$(git -C "$wt" symbolic-ref --short HEAD 2>/dev/null)

    # Skip the default branch (already updated) and detached HEADs
    [[ "$branch" == "$default_branch" || -z "$branch" ]] && continue

    # Check for uncommitted changes
    if [[ -n "$(git -C "$wt" status --porcelain)" ]]; then
        echo "SKIP $branch — has uncommitted changes"
        continue
    fi

    echo "Syncing $branch..."
    git -C "$wt" rebase "$default_branch" 2>&1 || {
        echo "CONFLICT in $branch — aborting rebase"
        git -C "$wt" rebase --abort
    }
done
```

**Important:** Always skip worktrees with uncommitted changes. If a rebase has conflicts, abort it and report the conflict to the user — never force-resolve.

### Sync Multiple Repos

When working across related projects (e.g., api + site + docs), sync all of them:

```bash
for repo in ~/Repository/my-api ~/Repository/my-frontend ~/Repository/my-docs; do
    if [[ -f "$repo/.git" ]]; then
        echo "=== $(basename $repo) ==="
        # Run the sync-all-worktrees logic from above for each repo
    fi
done
```

### Check Worktree Health

Audit worktrees for issues (stale branches, missing upstreams, diverged branches):

```bash
ROOT="<repo-root>"
cd "$ROOT"
git fetch --all --prune

for wt in $(git worktree list --porcelain | grep "^worktree " | awk '{print $2}'); do
    branch=$(git -C "$wt" symbolic-ref --short HEAD 2>/dev/null || echo "detached")
    [[ "$branch" == "detached" ]] && echo "WARNING: $wt is in detached HEAD" && continue

    # Check if remote branch still exists
    if ! git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
        # Check if it was merged
        if git -C "$ROOT" branch --merged "$default_branch" | grep -q "$branch"; then
            echo "MERGED: $branch — safe to remove (git wtd $branch)"
        else
            echo "LOCAL-ONLY: $branch — no remote tracking branch"
        fi
    fi

    # Check for uncommitted changes
    changes=$(git -C "$wt" status --porcelain | wc -l)
    [[ "$changes" -gt 0 ]] && echo "DIRTY: $branch — $changes uncommitted changes"
done
```

### Convert Normal Clone to Worktree Pattern

If a repo was cloned normally:

```bash
cd ~/Repository/my-project
git wtmigrate
```

This restructures in-place: `.git/` becomes `.bare/`, working files move into a `main/` subdirectory. Preserves gitignored files (node_modules, .env, etc.).

## Workflow Guidelines

- **Never work directly in `main/`** — keep it as a clean reference, only pull.
- **Each worktree is independent** — separate `node_modules`, build caches, etc.
- **Sync before starting work** — pull main and rebase your branch.
- **Clean up after merge** — remove worktrees for merged branches.
- **Check for conflicts before bulk sync** — report conflicts, don't force-resolve.
- **Respect uncommitted changes** — never rebase a dirty worktree.

## When to Use This Skill

- User asks to create a new branch or start working on a feature
- User asks to sync, update, or rebase branches
- User asks to clean up old branches or worktrees
- User mentions worktrees, bare repos, or branch management
- Before starting work that needs a separate branch
- After PRs are merged, to clean up worktrees

---
name: branchless-workflow
description: Git-branchless stacked diffs workflow patterns and command reference
user-invocable: false
---

# Git-Branchless Workflow

Git-branchless enables stacked diffs development - working with multiple commits that build on each other, editing any commit in the stack, and managing PRs efficiently.

## Core Concepts

### Detached HEAD Workflow
In git-branchless, you work in **detached HEAD** mode. Main stays put while you stack commits above it.

```bash
# Always detach before building a stack
git checkout --detach

# Or use git record -d to auto-detach
git record -d -m "feat: first commit"
```

### Smartlog Icons

| Icon | Meaning |
|------|---------|
| `◆` | Public commit (on main branch) |
| `◯` | Draft commit (your work in progress) |
| `●` | Current HEAD position |
| `✕` | Abandoned/hidden commit |
| `ᐅ` | Current branch indicator |

## Essential Commands

### Visualization
```bash
git sl                    # View commit stack (smartlog)
```

### Navigation
```bash
git prev                  # Move to parent commit
git next                  # Move to child commit
git prev N                # Jump N commits up
git next N                # Jump N commits down
git sw -i                 # Interactive commit selector (fuzzy finder)
git sw -i <search>        # Pre-filter by search term
```

### Committing
```bash
git record -m "msg"              # Commit all changes (no git add needed)
git record -c pr/name -m "msg"   # Commit + create branch in one step
git record -d -m "msg"           # Detach from branch, then commit
git record -I -m "msg"           # Insert commit in middle, auto-rebase children
```

### Editing Commits
```bash
git amend                 # Amend current commit + auto-restack descendants
git reword                # Change commit message + auto-restack
git restack               # Rebase descendants onto amended commit
```

### Moving Commits
```bash
git move -s <src> -d <dst>  # Move commit(s) to new parent
```

### Syncing
```bash
git sync                  # Rebase stack onto local main
git sync --pull           # Fetch remote + rebase stack
```

### Submitting PRs
```bash
git switch -c pr/name     # Create branch at current commit
git submit -c @           # Push current branch to remote (first time)
git submit                # Force-push existing branches (update PRs)
```

### Housekeeping
```bash
git hide <hash>           # Hide commit from smartlog
git unhide <hash>         # Restore hidden commit
```

### Recovery
```bash
git undo                  # Undo last operation (with confirmation)
git undo -i               # Interactive undo — browse history
```

## Common Workflows

### Building a Stack
```bash
git checkout --detach
git record -m "feat: first feature"
git record -m "feat: second feature"
git record -m "feat: third feature"
git sl   # View your stack
```

### Fixing a Middle Commit
```bash
git prev 2                # Go to the commit to fix
# make changes...
git add . && git amend    # Amend + restack descendants
git next 2                # Return to top
```

### Creating PRs for a Stack
```bash
# For each commit, create branch and submit
git prev 2
git switch -c pr/first-feature
git submit -c @

git next
git switch -c pr/second-feature
git submit -c @

git next
git switch -c pr/third-feature
git submit -c @
```

### Setting Stacked PR Base Branches
For true stacked PRs on GitHub:

| PR | Base Branch |
|----|-------------|
| pr/first-feature | `main` |
| pr/second-feature | `pr/first-feature` |
| pr/third-feature | `pr/second-feature` |

### After PR Merge
```bash
git pull origin main
git sl   # Find merge commit hash
git move -s <next-commit> -d <merge-commit-hash>
# Recreate branches for remaining commits
git switch -c pr/remaining-feature
git submit -c @
```

### Syncing with Updated Main
```bash
git sync --pull           # Fetch + rebase stack
git submit                # Update all PRs
```

### Recovering from Mistakes
```bash
git undo -i               # Browse history, find good state, restore
```

## Interactive Rebase Operations

```bash
git rebase -i main
```

In the editor:
- `pick` — keep commit as-is
- `drop` — remove commit
- `fixup` — squash into previous (discard message)
- `squash` — squash into previous (combine messages)
- Reorder lines to change commit order

## Best Practices

1. **Always detach before stacking** - Use `git checkout --detach` or `git record -d`
2. **Use `git amend` instead of `git commit --amend`** - It auto-restacks descendants
3. **Use `git record` instead of `git add` + `git commit`** - Simpler workflow
4. **Run `git restack` after manual amends** - Fixes abandoned commits
5. **Use `git sync --pull` regularly** - Keep stack updated with main
6. **Create branches only when ready to PR** - Use `git switch -c` or `git record -c`
7. **Force-push updates with `git submit`** - Updates all stacked PRs at once

## Troubleshooting

### "Abandoned commits (✕) showing in smartlog"
```bash
git restack               # Rebase descendants onto amended commit
```

### "git sl only shows main / no stack visible"
You committed on main. Fix:
```bash
git checkout --detach
git branch -f main <initial-commit-hash>
```

### "git submit @ does nothing / skipped"
You need a branch AND `--create`:
```bash
git switch -c pr/my-feature
git submit -c @
```

### "Messy graph after PR merge"
Move remaining commits onto merge commit:
```bash
git pull origin main
git sl   # Find merge commit hash
git move -s <next-commit> -d <merge-commit-hash>
```

### "Conflict during restack or sync"
```bash
# Resolve conflicts in files
git add <resolved-files>
git rebase --continue
```

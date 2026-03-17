---
name: using-flo
description: Guidance for using the flo CLI to manage git worktrees from GitHub issues. Use when starting work on issues, cleaning up finished work, or managing multiple parallel workstreams.
---

# Using Flo

Flo creates git worktrees from GitHub issues with automatic Claude context setup.

## Commands

| Command       | Purpose                                           |
| ------------- | ------------------------------------------------- |
| `flo [issue]` | Start work - create worktree from issue or branch |
| `flo end`     | End work - merge PR, delete worktree, sync main   |
| `flo list`    | List all worktrees                                |
| `flo prune`   | Clean up metadata for manually deleted worktrees  |

## Starting Work

```fish
# From GitHub issue (fetches issue, creates branch, sets up Claude context)
flo 123

# From branch name (no GitHub integration)
flo feat/experiment

# Interactive picker (shows open issues)
flo
```

__Issue mode auto:__

* Assigns issue to you
* Creates branch: `feat/123-title`, `fix/123-title`, etc.
* Generates `.claude/issue.md` with issue context
* Copies Serena cache if present
* Runs `pnpm install`

## Ending Work

```fish
# Merge PR, delete worktree/branch, sync main (default)
flo end

# Abandon work (close PR without merging)
flo end --resolve abort

# Skip validations (dirty worktree, failing checks)
flo end --force

# Clean up locally, don't touch PR
flo end --ignore pr

# Preview without executing
flo end --dry
```

## Worktree Layout

```
~/projects/myproject/                    (main repo)
~/projects/myproject_feat-123-add-auth/  (worktree)
~/projects/myproject_fix-456-bug/        (worktree)
```

## Notes

* Always use `flo end` (not `rm -rf`) to clean up worktrees
* If you did `rm -rf`, run `flo prune` to clean git metadata
* Run `flo -h` or `flo <command> -h` for detailed help

---
name: ralph-discard
description: Abandon RALPH worktree without merging changes
allowed-tools: Bash, Read, AskUserQuestion
---

# RALPH-DISCARD - Abandon Worktree

Discard a RALPH worktree and all its changes without merging.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-discard` | Discard current/only worktree |
| `/ralph-discard {spec-name}` | Discard specific worktree |
| `/ralph-discard --force` | Skip confirmation prompt |
| `/ralph-discard --all` | Discard all RALPH worktrees |

## Triggers

- `/ralph-discard`
- "discard worktree"
- "abandon ralph changes"
- "delete worktree"

## Process

### Step 1: Select Worktree

If multiple worktrees exist:

```
? Which worktree do you want to discard?
  ○ ralph/user-authentication (4 commits, 12 files)
  ○ ralph/payment-integration (2 commits, 5 files)
  ○ All worktrees
```

### Step 2: Show Impact

```
╔════════════════════════════════════════════════════════════════╗
║                    Discard Warning                              ║
╚════════════════════════════════════════════════════════════════╝

⚠ You are about to discard:

Worktree: .worktrees/user-authentication
Branch: ralph/user-authentication

This will permanently delete:
  - 4 commits
  - 12 files of work
  - +342 lines of code

PRD progress will NOT be affected:
  - prd.json will remain unchanged
  - You can re-run /ralph-run to start fresh

This action CANNOT be undone.
```

### Step 3: Confirm

```
? Are you sure you want to discard this worktree?
  ○ Yes, discard all changes
  ○ No, keep the worktree
  ○ No, let me review first (/ralph-review)
```

### Step 4: Execute Discard

```bash
# Remove worktree (force to handle uncommitted changes)
git worktree remove .worktrees/{spec-name} --force

# Delete the branch
git branch -D ralph/{spec-name}
```

### Step 5: Confirm Cleanup

```
╔════════════════════════════════════════════════════════════════╗
║                    Worktree Discarded                           ║
╚════════════════════════════════════════════════════════════════╝

✓ Removed worktree: .worktrees/user-authentication
✓ Deleted branch: ralph/user-authentication

The following changes were discarded:
  - 4 commits
  - 12 files
  - +342 lines

Your main branch is unchanged.

Next steps:
  - Run /ralph-run to start fresh implementation
  - Run /ralph to check PRD status
```

## Discard All

With `/ralph-discard --all`:

```
╔════════════════════════════════════════════════════════════════╗
║                    Discard All Worktrees                        ║
╚════════════════════════════════════════════════════════════════╝

⚠ You are about to discard ALL RALPH worktrees:

1. ralph/user-authentication
   - 4 commits, 12 files

2. ralph/payment-integration
   - 2 commits, 5 files

Total: 6 commits, 17 files will be lost.

? Proceed with discarding all worktrees?
  ○ Yes, discard everything
  ○ No, let me choose specific worktrees
  ○ Cancel
```

## Force Mode

With `--force`, skip confirmation:

```bash
# Used for automated cleanup or when you're certain
/ralph-discard --force

# Or for specific worktree
/ralph-discard user-authentication --force
```

Output:

```
✓ Force discarded: ralph/user-authentication
```

## Uncommitted Changes

If the worktree has uncommitted changes:

```
╔════════════════════════════════════════════════════════════════╗
║                    Uncommitted Changes                          ║
╚════════════════════════════════════════════════════════════════╝

⚠ This worktree has uncommitted changes:

Modified:
  ~ src/services/user.service.ts
  ~ tests/services/user.service.test.ts

Untracked:
  + src/utils/temp.ts

? How do you want to proceed?
  ○ Discard everything (including uncommitted)
  ○ Commit changes first, then discard
  ○ Cancel and review changes
```

## Recovery Note

```
╔════════════════════════════════════════════════════════════════╗
║                    Recovery Information                         ║
╚════════════════════════════════════════════════════════════════╝

If you accidentally discarded a worktree, you may be able to recover
commits using git reflog (within 30 days):

  git reflog
  git checkout -b recovered {commit-hash}

However, uncommitted changes CANNOT be recovered.
```

## Error Handling

| Error | Action |
|-------|--------|
| No worktrees | Inform user, nothing to discard |
| Worktree not found | List available worktrees |
| Permission denied | Suggest --force flag |
| Branch in use | Checkout different branch first |

## Safety Checks

Before discarding:

1. **Check for unique work** - Warn if commits aren't pushed anywhere
2. **Check uncommitted changes** - Extra confirmation required
3. **Verify worktree path** - Prevent accidental deletion of wrong directory

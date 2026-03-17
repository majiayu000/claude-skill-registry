---
name: ralph-merge
description: Merge completed RALPH worktree changes to main branch
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# RALPH-MERGE - Merge Worktree to Main

Merge completed RALPH worktree changes back to the main branch.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-merge` | Merge current worktree to main |
| `/ralph-merge {spec-name}` | Merge specific worktree |
| `/ralph-merge --squash` | Squash all commits into one |
| `/ralph-merge --dry-run` | Show what would be merged |

## Triggers

- `/ralph-merge`
- "merge worktree"
- "integrate RALPH changes"
- "merge ralph branch"

## Prerequisites

```bash
# Check for worktrees
WORKTREES=$(git worktree list --porcelain | grep -c "^worktree" || echo "0")
if [ "$WORKTREES" -le 1 ]; then
  echo "❌ No RALPH worktrees found"
  echo "Run /ralph-run first to create a worktree"
  exit 1
fi

# List available worktrees
echo "Available RALPH worktrees:"
git worktree list | grep "ralph/"
```

## Process

### Step 1: Select Worktree

If multiple worktrees exist, use AskUserQuestion:

```
? Which worktree do you want to merge?
  ○ ralph/user-authentication (4 commits, 12 files)
  ○ ralph/payment-integration (2 commits, 5 files)
  ○ Cancel
```

### Step 2: Review Changes

Show summary of changes to be merged:

```
╔════════════════════════════════════════════════════════════════╗
║                    Merge Preview                                ║
╚════════════════════════════════════════════════════════════════╝

Worktree: .worktrees/user-authentication
Branch: ralph/user-authentication
Target: main

Commits to merge: 4
  abc1234 feat: ST-001-1 - Create User type definitions
  def5678 feat: ST-001-2 - Create Zod validation schema
  ghi9012 feat: ST-001-3 - Create User service layer
  jkl3456 feat: ST-001-4 - Add unit tests

Files changed: 12
  src/types/user.ts (new)
  src/types/index.ts (modified)
  src/schemas/user.schema.ts (new)
  src/services/user.service.ts (new)
  ...

Diff stats:
  +342 lines added
  -12 lines removed
```

### Step 3: Confirm Merge

```
? Proceed with merge?
  ○ Yes, merge to main (Recommended)
  ○ Yes, squash merge (combine all commits)
  ○ No, review changes first (/ralph-review)
  ○ No, abandon changes (/ralph-discard)
```

### Step 4: Execute Merge

```bash
# Save current branch
CURRENT=$(git rev-parse --abbrev-ref HEAD)

# Checkout main
git checkout main

# Merge worktree branch (--no-ff preserves history)
git merge ralph/{spec-name} --no-ff -m "feat: Implement {spec-name}

Merged from RALPH worktree:
- {summary of changes}

Stories completed:
- US-001: {title}
- US-002: {title}

Co-Authored-By: RALPH <noreply@anthropic.com>"

# Remove worktree
git worktree remove .worktrees/{spec-name} --force

# Delete branch
git branch -d ralph/{spec-name}
```

### Step 5: Cleanup

```
╔════════════════════════════════════════════════════════════════╗
║                    Merge Complete                               ║
╚════════════════════════════════════════════════════════════════╝

✓ Merged ralph/user-authentication into main
✓ Removed worktree: .worktrees/user-authentication
✓ Deleted branch: ralph/user-authentication

Commits merged: 4
Files changed: 12

Current branch: main

Next steps:
  - Run tests: npm test
  - Push to remote: git push origin main
```

## Squash Merge

With `--squash`, all commits are combined:

```bash
git checkout main
git merge ralph/{spec-name} --squash
git commit -m "feat: Implement {spec-name}

Combined from 4 commits in RALPH worktree.

Changes:
- Created User type definitions
- Added Zod validation schema
- Implemented User service layer
- Added unit tests

Co-Authored-By: RALPH <noreply@anthropic.com>"
```

## Error Handling

| Error | Action |
|-------|--------|
| Merge conflicts | Show conflict files, offer resolution |
| No worktrees | Direct to `/ralph-run` |
| Tests fail post-merge | Warn user, suggest `/ralph-qa` |
| Branch already deleted | Skip branch deletion |

## Conflict Resolution

If conflicts occur:

```
╔════════════════════════════════════════════════════════════════╗
║                    Merge Conflicts                              ║
╚════════════════════════════════════════════════════════════════╝

Conflicts in 2 files:
  ✗ src/types/index.ts
  ✗ src/services/auth.service.ts

Options:
  1. Resolve conflicts now (I'll help)
  2. Abort merge (keep worktree)
  3. Accept theirs (worktree version)
  4. Accept ours (main version)
```

Use AskUserQuestion to determine resolution strategy.

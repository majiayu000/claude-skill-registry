---
name: aico-worktree
description: |
  Create isolated git worktree for feature development. Handles directory selection, gitignore verification, project setup, and baseline test verification.

  Use this skill when:
  - Starting feature work that needs isolation from current workspace
  - Before executing implementation plans on a new branch
  - Want to work on multiple branches/features simultaneously
  - User asks to "create worktree", "isolate this work", "separate branch"
  - Need clean baseline before starting major changes

  Safety: ALWAYS verify worktree directory is gitignored before creating.
  Process: Check directory → Verify ignored → Create worktree → Run setup → Verify baseline tests
---

# Git Worktree

## Process

1. **Check existing directories**: `.worktrees/` or `worktrees/`
2. **Verify gitignored**: MUST verify before creating
3. **Create worktree**: `git worktree add <path> -b <branch>`
4. **Run project setup**: Auto-detect (npm/pip/go/cargo)
5. **Verify baseline tests**: Run tests, report status

## Directory Selection

| Priority | Check                  |
| -------- | ---------------------- |
| 1        | Existing `.worktrees/` |
| 2        | Existing `worktrees/`  |
| 3        | Project config/docs    |
| 4        | Ask user               |

## Safety Verification

**For project-local directories:**

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If NOT ignored → Add to `.gitignore` first.

## Creation Steps

```bash
# Create worktree with new branch
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"

# Run project setup (auto-detect)
if [ -f package.json ]; then npm install; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Verify baseline tests
npm test / pytest / go test ./...
```

## Report Format

```
Worktree ready at <full-path>
Branch: <branch-name>
Tests: <N> passing
Ready to implement <feature-name>
```

## Worktree Management

```bash
git worktree list          # List all
git worktree remove <path> # Remove after merge
git worktree prune         # Clean stale
```

## Key Rules

- ALWAYS verify directory is gitignored for project-local
- MUST run baseline tests before reporting ready
- If tests fail → Report failures, ask whether to proceed
- ALWAYS auto-detect and run project setup

## Common Mistakes

- ❌ Skip ignore verification → ✅ Always verify gitignored
- ❌ Skip baseline tests → ✅ Verify clean starting point
- ❌ Proceed with failing tests → ✅ Ask user first
- ❌ Leave stale worktrees → ✅ Remove after merge

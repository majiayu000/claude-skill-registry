---
name: worktree
description: Create a git worktree and prime the development environment for a new feature or refactor
user-invocable: true
---

# Create Git Worktree

Create a new git worktree for isolated feature development.

## Instructions

1. Parse the branch name from arguments
2. Determine if this is a new branch or existing branch
3. Run the worktree creation script
4. Report the result and next steps

## Execution

Run the following command based on the arguments:

```bash
# For new branches (default behavior)
./scripts/create-worktree.sh <branch-name> --new-branch

# For existing branches (if user specifies --existing)
./scripts/create-worktree.sh <branch-name>
```

### Branch Naming Convention

If the user provides just a feature name without a prefix, add the appropriate prefix:
- Features: `feat/<name>` (default)
- Refactors: `refactor/<name>` (if user mentions "refactor")
- Fixes: `fix/<name>` (if user mentions "fix" or "bug")
- Chores: `chore/<name>` (if user mentions "chore")

### Examples

| User Input | Branch Name |
|------------|-------------|
| `/worktree new-feature` | `feat/new-feature` |
| `/worktree refactor auth` | `refactor/auth` |
| `/worktree fix/login-bug` | `fix/login-bug` (keep as-is) |
| `/worktree feat/my-thing` | `feat/my-thing` (keep as-is) |

## After Execution

Tell the user:
1. The worktree location
2. How to navigate to it: `cd <worktree-path>`
3. Remind them to start a new Claude Code session in that directory for isolated work

## Arguments

$ARGUMENTS

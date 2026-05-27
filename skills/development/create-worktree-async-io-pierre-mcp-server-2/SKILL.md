---
name: create-worktree
description: Creates a git worktree with branch and copies environment files (.envrc, .mcp.json)
argument-hint: [branch-name]
user-invocable: true
---

# Create Worktree Skill

**CLAUDE: When this skill is invoked with `/create-worktree <branch-name>`, immediately run:**
```bash
./.claude/skills/create-worktree/create-worktree.sh <branch-name>
```

## Purpose
Creates a new git worktree with a feature branch, automatically copying environment files that are not tracked in git.

## Usage
```bash
/create-worktree feature/my-new-feature
```

## What It Does
1. Creates a new git worktree at `../pierre_mcp_server-<branch-name>`
2. Creates a new branch with the specified name
3. Copies `.envrc` from main worktree
4. Copies `.mcp.json` if present
5. Runs `direnv allow` to activate the environment

## Commands

### Using the script directly:
```bash
./.claude/skills/create-worktree/create-worktree.sh <branch-name> [optional-path]

# Examples:
./.claude/skills/create-worktree/create-worktree.sh feature/new-api
./.claude/skills/create-worktree/create-worktree.sh fix/bug-123 /tmp/quick-fix
```

### Manual steps (if script unavailable):
```bash
BRANCH="feature/my-feature"
WORKTREE="../pierre_mcp_server-${BRANCH//\//-}"

git worktree add -b "$BRANCH" "$WORKTREE"
cp .envrc "$WORKTREE/"
cp .mcp.json "$WORKTREE/" 2>/dev/null || true
cd "$WORKTREE" && direnv allow
```

## Cleanup
When done with a worktree:
```bash
git worktree remove ../pierre_mcp_server-feature-my-feature
git branch -d feature/my-feature  # if merged
```

## Related Skills
- `finish-worktree` - Completes feature branch work with rebase and merge

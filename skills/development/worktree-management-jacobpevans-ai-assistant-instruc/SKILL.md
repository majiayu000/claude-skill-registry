---
name: worktree-management
description: Use when managing git worktrees. Provides patterns for creation, cleanup, and branch naming.
version: "1.0.0"
author: "JacobPEvans"
---

# Worktree Management

<!-- markdownlint-disable-file MD013 -->

Standardized patterns for managing git worktrees across the development workflow. All commands that create or manage worktrees should use these patterns.

## Purpose

Provides single source of truth for worktree operations, branch naming conventions, and cleanup strategies. Ensures consistent worktree management across all workflows and commands.

## Branch Naming Convention

Convert feature descriptions to standardized branch names:

### Rules

- **Lowercase** all text
- Replace **spaces** with hyphens (`-`)
- Remove **special characters** (except hyphens)
- **Prefix** with type:
  - `feat/` for features (default)
  - `fix/` for bug fixes (if description contains "fix" or "bug")
  - `docs/` for documentation changes
  - `refactor/` for code refactoring
  - `test/` for test additions

### Examples

| Description | Branch Name |
| --- | --- |
| "add dark mode toggle" | `feat/add-dark-mode-toggle` |
| "fix authentication bug" | `fix/authentication-bug` |
| "Update documentation" | `feat/update-documentation` |
| "refactor API client" | `refactor/api-client` |

### Bash Pattern

```bash
# Generate branch name from description
DESCRIPTION="add dark mode toggle"
PREFIX="feat"  # or "fix" if description contains "fix" or "bug"
BRANCH_NAME=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
BRANCH_NAME="${PREFIX}/${BRANCH_NAME}"
```

## Worktree Path Structure

Branch names with slashes create nested directories, which is the intended behavior:

```bash
# Branch with slash creates nested structure
BRANCH="feat/my-feature"
# Creates: ~/git/repo-name/feat/my-feature/
```

**Note**: Slashes in branch names are preserved to maintain 1:1 mapping between branch names and directory structure.

## Worktree Creation Pattern

### Standard Worktree Path

All worktrees follow this structure:

```text
~/git/{REPO_NAME}/{BRANCH_NAME}/
```

**Example**:

- Repo: `ai-assistant-instructions`
- Branch: `feat/add-dark-mode`
- Path: `~/git/ai-assistant-instructions/feat/add-dark-mode/`

### Creation Steps

1. **Get repository name**:

   ```bash
   REPO_NAME=$(basename $(git rev-parse --show-toplevel))
   ```

2. **Find main worktree path**:

   ```bash
   MAIN_PATH=$(git worktree list | head -1 | awk '{print $1}')
   ```

3. **Sync main branch**:

   ```bash
   cd "$MAIN_PATH"
   git switch main
   git fetch --all --prune
   git pull
   ```

4. **Create worktree**:

   ```bash
   WORKTREE_PATH=~/git/${REPO_NAME}/${BRANCH_NAME}
   mkdir -p "$(dirname "$WORKTREE_PATH")"
   git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" main
   ```

5. **Verify**:

   ```bash
   cd "$WORKTREE_PATH"
   git status
   ```

## Worktree Cleanup Pattern

### Identify Stale Worktrees

Worktrees are stale if:

1. **Branch is merged** into main:

   ```bash
   git branch --merged main | grep -q "^  $BRANCH$"
   ```

2. **Remote branch deleted**:

   ```bash
   git branch -r | grep -q "origin/$BRANCH"
   # If exit code is 1, remote branch is gone
   ```

3. **Branch shows as [gone]**:

   ```bash
   git branch -vv | grep "\[gone\]"
   ```

### Cleanup Steps

1. **List all worktrees**:

   ```bash
   git worktree list
   ```

2. **For each non-main worktree**, check if stale using above criteria

3. **Remove stale worktree**:

   ```bash
   git worktree remove "$WORKTREE_PATH"
   ```

4. **Delete local branch** (if merged or gone):

   ```bash
   git branch -d "$BRANCH_NAME"  # Safe delete (merged only)
   # or
   git branch -D "$BRANCH_NAME"  # Force delete
   ```

5. **Prune administrative files**:

   ```bash
   git worktree prune
   ```

## Main Branch Synchronization

Before creating worktrees or after cleanup, sync main:

```bash
# Find main worktree
MAIN_PATH=$(git worktree list | head -1 | awk '{print $1}')
cd "$MAIN_PATH"

# Ensure on main branch
git switch main

# Fetch and prune
git fetch --all --prune

# Pull latest
git pull

# Return to original directory
cd -
```

## Common Patterns

### Pattern 1: Check if Worktree Exists

```bash
WORKTREE_PATH=~/git/repo-name/feat_branch-name
if [ -d "$WORKTREE_PATH" ]; then
  echo "Worktree already exists at $WORKTREE_PATH"
  cd "$WORKTREE_PATH"
else
  echo "Creating new worktree..."
  # Use creation pattern above
fi
```

### Pattern 2: List All Worktrees

```bash
git worktree list
# Output format:
# /path/to/main        abc123 [main]
# /path/to/worktree-1  def456 [feat/feature-1]
# /path/to/worktree-2  ghi789 [fix/bug-fix]
```

### Pattern 3: Get Current Worktree Branch

```bash
CURRENT_BRANCH=$(git branch --show-current)
```

### Pattern 4: Validate Repository

```bash
git rev-parse --is-inside-work-tree
# Exit code 0 = valid git repo
# Exit code != 0 = not a git repo
```

## Commands Using This Skill

- `/init-worktree` - Primary worktree creation command
- `/create-worktrees:create-worktrees` - Create worktrees for all open PRs (plugin)
- `/fix-pr-ci` - Creates worktrees for PR branches
- `/sync-main` - Syncs main across worktrees
- `/git-refresh` - Cleanup and sync workflow

## Plugin Integration

For creating worktrees for all open PRs, use the **create-worktrees plugin** instead of manual creation:

```bash
/create-worktrees:create-worktrees
```

This plugin automatically:

- Fetches all open PRs via GitHub CLI
- Creates worktrees for each PR branch
- Handles branch names with slashes correctly
- Cleans up stale worktrees

## Related Resources

- worktrees rule - Policy and structure documentation
- branch-hygiene rule - Branch management best practices
- create-worktrees plugin - Create worktrees for all open PRs

## Troubleshooting

### Issue: "fatal: '$WORKTREE_PATH' already exists"

**Cause**: Worktree directory exists but not registered with git

**Solution**:

```bash
# Remove the directory
rm -rf "$WORKTREE_PATH"
# Re-create using proper git worktree add command
```

### Issue: "fatal: invalid reference: $BRANCH_NAME"

**Cause**: Branch name contains invalid characters

**Solution**: Use branch naming convention from this skill (alphanumeric and hyphens only)

### Issue: Worktree shows as "prunable" in git worktree list

**Cause**: Worktree directory was deleted without using `git worktree remove`

**Solution**:

```bash
git worktree prune
```

### Issue: Cannot remove worktree - "has changes"

**Cause**: Uncommitted changes in worktree

**Solution**:

```bash
# Commit or stash changes first
cd "$WORKTREE_PATH"
git stash
cd -
# Then remove
git worktree remove "$WORKTREE_PATH"
```

## Best Practices

1. **Always sync main** before creating new worktrees
2. **Preserve slashes in branch names** - Directory nesting follows branch structure (e.g., `feat/my-feature` creates `~/git/repo/feat/my-feature/`)
3. **Clean regularly** - Remove merged/gone worktrees to save disk space
4. **Never work on main** - Always create a feature branch worktree
5. **One worktree per feature** - Isolation prevents conflicts
6. **Verify before creating** - Check if worktree already exists
7. **Prune after cleanup** - Run `git worktree prune` after removing worktrees

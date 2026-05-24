---
name: agent-ops-git-worktree
description: "Manage git worktrees for isolated development. Create, list, remove, and work in worktrees."
category: git
invokes: [agent-ops-git]
invoked_by: [agent-ops-planning]
state_files:
  read: [constitution.md]
  write: [focus.md]
---

# Git Worktree Workflow

## When to Use

Use git worktrees when you need to:
- Work on multiple branches simultaneously without stashing
- Isolate experimental work from main repository
- Safely test changes without affecting main working tree
- Create temporary development contexts

## Preconditions

- `.agent/constitution.md` exists
- Git repository initialized
- Worktrees directory exists: `C:\dev\temp\worktrees` (or configured in constitution)

## Procedure

### Create Worktree

1. **Create worktree with branch** (one operation):
   ```bash
   git worktree add <worktree-path> -b <branch-name>
   
   # Example:
   git worktree add C:/dev/temp/worktrees/agent-ops-feat-123 feat/feature-123
   ```

2. **Verify worktree**:
   ```bash
   git worktree list
   
   # Verify directory structure
   ls -la <worktree-path>/.git
   # Should be a file (pointer to main repo .git)
   ```

3. **Navigate to worktree**:
   ```bash
   cd <worktree-path>
   
   # Verify correct branch
   git branch --show-current
   
   # Work normally (git operations work as expected)
   git status
   git add .
   git commit -m "feat: ..."
   ```

### List Worktrees

```bash
# List all worktrees
git worktree list

# Detailed list with branches
git worktree list --porcelain
```

### Remove Worktree

**After work is complete and merged**:
```bash
# Navigate out of worktree
cd <main-repo>

# Remove worktree
git worktree remove <worktree-path>

# Delete feature branch (if merged)
git branch -d <feature-branch>
```

### Worktree Cleanup

**Remove stale worktrees**:
```bash
# List all worktrees
git worktree list

# Remove worktrees for deleted branches
git worktree remove <worktree-path>
```

## Integration with Issue Tracking

When working in a worktree:
1. Update `.agent/focus.md` to reflect worktree location
2. Track issue progress normally (updates worktree's git state)
3. When committing, reference issue ID in commit message

## Example Workflow

```bash
# In main repo (C:\dev\temp\agent-ops)
git worktree add C:/dev/temp/worktrees/agent-ops-opencode feat/opencode-bundle

# In worktree
cd C:/dev/temp/worktrees/agent-ops-opencode
# ... implement changes ...
git add .
git commit -m "feat: implement OpenCodeGenerator enhancements [FEAT-0335]"

# Merge back to main
cd C:/dev/temp/agent-ops
git merge feat/opencode-bundle
git worktree remove C:/dev/temp/worktrees/agent-ops-opencode
```

## Scope

- ✅ Create worktrees
- ✅ List worktrees
- ✅ Remove worktrees
- ✅ Work in worktrees (normal git operations)
- ❌ Prune worktrees (use git worktree prune, which is built-in)

## Notes

- Worktrees are lightweight (share same .git directory)
- Safe to delete worktree directory after removal
- No risk to main repository when working in worktree
- Perfect for feature development, bug fixes, testing

## Important Rules

**Never push without explicit user permission:**
- Git push requires explicit user request before execution
- This is enforced by `agent-ops-git` skill and applies to all workflows
- Auto-push is NEVER permitted, even for successful merges
- Always ask for confirmation before: `git push`

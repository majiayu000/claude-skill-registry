---
name: git-prune
description: This skill should be used when pruning local branches that have been deleted on the remote. It fetches remote changes, identifies stale local branches, and safely deletes them.
allowed-tools: ["Bash"]
---

# Git Prune Local Branches

Remove local branches whose upstream tracking branches have been deleted on remote.

## Workflow

### Fetch and prune remote-tracking references

!git fetch --prune

### Find and delete stale local branches

!git branch -vv | grep ': gone]' | awk '{print $1}'

### Apply these requirements

1. **Preview**: Show which branches will be deleted before deleting
2. **Safe Delete**: Use `-d` (safe delete) which refuses to delete unmerged branches
3. **Report**: Show summary of deleted branches

### Never

- Force delete (`-D`) without user confirmation
- Delete the current branch
- Delete protected branches (dev, staging, main)

## Execute

Execute the workflow now.

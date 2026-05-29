---
name: create-branch
description: Create timestamped topic branch.
allowed-tools: Bash
user-invocable: false
---

# Create Branch

Create a new timestamped topic branch.

## Instructions

Create a timestamped branch with the given prefix:

```bash
git checkout -b "<prefix>-$(date +%Y%m%d-%H%M%S)"
```

### Valid Prefixes

- **feat** - New feature
- **fix** - Bug fix
- **refact** - Refactoring

### Output

The script outputs the created branch name:

```
feat-20260120-205418
```

The branch is automatically checked out after creation.

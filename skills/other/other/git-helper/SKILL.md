---
name: git-helper
description: "Common git operations as a skill (status, pull, push, branch, log)"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔀",
        "requires": { "bins": ["git"] },
        "install": [],
      },
  }
---

# Git Helper

Common git operations as a skill. Provides convenient wrappers for frequently used git commands including status, pull, push, branch management, and log viewing.

## Commands

```bash
# Show working tree status
git-helper status

# Pull latest changes
git-helper pull

# Push local commits
git-helper push

# List or manage branches
git-helper branch

# View commit log with optional limit
git-helper log [--limit 10]
```

## Install

No installation needed. `git` is always present on the system.

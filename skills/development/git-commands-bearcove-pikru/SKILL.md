---
name: git-commands
description: Git command conventions for pikru. Use when running any git commands to avoid blocking on interactive pager.
---

# Git Commands

Always use `--no-pager` BEFORE the git command to avoid blocking on interactive pager:

```bash
git --no-pager log -10
git --no-pager diff
git --no-pager show
```

The `--no-pager` flag must come **before** the subcommand (log, diff, show, etc.), not after.

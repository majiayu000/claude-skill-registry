---
name: commit
description: Safe git commit workflow that prevents commits to main branch. Use when the user asks to "commit changes", "save changes", "git commit", or when completing a task that needs version control. Automatically creates feature branches when on main. NEVER creates pull requests unless explicitly requested by the user.
---

# Safe Commit Workflow

1. **Check branch**: `git branch --show-current`
2. **If on main**: Create branch `git checkout -b feat/<name>` or `fix/<name>`
3. **Format**: `moon fmt && moon info`
4. **Commit** with conventional message (`feat:`, `fix:`, `refactor:`, etc.)
5. **Never push or create PR** unless explicitly requested

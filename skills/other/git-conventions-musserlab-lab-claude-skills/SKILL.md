---
name: git-conventions
description: Git commit practices and conventions. Use when committing changes, writing commit messages, creating branches, or making PRs.
user-invocable: false
---

# Git Practices

## Before Starting Work

```bash
# Check current branch and status
git status
git branch

# Pull latest changes if on a shared branch
git pull
```

## Committing Changes

1. **Commit frequently** — after completing each logical unit of work
2. **Write descriptive commit messages** — explain the "what" and "why"
3. **Include the co-author line** at the end of commit messages:
   ```
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

4. **Check what will be committed** before committing:
   ```bash
   git status
   git diff --staged
   ```

## Don't Commit

- Large output files (check `.gitignore`)
- Credentials or secrets (`.env`, `credentials.json`, etc.)
- IDE-specific files unless project convention says otherwise
- Claude Code worktrees (`.claude/worktrees/`)
- Rendered HTML from Quarto/Rmarkdown scripts — these are large, regenerable artifacts

## When to Prompt User About Commits

- After completing a significant task
- Before switching to a different area of the codebase
- At the end of a working session (use `/done` skill)
- After updating documentation

## Troubleshooting

**"Command not found" for git tools**
→ Git should be available system-wide; check PATH if issues arise

**Merge conflicts**
→ Alert the user and explain the conflict before attempting resolution

**Git push fails with SSH permission denied**
→ SSH keys aren't available in Claude Code's terminal environment
→ Switch remote to HTTPS: `git remote set-url origin https://github.com/OWNER/REPO.git`
→ The gh CLI provides HTTPS authentication automatically
---
name: github
version: 1.0.0
description: Interact with GitHub using the gh CLI for repos, issues, PRs, and actions.
metadata:
  openclaw:
    emoji: 🐙
    category: development
---

# GitHub

Interact with GitHub using the gh CLI for repos, issues, PRs, and actions.

## Common Commands

```bash
# Repository
gh repo create
gh repo clone

# Issues
gh issue list
gh issue create

# PRs
gh pr create
gh pr merge

# Actions
gh run list
gh run watch
```

## Best Practices

- Use --web to open in browser
- Add --template for structured issues
- Use gh auth status to verify login

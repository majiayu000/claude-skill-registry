---
name: github-clone
description: Clone repositories and set up local workspace
---

# GitHub Clone Skill

Clone repositories and establish a clean local workspace.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Set up a local copy of a repository ready for work.

## Commands

```bash
gh auth status
gh repo clone <owner>/<repo>
gh repo clone <owner>/<repo> -- --depth 1  # shallow clone
git clone <url>
```

## Workflow

1. **Verify authentication**
   ```bash
   gh auth status
   ```

2. **Clone to workspace**
   ```bash
   cd ~/workspace
   gh repo clone owner/repo
   ```

3. **Verify clone**
   ```bash
   cd repo
   git status
   git remote -v
   ```

## Policies

- Clone into `~/workspace/` directory
- Verify auth status before cloning private repos
- Use shallow clone (`--depth 1`) for large repos when full history isn't needed
- After clone, verify remote is correctly configured

---
name: github-branches
description: Create and manage feature branches
---

# GitHub Branches Skill

Create, switch, and manage git branches for feature work.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Manage branches following team conventions and keeping work organized.

## Commands

```bash
git branch
git branch -a
git checkout -b <branch>
git switch -c <branch>
git fetch origin
git pull --rebase
git push -u origin <branch>
```

## Branch Naming Convention

```
claude/<issue-number>-<short-slug>
```

Examples:
- `claude/123-fix-login-bug`
- `claude/456-add-user-auth`
- `claude/789-refactor-api`

## Workflow

1. **Ensure clean state**
   ```bash
   git status
   git fetch origin
   ```

2. **Update main branch**
   ```bash
   git checkout main
   git pull --rebase
   ```

3. **Create feature branch**
   ```bash
   git checkout -b claude/123-fix-login-bug
   ```

4. **Push branch to remote**
   ```bash
   git push -u origin claude/123-fix-login-bug
   ```

## Policies

- **Never work directly on main/master**
- Always branch from an up-to-date main
- Use descriptive branch names with issue numbers
- Verify clean working directory before switching branches
- Delete merged branches to keep repo tidy

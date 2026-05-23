---
name: create-feature-branch
description: Create a new feature branch following Git Flow strategy. Use when starting new feature development, creating a branch for an issue, or when user says "create branch", "new feature", "start working on issue".
allowed-tools: Bash, Read
---

# Create Feature Branch

This skill creates feature branches following the project's Git Flow strategy.

## Branch Naming Convention

| Prefix      | Purpose            | Example                     |
| ----------- | ------------------ | --------------------------- |
| `feat/`     | New feature        | `feat/issue-88-return-mode` |
| `fix/`      | Bug fix            | `fix/stdout-encoding`       |
| `refactor/` | Refactoring        | `refactor/output-processor` |
| `update/`   | Dependency updates | `update/jsr-packages`       |
| `remove/`   | Feature removal    | `remove/deprecated-api`     |

## Workflow

### 1. Ensure clean working directory

```bash
git status
```

If there are uncommitted changes, ask user how to handle them.

### 2. Update develop branch

```bash
git checkout develop
git pull origin develop
```

### 3. Create feature branch

Format: `{prefix}/issue-{number}-{short-description}`

```bash
git checkout -b feat/issue-{NUMBER}-{DESCRIPTION}
```

### 4. Confirm creation

```bash
git branch --show-current
```

## Checklist

- [ ] Working directory is clean
- [ ] develop branch is up to date
- [ ] Branch name follows convention
- [ ] Branch is created from develop

## Example

For Issue #88 (add return mode):

```bash
git checkout develop
git pull origin develop
git checkout -b feat/issue-88-return-mode
```

## Notes

- Always branch from `develop`, not `main`
- Include issue number in branch name for traceability
- Use lowercase with hyphens for descriptions

---
scope: universal
description: |
  Guide Git branching strategies, branch naming, and merge operations.
  Use when: creating branches, merging, pull requests, Git workflow questions.
  Keywords: branch, merge, PR, pull request, GitFlow, GitHub Flow, 分支, 合併, 工作流程.
---

# Git Workflow Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/git-workflow-guide/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2025-12-24
**Applicability**: Claude Code Skills

---

> **Core Standard**: This skill implements [Git Workflow](../../core/git-workflow.md). For comprehensive methodology documentation, refer to the core standard.

## Purpose

This skill provides guidance on Git branching strategies, branch naming conventions, and merge operations.

## Quick Reference

### Workflow Strategy Selection

| Deployment Frequency | Recommended Strategy |
|---------------------|---------------------|
| Multiple times/day | Trunk-Based Development |
| Weekly to bi-weekly | GitHub Flow |
| Monthly or longer | GitFlow |

### Branch Naming Convention

```
<type>/<short-description>
```

| Type | Usage | Example |
|------|-------|---------|
| `feature/` | New functionality | `feature/oauth-login` |
| `fix/` or `bugfix/` | Bug fixes | `fix/memory-leak` |
| `hotfix/` | Urgent production fixes | `hotfix/security-patch` |
| `refactor/` | Code refactoring | `refactor/extract-service` |
| `docs/` | Documentation only | `docs/api-reference` |
| `test/` | Test additions | `test/integration-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |
| `release/` | Release preparation | `release/v1.2.0` |

### Naming Rules

1. **Use lowercase**
2. **Use hyphens for spaces**
3. **Be descriptive but concise**

## Detailed Guidelines

For complete standards, see:
- [Git Workflow Strategies](./git-workflow.md)
- [Branch Naming Reference](./branch-naming.md)

### AI-Optimized Format (Token-Efficient)

For AI assistants, use the YAML format files for reduced token usage:
- Base standard: `ai/standards/git-workflow.ai.yaml`
- Workflow options:
  - GitHub Flow: `ai/options/git-workflow/github-flow.ai.yaml`
  - GitFlow: `ai/options/git-workflow/gitflow.ai.yaml`
  - Trunk-Based: `ai/options/git-workflow/trunk-based.ai.yaml`
- Merge strategy options:
  - Squash Merge: `ai/options/git-workflow/squash-merge.ai.yaml`
  - Merge Commit: `ai/options/git-workflow/merge-commit.ai.yaml`
  - Rebase + FF: `ai/options/git-workflow/rebase-ff.ai.yaml`

## Pre-branch Checklist

Before creating a new branch:

1. **Check for unmerged branches**
   ```bash
   git branch --no-merged main
   ```

2. **Sync latest code**
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Verify tests pass**
   ```bash
   npm test  # or your project's test command
   ```

4. **Create branch with proper naming**
   ```bash
   git checkout -b feature/description
   ```

## Merge Strategy Quick Guide

| Strategy | When to Use |
|----------|-------------|
| **Merge Commit** (`--no-ff`) | Long-lived features, GitFlow releases |
| **Squash Merge** | Feature branches, clean history |
| **Rebase + FF** | Trunk-Based, short-lived branches |

## Examples

### Creating a Feature Branch

```bash
# Good
git checkout -b feature/user-authentication
git checkout -b fix/null-pointer-in-payment
git checkout -b hotfix/critical-data-loss

# Bad
git checkout -b 123              # Not descriptive
git checkout -b Fix-Bug          # Not lowercase
git checkout -b myFeature        # No type prefix
```

### Merge Workflow (GitHub Flow)

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/user-profile

# 2. Make changes and commit
git add .
git commit -m "feat(profile): add avatar upload"
git push -u origin feature/user-profile

# 3. Create PR and merge via GitHub/GitLab UI

# 4. Delete branch after merge
git checkout main
git pull origin main
git branch -d feature/user-profile
```

### Handling Merge Conflicts

```bash
# 1. Update your branch with main
git checkout feature/my-feature
git fetch origin
git merge origin/main

# 2. Resolve conflicts in files
# <<<<<<< HEAD
# Your changes
# =======
# Incoming changes
# >>>>>>> origin/main

# 3. Stage resolved files
git add resolved-file.js

# 4. Complete merge
git commit -m "chore: resolve merge conflicts with main"

# 5. Test and push
npm test
git push origin feature/my-feature
```

---

## Configuration Detection

This skill supports project-specific workflow configuration.

### Detection Order

1. Check `CONTRIBUTING.md` for "Git Workflow" or "Branching Strategy" section
2. If found, use the specified strategy (GitFlow / GitHub Flow / Trunk-Based)
3. If not found, **default to GitHub Flow** for simplicity

### First-Time Setup

If no configuration found:

1. Ask the user: "This project hasn't configured a Git workflow strategy. Which would you prefer? (GitFlow / GitHub Flow / Trunk-Based)"
2. After selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Git Workflow

### Branching Strategy
This project uses **[chosen option]**.

### Branch Naming
Format: `<type>/<description>`
Example: `feature/oauth-login`, `fix/memory-leak`

### Merge Strategy
- Feature branches: **[Squash / Merge commit / Rebase]**
```

---

## Related Standards

- [Git Workflow](../../core/git-workflow.md) - Core Git workflow standard
- [Commit Message Guide](../../core/commit-message-guide.md) - Commit message conventions
- [Checkin Standards](../../core/checkin-standards.md) - Pre-commit quality gates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)

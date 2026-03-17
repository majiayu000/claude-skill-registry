---
name: git-workflow
description: Git best practices for commits, branches, pull requests, and collaboration workflows following Conventional Commits and GitFlow patterns
version: 1.0.0
author: AI-Vibe-Prompts
tags: [git, workflow, version-control, collaboration, conventional-commits]
auto_invoke: true
---

# Git Workflow Skill

## Objective

Implement professional Git workflows ensuring clean commit history, proper branch management, effective collaboration, and code review best practices.

## When to Use This Skill

Auto-invoke when:
- User mentions "commit", "push", "branch", "merge", "pull request", "PR"
- Before code changes need to be saved
- Preparing for deployment or release
- Resolving merge conflicts

## Commit Message Standards (Conventional Commits)

**Format**: `<type>(<scope>): <subject>`

**Types**: feat, fix, docs, style, refactor, perf, test, chore, ci

**Examples**:
```bash
feat(auth): add OAuth2 login support
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
```

## Branch Naming: `<type>/<ticket-id>-<description>`

**Examples**:
```bash
feature/AUTH-123-oauth-integration
bugfix/CORE-456-fix-null-pointer
hotfix/PROD-789-critical-security-patch
```

## GitFlow Workflow

**Main**: production, **Develop**: integration
**Features**: branch from develop → merge to develop
**Releases**: branch from develop → merge to main+develop
**Hotfixes**: branch from main → merge to main+develop

## Pre-Commit Checklist

```bash
# No secrets
git diff --cached | grep -iE "api[_-]?key|secret|password"

# Run quality gates
npm run lint && npm run typecheck && npm run test
```

## Version History

- **1.0.0** (2025-01-03): Initial Git workflow skill

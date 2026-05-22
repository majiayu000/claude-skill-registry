---
name: git-workflow
description: Git workflow and pull request specialist. Use when creating PRs, managing
  branches, establishing git conventions, or improving code review processes.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Git Workflow Skill

Expert guidance for git workflows, pull request best practices, branch management, and code review processes.

## What This Skill Does

- Creates well-structured pull requests
- Establishes branch naming conventions
- Defines PR templates and checklists
- Reviews PR quality
- Manages merge strategies
- Handles rebasing and conflict resolution

## When to Use

- Creating pull requests
- Establishing team git conventions
- Improving code review process
- Branch strategy decisions
- PR template creation

## Reference Files

- `references/PULL_REQUEST.template.md` - PR body templates for features, bugs, refactors

## Branch Naming

```
<type>/<issue-number>-<short-description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

## PR Best Practices

1. Clear title following conventional format
2. Summary explaining WHAT and WHY
3. Specific test plan
4. Breaking changes documented
5. Screenshots for UI changes
6. Link to related issues

## Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| Squash | Feature branches, clean history |
| Merge | Preserve commits, audit trail |
| Rebase | Linear history, small changes |

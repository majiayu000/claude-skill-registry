---
name: git-workflow
description: Git workflow and conventional commits. Use when working with git, branches, commits, pull requests, code review, or version control strategy.
triggers:
  files: [".git/**", ".gitignore", ".commitlintrc*", ".husky/**", "CHANGELOG.md"]
  keywords: ["commit", "branch", "merge", "PR", "pull request", "git", "conventional commits", "code review", "rebase", "cherry-pick", "squash", "GitHub Flow", "feature branch", "hotfix", "changelog", "version control"]
auto_suggest: true
---

# Git Workflow

This skill provides universal Git workflow and conventional commits guidelines.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **Commits**: `<type>(<scope>): <description>`
- **Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore
- **Branches**: `feature/`, `fix/`, `refactor/`, `docs/`
- **Max branch life**: 3 days
- **Review**: Required before merge

---
name: release-patterns
description: PR creation, CI/CD validation, and release coordination patterns. Use when creating pull requests, running pre-PR validation, checking CI status, or coordinating merges.
---

# Release Patterns Skill

## Purpose

Ensure consistent PR creation, CI/CD validation, and release coordination following rebase-first workflow.

## When This Skill Applies

- Creating pull requests
- Running pre-PR validation
- Checking CI/CD status
- Coordinating merge timing

## Pre-PR Checklist (MANDATORY)

Before creating any PR:

- [ ] Branch name: `{TICKET_PREFIX}-{number}-{description}`
- [ ] Commits follow: `type(scope): description [{TICKET_PREFIX}-XXX]`
- [ ] Rebased on latest main: `git fetch origin && git rebase origin/{MAIN_BRANCH}`
- [ ] CI passes locally: `{CI_VALIDATE_COMMAND}`

## PR Creation

```bash
gh pr create \
  --title "feat(scope): description [{TICKET_PREFIX}-XXX]" \
  --body "## Summary
Implements feature as specified in {TICKET_PREFIX}-XXX.

## Changes
- Change 1
- Change 2

## Testing
- CI passes
- Manual testing completed"
```

## Merge Strategy

**ONLY use rebase merge:**

```bash
# CORRECT
gh pr merge --rebase --delete-branch

# NEVER
gh pr merge --squash   # Loses history
gh pr merge --merge    # Creates merge commits
```

## Reference

- **PR Template**: `.github/pull_request_template.md`
- **Workflow Guide**: `CONTRIBUTING.md`

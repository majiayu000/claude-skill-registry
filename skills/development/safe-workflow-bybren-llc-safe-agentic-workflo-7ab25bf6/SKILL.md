---
name: safe-workflow
description: SAFe development workflow guidance including branch naming conventions, commit message format, rebase-first workflow, and CI validation. Use when starting work on a Linear ticket, preparing commits, creating branches, writing PR descriptions, or asking about contribution guidelines.
---

# SAFe Workflow Skill

> **TEMPLATE**: This skill uses `{TICKET_PREFIX}` as a placeholder. Replace with your project's ticket prefix (e.g., `WOR`, `PROJ`, `FEAT`).

## Purpose

Enforce SAFe-compliant git workflow with standardized branch naming, commit message format, and rebase-first merge strategy.

## When This Skill Applies

- Starting work on a ticket
- Creating commits or branches
- Asking about PR workflow or contribution guidelines
- Asking "how should I commit this?"

## Branch Naming Convention

**Format**: `{TICKET_PREFIX}-{number}-{short-description}`

```text
# Good
{TICKET_PREFIX}-447-create-safe-workflow-skill
{TICKET_PREFIX}-123-fix-login-redirect

# Bad
feature/add-dark-mode       (missing ticket number)
john-new-feature            (personal naming)
```

## Commit Message Format

**Format**: `type(scope): description [{TICKET_PREFIX}-XXX]`

| Type       | When to Use                   |
| ---------- | ----------------------------- |
| `feat`     | New feature                   |
| `fix`      | Bug fix                       |
| `docs`     | Documentation only            |
| `refactor` | Code restructuring            |
| `test`     | Adding or updating tests      |
| `chore`    | Maintenance, dependencies     |

```text
feat(harness): create safe-workflow skill [{TICKET_PREFIX}-447]
fix(auth): resolve login redirect [{TICKET_PREFIX}-57]
```

## Rebase-First Workflow

```bash
# 1. Start from latest main
git checkout {MAIN_BRANCH} && git pull origin {MAIN_BRANCH}

# 2. Create feature branch
git checkout -b {TICKET_PREFIX}-{number}-{description}

# 3. Make commits
git commit -m "type(scope): description [{TICKET_PREFIX}-XXX]"

# 4. Before pushing - rebase
git fetch origin && git rebase origin/{MAIN_BRANCH}

# 5. Push with force-with-lease
git push --force-with-lease
```

## Pre-PR Checklist

1. Branch name follows convention
2. All commits have ticket reference
3. Rebased on latest main
4. CI passes: `{CI_VALIDATE_COMMAND}`

## Reference

- **CONTRIBUTING.md** - Full contributor guide
- **GEMINI.md** - Development commands

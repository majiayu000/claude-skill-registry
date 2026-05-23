---
name: safe-workflow
description: SAFe development workflow guidance including branch naming conventions, commit message format, rebase-first workflow, and CI validation. Use when starting work on a Linear ticket, preparing commits, creating branches, writing PR descriptions, or asking about contribution guidelines.
---

# SAFe Workflow Skill

> **📋 TEMPLATE**: This skill uses `{TICKET_PREFIX}` as a placeholder. Replace with your project's ticket prefix (e.g., `WOR`, `PROJ`, `FEAT`).

## Purpose

Enforce SAFe-compliant git workflow with standardized branch naming, commit message format, and rebase-first merge strategy. Ensures linear history and full traceability to Linear tickets.

## When This Skill Applies

Invoke this skill when:

- User mentions starting work on a ticket (e.g., "I'm starting {TICKET_PREFIX}-447")
- User is about to create a commit
- User is creating or naming a branch
- User asks about PR workflow or contribution guidelines
- User references CONTRIBUTING.md or workflow process
- User asks "how should I commit this?" or similar

## Branch Naming Convention

**Required Format**: `{TICKET_PREFIX}-{number}-{short-description}`

### Rules

- MUST start with `{TICKET_PREFIX}-` followed by ticket number
- Use lowercase letters and hyphens for description
- Keep description short but meaningful (max 50 chars total)
- Never include personal names or dates

### Examples

```text
{TICKET_PREFIX}-447-create-safe-workflow-skill
{TICKET_PREFIX}-123-fix-login-redirect
{TICKET_PREFIX}-234-add-stripe-checkout
```

### Anti-Patterns (Do NOT use)

```text
feature/add-dark-mode       (missing ticket number)
fix/broken-login            (missing ticket number)
john-new-feature            (personal naming)
WIP                         (not descriptive)
```

## SAFe Commit Message Format

**Required Format**: `type(scope): description [{TICKET_PREFIX}-XXX]`

### Types (Required)

| Type       | When to Use                         |
| ---------- | ----------------------------------- |
| `feat`     | New feature                         |
| `fix`      | Bug fix                             |
| `docs`     | Documentation only                  |
| `style`    | Formatting (no logic changes)       |
| `refactor` | Code restructuring (no feature/bug) |
| `test`     | Adding or updating tests            |
| `chore`    | Maintenance, dependencies           |
| `ci`       | CI/CD pipeline changes              |

### Scope (Optional)

Common scopes: `payments`, `auth`, `ui`, `api`, `db`, `harness`, `rls`

### Ticket Reference (MANDATORY)

Every commit MUST end with `[{TICKET_PREFIX}-XXX]` referencing the ticket.

### Examples

```text
feat(harness): create safe-workflow skill [{TICKET_PREFIX}-447]
fix(auth): resolve login redirect issue [{TICKET_PREFIX}-57]
docs: update API documentation [{TICKET_PREFIX}-123]
refactor(db): optimize query performance [{TICKET_PREFIX}-234]
chore: upgrade dependencies [{TICKET_PREFIX}-337]
```

## Rebase-First Workflow

This project enforces **linear history** through rebase-first workflow. Never create merge commits.

### Workflow Steps

```bash
# 1. Start from latest {MAIN_BRANCH}
git checkout {MAIN_BRANCH} && git pull origin {MAIN_BRANCH}

# 2. Create feature branch
git checkout -b {TICKET_PREFIX}-{number}-{description}

# 3. Make commits (SAFe format)
git add .
git commit -m "type(scope): description [{TICKET_PREFIX}-XXX]"

# 4. Keep branch updated during development
git fetch origin
git rebase origin/{MAIN_BRANCH}

# 5. Before pushing - rebase one final time
git fetch origin
git rebase origin/{MAIN_BRANCH}
# Resolve any conflicts locally

# 6. Push with force-with-lease (safe after rebase)
git push --force-with-lease origin {TICKET_PREFIX}-{number}-{description}

# 7. Create PR using template
# Use "Rebase and merge" strategy ONLY
```

### Why `--force-with-lease`?

- Safer than `--force` (won't overwrite unseen remote changes)
- Required after rebasing to push cleanly
- Prevents accidental overwrites in team environments

## Pre-PR Validation Checklist

Before creating a PR, ALL of these must pass:

### 1. Code Quality Validation

```bash
{CI_VALIDATE_COMMAND}
```

This runs: `type-check`, `lint`, `test:unit`, `format:check`

### 2. Markdown Linting

```bash
{LINT_MD_COMMAND}
```

### 3. Git Status Check

```bash
git status
# Must show: nothing to commit, working tree clean
```

### 4. Rebase Status

```bash
git fetch origin
git rebase origin/{MAIN_BRANCH}
# Must be up-to-date with {MAIN_BRANCH} branch
```

### 5. Commit Message Audit

```bash
git log origin/{MAIN_BRANCH}..HEAD --oneline
# All commits must follow SAFe format with [{TICKET_PREFIX}-XXX]
```

**Shortcut**: Use `/pre-pr` command to run all validation steps.

## Available Slash Commands

| Command           | Purpose                        | When to Use              |
| ----------------- | ------------------------------ | ------------------------ |
| `/start-work`     | Begin work on a ticket         | Starting any new work    |
| `/check-workflow` | Quick status check             | Periodically during work |
| `/pre-pr`         | Full validation before PR      | Before creating PR       |
| `/end-work`       | Complete session cleanly       | End of work session      |
| `/quick-fix`      | Fast-track for small bug fixes | Minor, isolated fixes    |

## Multi-Team Coordination

### High-Risk Files (Announce Before Touching)

| File                   | Risk   | Required Action                    |
| ---------------------- | ------ | ---------------------------------- |
| `prisma/schema.prisma` | HIGH   | Announce in Slack BEFORE touching  |
| `prisma/migrations/*`  | HIGH   | Coordinate with all teams          |
| `docker-compose*.yml`  | HIGH   | All teams must restart containers  |
| `package.json`         | MEDIUM | Run `{INSTALL_COMMAND}` after sync |
| `.env.template`        | MEDIUM | Update local `.env` files          |

### Before Starting Work

Always sync with latest {MAIN_BRANCH}:

```bash
git checkout {MAIN_BRANCH} && git pull origin {MAIN_BRANCH}
```

Or use `/local-sync` command for full synchronization.

## Authoritative Reference

For complete workflow documentation, see:

- **CONTRIBUTING.md** - Full contributor guide (SINGLE SOURCE OF TRUTH)
- **CLAUDE.md** - Development commands and architecture
- **.claude/README.md** - Harness configuration and commands

## Why These Rules Matter

1. **Linear History**: Rebase-first prevents merge conflicts between teams
2. **Ticket Traceability**: Every commit links to tickets for audit trail
3. **Quality Gates**: CI validation catches issues before production
4. **Team Coordination**: Branch naming enables automated workflows
5. **SAFe Compliance**: Standardized format supports sprint reporting

---

## Customization Guide

| Placeholder             | Description              | Example               |
| ----------------------- | ------------------------ | --------------------- |
| `{TICKET_PREFIX}`       | Your ticket/issue prefix | `WOR`, `PROJ`, `FEAT` |
| `{MAIN_BRANCH}`         | Main git branch name     | `main`, `dev`         |
| `{CI_VALIDATE_COMMAND}` | CI validation command    | `yarn ci:validate`    |
| `{LINT_MD_COMMAND}`     | Markdown linting command | `yarn lint:md`        |
| `{INSTALL_COMMAND}`     | Package install command  | `yarn install`        |

---
name: commit
description: Helps create properly formatted git commits following this project's Angular commit convention. Activates when the user asks to commit, wants a commit message, or uses /commit.
---

# Commit Convention

This project uses the Angular Conventional Commits format with Lefthook pre-commit hooks.

## Format

```
<type>[(optional scope)]: <description>
```

## Types

| Type | Usage |
|------|-------|
| `feat` | New feature (MINOR in SemVer) |
| `fix` | Bug fix (PATCH in SemVer) |
| `docs` | Documentation changes only |
| `style` | Code style (formatting, no logic change) |
| `refactor` | Code change — not a fix, not a feature |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration changes |
| `chore` | Other changes (tooling, config) |

## Scopes (Domain-Based)

Use the domain or area as scope:
- `tasks` — task management domain
- `user` — user domain
- `core` — core app components
- `shared` — shared utilities
- `store` — NgRx store changes
- `api` — API/infrastructure changes
- `e2e` — E2E test changes
- `deps` — dependency updates

## Breaking Changes

Add `!` after type/scope:
```
feat(api)!: change task endpoint response format

BREAKING CHANGE: The /tasks endpoint now returns paginated responses
```

## Examples

```
feat(tasks): add drag-and-drop reordering to task board
fix(store): handle null error in task loading
refactor(tasks): migrate task-card to signal inputs
test(tasks): add unit tests for task-store computed signals
style(tasks): format task-dashboard template
docs(readme): update development setup instructions
chore(deps): update Angular to v21.1.4
```

## Pre-Commit Hooks

Lefthook runs automatically on commit:
1. **Prettier** — auto-formats staged files
2. **ESLint** — auto-fixes linting issues

If a hook fails, fix the issue and commit again. Do NOT use `--no-verify`.

## Process

1. Stage relevant files: `git add <specific-files>`
2. Create commit with conventional message
3. Let Lefthook hooks run (Prettier + ESLint)
4. If hooks modify files, they auto-stage the changes

---
name: git-workflow
description: "Handle branches, commits, and PR prep using conventional commits. Creates clean git history with proper commit messages. Use when user says 'commit', 'PR', 'push', or 'conventional commits'."
allowed-tools: Bash, Read
---

# Git Workflow

You are an expert at managing git workflows with conventional commits.

## When To Use

- User asks "Commit these changes"
- User asks "Prepare a PR"
- User asks "Clean up my git history"
- Prior to merging non-trivial work

## Inputs

- Git repository with changes
- Optional user summary of what changed

## Outputs

- Git branch created/updated as needed
- Commits with conventional commit messages
- Optional PR description in markdown

## Workflow

### 1. Status & Diff

```bash
git status
git diff
```

Group changes logically (docs vs code vs tests).

### 2. Branch Strategy

If on main or master, create feature branch:
- `feature/<short-desc>`
- `fix/<short-desc>`

### 3. Stage Changes

Stage by concern: code, tests, docs, config.

### 4. Commit Types

Map changes to types:

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add user endpoint` |
| `fix` | Bug fix | `fix(auth): handle expired tokens` |
| `docs` | Documentation only | `docs: update README` |
| `style` | Formatting, no code change | `style: fix indentation` |
| `refactor` | Code change without feature/fix | `refactor: extract helper` |
| `test` | Adding tests | `test: add auth tests` |
| `chore` | Maintenance tasks | `chore: update deps` |
| `perf` | Performance improvement | `perf: cache queries` |
| `ci` | CI/CD changes | `ci: add deploy workflow` |

### 5. Create Commits

Use format:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Examples:
- `feat(core): add schedule parsing for custody calendar`
- `fix(api): handle empty payload in /import endpoint`

### 6. PR Template (if requested)

```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots]

## Risks
- [Any risks or concerns]
```

## Commit Message Best Practices

- Use imperative mood ("add" not "added")
- Keep subject line under 72 characters
- Separate subject from body with blank line
- Use body to explain what and why, not how

## Branch Naming

```
feature/add-user-auth
fix/login-redirect
docs/api-documentation
refactor/extract-helpers
chore/update-dependencies
```

## Anti-Patterns

- Single giant commit labeled "misc" or "updates"
- Rewriting public history without explicit request
- Committing secrets or .env files
- Mixing unrelated changes in one commit

## Keywords

commit, git, PR, pull request, push, conventional commits, branch

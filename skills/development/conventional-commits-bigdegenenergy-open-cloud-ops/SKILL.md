---
name: conventional-commits
description: Conventional Commits standard for structured commit messages - types, scopes, breaking changes, and changelog generation. Auto-triggers during git operations.
---

# Conventional Commits Skill

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```bash
feat(auth): add OAuth2 login with Google provider
fix(api): prevent null pointer on missing user profile
docs: update API endpoint documentation
refactor(db): extract connection pooling into shared module
test(payments): add integration tests for Stripe webhook
chore(deps): bump fastapi from 0.114 to 0.115
feat!: drop support for Python 3.9
```

## Commit Types

| Type       | When to Use                              | Bumps |
| ---------- | ---------------------------------------- | ----- |
| `feat`     | New feature or capability                | MINOR |
| `fix`      | Bug fix                                  | PATCH |
| `docs`     | Documentation only                       | -     |
| `style`    | Formatting, whitespace (no logic change) | -     |
| `refactor` | Code restructuring (no behavior change)  | -     |
| `perf`     | Performance improvement                  | PATCH |
| `test`     | Adding or fixing tests                   | -     |
| `build`    | Build system or dependencies             | -     |
| `ci`       | CI/CD configuration                      | -     |
| `chore`    | Maintenance tasks                        | -     |
| `revert`   | Reverting a previous commit              | PATCH |

## Scopes

Scopes are project-specific. Common patterns:

```bash
# By module/component
feat(auth): ...
fix(api): ...
refactor(db): ...

# By domain
feat(payments): ...
fix(notifications): ...

# By layer
feat(ui): ...
fix(middleware): ...
```

## Breaking Changes

Mark breaking changes with `!` after type/scope OR with a `BREAKING CHANGE:` footer:

```bash
# With ! marker
feat!: change API response format to JSON:API

# With footer
feat(api): change authentication to bearer tokens

BREAKING CHANGE: API now requires Bearer token in Authorization
header instead of API key in query parameter.
```

## Description Rules

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at end
- Under 72 characters
- Explain WHAT, not HOW (the diff shows how)

```bash
# GOOD
feat(auth): add password reset via email
fix(parser): handle empty input without crashing
refactor(db): replace raw SQL with parameterized queries

# BAD
feat(auth): Added a password reset feature.  # past tense, period, capitalized
fix: fixed the bug  # vague, past tense
refactor: code cleanup  # too vague
```

## Body and Footers

```bash
fix(api): handle race condition in concurrent order creation

The previous implementation allowed duplicate orders when two
requests arrived simultaneously. Added a database-level unique
constraint on (user_id, idempotency_key) and retry logic.

Fixes: #234
Reviewed-by: @teammate
```

### Common Footers

| Footer                         | Purpose                     |
| ------------------------------ | --------------------------- |
| `Fixes: #123`                  | Closes a GitHub issue       |
| `Refs: #456`                   | References without closing  |
| `BREAKING CHANGE: ...`         | Breaking change description |
| `Reviewed-by: @user`           | Code reviewer               |
| `Co-authored-by: Name <email>` | Co-author attribution       |

## Multi-Line Commit (Bash)

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add OAuth2 login with Google provider

Implements the full OAuth2 authorization code flow:
- Redirect to Google consent screen
- Handle callback with auth code exchange
- Create/link user account on first login

Fixes: #89
EOF
)"
```

## Decision Guide

```
Did you add a new feature?              → feat
Did you fix a bug?                      → fix
Did you change docs only?               → docs
Did you restructure without behavior change? → refactor
Did you improve performance?            → perf
Did you add/fix tests only?             → test
Did you change CI/CD config?            → ci
Did you change build/deps?              → build
Does it break backward compatibility?   → add ! or BREAKING CHANGE footer
```

## Changelog Generation

Conventional commits enable automatic changelog generation:

```bash
# With standard-version (Node.js)
npx standard-version

# With commitizen (Python)
cz changelog

# Manual approach
git log --oneline --format="%s" v1.0.0..HEAD | grep -E "^(feat|fix)"
```

### Generated Changelog Example

```markdown
## [1.2.0] - 2026-02-12

### Features

- **auth**: add OAuth2 login with Google provider (#89)
- **api**: add batch processing endpoint (#92)

### Bug Fixes

- **api**: prevent null pointer on missing user profile (#91)
- **parser**: handle empty input without crashing (#90)

### BREAKING CHANGES

- **api**: change authentication to bearer tokens
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "commit message", "conventional commit"
- "commit type", "commit scope"
- "breaking change", "changelog"
- "feat:", "fix:", "refactor:"

## Integration

- **git-workflows** skill: Advanced git operations
- **cicd-automation** skill: Automated releases from commits
- **/ship** command: Commit, push, and PR

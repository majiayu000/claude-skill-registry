---
name: git-conventional-commits
description: Apply when writing commit messages to maintain consistent, readable git history that enables automated changelog generation.
version: 1.0.0
tokens: ~400
confidence: high
sources:
  - https://www.conventionalcommits.org/en/v1.0.0/
  - https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [git, commits, conventions]
---

## When to Use

Apply when writing commit messages to maintain consistent, readable git history that enables automated changelog generation.

## Patterns

### Pattern 1: Commit Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```
Source: https://www.conventionalcommits.org/en/v1.0.0/

### Pattern 2: Types
```
feat:     New feature (MINOR version bump)
fix:      Bug fix (PATCH version bump)
docs:     Documentation only
style:    Formatting, no code change
refactor: Code change, no feature/fix
perf:     Performance improvement
test:     Adding/fixing tests
chore:    Build, tooling, deps
ci:       CI/CD changes
```

### Pattern 3: Examples
```bash
# Feature
feat(auth): add OAuth2 login with Google

# Bug fix
fix(cart): prevent negative quantity values

# Breaking change (triggers MAJOR version)
feat(api)!: change response format to JSON:API

BREAKING CHANGE: All endpoints now return JSON:API format.
Migration guide: docs/migration-v2.md

# With scope
fix(ui/button): correct hover state color

# Multi-line body
feat(search): add full-text search

Implements Elasticsearch integration for product search.
Includes fuzzy matching and relevance scoring.

Closes #123
```

### Pattern 4: Scope Guidelines
```
Scope = module, component, or area affected

Good scopes:
- auth, cart, api, db
- ui/button, api/users
- deps, config, ci

No scope when change is broad:
- docs: update README
- chore: update dependencies
```

## Anti-Patterns

- **Vague messages** - "fix bug", "update code", "WIP"
- **Missing type** - Always prefix with type
- **Too long subject** - Keep under 72 chars
- **Multiple changes** - One logical change per commit

## Verification Checklist

- [ ] Type prefix present (feat/fix/docs/etc.)
- [ ] Subject is imperative ("add" not "added")
- [ ] Subject under 72 characters
- [ ] Breaking changes marked with `!` or footer
- [ ] One logical change per commit

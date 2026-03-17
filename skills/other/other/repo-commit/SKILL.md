---
name: repo:commit
description: Kagenti commit message format - emoji prefixes, sign-off, and conventions
---

# Kagenti Commit Conventions

## Format

```
<emoji> <Short descriptive message>

<Optional longer description>

Signed-off-by: <Name> <email>
Co-authored-by: Claude <noreply@anthropic.com>
```

## Emoji Prefixes

| Emoji | Type | When |
|-------|------|------|
| ✨ | Feature | New functionality |
| 🐛 | Bug fix | Fixing broken behavior |
| 📖 | Docs | Documentation only |
| 📝 | Proposal | Design proposals |
| ⚠️ | Breaking change | API or behavior changes |
| 🌱 | Other | Tests, CI, refactoring, tooling |

## Requirements

1. **Signed-off-by is MANDATORY** — always use `git commit -s`
2. **Co-authored-by Claude** — include when Claude creates the commit
3. **Imperative mood** — "Add feature" not "Added feature"
4. **Under 72 characters** — subject line
5. **No "Generated with Claude Code" line** — removed per team preference

## Examples

```
🌱 Add E2E testing infrastructure and deployment health tests

Implements initial end-to-end testing framework for Kagenti platform.

Signed-off-by: Developer <dev@example.com>
Co-authored-by: Claude <noreply@anthropic.com>
```

```
🐛 Fix VPC cleanup order: delete subnets before route tables

Signed-off-by: Developer <dev@example.com>
```

## Sign All Commits

After rebase or if commits are unsigned:

```bash
git rebase --signoff HEAD~$(git rev-list --count upstream/main..HEAD)
```

## Related Skills

- `git:commit` - Git commit mechanics
- `repo:pr` - PR creation conventions
- `tdd:ci` - TDD commit step

---
name: repo
description: Repository-specific conventions for commits, PRs, and issues
---

# Repository Conventions

Kagenti-specific conventions for commits, pull requests, and issues.

## Auto-Select Sub-Skill

```
What are you doing?
    │
    ├─ Making a commit → repo:commit
    ├─ Creating a PR → repo:pr
    └─ Filing an issue → repo:issue
```

## Available Skills

| Skill | Purpose |
|-------|---------|
| `repo:commit` | Commit message format, emoji prefixes, sign-off |
| `repo:pr` | PR template, summary format, issue linking |
| `repo:issue` | Issue templates (bug, feature, epic) |

## Related Skills

- `git:commit` - Git commit mechanics
- `git:rebase` - Rebase and sign-off
- `tdd:ci` - TDD workflow that produces commits and PRs

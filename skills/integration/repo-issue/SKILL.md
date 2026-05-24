---
name: repo:issue
description: Kagenti issue templates - bug reports, feature requests, epics
---

# Kagenti Issue Conventions

## Issue Templates

The repo has three issue templates in `.github/ISSUE_TEMPLATE/`:

| Template | When |
|----------|------|
| `bug_report.yaml` | Reporting a bug with reproduction steps |
| `feature_request.yaml` | Proposing new functionality |
| `epic.yaml` | Large multi-PR initiatives |

## Creating Issues

```bash
gh issue create --template bug_report.yaml
```

```bash
gh issue create --template feature_request.yaml
```

## Linking Issues to PRs

In the PR body:

```markdown
## Related issue(s)

Fixes #123
```

## Related Skills

- `repo:pr` - PR conventions (links issues)
- `repo:commit` - Commit conventions
- `ci:status` - Check CI status on issues

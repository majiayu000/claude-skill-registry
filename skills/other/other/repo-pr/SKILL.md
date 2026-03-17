---
name: repo:pr
description: Kagenti PR format - title, summary, issue linking
---

# Kagenti PR Conventions

## PR Title

```
<emoji> <Short descriptive title>
```

Same emoji prefixes as commits (see `repo:commit`).

## PR Body

```markdown
## Summary

<Clear description of what the PR does>

Key changes:
- <Bullet point 1>
- <Bullet point 2>

## Related issue(s)

Fixes #<number>
```

## Creating a PR

```bash
gh pr create --title "🌱 Add E2E tests" --body "$(cat <<'EOF'
## Summary

Description of changes.

Key changes:
- Point 1
- Point 2

## Related issue(s)

Fixes #309
EOF
)"
```

## Requirements

- **Summary section is REQUIRED**
- **Related issue(s) is OPTIONAL** — include if fixing an issue
- Use `Fixes #N` or `Closes #N` to auto-close issues
- Keep title under 72 characters

## Related Skills

- `repo:commit` - Commit format
- `git:rebase` - Rebase before PR
- `tdd:ci` - TDD workflow that creates PRs

---
name: git:commit
description: Create properly formatted commits following repository conventions
---

# Git Commit

Create commits following the repository's conventions. Links to repo-specific guidelines for format details.

## When to Use

- Every time you commit code
- After TDD fix iterations
- Before creating a PR

## Quick Commit

```bash
git add <files>
```

```bash
git commit -s -m "🌱 Short descriptive message"
```

The `-s` flag adds the required `Signed-off-by` line.

## Sign All Commits in Branch

If you have unsigned commits in your branch, sign them all:

```bash
git rebase --signoff HEAD~$(git rev-list --count upstream/main..HEAD)
```

## Commit Format

See `repo:commit` for the full repository-specific format. Quick reference:

| Emoji | Type |
|-------|------|
| ✨ | Feature |
| 🐛 | Bug fix |
| 📖 | Docs |
| 🌱 | Other (tests, CI, refactoring) |
| ⚠️ | Breaking change |

## Amending

```bash
git commit --amend -s --no-edit
```

## After Committing

Check the commit:

```bash
git log --oneline -1
```

Verify sign-off:

```bash
git log -1 --format='%B' | grep 'Signed-off-by'
```

## Related Skills

- `repo:commit` - Full commit format spec for this repo
- `repo:pr` - PR creation conventions
- `git:rebase` - Rebase before pushing
- `tdd:ci` - TDD workflow commit step

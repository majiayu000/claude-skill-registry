---
name: managing-git
description: Guides git workflows, branching strategies, commit conventions, and version control best practices. Use when managing repositories, creating branches, or handling merges.
license: MIT
compatibility: opencode
metadata:
  category: workflow
  audience: developers
---

# Managing Git

Best practices for version control, branching strategies, and collaborative development.

## When to Use This Skill

- Setting up branching strategies
- Writing commit messages
- Handling merges and conflicts
- Managing releases
- Code review workflows
- Maintaining clean history

---

## Branching Strategies

### Git Flow

```
main ─────●─────────────────────●─────────────────●────▶
           \                   /                 /
release     \───────●─────────●                 /
              \                                /
develop ───────●───────●───────●──────●───────●────────▶
                \       \       \      \
feature          \───────●───────●      \───●───●
                          \              \
hotfix                     \              \───●────▶ main
```

| Branch | Purpose | Branches From | Merges Into |
|--------|---------|---------------|-------------|
| `main` | Production code | - | - |
| `develop` | Integration | main | release |
| `feature/*` | New features | develop | develop |
| `release/*` | Release prep | develop | main, develop |
| `hotfix/*` | Production fixes | main | main, develop |

**Use when**: Scheduled releases, multiple versions supported

### GitHub Flow

```
main ─────●─────●─────●─────●─────●────▶
           \   /       \   /       \   /
feature     ●─●         ●─●         ●─●
            PR          PR          PR
```

| Branch | Purpose |
|--------|---------|
| `main` | Always deployable |
| `feature/*` | All changes (features, fixes) |

**Use when**: Continuous deployment, simple workflow

### Trunk-Based Development

```
main ─────●──●──●──●──●──●──●──●──●──●────▶
           │  │  │  │  │  │  │  │  │  │
          ●   ●  ●  ●  ●  ●  ●  ●  ●  ●
          Small, frequent commits (often direct to main)
```

**Use when**: High trust teams, strong CI/CD, frequent deploys

---

## Commit Message Conventions

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation | `docs(readme): update setup steps` |
| `style` | Formatting | `style: fix indentation` |
| `refactor` | Code restructuring | `refactor(db): simplify query builder` |
| `test` | Adding tests | `test(user): add registration tests` |
| `chore` | Maintenance | `chore(deps): update lodash` |
| `perf` | Performance | `perf(search): add index on email` |
| `ci` | CI/CD changes | `ci: add Node 18 to matrix` |

### Good vs Bad Commits

```
BAD:
  - "fix"
  - "update code"
  - "WIP"
  - "changes"
  - "asdfasdf"

GOOD:
  - "fix(auth): prevent session timeout on idle"
  - "feat(cart): add quantity validation"
  - "refactor(api): extract common error handling"
```

### Commit Body Guidelines

```
fix(payment): prevent double charge on retry

The payment gateway timeout was causing the retry logic to submit
duplicate charges. Added idempotency key to prevent double-processing.

Closes #1234
```

- First line: 50 chars max, imperative mood
- Body: Wrap at 72 chars, explain why, not what
- Footer: Reference issues, breaking changes

---

## Branch Naming Conventions

### Pattern

```
<type>/<ticket>-<short-description>
```

### Examples

| Type | Example |
|------|---------|
| Feature | `feature/AUTH-123-add-oauth-login` |
| Bugfix | `fix/CART-456-quantity-validation` |
| Hotfix | `hotfix/PROD-789-memory-leak` |
| Chore | `chore/update-dependencies` |
| Docs | `docs/api-documentation` |

### Branch Rules

1. Lowercase with hyphens
2. Include ticket number when available
3. Keep short but descriptive
4. Delete after merge

---

## Git Workflow Commands

### Daily Workflow

```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/AUTH-123-add-login

# Work on feature
git add -p                    # Stage hunks interactively
git commit -m "feat(auth): add login form"

# Keep up to date
git fetch origin
git rebase origin/main        # Preferred: clean history
# OR
git merge origin/main         # Alternative: preserves context

# Push and create PR
git push -u origin feature/AUTH-123-add-login
```

### Useful Commands

| Command | Purpose |
|---------|---------|
| `git stash` | Save uncommitted changes temporarily |
| `git stash pop` | Restore stashed changes |
| `git commit --amend` | Modify last commit |
| `git rebase -i HEAD~3` | Interactive rebase (squash, reorder) |
| `git cherry-pick <sha>` | Apply specific commit |
| `git bisect` | Binary search for bug introduction |
| `git reflog` | View all HEAD movements (recovery) |

### Cleanup Commands

```bash
# Delete merged branches locally
git branch --merged | grep -v main | xargs git branch -d

# Prune remote tracking branches
git fetch --prune

# Clean untracked files (careful!)
git clean -fd
```

---

## Handling Conflicts

### Conflict Resolution Flow

```
1. Identify conflicts
   git status

2. Open conflicted files
   <<<<<<< HEAD
   your changes
   =======
   their changes
   >>>>>>> feature-branch

3. Resolve (keep one, combine, or rewrite)

4. Mark resolved
   git add <resolved-file>

5. Continue
   git rebase --continue   # if rebasing
   git commit              # if merging
```

### Prevention Strategies

1. **Small, frequent merges** - Reduce conflict scope
2. **Communication** - Coordinate on shared files
3. **Feature flags** - Reduce long-lived branches
4. **Clear ownership** - Minimize overlapping work

---

## Pull Request Best Practices

### PR Checklist

- [ ] Branch is up to date with main
- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Ticket/issue linked
- [ ] Screenshots for UI changes

### PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| Small | 1-100 | 15 min | Ideal |
| Medium | 100-400 | 30-60 min | Acceptable |
| Large | 400+ | 1+ hour | Split if possible |

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Added X
- Modified Y
- Removed Z

## Testing
- [ ] Unit tests added
- [ ] Manual testing done

## Screenshots (if applicable)
[Before/After images]

## Related Issues
Closes #123
```

---

## Release Management

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Bug fixes (backward compatible)
  │     └── New features (backward compatible)
  └── Breaking changes
```

### Release Process

```bash
# Create release branch
git checkout -b release/v1.2.0 develop

# Bump version, update changelog
# ... make changes ...

# Merge to main and tag
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge release/v1.2.0
```

### Changelog Format

```markdown
# Changelog

## [1.2.0] - 2024-01-15
### Added
- OAuth2 authentication support

### Changed
- Improved error messages

### Fixed
- Memory leak in cache handler

### Deprecated
- Old authentication method (use OAuth2)

### Removed
- Legacy API v1 endpoints
```

---

## Git Hooks

### Common Hooks

| Hook | Timing | Use Case |
|------|--------|----------|
| `pre-commit` | Before commit | Linting, formatting |
| `commit-msg` | After message | Validate message format |
| `pre-push` | Before push | Run tests |
| `post-merge` | After merge | Install dependencies |

### Example pre-commit

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "Linting failed. Please fix errors."
  exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed. Please fix before committing."
  exit 1
fi
```

### Using Husky (Node.js)

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  }
}
```

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Accidental commit to main | `git reset HEAD~1` (before push) |
| Wrong branch | `git stash`, switch, `git stash pop` |
| Need to undo merge | `git revert -m 1 <merge-commit>` |
| Lost commits | `git reflog` to find, `git cherry-pick` |
| Large file committed | `git filter-branch` or BFG Repo-Cleaner |

### Recovery Commands

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Recover deleted branch
git reflog
git checkout -b recovered-branch <sha>

# Undo a pushed commit (safe)
git revert <sha>
```

---

## Anti-Patterns to Avoid

1. **Force pushing to shared branches** - Breaks others' history
2. **Giant commits** - Hard to review, hard to bisect
3. **Vague commit messages** - "fix" tells nothing
4. **Long-lived branches** - Merge conflict hell
5. **Committing generated files** - Bloats repo, causes conflicts
6. **Committing secrets** - Security risk (even after removal)
7. **Rebasing public history** - Breaks collaborators
8. **Ignoring CI failures** - Broken windows effect

---

## Quick Reference

```
BRANCHES:
  main       → Production (protected)
  develop    → Integration (Git Flow)
  feature/*  → New work
  fix/*      → Bug fixes
  hotfix/*   → Production emergencies

COMMITS:
  feat(scope): add feature
  fix(scope): fix bug
  docs(scope): update docs
  refactor(scope): restructure code

DAILY FLOW:
  git checkout -b feature/ticket-desc
  git add -p && git commit
  git rebase origin/main
  git push -u origin feature/ticket-desc

VERSIONING:
  MAJOR.MINOR.PATCH
  Breaking.Feature.Bugfix
```

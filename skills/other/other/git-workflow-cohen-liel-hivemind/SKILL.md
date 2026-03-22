---
name: git-workflow
description: Git workflow best practices. Use when committing code, managing branches, writing commit messages, or setting up git workflows.
---

# Git Workflow Patterns

## Commit Message Format (Conventional Commits)
```
<type>(<scope>): <short summary>

[optional body: WHY this change was made]

[optional footer: BREAKING CHANGE, closes #issue]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that doesn't add features or fix bugs
- `test`: Adding or updating tests
- `docs`: Documentation only
- `chore`: Build, deps, config changes
- `perf`: Performance improvement
- `ci`: CI/CD changes

Examples:
```
feat(auth): add JWT refresh token rotation

Implement sliding refresh tokens to improve security.
Old refresh tokens are invalidated immediately on use.

Closes #123

---

fix(api): return 404 when user not found instead of 500

The get_user endpoint was crashing when user_id didn't exist
because db.get() returns None and we were accessing None.email.

---

refactor(models): extract TimestampMixin from all models

All models had duplicate created_at/updated_at columns.
Extracted to reusable mixin to DRY the code.
```

## Branch Strategy (GitHub Flow — simple)
```
main              # Always deployable
feature/          # New features
fix/              # Bug fixes
chore/            # Maintenance

# Never commit directly to main
# Every change = branch → PR → review → merge
```

## Commands
```bash
# Start new feature
git checkout -b feat/user-authentication

# Stage only relevant files (never git add .)
git add src/auth.py src/models/user.py tests/test_auth.py

# Amend last commit (before push)
git commit --amend --no-edit

# Interactive rebase to clean up commits
git rebase -i HEAD~3

# Squash all feature commits before merge
git merge --squash feat/user-authentication

# Undo last commit but keep changes
git reset --soft HEAD~1

# See what changed in last commit
git diff HEAD~1 HEAD --stat

# Find when a bug was introduced
git bisect start
git bisect bad           # current commit has bug
git bisect good v1.0.0   # known good commit
```

## .gitignore (Python project)
```
__pycache__/
*.pyc
.env
.env.local
*.egg-info/
dist/
build/
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
*.log
.DS_Store
```

## Pre-commit Hooks (.pre-commit-config.yaml)
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
```

## Rules
- Commit early and often — small, focused commits
- Each commit should leave the codebase in a working state
- Write commit messages in imperative: "Add auth" not "Added auth"
- Never commit: .env, secrets, API keys, large binaries, generated files
- Pull before push (git pull --rebase to avoid merge commits)
- Review your own diff before committing: `git diff --staged`
- Tag releases: `git tag -a v1.0.0 -m "First stable release"`

---
name: git
description: Git workflow and commit standards for SignalRoom. Use when committing changes, creating PRs, or managing branches. Ensures consistent commit messages and safe git operations.
---

# Git Workflow

## Branch Strategy

```
main (production)
  │
  └── feature/* or fix/* (development)
```

- `main` is production, always deployable
- Feature branches for development
- Merge to main via PR or direct push (small changes)

## Commit Message Format

```
<type>: <short summary>

<optional body with details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that doesn't fix bug or add feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, config |

### Examples

```
feat: Add Redtrack daily spend source

fix: Correct Supabase pooler port to 6543

docs: Update ROADMAP with Phase 4 completion

refactor: Extract retry policy to temporal/config.py

chore: Update dlt to 0.4.0
```

## Safe Git Commands

### Before Committing

```bash
# See what changed
git status
git diff

# Stage specific files
git add path/to/file.py

# Stage all changes
git add -A
```

### Committing

```bash
# Commit with message
git commit -m "feat: Add new source"

# Commit with multi-line message (use heredoc)
git commit -m "$(cat <<'EOF'
feat: Add Redtrack source

- Implements daily_spend resource
- Uses merge disposition with date+source_id key
- Adds to pipeline runner registry

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Pushing

```bash
# Push to origin
git push origin main

# Push new branch
git push -u origin feature/my-feature
```

## Dangerous Commands (Avoid)

| Command | Risk | Alternative |
|---------|------|-------------|
| `git push --force` | Destroys remote history | `git push` (fix conflicts first) |
| `git reset --hard` | Loses uncommitted work | `git stash` then `git reset` |
| `git rebase -i` | Rewrites history | Only on unpushed commits |
| `git commit --amend` | Rewrites last commit | Only if not pushed |

## Pull Request Template

```markdown
## Summary
- Brief description of changes

## Changes
- Specific change 1
- Specific change 2

## Test Plan
- [ ] Tested locally with `python scripts/run_pipeline.py`
- [ ] Verified no type errors with `make typecheck`
- [ ] Ran `make ci` successfully

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Pre-Commit Checklist

Before any commit:

```bash
# 1. Check what you're committing
git diff --staged

# 2. Run linter
make lint

# 3. Run type checker
make typecheck

# 4. Run tests (if applicable)
make test
```

## Common Scenarios

### Undo Last Commit (Not Pushed)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes entirely
git reset --hard HEAD~1
```

### Discard Local Changes

```bash
# Discard changes to specific file
git checkout -- path/to/file.py

# Discard all local changes
git checkout -- .
```

### See What Changed Recently

```bash
# Recent commits
git log --oneline -10

# Changes in last commit
git show --stat

# Diff between commits
git diff abc123..def456
```

### Stash Work in Progress

```bash
# Save current changes
git stash

# List stashes
git stash list

# Restore stashed changes
git stash pop
```

## Files to Never Commit

Already in `.gitignore`:
- `.env` — secrets
- `*.pem`, `*.key` — certificates
- `.dlt/secrets.toml` — dlt credentials
- `credentials.json` — service accounts

If accidentally staged:
```bash
git reset HEAD path/to/secret/file
```

## Commit Hygiene

### Good Commits

- One logical change per commit
- Descriptive message explaining WHY
- Tests pass before commit
- No debug code or print statements

### Bad Commits

- "WIP" or "fix" with no context
- Multiple unrelated changes
- Broken tests
- Secrets or credentials

---
name: tzurot-git-workflow
description: Git workflow rules for Tzurot v3. Use when committing, creating PRs, or rebasing. Covers rebase-only strategy, commit format, and safety checks.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Git Workflow

**Use this skill when:** Creating commits, pushing changes, creating PRs, or performing any git operations.

## Quick Reference

```bash
# Start feature
git checkout develop && git pull origin develop
git checkout -b feat/your-feature

# Test before commit
pnpm test

# Create PR to develop
gh pr create --base develop --title "feat: description"
```

## 🚨 Critical Rules

### Never Merge Without User Approval

**NEVER merge a PR without explicit user approval.** This is non-negotiable.

- ✅ CI passing is necessary but NOT sufficient for merging
- ✅ User must explicitly approve/request the merge
- ❌ NEVER merge just because "CI is green"
- ❌ NEVER merge to "complete the task"

```bash
# Only merge with explicit user approval
gh pr merge <number> --rebase --delete-branch
```

### Rebase-Only Workflow

**NO SQUASH. NO MERGE COMMITS. ONLY REBASE.**

GitHub settings enforce this - rebase and merge is the only option enabled. Merge commits and squash merges are disabled at the repository level.

### Always Target `develop` for PRs

```bash
# ✅ CORRECT
gh pr create --base develop --title "feat: your feature"

# ❌ WRONG - Never create feature PRs to main!
gh pr create --base main --title "feat: your feature"
```

### Test Before Push

```bash
pnpm test && git push origin <branch>
```

## Standard Workflow

### 1. Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feat/your-feature-name
```

**Branch prefixes:** `feat/`, `fix/`, `docs/`, `refactor/`, `chore/`, `test/`

### 2. Commit Changes

```bash
git commit -m "$(cat <<'EOF'
feat(ai-worker): add pgvector memory retrieval

Brief description of what and why.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`
**Scopes:** `ai-worker`, `api-gateway`, `bot-client`, `common-types`, `ci`, `deps`

### 3. Push and Create PR

```bash
git push -u origin feat/your-feature
gh pr create --base develop --title "feat: description"
```

### 4. After PR Merged

```bash
git checkout develop
git pull origin develop
git branch -d feat/your-feature
```

## Git Safety Protocol

### 🚨 NEVER Run Without Explicit User Permission:

**These commands destroy work. ALWAYS ask before running:**

| Command            | Risk                       | Ask First? |
| ------------------ | -------------------------- | ---------- |
| `git restore`      | Discards uncommitted work  | **YES**    |
| `git checkout .`   | Discards all changes       | **YES**    |
| `git reset --hard` | Undoes commits permanently | **YES**    |
| `git clean -fd`    | Deletes untracked files    | **YES**    |
| `git push --force` | Rewrites history           | **YES**    |
| `git stash drop`   | Permanently removes stash  | **YES**    |

### Golden Rules

1. **Uncommitted changes = HOURS OF WORK** - Never discard without confirmation
2. **Use safe alternatives:** `--force-with-lease`, `git branch -d` (not -D)
3. **When user says "get changes"** → They mean COMMIT, not DISCARD
4. **NEVER unilaterally abandon agreed-upon work** - Ask before changing scope
5. **When work is complex** - Explain and ask, don't skip silently

## Git Hooks (Husky)

**Managed by Husky** - auto-installed on `pnpm install`.

| Hook       | Tools                   | What                          | Speed   |
| ---------- | ----------------------- | ----------------------------- | ------- |
| pre-commit | lint-staged, secretlint | Format staged files + secrets | ~3s     |
| commit-msg | commitlint              | Validate conventional commits | instant |
| pre-push   | Turborepo               | Cached build/lint/test        | varies  |

**Configuration:**

- `.husky/` - Hook scripts
- `.lintstagedrc.json` - Staged file linting
- `commitlint.config.cjs` - Commit message rules

**Skip for docs-only changes:** Pre-push auto-skips tests when only `.md`, `.json`, etc. files changed.

**Never skip:** Don't use `--no-verify`

## Handling Rebase Conflicts

```bash
git checkout develop && git pull origin develop
git checkout feat/your-feature
git rebase develop

# If conflicts:
# 1. Resolve files
# 2. git add <resolved>
# 3. git rebase --continue
# Repeat until done

git push --force-with-lease origin feat/your-feature
```

## Release Workflow

### Option 1: Changesets (Recommended)

```bash
# During development: add changeset describing your changes
pnpm changeset

# Before release: check pending changesets
pnpm changeset:status

# Apply changesets and bump versions
pnpm changeset:version

# Review and commit
git add . && git commit -m "chore: version packages"
git push origin develop
```

### Option 2: Manual Version Bump

```bash
# Use the bump-version script - handles all package.json files
pnpm bump-version 3.0.0-beta.31

# Review and commit
git diff
git commit -am "chore: bump version to 3.0.0-beta.31"
git push origin develop
```

### Create Release PR

```bash
gh pr create --base main --head develop \
  --title "Release v3.0.0-beta.31: Description"
```

### After Release: Sync Develop with Main

After merging release PR to main:

```bash
# Fetch and update local branches
git fetch --all
git checkout main && git pull origin main
git checkout develop && git pull origin develop

# Rebase develop onto main
git rebase origin/main

# Push (force needed after rebase)
git push origin develop --force-with-lease
```

**Why this is needed:** After a release PR merges to main, develop needs to be rebased onto main to incorporate any merge commit and keep history clean.

## Anti-Patterns

| ❌ Don't                      | ✅ Do                            |
| ----------------------------- | -------------------------------- |
| PRs to main (except releases) | PRs to develop                   |
| Push without testing          | `pnpm test && git push`          |
| Vague commits ("fix stuff")   | Descriptive commits              |
| Skip hooks (`--no-verify`)    | Fix the issues                   |
| Force push to main/develop    | Only force-push feature branches |

## Related Skills

- **tzurot-code-quality** - When lint fails, refactoring patterns
- **tzurot-docs** - Session handoff and CURRENT_WORK.md
- **tzurot-testing** - Run tests before committing
- **tzurot-security** - Pre-commit security checks

## GitHub CLI Commands

### 🚨 Use `ops gh:*` Commands (Not `gh pr edit`)

The `gh pr edit` command is **BROKEN** due to GitHub's "Projects (classic) deprecation" GraphQL error. **ALWAYS use the `ops gh:*` commands instead:**

```bash
# ✅ PREFERRED - Use ops commands
pnpm ops gh:pr-info 478        # Get PR title, body, state
pnpm ops gh:pr-reviews 478     # Get all reviews
pnpm ops gh:pr-comments 478    # Get line-level review comments
pnpm ops gh:pr-conversation 478 # Get conversation comments
pnpm ops gh:pr-edit 478 --title "New title"  # Edit PR
pnpm ops gh:pr-edit 478 --body "New body"
pnpm ops gh:pr-edit 478 --body-file pr.md    # Body from file
pnpm ops gh:pr-all 478         # Get everything

# ❌ BROKEN - Do NOT use
gh pr edit 478 --title "..."   # GraphQL error!
```

### Comment Types

PRs have THREE different comment types with different endpoints:

- **Issue comments** (general): `ops gh:pr-conversation` or `/issues/{pr}/comments`
- **Review comments** (line-specific): `ops gh:pr-comments` or `/pulls/{pr}/comments`
- **Reviews** (APPROVE, etc.): `ops gh:pr-reviews`

## References

- **GitHub CLI Reference**: `docs/reference/GITHUB_CLI_REFERENCE.md` ← **CHECK THIS FIRST!**
- Full workflow: `CLAUDE.md#git-workflow`
- Post-mortems: `docs/postmortems/PROJECT_POSTMORTEMS.md`

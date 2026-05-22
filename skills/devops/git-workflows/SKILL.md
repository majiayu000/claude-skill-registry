---
name: git-workflows
description: Guide for git operations with Claude Code. Commits, PRs, code review, branch management, and best practices. Use when committing changes, creating pull requests, reviewing code, or managing branches.
allowed-tools: ["Read", "Bash"]
---

# Git Workflows

Master git operations with Claude Code. This skill covers commits, pull requests, code review, branch management, and best practices.

## Quick Reference

| Operation | Command | Notes |
|-----------|---------|-------|
| Check status | `git status` | Always run before committing |
| Stage files | `git add <files>` | Never use `-i` (interactive) |
| Commit | `git commit -m "$(cat <<'EOF'...EOF)"` | Use heredoc for messages |
| Create PR | `gh pr create --title "..." --body "..."` | Use gh CLI, not git |
| View PR | `gh pr view <number>` | Get PR details |
| Push | `git push -u origin <branch>` | Use `-u` for new branches |

## Claude's Git Safety Rules

Claude Code follows strict safety protocols for git operations:

### Never Do
- Force push to main/master
- Run `git rebase -i` or `git add -i` (interactive mode unsupported)
- Skip hooks with `--no-verify`
- Update git config
- Commit without explicit user request
- Amend commits that have been pushed

### Always Do
- Check `git status` before committing
- Verify changes with `git diff`
- Use heredoc for multi-line commit messages
- Include co-author attribution when appropriate
- Verify branch is ahead before amending

## Commit Message Format

Claude uses conventional commits with heredoc syntax:

```bash
git commit -m "$(cat <<'EOF'
type(scope): short description

Longer explanation of changes if needed.
Multiple paragraphs allowed.

Co-authored-by: Name <email@example.com>
EOF
)"
```

### Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test` | Adding/fixing tests |
| `chore` | Maintenance tasks |

### Scope Examples

- `feat(auth)`: Authentication feature
- `fix(api)`: API bug fix
- `docs(readme)`: README update
- `refactor(utils)`: Utility refactoring

## Standard Commit Workflow

When asked to commit, Claude follows this sequence:

### 1. Gather Information (Parallel)

```bash
# Run these in parallel
git status                           # See untracked files
git diff --staged                    # See staged changes
git diff                             # See unstaged changes
git log --oneline -5                 # Recent commit style
```

### 2. Analyze Changes

- Determine commit type (feat, fix, docs, etc.)
- Identify scope from affected files
- Focus on "why" not "what"
- Check for sensitive files (.env, credentials)

### 3. Create Commit

```bash
# Stage relevant files
git add <files>

# Commit with heredoc
git commit -m "$(cat <<'EOF'
type(scope): descriptive message

Why this change was made.
EOF
)"

# Verify success
git status
```

## Pull Request Workflow

### Creating a PR

```bash
# 1. Gather context (parallel)
git status
git diff main...HEAD
git log main..HEAD --oneline

# 2. Push if needed
git push -u origin $(git branch --show-current)

# 3. Create PR with heredoc
gh pr create --title "feat: add user authentication" --body "$(cat <<'EOF'
## Summary
- Add login/logout functionality
- Implement JWT token handling
- Add protected route middleware

## Test plan
- [ ] Manual login flow test
- [ ] Verify token expiration
- [ ] Test protected routes
EOF
)"
```

### PR Description Template

```markdown
## Summary
- Key change 1
- Key change 2
- Key change 3

## Test plan
- [ ] Test case 1
- [ ] Test case 2

## Notes
Any additional context for reviewers.
```

## Amend Rules (Critical)

Claude only amends when ALL conditions are met:

1. User explicitly requested amend, OR commit succeeded but pre-commit hook auto-modified files
2. HEAD commit was created by Claude in current conversation (verify with `git log -1 --format='%an %ae'`)
3. Commit has NOT been pushed to remote (verify `git status` shows "Your branch is ahead")

### When Commit Fails

If a commit fails or is rejected by a hook:
- NEVER amend
- Fix the issue
- Create a NEW commit

### Safe Amend Pattern

```bash
# Verify conditions first
git log -1 --format='%an %ae'    # Check author
git status                        # Check not pushed

# Only then amend
git add <modified-files>
git commit --amend --no-edit
```

## Branch Management

### Feature Branch Workflow

```bash
# Create feature branch
git checkout -b feature/user-auth

# Work on feature...
# Commit changes...

# Push branch
git push -u origin feature/user-auth

# Create PR
gh pr create --title "..." --body "..."
```

### Branch Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `feature/<name>` | `feature/user-auth` | New features |
| `fix/<name>` | `fix/login-bug` | Bug fixes |
| `hotfix/<name>` | `hotfix/security-patch` | Production fixes |
| `chore/<name>` | `chore/update-deps` | Maintenance |
| `docs/<name>` | `docs/api-guide` | Documentation |

## Code Review Patterns

### Viewing PR Changes

```bash
# View PR details
gh pr view 123

# View PR diff
gh pr diff 123

# View PR comments
gh api repos/owner/repo/pulls/123/comments

# Check PR status
gh pr checks 123
```

### Addressing Review Feedback

```bash
# Make requested changes
# ... edit files ...

# Commit fixes
git add <files>
git commit -m "$(cat <<'EOF'
fix: address review feedback

- Fix issue mentioned in review
- Add missing validation
EOF
)"

# Push updates
git push
```

## GitHub CLI (gh) Commands

Claude uses `gh` CLI for all GitHub operations:

| Operation | Command |
|-----------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| View PR | `gh pr view <number>` |
| List PRs | `gh pr list` |
| Check PR status | `gh pr checks <number>` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "..." --body "..."` |
| View comments | `gh api repos/o/r/pulls/N/comments` |

## Conflict Resolution

When merge conflicts occur:

```bash
# 1. Fetch latest
git fetch origin main

# 2. Merge or rebase
git merge origin/main
# OR
git rebase origin/main

# 3. Resolve conflicts
# Edit conflicting files...
# Remove conflict markers (<<<<, ====, >>>>)

# 4. Complete merge
git add <resolved-files>
git commit -m "Merge main into feature branch"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Detached HEAD | `git checkout <branch>` |
| Wrong branch | `git stash && git checkout correct-branch && git stash pop` |
| Committed to wrong branch | `git reset HEAD~1 --soft && git stash && git checkout correct && git stash pop` |
| Need to undo last commit | `git reset HEAD~1 --soft` (keeps changes) |
| Forgot to add file | Stage file, then amend (if safe) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GIT_AUTHOR_NAME` | Commit author name |
| `GIT_AUTHOR_EMAIL` | Commit author email |
| `GIT_COMMITTER_NAME` | Committer name |
| `GIT_COMMITTER_EMAIL` | Committer email |

## Reference Files

| File | Contents |
|------|----------|
| [COMMITS.md](./COMMITS.md) | Detailed commit workflows and conventions |
| [PULL-REQUESTS.md](./PULL-REQUESTS.md) | PR creation, review, and merge workflows |
| [PATTERNS.md](./PATTERNS.md) | Branch strategies, hotfixes, and advanced patterns |

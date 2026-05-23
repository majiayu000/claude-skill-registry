---
name: git-workflow
description: Git worktree workflow, conventional commits, commit trailers, and PR guidelines. Activated during git operations and commits.
allowed-tools: ['Bash', 'Read']
---

# Git Workflow Expert

This skill provides guidance on Git worktree workflow, commit standards, and PR best practices.

## 🌳 Git Worktree Workflow

### Why Git Worktree?

Git worktree allows working on multiple branches simultaneously without stashing or switching contexts. Each worktree is an independent working directory with its own branch.

**Benefits**:
- No context switching between branches
- No stashing required
- Parallel development on different features
- Independent builds and tests per branch

### Setting Up Worktrees

```bash
# Create worktree for feature development
git worktree add ../project-feature-auth feature/user-authentication

# Create worktree for bug fixes
git worktree add ../project-bugfix-api hotfix/api-validation

# Create worktree for experiments
git worktree add ../project-experiment-new-ui experiment/react-19-upgrade
```

### Worktree Naming Convention

```
../project-<type>-<description>
```

**Types**:
- `feature` - New feature development
- `bugfix` - Bug fixes
- `hotfix` - Urgent production fixes
- `experiment` - Experimental changes
- `refactor` - Code refactoring

**Examples**:
- `../myapp-feature-user-auth`
- `../myapp-bugfix-login-error`
- `../myapp-hotfix-security-patch`

### Managing Worktrees

```bash
# List all worktrees
git worktree list

# Show details in long format
git worktree list --porcelain

# Remove worktree after merging
git worktree remove ../project-feature-auth

# Remove worktree (force if dirty)
git worktree remove --force ../project-experiment

# Prune stale worktree information
git worktree prune
```

### Worktree Best Practices

1. **Clean up after merging** - Remove worktrees after feature completion
2. **Use descriptive names** - Follow naming convention
3. **Keep main worktree clean** - Use for stable work only
4. **Regular pruning** - Run `git worktree prune` periodically

## 🔧 Commit Standards

### Conventional Commits

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Commit Types

```bash
# New feature
git commit -m "feat(auth): add JWT token refresh mechanism"

# Bug fix
git commit -m "fix(api): handle null response appropriately"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Performance improvement
git commit -m "perf(db): optimize query performance"

# Code refactoring
git commit -m "refactor(core): extract validation logic"

# Testing
git commit -m "test(auth): add unit tests for login flow"

# Build/tooling
git commit -m "build(deps): upgrade react to v18"

# CI/CD
git commit -m "ci(github): add automated deployment workflow"

# Chores
git commit -m "chore(deps): update development dependencies"

# Style changes (formatting, etc.)
git commit -m "style(components): format with prettier"
```

### Commit Type Reference

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | Adding user authentication |
| `fix` | Bug fix | Fixing null pointer error |
| `docs` | Documentation only | Update README |
| `style` | Formatting changes | Code formatting, no logic change |
| `refactor` | Code refactoring | Restructure without behavior change |
| `perf` | Performance improvement | Optimize algorithm |
| `test` | Adding/updating tests | Add unit tests |
| `build` | Build system changes | Update webpack config |
| `ci` | CI/CD changes | Update GitHub Actions |
| `chore` | Maintenance tasks | Update dependencies |
| `revert` | Revert previous commit | Revert "feat: add feature" |

### Commit Message Guidelines

**Subject line**:
- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

**Body**:
- Wrap at 72 characters
- Explain what and why, not how
- Use bullet points for multiple changes

**Example**:
```bash
git commit -m "$(cat <<'EOF'
feat(api): add user profile endpoint

- Add GET /api/users/:id endpoint
- Include avatar URL in response
- Add rate limiting (100 req/min)

This allows frontend to fetch user details
without additional API calls.

Closes #123
EOF
)"
```

### Commit Trailers

Add metadata to commits using trailers:

```bash
# Reference GitHub issue
git commit --trailer "Github-Issue: #123"

# Credit bug reporter
git commit --trailer "Reported-by: John Doe <john@example.com>"

# Reference related commits
git commit --trailer "See-also: abc123"

# Co-author
git commit --trailer "Co-authored-by: Jane Smith <jane@example.com>"
```

**Example with multiple trailers**:
```bash
git commit -m "$(cat <<'EOF'
fix(auth): resolve token expiration issue

Fixed bug where expired tokens weren't properly
refreshed, causing users to be logged out unexpectedly.

Github-Issue: #456
Reported-by: John Doe <john@example.com>
Reviewed-by: Jane Smith <jane@example.com>
EOF
)"
```

## 📝 Pull Request Guidelines

### PR Title

Follow the same format as commit messages:

```
<type>(<scope>): <description>
```

**Examples**:
- `feat(auth): add OAuth2 authentication`
- `fix(api): resolve race condition in data sync`
- `docs(contributing): update contributor guidelines`

### PR Description Template

```markdown
## Summary
Brief description of changes (1-3 sentences)

## Changes
- Bullet point list of main changes
- Focus on what and why, not implementation details
- Keep it high-level

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed
- [ ] Edge cases covered

## Breaking Changes
List any breaking changes (if applicable)

## Related Issues
Closes #123
Related to #456

## Screenshots/Videos
(if applicable)
```

### PR Best Practices

1. **Keep PRs small** - Easier to review, faster to merge
2. **One feature per PR** - Don't mix unrelated changes
3. **Update documentation** - Keep docs in sync with code
4. **Add tests** - Don't merge without test coverage
5. **Respond to reviews** - Address feedback promptly
6. **Squash commits** - Clean up commit history before merge
7. **Delete branch** - Clean up after merge

### PR Review Checklist

**Before requesting review**:
- [ ] All tests pass
- [ ] Code is formatted (linter passes)
- [ ] Documentation updated
- [ ] No console.log or debug code
- [ ] Type safety verified (TypeScript)
- [ ] Breaking changes documented

**For reviewers**:
- [ ] Code follows project conventions
- [ ] Logic is clear and maintainable
- [ ] Edge cases are handled
- [ ] Tests are adequate
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed

## 🎯 Git Workflow Checklist

Daily workflow checklist:

- [ ] Pull latest changes: `git pull`
- [ ] Create feature branch or worktree
- [ ] Make atomic commits with conventional format
- [ ] Write meaningful commit messages
- [ ] Push regularly: `git push`
- [ ] Create PR with proper description
- [ ] Address review feedback
- [ ] Squash commits if needed
- [ ] Merge and delete branch/worktree

## 💡 Advanced Git Tips

### Interactive Rebase

```bash
# Clean up last 3 commits
git rebase -i HEAD~3

# Rebase onto main
git rebase -i main
```

### Cherry-pick Commits

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick without committing
git cherry-pick --no-commit abc123
```

### Stash Management

```bash
# Stash with message
git stash push -m "WIP: feature in progress"

# List stashes
git stash list

# Apply and drop stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

### Bisect for Bug Hunting

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good abc123

# Let git find the culprit
# Test each commit and mark good/bad
git bisect good  # or bad

# End bisect
git bisect reset
```

## 🚫 Common Mistakes to Avoid

❌ **Don't**:
- Commit directly to main/master
- Use vague commit messages ("fix bug", "update")
- Mix unrelated changes in one commit
- Forget to pull before pushing
- Leave WIP commits in PR
- Skip commit message body for complex changes

✅ **Do**:
- Use feature branches or worktrees
- Write descriptive conventional commits
- Make atomic commits (one logical change)
- Pull regularly and before pushing
- Squash/reword commits before merging
- Provide context in commit body

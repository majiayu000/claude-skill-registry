---
name: git-workflow
description: 自动化Git操作，智能生成遵循Conventional Commits的提交信息、分支管理和PR描述生成。
metadata:
  short-description: 智能Git操作和提交信息
---

# Git Workflow Skill

## Description
Automate Git operations with intelligent commit messages, branch management, and PR descriptions.

## Trigger
- `/commit` command
- `/branch` command
- `/pr` command
- User requests Git assistance

## Prompt

You are a Git workflow expert that helps with version control operations.

### Commit Message Generation

Follow Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

#### Examples

```bash
# Feature
feat(auth): add OAuth2 login with Google provider

- Implement GoogleAuthProvider class
- Add callback endpoint /auth/google/callback
- Store refresh tokens securely

Closes #123

# Bug fix
fix(api): handle null response in user service

The getUserById method was throwing when user not found.
Now returns null and lets caller handle the case.

Fixes #456

# Breaking change
feat(api)!: change response format for pagination

BREAKING CHANGE: Pagination now uses cursor-based format.
Old: { page, limit, total }
New: { cursor, hasMore, items }
```

### Branch Naming

```bash
# Feature branches
feature/user-authentication
feature/JIRA-123-add-payment-gateway

# Bug fix branches
fix/login-redirect-loop
fix/JIRA-456-null-pointer-exception

# Hotfix branches
hotfix/security-patch-xss

# Release branches
release/v1.2.0
```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Added UserAuthService with JWT support
- Created login/register API endpoints
- Added password hashing with bcrypt

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
[Add screenshots here]

## Related Issues
Closes #123
Related to #456
```

### Git Commands Helper

```bash
# Interactive rebase last 3 commits
git rebase -i HEAD~3

# Squash commits
git rebase -i HEAD~N  # then change 'pick' to 'squash'

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Cherry-pick specific commit
git cherry-pick <commit-hash>

# Stash with message
git stash push -m "WIP: feature description"
```

## Tags
`git`, `version-control`, `workflow`, `automation`, `commits`

## Compatibility
- Codex: ✅
- Claude Code: ✅

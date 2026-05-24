---
name: git-workflow
description: Git workflow automation including commit messages, PR management, and branch strategies. Handles merge conflicts and maintains clean history. Use when committing, creating PRs, or managing branches.
---

# Git Workflow

Git operations including commits, PRs, branches, and conflict resolution.

## When to Use

- Commit message writing
- Pull request creation
- Branch management
- Merge conflict resolution
- History cleanup

## MCP Workflow

```bash
# View changes
git status
git diff

# Recent commits (for style)
git log --oneline -10

# Stage and commit
git add <files>
git commit -m "type(scope): message"

# Create PR
gh pr create --title "title" --body "body"
```

## Commit Convention

### Format
```
<type>(<scope>): <subject>

[body]

[footer]
```

### Types
| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting |
| refactor | Code restructure |
| perf | Performance |
| test | Tests |
| build | Build system |
| ci | CI configuration |
| chore | Maintenance |

### Rules
- Imperative mood ("add" not "added")
- No period at end
- Max 50 characters
- Lowercase first letter

### Example
```
feat(order): add order cancellation

Users can cancel orders within 24 hours.

- Add OrderCancellationService
- Integrate with RefundService

Closes #123
```

## Branch Naming

```
<type>/<issue>-<description>

feature/123-user-auth
bugfix/456-null-pointer
hotfix/789-security-patch
```

## PR Template

```markdown
## Summary
- [bullet points]

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change

## Test Plan
- [ ] Unit tests
- [ ] Integration tests

Closes #[issue]
```

## Conflict Resolution

```bash
# Update branch
git fetch origin
git rebase origin/main

# Identify conflicts
git status

# Resolve, then mark
git add <resolved-file>
git rebase --continue
```

## History Management

### Squash Commits
```bash
git rebase -i HEAD~3
# Change "pick" to "squash" for commits to combine
```

### Amend Last Commit
```bash
git add forgotten-file
git commit --amend --no-edit
```

### Cherry Pick
```bash
git cherry-pick abc123
```

## Common Commands

```bash
# Start work
git checkout main && git pull
git checkout -b feature/xxx

# Save WIP
git stash
git stash pop

# View history
git log --oneline --graph -20

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Delete branch
git branch -d feature/xxx
git push origin --delete feature/xxx

# Force push (safer)
git push --force-with-lease
```

## Output Format

```markdown
## Git: [operation]

### Commit
```
feat(user): add password reset

- Add PasswordResetService
- Add tests
```

### Files
- `UserService.kt` (+50/-10)

### Next
- [ ] Push
- [ ] Create PR
```

## Safety Rules

- NEVER force push to main/develop
- NEVER rewrite shared history
- ALWAYS use `--force-with-lease` not `--force`
- ALWAYS verify branch before destructive ops

## GitHub Commands

```bash
# Create PR
gh pr create --title "feat: feature" --body "## Summary..."

# View PR
gh pr view <PR> --json files,additions,deletions

# Approve
gh pr review <PR> --approve --body "LGTM"

# Merge
gh pr merge <PR> --squash
```

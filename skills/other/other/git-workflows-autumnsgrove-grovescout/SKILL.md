---
name: git-workflows
description: Execute git operations using Conventional Commits format with proper branching strategies and safe workflows. Use when making commits, managing branches, or performing git operations.
---

# Git Workflows Skill

## When to Activate

Activate this skill when:
- Making git commits
- Creating or merging branches
- Initializing repositories
- Resolving merge conflicts
- Reviewing git history

## Conventional Commits Format

```
<type>: <brief description>

<optional body>

<optional footer>
```

### Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat: Add user authentication` |
| `fix` | Bug fix | `fix: Correct validation error` |
| `docs` | Documentation | `docs: Update README` |
| `style` | Code formatting | `style: Format with Black` |
| `refactor` | Code restructure | `refactor: Extract helper function` |
| `test` | Add/modify tests | `test: Add auth tests` |
| `chore` | Maintenance | `chore: Update dependencies` |
| `perf` | Performance | `perf: Optimize query speed` |

## Quick Reference

```bash
# Check status
git status
git diff --stat

# Stage and commit
git add .
git commit -m "feat: add new feature"

# View history
git log --oneline -5
git log --graph --oneline --all

# Undo operations
git restore <file>              # Discard changes
git restore --staged <file>     # Unstage
git reset HEAD~1                # Undo last commit (keep changes)
```

## Commit Examples

### Feature
```bash
git commit -m "feat: Add dark mode toggle

- Implement theme switching logic
- Add localStorage persistence
- Update CSS variables"
```

### Bug Fix
```bash
git commit -m "fix: Correct timezone handling bug

Fixes off-by-one error in date calculations.

Closes #123"
```

### Breaking Change
```bash
git commit -m "feat!: Replace XML config with YAML

BREAKING CHANGE: XML configuration no longer supported.
See docs/migration.md for upgrade instructions."
```

## Branching Strategy

### Feature Branches
```bash
# Create and switch
git checkout -b feature/user-auth

# Work and commit
git add .
git commit -m "feat: add JWT authentication"

# Merge back
git checkout main
git merge feature/user-auth
git branch -d feature/user-auth
```

### Branch Naming
```
feature/feature-name    # New features
fix/bug-description     # Bug fixes
experiment/new-idea     # Experiments
release/v1.0.0          # Releases
```

## Repository Setup

```bash
# Initialize new repo
git init

# Create .gitignore
cat > .gitignore << 'EOF'
secrets.json
*.log
__pycache__/
.DS_Store
.venv/
node_modules/
.env
EOF

# Initial commit
git add .
git commit -m "chore: initialize repository"
```

## Stashing Changes

```bash
# Stash current work
git stash push -m "WIP: auth feature"

# List stashes
git stash list

# Apply most recent
git stash pop

# Apply specific stash
git stash apply stash@{1}
```

## Undoing Changes

### Git Restore (Recommended)
```bash
git restore file.py           # Discard changes
git restore --staged file.py  # Unstage
```

### Git Reset
```bash
git reset --soft HEAD~1  # Undo commit, keep staged
git reset HEAD~1         # Undo commit, keep unstaged
git reset --hard HEAD~1  # Undo commit, discard (DANGEROUS)
```

### Git Revert (Safe for Shared History)
```bash
git revert abc1234  # Create new commit undoing changes
```

## Merge Conflicts

```bash
# After conflict:
git status  # See conflicted files

# Edit files to resolve:
# <<<<<<< HEAD
# Your changes
# =======
# Incoming changes
# >>>>>>> feature-branch

# Complete merge
git add resolved-file.py
git commit
```

## Best Practices

### DO ✅
- Use conventional commit format
- One logical change per commit
- Keep subject under 50 characters
- Use imperative mood ("Add" not "Added")
- Add body for complex changes

### DON'T ❌
- Use vague messages ("Update files")
- Combine multiple concerns
- Use past tense ("Added feature")
- End subject with period

## Troubleshooting

### Committed to wrong branch
```bash
git log --oneline -1  # Note commit hash
git checkout correct-branch
git cherry-pick abc1234
git checkout wrong-branch
git reset --hard HEAD~1
```

### Lost commits
```bash
git reflog  # Find lost commit
git checkout abc1234
git checkout -b recovery-branch
```

## Related Resources

See `AgentUsage/git_guide.md` for complete documentation including:
- Breaking change handling
- Dev/main branch strategy
- Semantic versioning integration
- Automation tools

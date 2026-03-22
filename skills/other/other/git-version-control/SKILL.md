---
name: git-version-control
description: Master Git workflows, branching strategies, collaboration, and version control best practices. USE THIS for branch management, commit workflows, merging, rebasing, pull requests, conflict resolution, Git hooks, collaborative development, or version control strategy questions. Include when user mentions Git, branches, PR/MR, commits, merging, collaboration workflows, or version control.
---

# Git & Version Control Skill

Master Git workflows and collaborative development practices.

## Core Git Concepts

### Branching Strategy: Git Flow
```
main (production)
├── hotfix/*       (emergency production fixes)
└── release/*      (release candidates)

develop (integration)
├── feature/*      (new features)
├── bugfix/*       (bug fixes)
└── chore/*        (maintenance)
```

### Branch Naming Conventions
```
feature/user-authentication   # New feature
bugfix/fix-login-error        # Bug fix
hotfix/security-patch         # Emergency fix
chore/update-dependencies     # Maintenance
docs/api-documentation        # Documentation
```

## Workflow Patterns

### Feature Development (Recommended)
```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/new-auth-system

# 2. Work on feature
git add .
git commit -m "feat: implement JWT authentication"

# 3. Push to remote
git push origin feature/new-auth-system

# 4. Create Pull Request
# (on GitHub/GitLab/BitBucket: open PR to develop)

# 5. Merge after approval
git checkout develop
git pull origin develop
git merge --no-ff feature/new-auth-system
git push origin develop

# 6. Delete feature branch
git branch -d feature/new-auth-system
git push origin --delete feature/new-auth-system
```

### Commit Message Convention (Conventional Commits)
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes (no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Testing
- `chore`: Build/tooling changes

**Examples**:
```
feat(auth): implement OAuth 2.0 integration
fix(api): handle null response in user endpoint
docs(readme): add installation instructions
refactor(utils): optimize chunking algorithm
```

## Merging Strategies

### Merge vs Rebase vs Squash

#### 1. Merge (Preserve History)
```bash
# Creates a merge commit - preserves full history
git merge feature/xyz
# Use for: long-running branches, team collaboration
```

#### 2. Rebase (Clean History)
```bash
# Replays commits on top of main - clean linear history
git rebase main
# Use for: local branches before merging
```

#### 3. Squash (Single Commit)
```bash
# Combines all commits into one - clean main branch
git merge --squash feature/xyz
# Use for: small features, clean main history
```

### Conflict Resolution
```bash
# 1. Start merge
git merge feature/branch

# 2. Check conflicts
git status
# Look for "both modified" or "both added" files

# 3. Edit conflicted files
# Find markers: <<<<<<<, =======, >>>>>>>
# Edit to keep desired changes

# 4. Mark resolved
git add resolved-file.js

# 5. Complete merge
git commit -m "Merge feature/branch resolving conflicts"
```

## Collaboration Patterns

### Code Review Workflow
```bash
# As feature developer:
git push origin feature/my-feature
# → Open Pull Request for review

# As reviewer:
# 1. Review code on GitHub/GitLab
# 2. Request changes or approve
# 3. Developer implements feedback:
git add changes.js
git commit -m "refactor: address review feedback"
git push

# 4. Re-review and merge when approved
```

### Syncing with Remote
```bash
# Fetch latest changes (doesn't modify local)
git fetch origin

# Pull = Fetch + Merge
git pull origin main

# Pull with rebase (cleaner history)
git pull --rebase origin main
```

### Undoing Changes

```bash
# Undo uncommitted changes (revert file)
git restore filename.js

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (create new commit that undoes it)
git revert <commit-hash>

# Show what you'd lose
git diff HEAD~1
```

## Advanced Operations

### Interactive Rebase (Reorder/Squash Commits)
```bash
# Start interactive rebase of last 3 commits
git rebase -i HEAD~3

# Editor opens with options:
# pick   - use commit
# reword - edit message
# squash - combine with previous
# drop   - remove commit

# Example:
pick   abc123   feat: start feature
squash def456   feat: continue feature
squash ghi789   feat: finish feature
```

### Cherry-Pick (Apply Specific Commits)
```bash
# Copy a commit from another branch
git cherry-pick <commit-hash>

# Apply multiple commits
git cherry-pick <start-hash>..<end-hash>

# Interactive cherry-pick
git cherry-pick -i <branch>
```

### Stash (Temporary Storage)
```bash
# Save uncommitted changes
git stash

# Save with message
git stash save "WIP: feature in progress"

# List stashes
git stash list

# Apply stash
git stash apply  # Keep in stash
git stash pop    # Remove from stash

# Delete stash
git stash drop stash@{0}
```

## Tags & Releases

### Version Tagging
```bash
# Create tag for release
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags  # Push all tags

# List releases
git tag -l --sort=-version:refname
```

## Git Hooks (Automation)

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "Commit failed: lint errors"
  exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "Commit failed: tests failed"
  exit 1
fi
```

### Commit Message Hook
```bash
#!/bin/bash
# .git/hooks/commit-msg

# Validate commit message format
if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?:" "$1"; then
  echo "Commit message must follow conventional commits format"
  exit 1
fi
```

## Useful Commands Reference

```bash
# View history
git log --oneline --graph --all
git log --author="name" --since="2 weeks ago"

# Diff operations
git diff                    # Working vs staged
git diff --staged           # Staged vs committed
git diff main feature/xyz   # Compare branches

# Find commits
git log -S "search term"    # Search commits by content
git blame filename.js       # Who changed each line

# Clean up
git gc                      # Garbage collection
git clean -fd               # Remove untracked files
git branch -d branch-name   # Delete local branch
git push origin --delete branch-name  # Delete remote

# Troubleshooting
git reflog               # Recover lost commits
git fsck --lost-found    # Find orphaned commits
```

## Best Practices

### Commit Hygiene
- ✅ Commit logical units (one feature per commit)
- ✅ Write clear, descriptive messages
- ✅ Test before committing
- ❌ Don't commit commented-out code
- ❌ Don't commit dependencies (use .gitignore)

### Pull Requests
- ✅ Keep PRs small and focused
- ✅ Write detailed descriptions
- ✅ Link to related issues
- ✅ Request specific reviewers
- ❌ Don't merge your own PR
- ❌ Don't bypass code review

### Branch Management
- ✅ Delete merged branches
- ✅ Keep up to date with main branch
- ✅ Use protection rules on main/develop
- ❌ Don't push directly to main
- ❌ Don't leave stale branches

## Team Workflows

### Continuous Integration (CI)
```yaml
# Example GitHub Actions
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm test
      - run: npm run lint
```

### Protected Branches
Configure on GitHub/GitLab:
- Require pull request reviews
- Require CI to pass
- Dismiss stale reviews when new commits pushed
- Require branches to be up to date

---

**Output**: Clean Git history, smooth collaboration, and professional version control practices.

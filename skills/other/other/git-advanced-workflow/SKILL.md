---
name: Git Advanced Workflow Expert
description: Expert guidance for advanced Git workflows, trunk-based development, monorepo strategies, and Git automation. Use when implementing Git workflows, managing complex repositories, or automating Git operations.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
---

# Git Advanced Workflow Expert

Advanced Git workflows and automation for modern development teams.

## Trunk-Based Development

```bash
# Main branch protection
git config branch.main.mergeoptions --no-ff

# Short-lived feature branches
git checkout -b feature/user-auth
# Work on feature (max 2 days)
git commit -m "feat: add user authentication"
git push origin feature/user-auth
# Create PR → Review → Merge → Delete branch

# Feature flags for incomplete features
if (featureFlags.isEnabled('new-ui')) {
  renderNewUI();
} else {
  renderOldUI();
}
```

## Conventional Commits

```bash
# Format: <type>(<scope>): <subject>

feat(auth): add OAuth2 support
fix(api): resolve race condition in user creation
docs(readme): update installation instructions
style(ui): format button components
refactor(db): optimize query performance
test(api): add integration tests for auth
chore(deps): upgrade react to v18
perf(api): implement caching layer
ci(github): add automated deployment
build(webpack): optimize production bundle
```

## Git Hooks with Husky

```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run lint-staged
npx lint-staged

# Run tests on staged files
npm test -- --findRelatedTests --passWithNoTests

# Prevent commits to main
branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$branch" = "main" ]; then
  echo "Direct commits to main are not allowed"
  exit 1
fi
```

```bash
# .husky/commit-msg
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Validate conventional commit format
npx commitlint --edit $1
```

## Monorepo Strategies

### Git Sparse Checkout

```bash
# Clone only specific directories
git clone --filter=blob:none --sparse https://github.com/user/monorepo
cd monorepo
git sparse-checkout init --cone
git sparse-checkout set apps/web packages/ui

# Add more paths
git sparse-checkout add apps/api
```

### Git Worktrees

```bash
# Multiple working directories from same repo
git worktree add ../monorepo-feature feature/new-ui
git worktree add ../monorepo-hotfix hotfix/critical-bug
git worktree list

# Clean up
git worktree remove ../monorepo-feature
```

## Advanced Git Operations

### Interactive Rebase

```bash
# Clean up commits before PR
git rebase -i HEAD~5

# Squash fixup commits
git commit --fixup HEAD~2
git rebase -i --autosquash HEAD~5

# Edit commit history
pick a1b2c3d feat: add feature
fixup d4e5f6g fix typo
reword g7h8i9j Update message
drop j0k1l2m Remove this commit
```

### Cherry-Pick Workflows

```bash
# Apply specific commits
git cherry-pick abc123

# Cherry-pick range
git cherry-pick abc123..def456

# Cherry-pick from another branch
git cherry-pick feature-branch~3..feature-branch
```

### Bisect for Bug Hunting

```bash
# Find bug-introducing commit
git bisect start
git bisect bad HEAD
git bisect good v1.0.0

# Mark each commit
git bisect good  # or bad

# Automated bisect
git bisect run npm test
```

## Git Automation Scripts

### Auto-sync Script

```bash
#!/bin/bash
# auto-sync.sh

MAIN_BRANCH="main"
CURRENT_BRANCH=$(git branch --show-current)

# Fetch latest
git fetch origin

# Check if main has updates
if [ "$(git rev-parse $MAIN_BRANCH)" != "$(git rev-parse origin/$MAIN_BRANCH)" ]; then
  echo "Main branch has updates. Rebasing..."

  # Stash changes
  git stash

  # Update main
  git checkout $MAIN_BRANCH
  git pull --rebase origin $MAIN_BRANCH

  # Rebase current branch
  git checkout $CURRENT_BRANCH
  git rebase $MAIN_BRANCH

  # Restore stash
  git stash pop

  echo "✅ Successfully synced with main"
else
  echo "✅ Already up to date"
fi
```

### Release Automation

```bash
#!/bin/bash
# release.sh

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version>"
  exit 1
fi

# Ensure clean working directory
if [[ -n $(git status -s) ]]; then
  echo "❌ Working directory not clean"
  exit 1
fi

# Update version
npm version $VERSION --no-git-tag-version

# Build
npm run build

# Commit
git add package.json package-lock.json
git commit -m "chore: release v$VERSION"

# Tag
git tag -a "v$VERSION" -m "Release v$VERSION"

# Push
git push origin main --tags

echo "✅ Released v$VERSION"
```

## GitHub Actions Integration

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better diffs

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          files: |
            **/*.ts
            **/*.tsx

      - name: Run tests on changed files
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          npm test -- ${{ steps.changed-files.outputs.all_changed_files }}

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint

  semantic-release:
    needs: [test, lint]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cycjimmy/semantic-release-action@v4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Git Aliases

```bash
# ~/.gitconfig
[alias]
  # Shortcuts
  co = checkout
  ci = commit
  st = status
  br = branch

  # Logging
  lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
  recent = for-each-ref --count=10 --sort=-committerdate refs/heads/ --format='%(refname:short)'

  # Workflow
  undo = reset --soft HEAD~1
  amend = commit --amend --no-edit
  sync = !git fetch origin && git rebase origin/main
  cleanup = !git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d

  # Review
  diff-staged = diff --staged
  contributors = shortlog --summary --numbered --email
```

## Best Practices

✅ Use conventional commits for clarity
✅ Keep commits atomic and focused
✅ Rebase feature branches regularly
✅ Use feature flags for incomplete work
✅ Automate with Git hooks
✅ Protect main branch
✅ Require PR reviews
✅ Use semantic versioning
✅ Tag releases properly
✅ Clean up merged branches

---

**When to Use:** Git workflow setup, repository management, automation, trunk-based development, monorepo strategies.

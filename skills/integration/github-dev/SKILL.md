---
name: github-dev
description: World-class #1 expert GitHub developer specializing in Git operations, GitHub Actions CI/CD, Pull Requests, Issues, GitHub CLI (gh), GitHub API, Copilot, Pages, Security, branching strategies, release management, and GitHub Apps. Use when managing repositories, automating workflows, code review, or implementing DevOps practices with GitHub at production scale.
license: Complete terms in LICENSE.txt
---

# GitHub Development Expert - World-Class Edition

## Overview

You are a world-class GitHub expert with deep knowledge of Git operations, GitHub platform features, CI/CD automation, security best practices, and collaborative development workflows at enterprise scale.

---

# Philosophy & Principles

## Core Principles

1. **Trunk-Based Development** - Short-lived branches, frequent integration
2. **Automation First** - CI/CD gates, automated testing, Dependabot
3. **Security by Default** - Branch protection, secret scanning, code signing
4. **Collaboration Excellence** - Clear PR descriptions, template enforcement, code review standards
5. **Documentation as Code** - README, CONTRIBUTING, CODEOWNERS, PR/Issue templates

## Best Practices

```
✅ DO:
- Use branch protection rules on main
- Require PR reviews and status checks
- Automate with GitHub Actions
- Use semantic versioning for releases
- Keep branches short-lived (< 2 days)
- Write descriptive commit messages
- Use CONVENTIONAL_COMMITS specification

❌ DON'T:
- Commit directly to main/master
- Create long-lived feature branches
- Hardcode secrets in workflows
- Ignore security alerts
- Skip code review
- Use force push on shared branches
- Store large files in git (use Git LFS)
```

---

# Decision Tree - When to Use This Skill

```
Need to work with code version control?
├─ Yes → Is it on GitHub?
│   ├─ Yes → Use this skill (github-dev)
│   └─ No → Use git-focused approach
└─ No → Consider other skills

GitHub Task Types:
├─ Repository Setup → Create, clone, fork, mirror
├─ Daily Operations → Branch, commit, push, pull, merge
├─ Collaboration → PR, review, issue, discussion
├─ Automation → GitHub Actions, workflows, CI/CD
├─ Security → Branch protection, secrets, scanning
├─ Release → Tags, releases, changelog
├─ CLI Operations → gh commands for efficiency
└─ API Integration → REST/GraphQL automation
```

---

# Core Concepts

## Git Operations

### Essential Commands

```bash
# Repository Setup
git init                          # Initialize new repository
git clone <url>                   # Clone repository
git clone --depth 1 <url>         # Shallow clone (last commit only)

# Branching
git branch <name>                 # Create branch
git checkout -b <name>            # Create and switch branch
git switch -c <name>              # Modern checkout alternative
git branch -d <name>              # Delete local branch
git push origin --delete <name>   # Delete remote branch

# Staging & Committing
git status                        # Show working tree status
git add <file>                    # Stage file
git add .                         # Stage all changes
git add -p                        # Interactive staging
git commit -m "message"           # Commit staged changes
git commit -am "message"          # Stage and commit (tracked files)
git commit --amend                # Edit last commit

# Synchronization
git fetch origin                  # Fetch remote changes
git pull origin main              # Pull and merge
git pull --rebase origin main     # Pull with rebase
git push origin <branch>          # Push to remote
git push -u origin <branch>       # Push and set upstream

# History
git log --oneline --graph --all   # Visual commit history
git log -p -2                     # Last 2 commits with diffs
git diff                         # Unstaged changes
git diff --staged                # Staged changes
git show <commit>                # Show commit details

# Undo Operations
git restore <file>               # Discard local changes
git restore --staged <file>      # Unstage file
git reset HEAD~1                 # Undo last commit (keep changes)
git reset --hard HEAD~1          # Undo last commit (discard changes)
git revert <commit>              # Create revert commit
```

### Merge vs Rebase vs Squash

```
┌─────────────────────────────────────────────────────────────┐
│                    Merge Strategies                          │
├─────────────────────────────────────────────────────────────┤
│  Strategy    │ When to Use           │ Pros           │ Cons │
├─────────────────────────────────────────────────────────────┤
│  Merge       │ Preserving history    │ Complete history│ Noisy │
│  (default)   │ Team collaboration    │ True timeline  │ graph │
├─────────────────────────────────────────────────────────────┤
│  Rebase      │ Clean linear history  │ Clean commits  │ Lost  │
│              │ Before PR submission  │ Easy bisect    │ context│
├─────────────────────────────────────────────────────────────┤
│  Squash      │ Fix/feature branches  │ Single commit  │ Lost  │
│  merge       │ WIP commits           │ Clean history  │ detail │
└─────────────────────────────────────────────────────────────┘
```

### Git Configuration

```bash
# User Identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default Branch Name
git config --global init.defaultBranch main

# Line Endings (Windows)
git config --global core.autocrlf true

# Pull Behavior
git config --global pull.rebase false  # Merge (default)
git config --global pull.rebase true   # Rebase

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
```

---

## GitHub CLI (gh)

### Essential Commands

```bash
# Authentication
gh auth login                      # Interactive login
gh auth status                     # Check auth status
gh auth logout                     # Logout

# Repository Operations
gh repo create <name>              # Create repository
gh repo clone <org/repo>           # Clone with gh auth
gh repo view                       # View repository info
gh repo list                       # List your repositories

# Issues & Pull Requests
gh issue list                      # List issues
gh issue create                    # Create issue (interactive)
gh issue view <number>             # View issue
gh issue close <number>            # Close issue

gh pr list                         # List pull requests
gh pr create                       # Create PR (interactive)
gh pr view <number>                # View PR
gh pr merge <number>                # Merge PR
gh pr diff <number>                # View PR diff
gh pr checks <number>              # View CI status

# Actions
gh run list                        # List workflow runs
gh run view <run-id>               # View run details
gh run watch <run-id>              # Watch run in real-time
gh run rerun <run-id>              # Re-run failed workflow

# Release Management
gh release list                    # List releases
gh release create <tag>            # Create release
gh release view <tag>              # View release

# Git Operations
gh repo sync                       # Sync fork with upstream
gh repo set-default               # Set default branch

# Extensions
gh extension list                  # List installed extensions
gh extension install <repo>        # Install extension
```

### Advanced gh Workflows

```bash
# PR with template and assignees
gh pr create \
  --title "feat: Add user authentication" \
  --body "Fixes #123" \
  --assignee @me \
  --reviewer user1,user2 \
  --label enhancement,security \
  --base main

# Bulk close issues
gh issue list --label "duplicate" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {}

# View workflow failures
gh run list --workflow=ci.yml --json databaseId,conclusion,status | \
  jq -r '.[] | select(.conclusion == "failure") | .databaseId' | \
  xargs -I {} gh run view {}

# Create PR from issue
gh issue develop 123  # Creates branch from issue

# Project management
gh project list                    # List projects
gh project view <number>           # View project board
gh project item add <id>           # Add item to project
```

---

## GitHub Actions (CI/CD)

### Workflow Structure

```yaml
# .github/workflows/example.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:              # Manual trigger
  schedule:
    - cron: '0 0 * * *'           # Daily at midnight

permissions:
  contents: read
  issues: read
  pull-requests: read

env:
  NODE_VERSION: '20'
  CACHE_VERSION: 'v1'

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm test

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    outputs:
      version: ${{ steps.meta.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: Extract metadata
        id: meta
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist

      - name: Deploy
        run: |
          # Your deployment commands
          echo "Deploying to production"
```

### Caching Strategies

```yaml
# Node.js dependencies cache
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Docker layer cache
- name: Cache Docker layers
  uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ hashFiles('**/Dockerfile') }}

# Custom cache
- name: Cache build output
  uses: actions/cache@v4
  with:
    path: build/cache
    key: cache-${{ github.sha }}
```

### Secrets & Variables

```yaml
# Using secrets (never log these!)
- name: Deploy with secret
  run: |
    curl -X POST \
      -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" \
      https://api.example.com/deploy

# Using environment variables
env:
  APP_ENV: ${{ vars.ENVIRONMENT }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Passing secrets to composite actions
- uses: ./.github/actions/deploy
  with:
    api-key: ${{ secrets.API_KEY }}
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-ci.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          token: ${{ secrets.token }}

# Calling reusable workflow
# .github/workflows/ci.yml
jobs:
  call-ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '20'
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

### Composite Actions

```yaml
# .github/actions/setup-env/action.yml
name: 'Setup Environment'
description: 'Setup Node.js and install dependencies'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
      shell: bash

    - name: Install dependencies
      run: npm ci
      shell: bash

# Using composite action
- uses: ./.github/actions/setup-env
  with:
    node-version: '22'
```

### Self-Hosted Runners

```yaml
# Target specific runners
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
    # or specific runner group
    runs-on:
      group: production-runners

# Using runner labels
runs-on:
  - self-hosted
  - gpu
  - high-memory
```

### Deployment Patterns

```yaml
# Blue-Green Deployment
deploy-blue-green:
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://app.example.com
  steps:
    - name: Deploy to blue
      if: github.event_name == 'push' && github.ref == 'refs/heads/main'
      run: ./deploy.sh blue

    - name: Switch traffic to blue
      if: success()
      run: ./switch-traffic.sh blue

# Canary Deployment
deploy-canary:
  runs-on: ubuntu-latest
  environment:
    name: production-canary
    url: https://canary.example.com
  steps:
    - name: Deploy canary (10%)
      run: ./deploy.sh --canary 10

# Progressive Deployment
deploy-progressive:
  runs-on: ubuntu-latest
  environment:
    name: production
    deployment: production  # Enable deployment protection rules
  steps:
    - name: Deploy
      run: ./deploy.sh
```

---

## Pull Requests & Code Review

### PR Templates

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes Made
- List main changes
- Include screenshots for UI changes

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Changes generate no new warnings
- [ ] Any dependent changes merged

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->
```

### Code Review Guidelines

```markdown
## Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling appropriate

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Naming is clear and consistent
- [ ] Logic is simple and straightforward
- [ ] No unnecessary complexity

### Testing
- [ ] Tests cover new functionality
- [ ] Tests are meaningful
- [ ] No tests are skipped

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output escaping where needed
- [ ] Dependencies are secure

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Caching considered where applicable
```

### CODEOWNERS File

```python
# .github/CODEOWNERS

# Global owners
* @github-team @fallback-owner

# Specific patterns
*.js @frontend-team
*.py @backend-team
*.md @docs-team

# Directory-based
/src/components/ @ui-team
/src/api/ @api-team
/tests/ @qa-team

# File-specific
/README.md @maintainer
/SECURITY.md @security-team

# Negation (override)
*.js @frontend-team
/src/legacy/**/*.js @legacy-team
```

### Automated PR Workflows

```yaml
# .github/workflows/pr-automation.yml
name: PR Automation

on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  labeler:
    name: Label PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml

  assign-author:
    name: Auto-assign Author
    runs-on: ubuntu-latest
    steps:
      - uses: toshimaru/auto-author-assign@v2
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}

  size-reporter:
    name: PR Size
    runs-on: ubuntu-latest
    steps:
      - uses: toshimaru/size-labeler@v1
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          xs_max: 10
          s_max: 50
          m_max: 200
          l_max: 500
          xl_max: 1000
```

```yaml
# .github/labeler.yml
feature:
  - "**/*.feature"
  - any: ['src/features/**']

bug:
  - any: ['**/fix/**', '**/bugfix/**']

documentation:
  - any: ['**/*.md', '**/docs/**']

dependencies:
  - any: ['**/package.json', '**/requirements.txt', '**/go.mod']

tests:
  - any: ['**/__tests__/**', '**/*.test.*', '**/*.spec.*']
```

---

## Issues & Project Management

### Issue Templates

```markdown
<!-- .github/ISSUE_TEMPLATE/bug_report.md -->
---
name: Bug Report
about: Report a problem with the project
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
<!-- Clear and concise description of the bug -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- OS:
- Browser/Version:
- Application Version:

## Screenshots
<!-- If applicable -->

## Additional Context
<!-- Logs, error messages, etc. -->
```

```markdown
<!-- .github/ISSUE_TEMPLATE/feature_request.md -->
---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Feature Description
<!-- What would you like to see added -->

## Problem Statement
<!-- What problem does this solve? -->

## Proposed Solution
<!-- How should it work? -->

## Alternatives Considered
<!-- What other approaches did you consider? -->

## Additional Context
<!-- Mockups, examples, etc. -->
```

### Task Lists in Issues

```markdown
## Implementation Tasks

- [ ] Design database schema
- [ ] Implement API endpoints
- [ ] Write unit tests
- [ ] Update documentation
- [ ] Deploy to staging

## Subtasks
- [ ] [ ] User registration
- [x] User login
- [ ] Password reset
```

### Project Board Automation

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, labeled, closed]
  pull_request:
    types: [opened, labeled, closed, merged]

jobs:
  add-to-project:
    name: Add to Project Board
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v1
        with:
          project-url: https://github.com/orgs/org/projects/1
          labeled: bug,enhancement

  move-columns:
    name: Move Between Columns
    runs-on: ubuntu-latest
    steps:
      - name: Move to In Progress when PR is opened
        if: github.event_name == 'pull_request' && github.event.action == 'opened'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.projects.moveCard({
              card_id: context.payload.project_card.id,
              position: 'after:column_id:in_progress'
            })
```

---

## Branch Protection & Rules

### Branch Protection Rules

```bash
# Using gh CLI
gh api \
  repos/:owner/:repo/branches/main/protection \
  --method PUT \
  -f enforce_admins=true \
  -f required_status_checks='{"strict":true,"contexts":["ci/lint","ci/test"]}' \
  -f require_pull_request='{"required_approving_review_count":1}' \
  -f restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

### Required Checks

```yaml
# Branch protection settings via API
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "ci/lint",
      "ci/test",
      "ci/build",
      "security/dependabot",
      "security/codeql"
    ],
    "checks": [
      { "context": "ci/lint" },
      { "context": "ci/test" },
      { "context": "ci/build" }
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {},
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "require_linear_history": true,
  "require_conversation_resolution": true
}
```

---

## Release Management

### Semantic Versioning

```
MAJOR.MINOR.PATCH (e.g., 2.1.3)

- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

Pre-release tags: 1.0.0-alpha, 1.0.0-beta.1, 1.0.0-rc.2
Build metadata: 1.0.0+20130313144700
```

### Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style (formatting, etc.)
- refactor: Code refactoring
- perf: Performance improvement
- test: Adding or updating tests
- chore: Maintenance tasks
- ci: CI/CD changes
- build: Build system changes
- revert: Revert a previous commit

Examples:
feat(api): add user authentication
fix(auth): resolve token expiration bug
docs(readme): update installation instructions
ci(workflow): add node 22 support
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        uses:actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') }}
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Automated Release with semantic-release

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci
      - run: npm test

      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## GitHub Security

### Secret Scanning

```yaml
# Enable secret scanning (UI setting)
# Settings > Security > Secret scanning

# Secret scanning patterns
- AWS keys
- GitHub tokens
- API keys
- Database credentials
- Private keys
- OAuth tokens
```

### Code Scanning (CodeQL)

```yaml
# .github/workflows/codeql.yml
name: CodeQL Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '30 1 * * 0'  # Weekly

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [javascript, python]

    steps:
      - uses: actions/checkout@v4

      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended,security-and-quality

      - uses: github/codeql-action/autobuild@v3

      - uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{matrix.language}}"
```

### Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    target-branch: "main"
    labels:
      - "dependencies"
      - "npm"
    commit-message:
      prefix: "deps"
      include: "scope"
    groups:
      development-dependencies:
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier*"
    reviewers:
      - "maintainer-team"
    assignees:
      - "maintainer"

  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Dependabot Security Updates

```yaml
# Enable in UI: Settings > Security > Dependabot

# Or via API
gh api \
  repos/:owner/:repo/automated-security-fixes \
  --method PUT \
  -f enabled=true
```

### Security Policy

```markdown
<!-- SECURITY.md -->
# Security Policy

## Supported Versions
| Version | Supported          |
|---------|--------------------|
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities privately:

1. Email: security@example.com
2. PGP Key: [Key link]
3. Include: Description, steps to reproduce, impact

We will respond within 48 hours.

## Security Best Practices

- Never commit secrets
- Use environment variables
- Enable branch protection
- Review dependencies
- Keep dependencies updated
```

---

## GitHub Pages

### Deployment Workflows

```yaml
# Static HTML/CSS/JS
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/configure-pages@v4

      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'

      - uses: actions/deploy-pages@v4
```

```yaml
# Build with static site generator
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### Multi-Language Site

```yaml
name: Deploy Multi-Language Site

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        lang: [en, th, ja]
    steps:
      - uses: actions/checkout@v4

      - name: Build ${{ matrix.lang }}
        run: |
          npm run build -- --lang=${{ matrix.lang }}
          mv dist dist-${{ matrix.lang }}

      - name: Deploy ${{ matrix.lang }}
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist-${{ matrix.lang }}
          destination_dir: ${{ matrix.lang }}
```

---

## GitHub API

### REST API Examples

```bash
# Using curl
# Get repository information
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo

# Create an issue
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo/issues \
  -d '{"title":"Found a bug","body":"This is a bug report"}'

# List commits
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/commits?per_page=10

# Create a release
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo/releases \
  -d '{"tag_name":"v1.0.0","name":"Release 1.0.0"}'
```

### GraphQL API Examples

```bash
# Using GraphQL
gh api graphql \
  -F owner='owner' \
  -F repo='repo' \
  -f query='
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        name
        description
        stargazerCount
        forkCount
        releases(last: 5) {
          nodes {
            name
            publishedAt
          }
        }
      }
    }'
```

### Octokit (JavaScript)

```javascript
// REST API
const octokit = new Octokit({
  auth: 'personal-access-token'
});

// Create an issue
await octokit.rest.issues.create({
  owner: 'owner',
  repo: 'repo',
  title: 'Found a bug',
  body: 'This is a bug report'
});

// GraphQL
const query = `query ($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    name
    stargazerCount
  }
}`;

const response = await octokit.graphql(query, {
  owner: 'owner',
  repo: 'repo'
});
```

---

## Git LFS (Large File Storage)

```bash
# Install Git LFS
git lfs install

# Track file types
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "assets/videos/*"

# View tracked patterns
git lfs track

# Untrack a pattern
git lfs untrack "*.zip"

# Clone with LFS
git clone --depth 1 https://github.com/user/repo.git
git lfs pull

# Migrate existing repo
git lfs migrate import --include="*.psd,*.ai"

# Lock files (prevent conflicts)
git lfs lock design.psd
git lfs unlock design.psd
```

---

## Branching Strategies

### Trunk-Based Development

```
main (protected, always deployable)
  ├─ Short-lived feature branches (< 1 day)
  ├─ Direct commits for small fixes
  └─ CI gates all merges

Benefits:
- Fast integration
- Reduced merge conflicts
- Continuous deployment ready
```

### GitHub Flow

```
main (protected, always deployable)
  └─ feature branches (created from main)

1. Create branch from main
2. Commit changes
3. Open Pull Request
4. Review and discuss
5. Merge to main (with CI passing)
6. Deploy immediately
```

### GitFlow

```
main (production releases)
  └─ develop (integration branch)
       ├─ feature/* (new features)
       ├─ release/* (release preparation)
       └─ hotfix/* (emergency production fixes)

feature branches → develop → release → main
hotfix branches → main → develop
```

---

# Advanced Patterns

## Matrix Builds

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
    experimental: [false]
    include:
      - node-version: 22
        os: macos-latest
        experimental: true
  fail-fast: false
```

## Conditional Execution

```yaml
# Expressions
if: github.event_name == 'push'
if: startsWith(github.ref, 'refs/tags/v')
if: contains(github.event.head_commit.message, '[skip ci]') == false
if: github.actor == 'dependabot[bot]'
if: success() || failure()
if: always()

# Environment-specific
if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

## Composite Actions with Inputs

```yaml
# action.yml
name: 'Custom Action'
description: 'A composite action'
inputs:
  input1:
    description: 'First input'
    required: true
    default: 'default-value'
outputs:
  output1:
    description: 'First output'
    value: ${{ steps.step1.outputs.result }}
runs:
  using: 'composite'
  steps:
    - run: echo "Hello ${{ inputs.input1 }}"
      shell: bash
```

## Dynamic Matrix

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: echo "matrix=[\"test1\",\"test2\"]" >> $GITHUB_OUTPUT

  test:
    needs: setup
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test: ${{ fromJSON(needs.setup.outputs.matrix) }}
    steps:
      - run: echo "Running ${{ matrix.test }}"
```

---

# World-Class Resources

## Official Documentation
- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Actions Documentation: https://docs.github.com/en/actions
- GitHub CLI Manual: https://cli.github.com/manual
- GitHub API: https://docs.github.com/en/rest

## Learning Resources
- GitHub Skills: https://skills.github.com
- GitHub Learning Lab: https://lab.github.com
- Pro Git Book: https://git-scm.com/book
- GitHub Glossary: https://docs.github.com/en/get-started/learning-about-github/github-glossary

## Security Resources
- GitHub Security: https://docs.github.com/en/security
- Dependabot: https://docs.github.com/en/code-security/dependabot
- CodeQL: https://codeql.github.com/docs
- Secret Scanning: https://docs.github.com/en/code-security/secret-scanning

## Best Practices
- GitHub Flow: https://docs.github.com/en/get-started/quickstart/github-flow
- Branching Strategies: https://www.atlassian.com/git/tutorials/comparing-workflows
- Conventional Commits: https://www.conventionalcommits.org
- Semantic Versioning: https://semver.org

## Tools & Integrations
- GitHub CLI Extensions: https://github.com/cli/cli-extensions
- GitHub Actions Marketplace: https://github.com/marketplace?type=actions
- GitHub Desktop: https://desktop.github.com

---

# Common Anti-Patterns

```
❌ ANTI-PATTERN: Direct commits to main
git push origin main
✅ BETTER: Use pull requests
git checkout -b feature-branch
git push origin feature-branch
# Create PR and merge after review

❌ ANTI-PATTERN: Ignoring failed CI
✅ BETTER: Fix or skip tests properly
# Use [skip ci] in commit if intentionally skipping

❌ ANTI-PATTERN: Hardcoded secrets
const API_KEY = "ghp_xxxxx"
✅ BETTER: Use environment variables
const API_KEY = process.env.API_KEY

❌ ANTI-PATTERN: Force push on shared branches
git push --force
✅ BETTER: Use --force-with-lease
git push --force-with-lease origin feature-branch

❌ ANTI-PATTERN: Huge monorepo workflow runs on every push
on: [push]
✅ BETTER: Use path filters
on:
  push:
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend.yml'

❌ ANTI-PATTERN: Re-running entire workflow for one flaky test
✅ BETTER: Use retry or split tests
- run: npm test -- --retry=3

❌ ANTI-PATTERN: Merging without resolving conflicts locally
✅ BETTER: Update branch locally before PR
git pull --rebase origin main
# Fix conflicts, then push
```

---

# DriverConnect Project Context

## Current GitHub Setup

- **Repository**: Private GitHub repository
- **Branch**: `main` (protected)
- **CI/CD**: GitHub Actions for deployment
- **Deployment**: GitHub Pages for subpath projects

## Relevant Files

| Purpose | File |
|---------|------|
| Workflow | [.github/workflows/deploy.yml](.github/workflows/deploy.yml) |
| Templates | [.github/](.github/) |
| Documentation | [README.md](README.md) |

## Current Deployment Strategy

```yaml
# Current GitHub Actions workflow deploys:
# - liff-doctor app to /liff-doctor/
# - driver-connect to / (root)
# - Using subpath configuration
```

---

# Maintenance Checklist

## Daily
- Monitor Actions failures
- Review and merge PRs
- Check security alerts

## Weekly
- Review Dependabot updates
- Clean up stale branches
- Check code scanning alerts

## Monthly
- Review and update workflows
- Audit branch protection rules
- Review access permissions
- Update dependencies

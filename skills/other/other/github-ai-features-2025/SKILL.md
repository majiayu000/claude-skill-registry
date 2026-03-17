---
name: github-ai-features-2025
description: GitHub AI-powered security and automation features for 2025
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# GitHub AI Features 2025

## Trunk-Based Development (TBD)

Modern workflow used by largest tech companies (Google: 35,000+ developers):

### Principles

1. **Short-lived branches:** Hours to 1 day maximum
2. **Small, frequent commits:** Reduce merge conflicts
3. **Continuous integration:** Always deployable main branch
4. **Feature flags:** Hide incomplete features

### Implementation

```bash
# Create task branch from main
git checkout main
git pull origin main
git checkout -b task/add-login-button

# Make small changes
git add src/components/LoginButton.tsx
git commit -m "feat: add login button component"

# Push and create PR (same day)
git push origin task/add-login-button
gh pr create --title "Add login button" --body "Implements login UI"

# Merge within hours, delete branch
gh pr merge --squash --delete-branch
```

### Benefits

- Reduced merge conflicts (75% decrease)
- Faster feedback cycles
- Easier code reviews (smaller changes)
- Always releasable main branch
- Simplified CI/CD pipelines

## GitHub Secret Protection (AI-Powered)

AI detects secrets before they reach repository:

### Push Protection

```bash
# Attempt to commit secret
git add config.py
git commit -m "Add config"
git push

# GitHub AI detects secret:
"""
⛔ Push blocked by secret scanning

Found: AWS Access Key
Pattern: AKIA[0-9A-Z]{16}
File: config.py:12

Options:
1. Remove secret and try again
2. Mark as false positive (requires justification)
3. Request review from admin
"""

# Fix: Use environment variables
# config.py
import os
aws_key = os.environ.get('AWS_ACCESS_KEY')

git add config.py
git commit -m "Use env vars for secrets"
git push  # ✅ Success
```

### Supported Secret Types (AI-Enhanced)

- AWS credentials
- Azure service principals
- Google Cloud keys
- GitHub tokens
- Database connection strings
- API keys (OpenAI, Stripe, etc.)
- Private keys (SSH, TLS)
- OAuth tokens
- Custom patterns (regex-based)

## GitHub Code Security

### CodeQL Code Scanning

AI-powered static analysis:

```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: javascript, python, java

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
```

**Detects:**
- SQL injection
- XSS vulnerabilities
- Path traversal
- Command injection
- Insecure deserialization
- Authentication bypass
- Logic errors

### Copilot Autofix

AI automatically fixes security vulnerabilities:

```python
# Vulnerable code detected by CodeQL
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ SQL injection
    return db.execute(query)

# Copilot Autofix suggests:
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    return db.execute(query, (user_id,))  # ✅ Parameterized query

# One-click to apply fix
```

## GitHub Agents (Automated Workflows)

AI agents for automated bug fixes and PR generation:

### Bug Fix Agent

```yaml
# .github/workflows/ai-bugfix.yml
name: AI Bug Fixer

on:
  issues:
    types: [labeled]

jobs:
  autofix:
    if: contains(github.event.issue.labels.*.name, 'bug')
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Analyze Bug
      uses: github/ai-agent@v1
      with:
        task: 'analyze-bug'
        issue-number: ${{ github.event.issue.number }}

    - name: Generate Fix
      uses: github/ai-agent@v1
      with:
        task: 'generate-fix'
        create-pr: true
        pr-title: "Fix: ${{ github.event.issue.title }}"
```

### Automated PR Generation

```bash
# GitHub Agent creates PR automatically
# When issue is labeled "enhancement":
# 1. Analyzes issue description
# 2. Generates implementation code
# 3. Creates tests
# 4. Opens PR with explanation

# Example: Issue #42 "Add dark mode toggle"
# Agent creates PR with:
# - DarkModeToggle.tsx component
# - ThemeContext.tsx provider
# - Tests for theme switching
# - Documentation update
```

## Dependency Review (AI-Enhanced)

AI analyzes dependency changes in PRs:

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review

on: [pull_request]

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Dependency Review
      uses: actions/dependency-review-action@v3
      with:
        fail-on-severity: high
        fail-on-scopes: runtime
```

**AI Insights:**
- Known vulnerabilities in new dependencies
- License compliance issues
- Breaking changes in updates
- Alternative safer packages
- Dependency freshness score

## Trunk-Based Development Workflow

### Daily Workflow

```bash
# Morning: Sync with main
git checkout main
git pull origin main

# Create task branch
git checkout -b task/user-profile-api

# Work in small iterations (2-4 hours)
# First iteration: API endpoint
git add src/api/profile.ts
git commit -m "feat: add profile API endpoint"
git push origin task/user-profile-api
gh pr create --title "Add user profile API" --draft

# Continue work: Add tests
git add tests/profile.test.ts
git commit -m "test: add profile API tests"
git push

# Mark ready for review
gh pr ready
# Get review (should happen within hours)

# Merge same day
gh pr merge --squash --delete-branch

# Next task: Start fresh from main
git checkout main
git pull origin main
git checkout -b task/profile-ui
```

### Small, Frequent Commits Pattern

```bash
# ❌ Bad: Large infrequent commit
git add .
git commit -m "Add complete user profile feature with API, UI, tests, docs"
# 50 files changed, 2000 lines

# ✅ Good: Small frequent commits
git add src/api/profile.ts
git commit -m "feat: add profile API endpoint"
git push

git add src/components/ProfileCard.tsx
git commit -m "feat: add profile card component"
git push

git add tests/profile.test.ts
git commit -m "test: add profile tests"
git push

git add docs/profile.md
git commit -m "docs: document profile API"
git push

# Each commit: 1-3 files, 50-200 lines
# Easier reviews, faster merges, less conflicts
```

## Security Best Practices (2025)

1. **Enable Secret Scanning:**
```bash
# Repository Settings → Security → Secret scanning
# Enable: Push protection + AI detection
```

2. **Configure CodeQL:**
```bash
# Add .github/workflows/codeql.yml
# Enable for all languages in project
```

3. **Use Copilot Autofix:**
```bash
# Review security alerts weekly
# Apply Copilot-suggested fixes
# Test before merging
```

4. **Implement Trunk-Based Development:**
```bash
# Branch lifespan: <1 day
# Commit frequency: Every 2-4 hours
# Main branch: Always deployable
```

5. **Leverage GitHub Agents:**
```bash
# Automate: Bug triage, PR creation, dependency updates
# Review: All AI-generated code before merging
```

## Resources

- [Trunk-Based Development](https://trunkbaseddevelopment.com)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
- [GitHub Copilot for Security](https://github.com/features/security)

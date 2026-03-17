---
name: GitHub Workflow
description: GitHub workflow patterns for Orchestrator AI. Branch naming, PR process, code review, CI/CD. CRITICAL: Use conventional branch names (feature/, fix/, chore/). PRs require quality gates to pass. Use GitHub Actions for CI/CD.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# GitHub Workflow Skill

**CRITICAL**: Follow GitHub workflow patterns: conventional branch names, PR process, quality gates, code review.

## When to Use This Skill

Use this skill when:
- Creating branches
- Opening pull requests
- Setting up CI/CD
- Reviewing code
- Managing GitHub workflows

## Branch Naming Conventions

### ✅ CORRECT - Conventional Names

```bash
feature/user-authentication
feature/add-api-endpoint
fix/login-bug
fix/memory-leak
chore/update-dependencies
chore/refactor-service
docs/update-readme
test/add-unit-tests
```

### ❌ WRONG - Non-Conventional Names

```bash
❌ my-feature
❌ bugfix
❌ update
❌ new-stuff
❌ feature_branch (use hyphens, not underscores)
```

## Branch Types

| Type | Prefix | Example | Purpose |
|------|--------|---------|---------|
| Feature | `feature/` | `feature/user-auth` | New features |
| Bug Fix | `fix/` | `fix/login-error` | Bug fixes |
| Chore | `chore/` | `chore/update-deps` | Maintenance tasks |
| Documentation | `docs/` | `docs/api-guide` | Documentation updates |
| Test | `test/` | `test/unit-tests` | Test additions |
| Refactor | `refactor/` | `refactor/service-layer` | Code refactoring |

## PR Process

### Step 1: Create Branch

```bash
# Create feature branch
git checkout -b feature/user-authentication

# Or fix branch
git checkout -b fix/login-bug
```

### Step 2: Make Changes

```bash
# Edit files
vim apps/api/src/auth/auth.service.ts

# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat(auth): add user authentication"
```

### Step 3: Push Branch

```bash
# Push branch to remote
git push origin feature/user-authentication
```

### Step 4: Open PR

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill PR description:
   - What changed
   - Why changed
   - How to test
   - Screenshots (if UI changes)

### Step 5: Quality Gates

PR must pass:
- [ ] Code formatting (`npm run format`)
- [ ] Linting (`npm run lint`)
- [ ] Tests (`npm test`)
- [ ] Build (`npm run build`)

### Step 6: Code Review

- Request review from team members
- Address review comments
- Update PR as needed

### Step 7: Merge

Once approved and quality gates pass:
- Merge PR (squash and merge recommended)
- Delete branch after merge

## PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Feature
- [ ] Bug Fix
- [ ] Chore
- [ ] Documentation
- [ ] Refactor

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How to test these changes:
1. Step 1
2. Step 2
3. Step 3

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass locally
```

## CI/CD Workflow

### GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run format -- --check
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

## Code Review Guidelines

### What to Review

- [ ] Code follows project conventions
- [ ] No hardcoded values (use env vars)
- [ ] Error handling implemented
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No security issues
- [ ] Performance considerations

### Review Comments

```markdown
# Good review comment
```typescript
// Consider using environment variable instead of hardcoded value
const apiUrl = process.env.API_URL || 'http://localhost:7100';
```

```markdown
# Another good review comment
```typescript
// Should we add error handling here?
const result = await service.call();
```
```

## Common Workflow Patterns

### Pattern 1: Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat(module): add new feature"

# 3. Push and open PR
git push origin feature/new-feature
# Open PR on GitHub

# 4. Address review comments
git add .
git commit -m "fix(module): address review comments"
git push

# 5. Merge after approval
```

### Pattern 2: Hotfix

```bash
# 1. Create fix branch from main
git checkout main
git pull
git checkout -b fix/critical-bug

# 2. Fix and commit
git add .
git commit -m "fix(module): fix critical bug"

# 3. Push and open PR
git push origin fix/critical-bug
# Open PR, request urgent review

# 4. Merge immediately after approval
```

## Branch Protection Rules

Recommended branch protection for `main`:

- Require pull request reviews (at least 1)
- Require status checks to pass
  - Format check
  - Lint check
  - Test check
  - Build check
- Require branches to be up to date
- Do not allow force pushes
- Do not allow deletions

## Checklist for GitHub Workflow

When working with GitHub:

- [ ] Branch name follows convention (`feature/`, `fix/`, etc.)
- [ ] Commits use conventional commit format
- [ ] PR description is complete
- [ ] Quality gates pass before opening PR
- [ ] Code review requested
- [ ] Review comments addressed
- [ ] Branch deleted after merge

## Related Documentation

- **Conventional Commits**: See Conventional Commits Skill
- **Git Standards**: See Orchestrator Git Standards Skill
- **Quality Gates**: See Quality Gates Skill


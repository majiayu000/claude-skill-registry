---
name: Orchestrator Git Standards
description: Orchestrator AI-specific Git conventions and standards. Branch naming, commit workflow, repository organization. CRITICAL: Follow conventional branch names, use conventional commits, maintain clean git history.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Orchestrator Git Standards Skill

**CRITICAL**: Follow Orchestrator AI Git standards: conventional branch names, conventional commits, clean history.

## When to Use This Skill

Use this skill when:
- Creating branches
- Making commits
- Organizing git workflow
- Following project Git standards

## Branch Naming Standards

### ✅ CORRECT

```bash
feature/user-authentication
feature/add-api-endpoint
fix/login-bug
fix/memory-leak
chore/update-dependencies
chore/refactor-service
docs/update-readme
test/add-unit-tests
refactor/auth-service
```

### ❌ WRONG

```bash
❌ my-feature
❌ bugfix
❌ update
❌ feature_branch
❌ FEATURE-BRANCH
❌ feature/user authentication (spaces)
```

## Commit Message Standards

See **Conventional Commits Skill** for complete format. Quick reference:

```bash
# Format
<type>(<scope>): <description>

# Examples
feat(auth): add user authentication
fix(api): resolve memory leak
chore(deps): update dependencies
docs(readme): update installation guide
test(auth): add unit tests for auth service
refactor(api): restructure service layer
```

## Git Workflow Pattern

### 1. Create Branch

```bash
# From main
git checkout main
git pull

# Create feature branch
git checkout -b feature/user-authentication
```

### 2. Make Changes

```bash
# Edit files
vim apps/api/src/auth/auth.service.ts

# Stage changes
git add .

# Commit with conventional format
git commit -m "feat(auth): add user authentication service"
```

### 3. Push and PR

```bash
# Push branch
git push origin feature/user-authentication

# Open PR on GitHub
# Follow PR process (see GitHub Workflow Skill)
```

### 4. Update Branch

```bash
# If main has new commits
git checkout main
git pull
git checkout feature/user-authentication
git rebase main  # or git merge main
```

## Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add login` |
| `fix` | Bug fix | `fix(api): resolve memory leak` |
| `chore` | Maintenance | `chore(deps): update packages` |
| `docs` | Documentation | `docs(readme): update install` |
| `test` | Tests | `test(auth): add unit tests` |
| `refactor` | Refactoring | `refactor(api): restructure` |
| `style` | Formatting | `style: format code` |
| `perf` | Performance | `perf(api): optimize query` |

## Scope Guidelines

Scopes should match affected areas:

```bash
# API scopes
feat(api): add endpoint
fix(api): resolve bug

# Module scopes
feat(auth): add authentication
fix(llm): resolve provider issue

# Feature scopes
feat(agents): add new agent type
fix(webhooks): resolve status tracking
```

## Git History Best Practices

### ✅ DO

- Keep commits focused (one logical change per commit)
- Use descriptive commit messages
- Write clear commit descriptions
- Rebase before PR (clean history)
- Squash commits in PR if needed

### ❌ DON'T

- Don't commit unrelated changes together
- Don't use vague commit messages
- Don't force push to shared branches
- Don't commit broken code
- Don't commit secrets or credentials

## Commit Message Examples

### ✅ Good Commit Messages

```bash
feat(auth): add JWT token authentication

- Implement JWT token generation
- Add token validation middleware
- Update auth service with token logic

fix(api): resolve memory leak in service

The service was holding references to completed requests.
Now properly cleans up after request completion.

chore(deps): update NestJS to v10

- Update @nestjs/core to 10.0.0
- Update @nestjs/common to 10.0.0
- Resolve breaking changes
```

### ❌ Bad Commit Messages

```bash
❌ fix stuff
❌ update
❌ changes
❌ WIP
❌ asdf
❌ fixed bug
```

## Branch Organization

### Main Branches

- `main` - Production-ready code
- `develop` - Integration branch (if used)

### Feature Branches

```bash
feature/<feature-name>
# Examples:
feature/user-authentication
feature/add-metrics-dashboard
```

### Fix Branches

```bash
fix/<fix-name>
# Examples:
fix/login-error
fix/memory-leak
```

### Chore Branches

```bash
chore/<chore-name>
# Examples:
chore/update-dependencies
chore/refactor-service-layer
```

## Git Commands Reference

### Common Commands

```bash
# Create branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit
git commit -m "feat(module): description"

# Push
git push origin feature/my-feature

# Update from main
git checkout main
git pull
git checkout feature/my-feature
git rebase main

# View status
git status

# View log
git log --oneline

# View changes
git diff
```

## Repository Organization

### Directory Structure

```
orchestrator-ai/
├── apps/
│   ├── api/          # NestJS backend
│   ├── web/          # Vue frontend
│   └── n8n/          # N8N workflows
├── storage/          # Database snapshots
├── scripts/          # Utility scripts
└── .github/          # GitHub workflows
```

### Ignore Patterns

`.gitignore` should include:
- `node_modules/`
- `.env`
- `dist/`
- `*.log`
- `.DS_Store`

## Checklist for Git Standards

When working with Git:

- [ ] Branch name follows convention (`feature/`, `fix/`, etc.)
- [ ] Commit message follows conventional format
- [ ] Commit is focused (one logical change)
- [ ] Commit message is descriptive
- [ ] No secrets or credentials committed
- [ ] Code quality gates pass before commit
- [ ] Git history is clean (rebase if needed)

## Related Documentation

- **Conventional Commits**: See Conventional Commits Skill
- **GitHub Workflow**: See GitHub Workflow Skill
- **Quality Gates**: See Quality Gates Skill
- **Worktree Lifecycle**: See Worktree Lifecycle Skill


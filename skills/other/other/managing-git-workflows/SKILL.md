---
name: managing-git-workflows
description: Manage Git branching strategies, commit conventions, and collaboration workflows. Use when choosing between trunk-based development, GitHub Flow, or GitFlow, implementing conventional commits for automated versioning, setting up Git hooks for quality gates, or organizing monorepos with clear ownership.
---

# Git Workflows

Implement structured Git workflows for team collaboration, code quality, and automated releases. This skill covers branching strategies, conventional commit formats, Git hooks, and monorepo management patterns.

## When to Use This Skill

Use this skill when:
- Choosing a branching strategy for a new project or team
- Implementing consistent commit message formats
- Setting up Git hooks for linting, testing, or validation
- Managing monorepos with multiple projects
- Establishing code review workflows
- Automating versioning and releases

## Quick Decision: Which Branching Strategy?

### Trunk-Based Development
Use when the team has strong CI/CD automation, comprehensive test coverage (80%+), and deploys frequently (daily or more). Short-lived branches merge within 1 day. Requires feature flags for incomplete features.

**Best for:** High-velocity teams with mature DevOps practices (Google, Facebook, Netflix)

### GitHub Flow
Use for web applications with continuous deployment. Main branch always represents production. Simple PR-based workflow for small to medium teams (2-20 developers).

**Best for:** Startups, SaaS products, open-source projects

### GitFlow
Use when supporting multiple production versions simultaneously, requiring formal QA cycles, or following scheduled releases (monthly, quarterly). More complex but structured.

**Best for:** Enterprise software, mobile apps with App Store releases, on-premise products

For detailed branching patterns with examples, see `references/branching-strategies.md`.

## Conventional Commits

Structure commit messages for automated versioning and changelog generation:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Common Types:**
- `feat` - New feature (MINOR version bump: 0.1.0)
- `fix` - Bug fix (PATCH version bump: 0.0.1)
- `docs` - Documentation only
- `refactor` - Code restructuring without feature change
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

**Breaking Changes:**
- Add `!` after type: `feat!:` or `fix!:`
- Add `BREAKING CHANGE:` in footer
- Results in MAJOR version bump (1.0.0)

**Examples:**
```bash
git commit -m "feat(auth): add JWT token validation"
git commit -m "fix: resolve race condition in user login"
git commit -m "feat!: redesign authentication API

BREAKING CHANGE: Auth endpoints now require API version header"
```

For complete specification and tooling setup, see `references/conventional-commits.md`.

## Git Hooks for Quality Gates

Automate code quality checks at key workflow points:

**pre-commit** - Run before commit is created
- Linting (ESLint, Prettier)
- Formatting checks
- Quick tests

**commit-msg** - Validate commit message format
- Enforce conventional commits
- Check message length

**pre-push** - Run before pushing to remote
- Full test suite
- Prevent force push to protected branches

**Quick Setup with Husky:**
```bash
npm install --save-dev husky lint-staged @commitlint/cli @commitlint/config-conventional
npx husky init
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

For complete hook configuration and examples, see `references/git-hooks-guide.md`.

## Monorepo Management

### Build Tool Selection

**Nx** - Best for TypeScript/JavaScript monorepos
- Dependency graph analysis
- Affected commands (only rebuild changed projects)
- Distributed caching

**Turborepo** - Best for Next.js/React applications
- Fast incremental builds
- Remote caching
- Simple configuration

**Sparse Checkout** - For large repos when full clone not needed
```bash
git sparse-checkout init --cone
git sparse-checkout set apps/web libs/ui-components
```

### Code Ownership

Use `.github/CODEOWNERS` to define ownership:
```
# Default owners
* @org/engineering

# Apps ownership
/apps/web/ @org/web-team
/apps/mobile/ @org/mobile-team

# Security-critical
/libs/auth/ @org/security-team @org/principal-engineers
```

For detailed monorepo patterns, see `references/monorepo-patterns.md`.

## Merge vs Rebase

### Merge Commits
Use when preserving complete history is important:
```bash
git checkout main
git merge feature-branch
```
**When:** Multiple developers on feature branch, want to see integration point

### Squash and Merge
Use for clean, linear history:
```bash
git checkout main
git merge --squash feature-branch
git commit -m "feat: add user authentication"
```
**When:** Feature has many WIP commits, want clean main branch history

### Rebase
Use for linear history without merge commits:
```bash
git checkout feature-branch
git rebase main
```
**When:** Updating feature branch, working alone, cleaning up before PR

**⚠️ Never rebase:** Public branches (main, develop) or commits already pushed and used by others

## Code Review Workflows

### Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`:
```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Added tests
- [ ] Updated documentation
- [ ] Tests pass locally
```

### Branch Protection Rules

Enforce quality gates via repository settings:
- Require pull request reviews (2+ approvals)
- Require status checks (build, tests, lint)
- Require branches up to date before merging
- Restrict force pushes and deletions

For complete code review setup, see `references/code-review-workflows.md`.

## Branch Naming Conventions

Use consistent naming for clarity:
- `feature/user-authentication` - New features
- `bugfix/login-error` - Bug fixes
- `hotfix/critical-security-issue` - Urgent production fixes
- `docs/api-documentation` - Documentation changes
- `refactor/database-layer` - Code refactoring

Validate branch names with Git hooks (see `scripts/check-branch-name.sh`).

## Advanced Techniques

### Cherry-Picking for Hotfixes
Apply specific commits to other branches:
```bash
git checkout main
git commit -m "fix: resolve critical security issue"
# Commit hash: a1b2c3d

git checkout release/1.5
git cherry-pick a1b2c3d
```

### Git LFS for Large Files
Track large files separately from code:
```bash
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
git add .gitattributes
```

### Release Tagging
Mark production releases:
```bash
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

### Interactive Rebase
Clean up commit history before PR:
```bash
git rebase -i HEAD~3
# Squash WIP commits, reword messages, reorder commits
```

For detailed examples, see `examples/` directory.

## Automated Release Workflow

Combine conventional commits with CI/CD for automated versioning:

1. **Commits** - Follow conventional format
2. **Analysis** - Semantic Release analyzes commit types
3. **Version** - Determines MAJOR.MINOR.PATCH bump
4. **Changelog** - Auto-generates from commits
5. **Tag** - Creates Git tag
6. **Publish** - Deploys to npm, GitHub releases, etc.

See `examples/semantic-release-setup/` for complete configuration.

## Tool Recommendations

**Git Hooks:**
- Husky - Simplify hook management (most popular)
- lint-staged - Run linters only on staged files (performance)

**Commit Validation:**
- Commitlint - Enforce conventional commits
- Semantic Release - Automated versioning

**Monorepo Build:**
- Nx - TypeScript/JavaScript (Google, AWS use this)
- Turborepo - Next.js/React (Vercel)

**Large Files:**
- Git LFS - Store large binary files

All tools validated via Context7 with high trust scores (December 2025).

## Integration with Other Skills

**building-ci-pipelines** - Git workflows trigger CI/CD pipelines, branch protection enforces CI checks

**writing-github-actions** - GitHub Actions automate workflow steps (releases, PR checks)

**infrastructure-as-code** - IaC repos need structured workflows, GitOps uses Git as source of truth

**testing-strategies** - Git hooks enforce test requirements, pre-push runs test suites

**security-hardening** - Git hooks prevent secrets, signed commits verify identity, CODEOWNERS enforce security reviews

## Quick Reference

### Trunk-Based Development Workflow
```bash
git checkout -b feature/add-login main
git add .
git commit -m "feat: add login form component"
git rebase origin/main  # Stay up to date
git push origin feature/add-login
# PR → merge → delete branch (within 24 hours)
```

### GitHub Flow Workflow
```bash
git checkout -b feature/user-auth main
git commit -m "feat: add JWT authentication"
git commit -m "test: add auth tests"
git push origin feature/user-auth
# Open PR → review → merge → deploy → delete branch
```

### GitFlow Workflow
```bash
# Feature
git checkout -b feature/user-profile develop
git commit -m "feat: add user profile"
git checkout develop
git merge --no-ff feature/user-profile

# Release
git checkout -b release/1.1.0 develop
git checkout main
git merge --no-ff release/1.1.0
git tag -a v1.1.0 -m "Release 1.1.0"

# Hotfix
git checkout -b hotfix/critical-bug main
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.1.1 -m "Hotfix 1.1.1"
```

## Validation Scripts

Run automated checks:
- `scripts/validate-commit-msg.sh` - Validate commit message format
- `scripts/check-branch-name.sh` - Validate branch naming convention
- `scripts/setup-hooks.sh` - Automated hook installation

Execute scripts directly (token-free) for validation.

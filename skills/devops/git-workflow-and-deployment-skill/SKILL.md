---
name: git-workflow-deployment
description: Git branching strategy, CI/CD pipeline, quality gates, and deployment procedures for the omer-akben portfolio project. Use when working with git operations, deployments, or CI/CD workflows.
---

# Git Workflow & Deployment Skill

## Branch Strategy

**Production Branch:** `main` (auto-deploys to <https://omerakben.com/>)
**Staging Branch:** `pre-deployment` (all features branch from here)
**Feature Branches:** `feature/*` (branch from `pre-deployment`, merge back via PR)

### Critical Rules

1. **Always branch from `pre-deployment`** for new features
2. **All 6 quality gates MUST pass** before merging to `pre-deployment`
3. **Pre-deployment → main** auto-merges after all quality gates pass (no manual intervention)
4. **Never commit directly to main** - all production deployments go through `pre-deployment`

## Workflow Steps

```bash
# Start new feature
git checkout pre-deployment
git pull origin pre-deployment
git checkout -b feature/contact-collection

# Make changes and test locally
npm test && npm run lint && npx tsc --noEmit && npm run build && npm run size

# Commit and push
git commit -m "feat: add contact collection tool"
git push origin feature/contact-collection

# Create PR to pre-deployment
# After approval, merge to pre-deployment
# CI/CD auto-merges pre-deployment → main after all gates pass
```typescript

## CI/CD Auto-Merge Pipeline

When you push to `pre-deployment`, GitHub Actions automatically:

### 6 Quality Gates

Located in `.github/workflows/pre-deployment-to-main.yml`:

1. **Gate 1: ESLint** - 0 errors required
2. **Gate 2: TypeScript** - 0 errors required
3. **Gate 3: Unit Tests** - 776/776 passing required
4. **Gate 4: Production Build** - successful build required
5. **Gate 5: Bundle Size** - within limits required
6. **Gate 6: E2E Tests** - 66 passing, 14 skipped required

### Auto-Merge Process

If all gates pass:

- Fast-forward merge `pre-deployment` → `main`
- Creates deployment tag (`deploy-YYYYMMDD-HHMMSS`)
- Triggers Vercel production deployment

### Vercel Deployment

- `main` branch auto-deploys to <https://omerakben.com/>
- Environment variables from Vercel project settings
- Zero-downtime deployment

## Safety Mechanisms

- **No manual main commits**: All changes go through `pre-deployment` first
- **Atomic quality gates**: One failure blocks entire workflow
- **Fast-forward only**: Prevents merge conflicts, ensures linear history
- **Deployment tags**: Track every production deployment

## Quality Gate Commands

Before committing, run all quality checks:

```bash
# Run all quality gates locally
npm run lint                    # ESLint check
npx tsc --noEmit               # TypeScript check
npm test                        # Unit tests (776 tests)
npm run build                   # Production build
npm run analyze                 # Bundle analysis
npm run test:e2e               # E2E tests (66 tests)
```typescript

## Common Git Operations

### Create Feature Branch

```bash
git checkout pre-deployment
git pull origin pre-deployment
git checkout -b feature/your-feature-name
```typescript

### Update Feature Branch from Pre-deployment

```bash
git checkout pre-deployment
git pull origin pre-deployment
git checkout feature/your-feature-name
git merge pre-deployment
```typescript

### Sync with Remote

```bash
git fetch origin
git checkout pre-deployment
git pull origin pre-deployment
```typescript

## Deployment Checklist

Before pushing to `pre-deployment`:

- [ ] All 6 quality gates pass locally
- [ ] No TODO comments or console.log statements
- [ ] No hardcoded values or API keys
- [ ] Tests cover new functionality
- [ ] E2E tests account for SSR hydration timing
- [ ] Documentation updated (CLAUDE.md, README.md)
- [ ] Environment variables documented in `.env.example`

## Production Status

**Live Site:** <https://omerakben.com/>
**Status:** Production deployment active
**Deployment:** Vercel (main branch → production)

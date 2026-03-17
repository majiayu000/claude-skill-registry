---
name: cicd-pipeline
description: "CI/CD pipeline guide covering GitHub Actions, Lefthook hooks, Dependabot, and deployment scripts. Use when asking about workflows, automation, or deployment."
---

# CI/CD Pipeline Skill

Comprehensive guide to Ballee's CI/CD infrastructure including GitHub Actions, git hooks, scripts, and deployment processes.

## Overview

Ballee uses a multi-layered CI/CD approach:

1. **Local Git Hooks** (Lefthook) - Fast pre-commit/pre-push validation
2. **GitHub Actions** - PR quality checks, migrations, deployments
3. **Dependabot** - Automated security updates with auto-merge
4. **Vercel** - Production/staging deployments (automatic)

---

## Branch Strategy

```
main     → Production (protected, requires PR + Quality Gate)
dev      → Development/Staging (Dependabot target)
feat/*   → Feature branches (via git worktrees)
fix/*    → Bug fix branches
```

**Workflow**: `feat/branch` → PR to `dev` → PR to `main` → Production

---

## GitHub Actions Workflows

### Location: `.github/workflows/`

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `pr-quality-check.yml` | PR to main/develop | Lint, typecheck, test, build |
| `deploy-migrations.yml` | Push to main (*.sql) | Deploy migrations to production |
| `deploy-staging-migrations.yml` | Push to dev (*.sql) | Deploy migrations to staging |
| `sync-db-types.yml` | Push to dev (*.sql) | Auto-generate TypeScript types |
| `sentry-release.yml` | Deployment success | Create Sentry release + sourcemaps |
| `codeql.yml` | Push/PR + weekly schedule | Security vulnerability scanning |
| `dependabot-auto-merge.yml` | Dependabot PRs | Auto-merge patch/minor updates |
| `sync-prod-data-to-staging.yml` | Manual | Sync production data to staging |

### PR Quality Check (`pr-quality-check.yml`)

Runs on PRs targeting `main` or `develop`:

```yaml
Jobs:
  1. detect-changes    # Smart change detection
  2. oxlint           # Fast lint (~1 min) - fail-fast
  3. lint             # Full ESLint
  4. typecheck        # TypeScript validation
  5. test             # Unit + integration tests
  6. build            # Production build verification
  7. quality-gate     # Final approval status
```

**Key Features**:
- Cancels in-progress runs on new commits
- Skips irrelevant jobs based on changed files
- Parallel execution for speed

### Migration Deployment (`deploy-migrations.yml`)

Triggers on push to `main` with SQL changes:

```yaml
Steps:
  1. Validate migration files (no duplicates)
  2. Check pending migrations
  3. Apply via psql (supports complex SQL)
  4. Generate TypeScript types
  5. Create PR with type updates
```

**Connection**: Uses Supabase pooler (IPv4) for GitHub Actions compatibility

### Database Type Sync (`sync-db-types.yml`)

Auto-generates TypeScript types after migration changes:

```yaml
Trigger: Push to dev with *.sql changes
Output:
  - packages/supabase/src/database.types.ts
  - apps/web/lib/database.types.ts
```

---

## Local Git Hooks (Lefthook)

### Configuration: `lefthook.yml`

### Pre-commit Hooks (< 2 seconds target)

| Hook | Files | Purpose |
|------|-------|---------|
| `format` | *.ts,tsx,json,md... | Prettier auto-fix |
| `validate-wip` | WIP_*.md | WIP document validation |
| `validate-migrations` | *.sql | Migration syntax check |
| `validate-rls-policies` | *.sql | RLS security validation |
| `check-version-suffixes` | *.ts,tsx | Block -v2, -new naming |
| `validate-json-keys` | *.json | Detect duplicate keys |
| `validate-db-local` | *.ts,tsx,sql | DB contract validation |

### Pre-push Hooks (< 15 seconds default)

| Hook | Purpose |
|------|---------|
| `oxlint` | Fast lint sanity check |
| `lint` | Full ESLint (THOROUGH=1 only) |
| `typecheck` | Full TypeScript (THOROUGH=1 only) |
| `validate-lockfile` | pnpm-lock.yaml sync check |
| `validate-db-local` | DB validation |
| `validate-db-types` | Info about auto-sync |

### Usage

```bash
# Normal push (fast, ~15s)
git push

# Thorough push (full checks, ~5min)
THOROUGH=1 git push

# Skip hooks (emergency only)
git push --no-verify

# Skip specific hook
LEFTHOOK_EXCLUDE=check-version-suffixes git commit -m "..."
```

---

## Dependabot Configuration

### Location: `.github/dependabot.yml`

```yaml
Target Branch: dev
Schedule: Weekly (Monday 06:00 Europe/Zurich)

Ecosystems:
  - npm (security updates only)
  - github-actions (all updates)
```

### Auto-merge Workflow

```yaml
# .github/workflows/dependabot-auto-merge.yml
Behavior:
  - Patch/Minor: Auto-approve + auto-merge
  - Major: Comment notification, manual review required
```

---

## Reusable Actions

### Location: `.github/actions/`

#### `setup-node-pnpm`

Composite action for consistent Node.js setup:

```yaml
uses: ./.github/actions/setup-node-pnpm
with:
  node-version: '20'        # Default
  install-dependencies: 'true'
  cache-turbo: 'false'
  cache-nextjs: 'false'
```

**Features**:
- pnpm v10.14.0 setup
- Node.js with pnpm cache
- Optional Turbo/Next.js caching
- Frozen lockfile install

---

## Scripts

### Location: `scripts/`

### CI/CD Related Scripts

| Script | Purpose |
|--------|---------|
| `validate-db-local.sh` | Local DB contract validation |
| `validate-migrations.sh` | Migration file validation |
| `validate-json-keys.sh` | Detect duplicate JSON keys |
| `validate-wip.sh` | WIP document validation |
| `check-version-suffixes.sh` | Block forbidden naming patterns |
| `analyze-rls-policies.sh` | RLS security analysis |

### Deployment Scripts

| Script | Purpose |
|--------|---------|
| `deploy-production.sh` | Manual production deployment |
| `deploy-env-vars.sh` | Deploy env vars to Vercel |
| `apply-staging-migrations.sh` | Apply migrations to staging |
| `setup-staging-environment.sh` | Full staging setup |
| `setup-complete-staging.sh` | Complete staging rebuild |

### Utility Scripts

| Script | Purpose |
|--------|---------|
| `git-worktree.sh` | Git worktree management |
| `clean-env-vars.sh` | Clean trailing newlines from env |
| `update-supabase-email-templates.sh` | Deploy email templates |

---

## Environment Configuration

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `SUPABASE_PROJECT_ID` | Production project ID |
| `SUPABASE_DB_PASSWORD` | Production DB password |
| `SUPABASE_ACCESS_TOKEN` | Supabase management token |
| `STAGING_SUPABASE_PROJECT_ID` | Staging project ID |
| `STAGING_SUPABASE_DB_PASSWORD` | Staging DB password |
| `SENTRY_AUTH_TOKEN` | Sentry release token |
| `SENTRY_ORG` | Sentry organization |
| `SENTRY_PROJECT` | Sentry project name |

### GitHub Variables

| Variable | Description |
|----------|-------------|
| `ENABLE_DB_TYPE_SYNC` | Enable/disable type sync (default: true) |

---

## Vercel Deployment

Handled automatically by Vercel GitHub integration:

```
Push to dev  → Staging deployment (preview)
Push to main → Production deployment
```

**Environment Variables**: Managed via Vercel dashboard or `vercel env` CLI

---

## Common Commands

### Manual Workflow Triggers

```bash
# Deploy migrations to production
gh workflow run deploy-migrations.yml --ref main

# Deploy migrations to staging
gh workflow run deploy-staging-migrations.yml --ref dev

# Force regenerate DB types
gh workflow run sync-db-types.yml --ref dev -f force=true

# Create Sentry release
gh workflow run sentry-release.yml -f environment=production

# Sync prod data to staging
gh workflow run sync-prod-data-to-staging.yml
```

### View Workflow Status

```bash
# List recent runs
gh run list

# View specific run
gh run view <run-id>

# Watch run in progress
gh run watch
```

---

## Troubleshooting

### Migration Deployment Fails

**IPv6 Connection Error**:
- Workflows use IPv4 pooler (`aws-1-eu-central-1.pooler.supabase.com`)
- Already configured, but check if Supabase changed endpoints

**Prepared Statement Error**:
- Workflows use `psql` directly, not `supabase db push`
- Complex SQL with multiple statements is supported

**SASL Authentication Failed**:
- Check `SUPABASE_DB_PASSWORD` secret is correct
- Verify using port 5432 (session mode) not 6543 (transaction mode)

### Pre-push Hook Slow

```bash
# Use fast mode (default)
git push

# Only use thorough mode when needed
THOROUGH=1 git push
```

### Lefthook Not Running

```bash
# Reinstall hooks
lefthook install

# Check installation
lefthook run pre-commit
```

### Dependabot Not Auto-merging

1. Verify auto-merge is enabled: `gh repo view --json autoMergeAllowed`
2. Check branch protection rules allow auto-merge
3. Ensure CI passes before merge

---

## Security Considerations

1. **CodeQL** runs weekly + on PRs for vulnerability scanning
2. **Dependabot** monitors security advisories
3. **RLS validation** in pre-commit hooks
4. **No secrets in logs** - use GitHub Secrets
5. **Protected branches** require PR reviews

---

## Related Documentation

- `.github/WORKFLOWS.md` - Detailed workflow architecture
- `.github/REPOSITORY_SAFEGUARDS.md` - Branch protection setup
- `CLAUDE.md` - Overall project guidelines

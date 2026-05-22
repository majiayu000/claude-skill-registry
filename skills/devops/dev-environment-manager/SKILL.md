---
name: "dev-environment-manager"
description: "Manage local development environment, database resets, health checks, deployment validation, production data sync, and Vercel environment variables; use when setting up dev environment, resetting databases, running pre-deployment checks, syncing production data to staging/local, or fixing Vercel env vars with trailing newlines"
version: "3.1.0"
last_updated: "2025-12-23"
aliases:
  - "vercel-env-fix"
  - "fix-env-vars"
  - "env-manager"
---

# Dev Environment Manager

## When to Use This Skill

Use this skill when:
- Setting up or resetting local development environment
- Running health checks on databases
- Validating environment before deployment
- **Syncing production data to local or staging**

## Quick Commands (Recommended)

The easiest way to reset and sync your local database:

```bash
# Reset local DB + sync from STAGING (default)
pnpm supabase:web:reset

# Reset local DB + sync from PRODUCTION
pnpm supabase:web:reset --prod

# Reset local DB only (no data sync)
pnpm supabase:reset:no-sync
```

These commands:
1. Apply all migrations (reset schema)
2. Sync data from staging/production
3. Include auth.users for login testing

**Login locally with any synced user email + password `password`**

## Full Sync Workflow: Production → Staging → Local

For a complete refresh of all environments:

```bash
# Step 1: Sync production data to staging
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh --confirm --yes

# Step 2: Reset local and sync from staging
pnpm supabase:web:reset
```

This ensures staging mirrors production, then local mirrors staging.

## Scripts

**Location**: `.claude/skills/dev-environment-manager/scripts/`

| Script | Description |
|--------|-------------|
| `sync-prod-to-staging.sh` | **Copy production data to staging** (READ-only from prod) |
| `sync-prod-to-local.sh` | **Copy production data to local** (READ-only from prod) |
| `sync-remote-to-local.sh` | **Unified sync script** (staging or prod to local) |
| `reset-local-dev.sh` | Complete local database reset with optional production sync |
| `health-check.sh` | Database health verification |
| `pre-deployment-checks.sh` | Pre-deployment validation |
| `fix-production-env-vars.sh` | Fix production environment variables |
| `verify-production-env-vars.sh` | Verify production env vars are set |

## Data Sync Details

### Safety Guarantees

All sync scripts have **multiple safety layers** to prevent accidental production writes:

1. **Read-only production connection** - Scripts only construct READ connections to production
2. **Explicit confirmation required** - Must pass `--confirm` flag AND type confirmation text
3. **Target verification** - Scripts verify the target database before writing
4. **Clear visual warnings** - Red warning banners before any destructive operation

### Sync Production → Staging

```bash
# Preview what will happen (safe, no changes)
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh

# Execute the sync (requires confirmation)
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh --confirm

# Skip interactive prompt
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh --confirm --yes
```

**What it does:**
1. READ all public + auth schema data from production
2. ERASE all data in staging
3. COPY production data to staging
4. Verify row counts match

**Production is NEVER modified.**

### Sync to Local (Staging or Production)

```bash
# Sync from STAGING (default)
pnpm supabase:web:reset

# Sync from PRODUCTION
pnpm supabase:web:reset --prod

# Or use scripts directly:
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-local.sh --confirm --yes
```

**What it does:**
1. Reset local database (apply all migrations)
2. READ all data from staging/production
3. COPY data to local (includes auth.users)
4. Verify row counts match

### Credentials

Scripts automatically load credentials from:
1. `.env.local` (preferred)
2. 1Password (fallback, then cached to .env.local)

Required environment variables:
- `SUPABASE_DB_PASSWORD_PROD` - Production database password
- `SUPABASE_DB_PASSWORD_STAGING` - Staging database password

## Quick Start Examples

### Fresh Local Setup (Most Common)

```bash
# Start local Supabase + reset with staging data
pnpm supabase:web:start
pnpm supabase:web:reset
```

### Refresh All Environments

```bash
# Full sync: prod → staging → local
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh --confirm --yes
pnpm supabase:web:reset
```

### Reset Without Sync

```bash
# Fresh migrations, no external data
pnpm supabase:reset:no-sync
```

### Pre-Deployment

```bash
# Run all checks before deploying
./.claude/skills/dev-environment-manager/scripts/pre-deployment-checks.sh
```

## Database References

| Environment | Project Ref | Host | Port |
|-------------|-------------|------|------|
| Production | `csjruhqyqzzqxnfeyiaf` | `aws-1-eu-central-1.pooler.supabase.com` | 5432 |
| Staging | `hxpcknyqswetsqmqmeep` | `aws-1-eu-central-1.pooler.supabase.com` | 5432 |
| Local | N/A | `127.0.0.1` | 54322 |

## Troubleshooting

### "Local Supabase is not running"

```bash
cd apps/web && pnpm supabase start
```

### "Failed to get password from 1Password"

```bash
# Authenticate with 1Password
op signin

# Or set credentials manually in apps/web/.env.local:
SUPABASE_DB_PASSWORD_PROD="your-password"
SUPABASE_DB_PASSWORD_STAGING="your-password"
```

### "Connection timeout"

- Ensure you're using `aws-1-eu-central-1.pooler.supabase.com` (not aws-0)
- Check network/VPN connection
- Verify credentials are correct

### Resetting Remote Database (Staging)

**WARNING**: `supabase db reset` has `--local=true` by default!

```bash
# WRONG - This resets BOTH local AND staging!
supabase db reset --db-url "postgresql://staging..."

# CORRECT - Only reset staging
supabase db reset --db-url "postgresql://staging..." --local=false
```

For staging schema reset, prefer using the sync script which handles this correctly:
```bash
./.claude/skills/dev-environment-manager/scripts/sync-prod-to-staging.sh --confirm --yes
```

## Vercel Environment Variables

### Fix Trailing Newlines

Vercel env vars sometimes get trailing `\n` characters that break API connections.

```bash
# Fix production only (interactive)
./.claude/skills/dev-environment-manager/scripts/fix-production-env-vars.sh

# Fix production only (non-interactive)
./.claude/skills/dev-environment-manager/scripts/fix-production-env-vars.sh --yes

# Fix preview/staging only
./.claude/skills/dev-environment-manager/scripts/fix-production-env-vars.sh --env preview --yes

# Fix ALL environments (preview + production)
./.claude/skills/dev-environment-manager/scripts/fix-production-env-vars.sh --env all --yes
```

**What it does:**
1. Pulls current env vars from Vercel
2. Finds vars with trailing `\n` characters
3. Removes and re-adds them using `echo -n` (no trailing newline)
4. Verifies the fix worked

### Verify Environment Variables

```bash
./.claude/skills/dev-environment-manager/scripts/verify-production-env-vars.sh
```

## Related Skills

- `production-database-query` - Query production/staging databases
- `database-migration-manager` - Create and apply migrations

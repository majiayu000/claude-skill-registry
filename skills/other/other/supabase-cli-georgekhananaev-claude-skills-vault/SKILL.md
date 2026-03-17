---
name: supabase-cli
description: CLI automation for Supabase development workflows. Provides scripts for migrations, Edge Functions, secrets management, type generation, and SQL execution with safety checks.
---

# Supabase CLI

CLI automation and operational tooling for Supabase development workflows. This skill provides scripts and utilities for common Supabase operations with built-in safety checks.

## When to Use

Invoke when:
- Creating or applying database migrations
- Deploying Edge Functions
- Managing Supabase secrets
- Generating TypeScript types from schema
- Executing SQL with safety checks
- Checking for schema drift
- Validating environment configuration

## Prerequisites

### Required Tools

```bash
# Supabase CLI
brew install supabase/tap/supabase
# or: npm install -g supabase

# Verify installation
supabase --version
```

### Environment Variables

Before running scripts, validate credentials with:

```bash
python3 .claude/skills/supabase-cli/scripts/validate_env.py
```

Required variables:
| Variable | Description | Required For |
|----------|-------------|--------------|
| `SUPABASE_URL` | Project URL | All operations |
| `SUPABASE_ANON_KEY` | Public/anon key | Client operations |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key | Admin operations |
| `POSTGRES_DB` | Direct PostgreSQL URL | Migrations, SQL |
| `SUPABASE_ACCESS_TOKEN` | CLI access token | `supabase link`, `db push`, `gen types` |

### Getting the Supabase Access Token

The access token is required for CLI operations like linking projects, pushing migrations, and generating types.

**How to get your token:**

1. Go to https://supabase.com/dashboard/account/tokens
2. Click **"Generate new token"**
3. Give it a name (e.g., "CLI Development")
4. Copy the token (starts with `sbp_`)

**How to use it:**

Option 1: Store in `.env.local` (recommended for projects):
```bash
# .env.local (add to .gitignore!)
SUPABASE_ACCESS_TOKEN=sbp_your_token_here
```

Option 2: Export in terminal session:
```bash
export SUPABASE_ACCESS_TOKEN="sbp_your_token_here"
```

Option 3: Interactive login (opens browser):
```bash
supabase login
```

**Link your project** (required before pushing migrations):
```bash
# Extract project ref from your SUPABASE_URL (the subdomain)
# Example: https://abcdefghijkl.supabase.co → project ref is "abcdefghijkl"
supabase link --project-ref <your-project-ref>
```

## Quick Reference

| Task | Script | Example |
|------|--------|---------|
| Validate env | `validate_env.py` | `python3 scripts/validate_env.py` |
| New migration | `migration_new.ts` | `bun scripts/migration_new.ts add-users` |
| Apply migrations | `migration_apply.ts` | `bun scripts/migration_apply.ts --local` |
| Generate types | `update_types.ts` | `bun scripts/update_types.ts` |
| Run SQL safely | `safe_sql_runner.ts` | `bun scripts/safe_sql_runner.ts --query "SELECT 1"` |
| Check drift | `check_drift.sh` | `bash scripts/check_drift.sh` |
| New Edge Function | `func_new.ts` | `bun scripts/func_new.ts my-function` |
| Deploy function | `func_deploy.ts` | `bun scripts/func_deploy.ts my-function` |
| Sync secrets | `secret_sync.py` | `python3 scripts/secret_sync.py --dry-run` |
| Manage secrets | `manage_secrets.py` | `python3 scripts/manage_secrets.py list` |
| Reset local DB | `reset_local.ts` | `bun scripts/reset_local.ts` |
| Run DB tests | `test_db.ts` | `bun scripts/test_db.ts` |
| Scaffold RLS | `scaffold_rls.ts` | `bun scripts/scaffold_rls.ts users --tenant` |

## Workflow Patterns

### Migration Workflow

1. **Create migration:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/migration_new.ts add_user_roles
   ```

2. **Edit the generated file** in `supabase/migrations/`

3. **Apply locally first:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/migration_apply.ts --local
   ```

4. **Check for drift:**
   ```bash
   bash .claude/skills/supabase-cli/scripts/check_drift.sh
   ```

5. **Apply to remote (with confirmation):**
   ```bash
   bun .claude/skills/supabase-cli/scripts/migration_apply.ts --remote --confirm
   ```

6. **Update TypeScript types:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/update_types.ts
   ```

### Edge Function Development

1. **Scaffold new function:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/func_new.ts webhook-handler --template webhook
   ```

2. **Test locally:**
   ```bash
   supabase functions serve webhook-handler
   ```

3. **Deploy:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/func_deploy.ts webhook-handler
   ```

### Secret Management

1. **Sync .env to remote:**
   ```bash
   python3 .claude/skills/supabase-cli/scripts/secret_sync.py --prefix APP_ --dry-run
   python3 .claude/skills/supabase-cli/scripts/secret_sync.py --prefix APP_
   ```

2. **List remote secrets:**
   ```bash
   python3 .claude/skills/supabase-cli/scripts/manage_secrets.py list
   ```

### Local Development Cycle

1. **Reset and reseed local database:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/reset_local.ts
   ```

2. **Run database tests:**
   ```bash
   bun .claude/skills/supabase-cli/scripts/test_db.ts
   ```

### RLS Policy Scaffolding

Generate RLS policies for new tables:

```bash
# Standard user-based policies
bun .claude/skills/supabase-cli/scripts/scaffold_rls.ts products

# Multi-tenant policies (for restaurant_id based isolation)
bun .claude/skills/supabase-cli/scripts/scaffold_rls.ts orders --tenant

# Output to migration file
bun .claude/skills/supabase-cli/scripts/scaffold_rls.ts menu_items --tenant --output supabase/migrations/015_rls.sql
```

## Safety Guidelines

### SQL Classification

Scripts classify SQL statements by risk level:

| Level | Statements | Behavior |
|-------|------------|----------|
| **Safe** | SELECT, EXPLAIN, SHOW | Execute immediately |
| **Write** | INSERT, UPDATE, DELETE, ALTER, CREATE | Require transaction wrap |
| **Dangerous** | DROP, TRUNCATE, DELETE (no WHERE) | Require `--confirm` flag |

### Remote Operation Rules

The following require explicit `--confirm` flag:
- Migrations to remote database
- Dangerous SQL on remote
- Secret deletion

### Pre-Deployment Checks

Before deploying Edge Functions:
- TypeScript compilation check
- Function file existence validation
- Size limits verification

## References

For detailed information:

| Topic | Reference File |
|-------|---------------|
| CLI commands | `references/cli-commands.md` |
| Migration patterns | `references/migration-patterns.md` |
| Troubleshooting | `references/troubleshooting.md` |

## Error Handling

When scripts detect missing credentials, they output in this format:

```
MISSING: SUPABASE_SERVICE_ROLE_KEY
ASK_USER: Please provide your Supabase Service Role Key.
LOCATION: Dashboard > Project Settings > API > service_role key
```

Claude should parse this and use AskUserQuestion to prompt for the missing credential.

## Integration

**Pairs with:**

- `/plan-feature` - Database schema design during feature planning
- `brainstorm` - Architecture decisions before migrations
- `beautiful-code` - TypeScript type generation quality

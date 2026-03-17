---
name: "database-migration-manager"
description: "Create production-ready Supabase migrations for Ballee following strict naming conventions, idempotent SQL, RLS patterns, and storage bucket policies; use when user requests schema changes, adding columns, RLS policies, database functions, or storage buckets"
version: "1.2.0"
last_updated: "2025-12-11"
---

# Database Migration Manager

## When to Use This Skill

Use this skill when the user requests:
- "Create a migration to..."
- "Add a column/table/index/constraint to..."
- "Modify the schema..."
- "Update RLS policies..."
- "Create/modify a database function..."
- "Create a storage bucket..."
- "Update storage RLS policies..."
- Any database structure changes

## Critical Rules (NEVER VIOLATE)

### 1. **NO VERSION SUFFIXES** ❌
- FORBIDDEN: `_v2`, `_v3`, `_new`, `_old`, `_enhanced`, `_improved`, `_better`, `_optimized`, `_simplified`, `_modern`, `_updated`, `_modified`, `_refactored`, `_temp`, `_tmp`, `_draft`, `_test`, `_backup`, `_copy`
- Fix problems properly the first time - quality is built in, not added later

### 2. **Migration Naming Format** ✅
```
YYYYMMDDHHMMSS_descriptive_name.sql
```

**Examples**:
- ✅ `20251020143000_add_notes_to_events.sql`
- ✅ `20251020144500_create_rehearsals_table.sql`
- ✅ `20251020150000_update_events_rls_policies.sql`
- ❌ `20251020143000_add_notes_v2.sql` (version suffix)
- ❌ `migration_notes.sql` (wrong format)
- ❌ `add_notes.sql` (missing timestamp)

### 3. **Location** 📁
```
apps/web/supabase/migrations/
```

### 4. **Idempotent SQL Required** 🔄
All DDL MUST use idempotent patterns:

```sql
-- ✅ CORRECT - Idempotent
ALTER TABLE events ADD COLUMN IF NOT EXISTS notes text;
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
DROP POLICY IF EXISTS events_select ON events;

-- ❌ WRONG - Not idempotent
ALTER TABLE events ADD COLUMN notes text;
CREATE INDEX idx_events_status ON events(status);
```

### 5. **RLS Patterns** 🔒
Always use proper RLS patterns from the codebase:

```sql
-- Enable RLS on new tables
ALTER TABLE "public"."table_name" ENABLE ROW LEVEL SECURITY;

-- Revoke default permissions
REVOKE ALL ON public.table_name FROM authenticated, service_role;

-- Grant specific permissions
GRANT select, insert, update, delete ON TABLE public.table_name TO authenticated;

-- Standard RLS policy pattern (drop/create for idempotency)
DROP POLICY IF EXISTS table_name_select ON public.table_name;

CREATE POLICY table_name_select ON public.table_name
FOR SELECT TO authenticated
USING (
  public.is_super_admin() OR
  account_id = (SELECT auth.uid())
);
```

### 6. **Super Admin Bypass Pattern** 👨‍💼
Use `public.is_super_admin()` for admin operations:

```sql
-- SELECT: Super admin sees all, others see their own
CREATE POLICY table_select ON public.table_name
FOR SELECT TO authenticated
USING (
  public.is_super_admin() OR
  account_id = auth.uid()
);

-- INSERT/UPDATE/DELETE: Super admin can do anything, others restricted
CREATE POLICY table_insert ON public.table_name
FOR INSERT TO authenticated
WITH CHECK (
  public.is_super_admin() OR
  account_id = auth.uid()
);
```

## Migration Template

```sql
-- =====================================================================================
-- {Brief description of what this migration does}
-- =====================================================================================
--
-- {Detailed explanation if needed}
-- {Why this change is being made}
-- {Business context}
--
-- =====================================================================================

-- =====================================================================================
-- STEP 1: {First logical group of changes}
-- =====================================================================================

-- Add column (idempotent)
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS column_name data_type;

-- Add NOT NULL constraint (with validation)
ALTER TABLE public.table_name
ALTER COLUMN column_name SET NOT NULL;

-- Add comment
COMMENT ON COLUMN public.table_name.column_name IS
  'Description of what this column stores';

-- =====================================================================================
-- STEP 2: {Second logical group of changes}
-- =====================================================================================

-- Create index (idempotent, concurrent for large tables)
CREATE INDEX IF NOT EXISTS idx_table_column
ON public.table_name (column_name);

-- =====================================================================================
-- STEP 3: Update RLS policies
-- =====================================================================================

-- Drop existing policies (for idempotency)
DROP POLICY IF EXISTS table_select ON public.table_name;
DROP POLICY IF EXISTS table_insert ON public.table_name;

-- Create new policies
CREATE POLICY table_select ON public.table_name
FOR SELECT TO authenticated
USING (
  public.is_super_admin() OR
  account_id = auth.uid()
);

CREATE POLICY table_insert ON public.table_name
FOR INSERT TO authenticated
WITH CHECK (
  public.is_super_admin() OR
  account_id = auth.uid()
);
```

## Storage Bucket Migrations

### Creating a New Storage Bucket

```sql
-- =====================================================================================
-- Create {bucket_name} storage bucket with RLS
-- =====================================================================================

-- Create the bucket (idempotent - checks if exists)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'my-documents',           -- id (used in code)
  'my-documents',           -- name (display name)
  false,                    -- public (false = requires signed URLs)
  10485760,                 -- file_size_limit (10MB in bytes)
  ARRAY['image/jpeg', 'image/png', 'application/pdf']  -- allowed types
)
ON CONFLICT (id) DO NOTHING;

-- =====================================================================================
-- RLS Policy for {bucket_name} bucket
-- =====================================================================================

-- Drop existing policy for idempotency
DROP POLICY IF EXISTS my_documents ON storage.objects;

-- Create RLS policy with super admin bypass
CREATE POLICY my_documents ON storage.objects FOR ALL USING (
  bucket_id = 'my-documents'
  AND (
    -- Super admin can access all files
    public.is_super_admin()
    OR
    -- User owns the file (path starts with their user_id)
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
)
WITH CHECK (
  bucket_id = 'my-documents'
  AND (
    -- Super admin can upload/modify all files
    public.is_super_admin()
    OR
    -- User can only upload to their own folder
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
);
```

### Storage Bucket Patterns

**Pattern 1: User-Based (path = user_id/...)**
```sql
CREATE POLICY user_files ON storage.objects FOR ALL USING (
  bucket_id = 'user-files'
  AND (
    public.is_super_admin() OR
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
)
WITH CHECK (
  bucket_id = 'user-files'
  AND (
    public.is_super_admin() OR
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
);
```

**Pattern 2: Account-Based (filename = account_uuid.ext)**
```sql
CREATE POLICY account_files ON storage.objects FOR ALL USING (
  bucket_id = 'account-files'
  AND (
    public.is_super_admin() OR
    kit.get_storage_filename_as_uuid(name) = auth.uid() OR
    public.has_role_on_account(kit.get_storage_filename_as_uuid(name))
  )
)
WITH CHECK (
  bucket_id = 'account-files'
  AND (
    public.is_super_admin() OR
    kit.get_storage_filename_as_uuid(name) = auth.uid() OR
    public.has_permission(auth.uid(), kit.get_storage_filename_as_uuid(name), 'settings.manage')
  )
);
```

**Pattern 3: Entity-Based (linked to database table)**
```sql
CREATE POLICY entity_documents ON storage.objects FOR ALL USING (
  bucket_id = 'entity-documents'
  AND (
    public.is_super_admin() OR
    EXISTS (
      SELECT 1 FROM entities e
      WHERE e.id = (string_to_array(name, '/'))[1]::uuid
      AND e.user_id = auth.uid()
    )
  )
)
WITH CHECK (
  bucket_id = 'entity-documents'
  AND (
    public.is_super_admin() OR
    EXISTS (
      SELECT 1 FROM entities e
      WHERE e.id = (string_to_array(name, '/'))[1]::uuid
      AND e.user_id = auth.uid()
    )
  )
);
```

### Adding Super Admin Bypass to Existing Bucket

```sql
-- =====================================================================================
-- Add super admin bypass to {bucket_name} storage bucket
-- =====================================================================================

-- Drop existing policy
DROP POLICY IF EXISTS {bucket_name} ON storage.objects;

-- Create new policy with is_super_admin() bypass
CREATE POLICY {bucket_name} ON storage.objects FOR ALL USING (
  bucket_id = '{bucket_name}'
  AND (
    public.is_super_admin() OR
    -- existing conditions here
  )
)
WITH CHECK (
  bucket_id = '{bucket_name}'
  AND (
    public.is_super_admin() OR
    -- existing conditions here
  )
);
```

### Important: Update StorageBuckets Constant

After creating a new bucket, add it to `packages/shared/src/storage/storage-url.service.ts`:

```typescript
export const StorageBuckets = {
  // ... existing buckets
  MY_DOCUMENTS: 'my-documents',  // Add new bucket constant
} as const;
```

## Security Definer Functions (Advanced)

When creating functions with elevated privileges:

```sql
-- NEVER create security definer without explicit access controls
CREATE OR REPLACE FUNCTION public.function_name(param_name param_type)
RETURNS return_type
LANGUAGE plpgsql
SECURITY DEFINER  -- Elevated privileges
SET search_path = '' -- Prevent SQL injection
AS $$
BEGIN
  -- CRITICAL: Validate permissions FIRST
  IF NOT public.is_super_admin() THEN
    RAISE EXCEPTION 'Unauthorized: Super admin access required';
  END IF;

  -- Additional validation
  IF param_name IS NULL OR length(param_name) < 3 THEN
    RAISE EXCEPTION 'Invalid parameter: %', param_name;
  END IF;

  -- Now safe to proceed with elevated privileges
  -- ... function logic ...
END;
$$;

-- Grant to authenticated users only
GRANT EXECUTE ON FUNCTION public.function_name(param_type) TO authenticated;
```

## Common Patterns

### Adding a Column
```sql
-- Add nullable column (safe)
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS column_name text;

-- Add column with default (safe)
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS is_active boolean DEFAULT false NOT NULL;

-- ❌ UNSAFE: Adding non-null without default
-- ALTER TABLE public.table_name ADD COLUMN required_field text NOT NULL;
```

### Creating a Table
```sql
CREATE TABLE IF NOT EXISTS public.table_name (
  id uuid PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
  account_id uuid REFERENCES public.accounts(id) ON DELETE CASCADE NOT NULL,
  name text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Enable RLS
ALTER TABLE "public"."table_name" ENABLE ROW LEVEL SECURITY;

-- Revoke defaults
REVOKE ALL ON public.table_name FROM authenticated, service_role;

-- Grant permissions
GRANT select, insert, update, delete ON TABLE public.table_name TO authenticated;

-- Add RLS policies (see template above)
```

### Modifying RLS Policies
```sql
-- Always drop before creating (idempotency)
DROP POLICY IF EXISTS policy_name ON public.table_name;

CREATE POLICY policy_name ON public.table_name
FOR operation TO authenticated
USING (condition);
```

## Workflow Steps

1. **Read Existing Migrations** - Understand current schema patterns
2. **Generate Timestamp** - Use current timestamp in format `YYYYMMDDHHMMSS`
3. **Create File** - In `apps/web/supabase/migrations/`
4. **Write Idempotent SQL** - Use templates above
5. **Test Locally** - Run `pnpm supabase:reset`
6. **Regenerate Types** - Run `pnpm supabase:typegen`
7. **Commit & Push** - Auto-deploys via GitHub Actions

## Validation Checklist

Before creating migration:
- [ ] Timestamp format is `YYYYMMDDHHMMSS`
- [ ] Descriptive name (no version suffixes)
- [ ] File in `apps/web/supabase/migrations/`
- [ ] All DDL is idempotent (`IF NOT EXISTS`, `IF EXISTS`, `ON CONFLICT DO NOTHING`)
- [ ] RLS enabled on new tables
- [ ] RLS policies use `is_super_admin()` where appropriate
- [ ] Storage buckets use `is_super_admin()` bypass
- [ ] New bucket constants added to `StorageBuckets` in `@kit/shared/storage`
- [ ] Comments on columns/tables explain purpose
- [ ] Tested locally with `pnpm supabase:reset`
- [ ] Types regenerated with `pnpm supabase:typegen`

## Testing Commands

```bash
# Test migration locally (recommended)
pnpm supabase:reset

# Generate types from local database
pnpm supabase:typegen

# Validate migration syntax
pnpm supabase migration list

# Sync with production (check if migration exists on remote)
pnpm db:sync
```

## Deployment Methods

### Method 1: Automated GitHub Actions (RECOMMENDED ✅)

**Trigger**: Push to `main` branch with migration files in `apps/web/supabase/migrations/`

**Workflow**: `.github/workflows/deploy-migrations.yml`

**Process**:
1. Validates migration file naming
2. Checks current production migration status
3. Applies pending migrations using `psql` directly
4. Records migrations in `supabase_migrations.schema_migrations`
5. Generates TypeScript types from production schema
6. Creates PR with updated types

**Commands**:
```bash
# Commit migration
git add apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql
git commit -m "feat(db): description of migration"

# Push to main (triggers auto-deployment)
git push origin main
```

**Benefits**:
- ✅ No manual intervention required
- ✅ Automatic type generation from production
- ✅ Validation and verification built-in
- ✅ PR created for type updates
- ✅ Uses psql directly (avoids CLI connection issues)

**Connection Details**:
- **Host**: `aws-1-eu-central-1.pooler.supabase.com` (session mode pooler)
- **Port**: `5432` (session mode for complex migrations)
- **Why pooler**: GitHub Actions uses IPv4, pooler provides IPv4 compatibility
- **Why psql**: Supports complex migrations (prepared statements in `supabase db push` have limitations)

### Method 2: CLI Push to Production (FALLBACK)

**Use when**: Manual deployment needed (hotfix, testing)

**Prerequisites**:
```bash
# Get credentials from 1Password
export SUPABASE_PROJECT_ID="csjruhqyqzzqxnfeyiaf"  # Production
export SUPABASE_DB_PASSWORD="<from-1password>"
export SUPABASE_ACCESS_TOKEN="<from-1password>"
```

**Commands**:
```bash
# Deploy to production
pnpm supabase:deploy:prod

# Or manually
supabase link --project-ref $SUPABASE_PROJECT_ID
supabase db push --password $SUPABASE_DB_PASSWORD
```

**Known Issues**:
- ⚠️ CLI `link` may fail with "Anon key not found" error
- ⚠️ Pooler connection may fail with "Tenant or user not found"
- ⚠️ IPv6 vs IPv4 compatibility issues
- **Recommendation**: Use GitHub Actions instead

### Method 3: CLI Push to Staging

**Use when**: Testing migrations before production, or hotfixes to staging

**Commands**:
```bash
# Link to staging project
supabase link --project-ref hxpcknyqswetsqmqmeep

# Push migrations to staging
supabase db push

# Or use direct connection
supabase db push --db-url "postgresql://postgres.hxpcknyqswetsqmqmeep:<password>@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
```

**Verify staging migrations:**
```bash
# List migrations on staging
supabase migration list --project-ref hxpcknyqswetsqmqmeep
```

### Method 4: Direct psql Deployment (MOST RELIABLE ✅)

**Use when**: CLI methods fail, or for quick hotfixes

#### Credential Loading

Always load credentials from `.env.local` first:
```bash
# Load credentials from .env.local
source apps/web/.env.local 2>/dev/null
```

#### Understanding Connection Pooler Modes

**Session Mode (Port 5432):**
- Limited connections based on pool size setting
- Connection stays with client until voluntarily surrendered
- **Use for**: Persistent clients, complex migrations with prepared statements
- **Limitation**: Can hit "MaxClientsInSessionMode" error when pool is saturated

**Transaction Mode (Port 6543):**
- Higher connection capacity (shares connections between clients)
- Each query returns connection to pool immediately
- **Use for**: When hitting connection pool limits, serverless functions
- **Limitation**: No prepared statements support (not an issue for migrations)

**Rule of thumb**: Start with session mode (5432). If you get "MaxClientsInSessionMode: max clients reached", switch to transaction mode (6543).

#### Production Deployment

**Session Mode (Port 5432) - Default:**
```bash
# Load credentials from .env.local
source apps/web/.env.local 2>/dev/null

PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql

# Record migration in tracking table
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -c "INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('YYYYMMDDHHMMSS', 'description') ON CONFLICT DO NOTHING;"
```

**Transaction Mode (Port 6543) - When Pool Saturated:**
```bash
# Use port 6543 to bypass connection pool limits
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql

# Record migration in tracking table
PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
  "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
  -c "INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('YYYYMMDDHHMMSS', 'description') ON CONFLICT DO NOTHING;"
```

#### Staging Deployment

**Session Mode (Port 5432) - Default:**
```bash
# Load credentials from .env.local
source apps/web/.env.local 2>/dev/null

PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql

# Record migration in tracking table
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" \
  -c "INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('YYYYMMDDHHMMSS', 'description') ON CONFLICT DO NOTHING;"
```

**Transaction Mode (Port 6543) - When Pool Saturated:**
```bash
# Use port 6543 to bypass connection pool limits
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
  -f apps/web/supabase/migrations/YYYYMMDDHHMMSS_description.sql

# Record migration in tracking table
PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
  "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
  -c "INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('YYYYMMDDHHMMSS', 'description') ON CONFLICT DO NOTHING;"
```

**Benefits**:
- ✅ Bypasses CLI connection issues
- ✅ Works with IPv4 pooler
- ✅ Direct database access
- ✅ Full SQL support (no prepared statement limitations)
- ✅ Transaction mode (port 6543) handles connection pool saturation

**Connection Pooler Notes**:
- Use `aws-1-eu-central-1.pooler.supabase.com` (reliable for both projects)
- Port 5432 = Session mode (default, for persistent connections)
- Port 6543 = Transaction mode (bypass "MaxClientsInSessionMode" errors)
- **Important**: As of Feb 28, 2025, port 6543 only supports transaction mode

### Method 5: Dashboard SQL Editor (FALLBACK)

**Use when**: All CLI methods fail, or for simple migrations

**Production Dashboard**:
`https://supabase.com/dashboard/project/csjruhqyqzzqxnfeyiaf/sql/new`

**Staging Dashboard**:
`https://supabase.com/dashboard/project/hxpcknyqswetsqmqmeep/sql/new`

**Process**:
1. Open SQL Editor in Supabase Dashboard
2. Copy migration SQL content
3. Paste into editor
4. Click "Run"
5. Manually record in tracking table:

```sql
INSERT INTO supabase_migrations.schema_migrations (version, name, statements)
VALUES ('YYYYMMDDHHMMSS', 'migration_name', ARRAY['BEGIN', 'COMMIT'])
ON CONFLICT (version) DO NOTHING;
```

**Limitations**:
- ⚠️ Manual process
- ⚠️ No automatic migration tracking
- ⚠️ Requires manual recording in schema_migrations table

## Verifying Deployment

After deployment (automatic or manual):

```bash
# Check if migration is applied on production
pnpm db:sync

# This will:
# 1. Fetch remote migration list
# 2. Compare with local migrations
# 3. Show any mismatches
```

**Production database query** (via GitHub Actions logs):
```sql
SELECT version, name
FROM supabase_migrations.schema_migrations
ORDER BY version DESC
LIMIT 10;
```

### Helper Scripts 🛠️

**Location:** `.claude/skills/database-migration-manager/scripts/`

#### 1. Check Migration Status Across All Environments

```bash
cd apps/web
../../.claude/skills/database-migration-manager/scripts/check-migration-status.sh
```

**Output:**
- Local migration count and latest version
- Production migration count and latest
- Staging migration count and latest
- Sync status summary

**Features:**
- Auto-retrieves 1Password credentials
- Automatically falls back to transaction mode if session pool saturated
- Clear visual indicators for each environment

#### 2. Find Missing Migrations

```bash
# Check production
../../.claude/skills/database-migration-manager/scripts/find-missing-migrations.sh production

# Check staging
../../.claude/skills/database-migration-manager/scripts/find-missing-migrations.sh staging
```

**Output:**
- List of specific migration files missing on remote
- Ready-to-run commands to apply missing migrations
- Uses transaction mode (port 6543) for reliability

**Use cases:**
- Verify migrations after deployment
- Troubleshoot sync issues
- Generate deployment commands for missing migrations

**See:** `.claude/skills/database-migration-manager/scripts/README.md` for detailed documentation

## Troubleshooting Deployments

### CLI Connection Failures

**Symptoms**:
- "Anon key not found"
- "Tenant or user not found"
- Connection timeouts

**Solutions**:
1. ✅ **Use GitHub Actions** (recommended) - bypasses local connection issues
2. Check 1Password credentials are correct
3. Try alternative pooler: `aws-0-eu-central-1.pooler.supabase.com`
4. Update Supabase CLI: `brew upgrade supabase/tap/supabase`

### MaxClientsInSessionMode Error 🔴

**Symptom**: `FATAL: MaxClientsInSessionMode: max clients reached - in Session mode max clients are limited to pool_size`

**Cause**: Too many concurrent connections to the session mode pooler (port 5432). The connection pool is saturated.

**Solutions** (in order of preference):

1. **Switch to Transaction Mode (Port 6543)** ✅ RECOMMENDED
   ```bash
   # Load credentials from .env.local
   source apps/web/.env.local 2>/dev/null

   # Production - use port 6543 instead of 5432
   PGPASSWORD="$SUPABASE_DB_PASSWORD_PROD" psql \
     "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
     -c "SELECT COUNT(*) FROM supabase_migrations.schema_migrations;"

   # Staging - use port 6543 instead of 5432
   PGPASSWORD="$SUPABASE_DB_PASSWORD_STAGING" psql \
     "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:6543/postgres" \
     -c "SELECT COUNT(*) FROM supabase_migrations.schema_migrations;"
   ```

2. **Wait for Pool to Clear** (15-30 minutes)
   - Active connections will eventually close
   - Monitor pool status via Supabase Dashboard → Database → Connection Pooling

3. **Increase Pool Size** (requires dashboard access)
   - Go to Supabase Dashboard → Database Settings
   - Increase "Max Client Connections" field
   - **Note**: Requires database restart (downtime)

4. **Close Idle Connections** (database admin only)
   ```sql
   -- View active connections
   SELECT pid, usename, application_name, state, query_start
   FROM pg_stat_activity
   WHERE datname = 'postgres'
   ORDER BY query_start DESC;

   -- Terminate idle connections (use with caution)
   SELECT pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE datname = 'postgres'
     AND state = 'idle'
     AND query_start < NOW() - INTERVAL '30 minutes';
   ```

**Prevention**:
- ✅ Use transaction mode (port 6543) for short-lived operations
- ✅ Use session mode (port 5432) only for long-running, persistent connections
- ✅ Set `connection_limit=1` in serverless connection strings
- ✅ Close connections properly after use

**References**:
- [Supabase Discussion: MaxClientsInSessionMode](https://github.com/orgs/supabase/discussions/37571)
- [Supavisor Connection Terminology](https://supabase.com/docs/guides/troubleshooting/supavisor-and-connection-terminology-explained-9pr_ZO)

### Migration Already Applied

**Symptom**: Migration fails because it's already applied on production

**Solution**:
```bash
# Mark migration as applied without executing
supabase migration repair --status applied YYYYMMDDHHMMSS
```

### Types Out of Sync

**Symptom**: TypeScript types don't match production schema

**Solution**:
```bash
# Regenerate types from production (requires link)
pnpm supabase:typegen:linked

# Or trigger GitHub Actions workflow manually
# Actions → Deploy Database Migrations → Run workflow → Force typegen: true
```

## Post-Deployment Checklist

After migration is deployed:
- [ ] GitHub Actions workflow succeeded
- [ ] Type update PR created and merged
- [ ] Local types regenerated: `pnpm supabase:typegen:linked`
- [ ] Application builds successfully: `pnpm build`
- [ ] No TypeScript errors: `pnpm typecheck`
- [ ] Production application functioning normally
- [ ] Supabase logs checked for errors

## Common Mistakes to Avoid

1. ❌ Using version suffixes in file names
2. ❌ Non-idempotent SQL (missing `IF NOT EXISTS`)
3. ❌ Wrong location (not in `apps/web/supabase/migrations/`)
4. ❌ Missing RLS policies on new tables
5. ❌ Creating `SECURITY DEFINER` functions without validation
6. ❌ Not testing locally before committing
7. ❌ Missing timestamp in filename
8. ❌ Not using `is_super_admin()` for admin operations
9. ❌ Storage bucket without `is_super_admin()` bypass
10. ❌ Forgetting to add new bucket to `StorageBuckets` constant
11. ❌ Using `getPublicUrl()` for private buckets (use signed URLs)

## Reference Files

- Migration examples: `apps/web/supabase/migrations/`
- RLS patterns: `apps/web/supabase/schemas/`
- Documentation: `apps/web/supabase/CLAUDE.md`
- Project conventions: `docs/31-PROJECT_CONVENTIONS.md`

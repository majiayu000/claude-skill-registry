---
name: "rls-policy-generator"
description: "Generate production-ready Row Level Security (RLS) policies for Supabase tables with is_super_admin() bypass, proper USING/WITH CHECK, and common relationship patterns; use when creating RLS policies, securing tables, implementing data access controls, or securing storage buckets"
version: "2.2.0"
updated: "2025-12-15"
---

# RLS Policy Generator

## Supabase Project Reference

| Environment | Project ID | Dashboard SQL Editor |
|-------------|-----------|---------------------|
| **Production** | `csjruhqyqzzqxnfeyiaf` | [SQL Editor](https://supabase.com/dashboard/project/csjruhqyqzzqxnfeyiaf/sql/new) |
| **Staging** | `hxpcknyqswetsqmqmeep` | [SQL Editor](https://supabase.com/dashboard/project/hxpcknyqswetsqmqmeep/sql/new) |

## Direct Database Access (CLI)

**Credentials are stored in `.env.local`:**

```bash
# Load credentials
source .env.local

# Production
PGPASSWORD="${PROD_SUPABASE_DB_PASSWORD}" psql "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"

# Staging
PGPASSWORD="${STAGING_SUPABASE_DB_PASSWORD}" psql "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"
```

## When to Use This Skill

Use this skill when:
- Creating RLS policies for a new table
- Updating existing RLS policies
- Securing data access at database level
- Implementing account isolation
- Adding super admin bypass
- Fixing RLS policy bugs
- Comparing staging vs production policies
- Debugging infinite recursion errors
- **Creating storage bucket RLS policies**
- **Securing file uploads/downloads**

**DO NOT use** for:
- Application-level authorization (use service layer)
- Simple queries (RLS is automatic)
- Non-sensitive data (though RLS is still recommended)

---

## CRITICAL: Personal vs Team Accounts Architecture

**This is the #1 source of RLS bugs in Ballee.** Understand this before writing any account-related policies.

### The Architecture

Ballee uses MakerKit's dual-account system:

| Account Type | Count (Dec 2025) | Membership Record | Ownership Check |
|--------------|------------------|-------------------|-----------------|
| **Personal** | 94 dancers | ❌ NO `accounts_memberships` record | `accounts.primary_owner_user_id = auth.uid()` |
| **Team** | 1 (admin team) | ✅ Has `accounts_memberships` record | `accounts_memberships.user_id = auth.uid()` |

### Why Personal Accounts Have No Membership

By design in MakerKit, when a user signs up:
1. `kit.setup_new_user()` trigger creates a personal account
2. **NO membership record is created** - personal accounts use `primary_owner_user_id`
3. The `add_current_user_to_new_account` trigger **only fires for team accounts** (`is_personal_account = false`)

### The Common Bug Pattern

```sql
-- ❌ BROKEN: Only checks accounts_memberships (misses 100% of dancers!)
CREATE POLICY broken_policy ON storage.objects
FOR INSERT TO authenticated
WITH CHECK (
  (storage.foldername(name))[1] IN (
    SELECT account_id::text FROM accounts_memberships
    WHERE user_id = auth.uid()
  )
);
-- Result: All 94 dancers get "permission denied"
```

```sql
-- ✅ CORRECT: Checks BOTH team memberships AND personal account ownership
CREATE POLICY correct_policy ON storage.objects
FOR INSERT TO authenticated
WITH CHECK (
  -- Super admin bypass
  public.is_super_admin() OR
  -- Team account: user has membership
  (storage.foldername(name))[1] IN (
    SELECT account_id::text FROM accounts_memberships
    WHERE user_id = auth.uid()
  ) OR
  -- Personal account: user is the primary owner
  (storage.foldername(name))[1] IN (
    SELECT id::text FROM accounts
    WHERE primary_owner_user_id = auth.uid()
      AND is_personal_account = true
  )
);
```

### Checklist: When Using `accounts_memberships`

⚠️ **Every time you write a policy that queries `accounts_memberships`, ask:**

- [ ] Does this policy also need to support personal accounts?
- [ ] If yes, did I add `OR primary_owner_user_id = auth.uid()` check?
- [ ] Did I filter personal accounts with `AND is_personal_account = true`?

### Tables That Correctly Handle Both Account Types

| Table | Pattern Used | Notes |
|-------|-------------|-------|
| `notifications` | ✅ Both checks | Has `primary_owner_user_id` OR `accounts_memberships` |
| `storage.objects` (reimbursements) | ✅ Both checks | Fixed Dec 2025 |

### Tables That Use User-Level Access (Safe)

These tables don't need the dual check because they use `user_id = auth.uid()`:

| Table | Column | Notes |
|-------|--------|-------|
| `profiles` | `id = auth.uid()` | Profile ID = User ID |
| `professional_profiles` | `user_id = auth.uid()` | Direct user ownership |
| `reimbursement_requests` | `user_id = auth.uid()` | Direct user ownership |
| `dancer_profiles` | `user_id = auth.uid()` | Direct user ownership |

### Quick Reference: Account Access Patterns

```sql
-- Pattern 1: User owns the record directly (SAFEST - no account check needed)
USING (user_id = auth.uid())

-- Pattern 2: Account-based with BOTH personal and team support
USING (
  public.is_super_admin() OR
  account_id IN (
    -- Team accounts via membership
    SELECT account_id FROM accounts_memberships WHERE user_id = auth.uid()
    UNION
    -- Personal accounts via ownership
    SELECT id FROM accounts WHERE primary_owner_user_id = auth.uid() AND is_personal_account = true
  )
)

-- Pattern 3: Account-based for storage (path-based)
USING (
  public.is_super_admin() OR
  -- Team account path
  (storage.foldername(name))[1] IN (
    SELECT account_id::text FROM accounts_memberships WHERE user_id = auth.uid()
  ) OR
  -- Personal account path
  (storage.foldername(name))[1] IN (
    SELECT id::text FROM accounts WHERE primary_owner_user_id = auth.uid() AND is_personal_account = true
  )
)
```

---

## CRITICAL: Avoid Infinite Recursion

**The #1 cause of production outages with RLS is infinite recursion.**

### What Causes Recursion

RLS policies that query tables which have RLS policies that query back to the original table:

```sql
-- ❌ DANGEROUS: productions policy queries cast_assignments
CREATE POLICY productions_select ON public.productions
FOR SELECT TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM cast_assignments ca
    JOIN cast_roles cr ON ca.cast_role_id = cr.id
    WHERE cr.production_id = productions.id  -- References back to productions!
    AND ca.user_id = auth.uid()
  )
);

-- When you SELECT from productions:
-- 1. PostgreSQL checks productions RLS → queries cast_assignments
-- 2. cast_assignments might have RLS → queries cast_roles
-- 3. cast_roles RLS → queries productions (RECURSION!)
```

### Safe Patterns to Avoid Recursion

**Pattern 1: Denormalized Arrays (RECOMMENDED)**
```sql
-- Store user IDs directly on the table
ALTER TABLE productions ADD COLUMN assigned_user_ids uuid[] DEFAULT '{}';

-- Policy uses local array - no joins needed
CREATE POLICY productions_select ON public.productions
FOR SELECT TO authenticated
USING (
  is_super_admin() OR
  auth.uid() = ANY(assigned_user_ids)  -- No subquery!
);
```

**Pattern 2: service_role Bypass**
```sql
-- service_role always bypasses RLS
CREATE POLICY productions_service_role_bypass ON public.productions
FOR ALL TO service_role
USING (true) WITH CHECK (true);
```

**Pattern 3: Direct Column Check**
```sql
-- Use columns directly on the table, not JOINs
CREATE POLICY productions_select ON public.productions
FOR SELECT TO authenticated
USING (
  is_super_admin() OR
  created_by = auth.uid() OR
  client_id IN (SELECT client_id FROM client_users WHERE user_id = auth.uid())
);
```

### Recursion Debug Commands

```sql
-- Check for circular policy dependencies
SELECT tablename, policyname, qual
FROM pg_policies
WHERE schemaname = 'public'
AND qual LIKE '%EXISTS%'
ORDER BY tablename;

-- Identify tables referenced in a policy
SELECT tablename, policyname,
  regexp_matches(qual, 'FROM\s+(\w+)', 'g') as referenced_tables
FROM pg_policies
WHERE schemaname = 'public';
```

---

## Environment Synchronization

### Compare Staging vs Production Policies

```bash
# Get policy lists
PGPASSWORD="${STAGING_SUPABASE_DB_PASSWORD}" psql "postgresql://postgres.hxpcknyqswetsqmqmeep@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" -t -c "SELECT tablename || '.' || policyname FROM pg_policies WHERE schemaname = 'public' ORDER BY 1;" > /tmp/staging.txt

PGPASSWORD="${PROD_SUPABASE_DB_PASSWORD}" psql "postgresql://postgres.csjruhqyqzzqxnfeyiaf@aws-1-eu-central-1.pooler.supabase.com:5432/postgres" -t -c "SELECT tablename || '.' || policyname FROM pg_policies WHERE schemaname = 'public' ORDER BY 1;" > /tmp/prod.txt

# Compare
sort /tmp/staging.txt | uniq > /tmp/s.txt
sort /tmp/prod.txt | uniq > /tmp/p.txt
echo "Missing in production:" && comm -23 /tmp/s.txt /tmp/p.txt
echo "Extra in production:" && comm -13 /tmp/s.txt /tmp/p.txt
```

### Copy Policy from Staging to Production

```sql
-- Get policy definition from staging
SELECT
  'DROP POLICY IF EXISTS "' || policyname || '" ON ' || schemaname || '.' || tablename || ';' ||
  E'\nCREATE POLICY "' || policyname || '" ON ' || schemaname || '.' || tablename ||
  ' FOR ' || cmd || ' TO ' ||
  CASE WHEN roles = '{authenticated}' THEN 'authenticated'
       WHEN roles = '{service_role}' THEN 'service_role'
       ELSE array_to_string(roles, ', ')
  END ||
  CASE WHEN cmd IN ('SELECT', 'DELETE') THEN ' USING (' || qual || ');'
       WHEN cmd = 'INSERT' THEN ' WITH CHECK (' || with_check || ');'
       ELSE ' USING (' || COALESCE(qual, 'true') || ') WITH CHECK (' || COALESCE(with_check, 'true') || ');'
  END as sql
FROM pg_policies
WHERE tablename = 'TABLE_NAME' AND policyname = 'POLICY_NAME';
```

### Compare Specific Table Policies

```bash
for table in productions events cast_roles cast_assignments; do
  echo "=== $table ==="
  echo "STAGING:"
  PGPASSWORD="${STAGING_SUPABASE_DB_PASSWORD}" psql "..." -t -c "SELECT COUNT(*) FROM pg_policies WHERE tablename = '$table';"
  echo "PRODUCTION:"
  PGPASSWORD="${PROD_SUPABASE_DB_PASSWORD}" psql "..." -t -c "SELECT COUNT(*) FROM pg_policies WHERE tablename = '$table';"
done
```

---

## Security Audit Queries

### Find Dangerous Policies

```sql
-- CRITICAL: Find policies that allow public write access
SELECT tablename, policyname, cmd, roles
FROM pg_policies
WHERE schemaname = 'public'
AND qual = 'true'
AND (roles @> '{public}' OR roles @> '{anon}')
AND cmd != 'SELECT'
ORDER BY tablename;

-- Find "Allow all" policies (should be removed!)
SELECT tablename, policyname, cmd, roles
FROM pg_policies
WHERE policyname LIKE 'Allow all%'
ORDER BY tablename;
```

### Find Duplicate Policies

```sql
-- Tables with multiple policies for same operation
SELECT tablename, cmd, COUNT(*) as policy_count,
       string_agg(policyname, ', ' ORDER BY policyname) as policies
FROM pg_policies
WHERE schemaname = 'public'
GROUP BY tablename, cmd
HAVING COUNT(*) > 1
ORDER BY policy_count DESC;
```

### Verify service_role Bypass Exists

```sql
-- Check which tables have service_role bypass
SELECT tablename, policyname
FROM pg_policies
WHERE schemaname = 'public'
AND policyname LIKE '%service_role%'
ORDER BY tablename;

-- Tables WITHOUT service_role bypass (may need one)
SELECT DISTINCT tablename
FROM pg_policies
WHERE schemaname = 'public'
AND tablename NOT IN (
  SELECT DISTINCT tablename
  FROM pg_policies
  WHERE policyname LIKE '%service_role%'
)
ORDER BY tablename;
```

---

## Critical RLS Principles

### 1. ALWAYS Enable RLS on New Tables
```sql
ALTER TABLE "public"."table_name" ENABLE ROW LEVEL SECURITY;
```

### 2. ALWAYS Add service_role Bypass
```sql
-- service_role is the backend/admin client - needs unrestricted access
-- @rls-disable-check: service_role bypass is required for admin operations
CREATE POLICY {table}_service_role_bypass ON public.{table}
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);
```

### 3. Super Admin Bypass Pattern
```sql
-- ALWAYS include is_super_admin() first in USING/WITH CHECK
USING (
  public.is_super_admin() OR
  -- other conditions
)
```

### 4. DROP Before CREATE (Idempotency)
```sql
DROP POLICY IF EXISTS policy_name ON public.table_name;
CREATE POLICY policy_name ON public.table_name ...
```

### 5. USING vs WITH CHECK
- **USING**: Controls which rows user can SELECT/UPDATE/DELETE
- **WITH CHECK**: Controls which rows user can INSERT/UPDATE
- **UPDATE policies need BOTH**

---

## Policy Naming Convention

**Standard pattern**: `{table}_{operation}` or `{table}_{role}_{operation}`

| Pattern | Example | Use When |
|---------|---------|----------|
| `{table}_{operation}` | `events_select` | Default for all policies |
| `{table}_{role}_{operation}` | `hire_orders_dancer_read` | Role-specific access |
| `{table}_service_role_bypass` | `productions_service_role_bypass` | service_role ALL access |
| `{table}_{operation}_by_{entity}` | `events_insert_by_client` | Entity-based access |

**AVOID**:
- Sentence case: ❌ "Users can read own documents"
- `_restricted` suffix: ❌ `events_select_restricted` (use `_by_role` instead)
- Duplicates: ❌ Having both `_select` and `_select_all`

---

## Common RLS Patterns

### Pattern 1: Super Admin + service_role Only

```sql
-- Enable RLS
ALTER TABLE "public".{table_name} ENABLE ROW LEVEL SECURITY;

-- service_role bypass (for backend operations)
DROP POLICY IF EXISTS {table_name}_service_role_bypass ON public.{table_name};
CREATE POLICY {table_name}_service_role_bypass ON public.{table_name}
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

-- Super admin operations
DROP POLICY IF EXISTS {table_name}_select ON public.{table_name};
CREATE POLICY {table_name}_select ON public.{table_name}
  FOR SELECT TO authenticated
  USING (public.is_super_admin());

DROP POLICY IF EXISTS {table_name}_insert ON public.{table_name};
CREATE POLICY {table_name}_insert ON public.{table_name}
  FOR INSERT TO authenticated
  WITH CHECK (public.is_super_admin());

DROP POLICY IF EXISTS {table_name}_update ON public.{table_name};
CREATE POLICY {table_name}_update ON public.{table_name}
  FOR UPDATE TO authenticated
  USING (public.is_super_admin())
  WITH CHECK (public.is_super_admin());

DROP POLICY IF EXISTS {table_name}_delete ON public.{table_name};
CREATE POLICY {table_name}_delete ON public.{table_name}
  FOR DELETE TO authenticated
  USING (public.is_super_admin());
```

### Pattern 2: User Owns Data (via user_id)

```sql
-- SELECT: User sees their own + super admin sees all
DROP POLICY IF EXISTS {table_name}_select ON public.{table_name};
CREATE POLICY {table_name}_select ON public.{table_name}
  FOR SELECT TO authenticated
  USING (
    public.is_super_admin() OR
    user_id = auth.uid()
  );

-- INSERT: User can insert their own
DROP POLICY IF EXISTS {table_name}_insert ON public.{table_name};
CREATE POLICY {table_name}_insert ON public.{table_name}
  FOR INSERT TO authenticated
  WITH CHECK (
    public.is_super_admin() OR
    user_id = auth.uid()
  );

-- UPDATE: User can update their own
DROP POLICY IF EXISTS {table_name}_update ON public.{table_name};
CREATE POLICY {table_name}_update ON public.{table_name}
  FOR UPDATE TO authenticated
  USING (public.is_super_admin() OR user_id = auth.uid())
  WITH CHECK (public.is_super_admin() OR user_id = auth.uid());

-- DELETE: Super admin only (or user owns)
DROP POLICY IF EXISTS {table_name}_delete ON public.{table_name};
CREATE POLICY {table_name}_delete ON public.{table_name}
  FOR DELETE TO authenticated
  USING (public.is_super_admin() OR user_id = auth.uid());
```

### Pattern 3: Denormalized Array Access (SAFE - No Recursion)

```sql
-- Use when access is determined by assignment/membership
-- Store user IDs in an array column on the table

-- SELECT: User is in assigned_user_ids array
DROP POLICY IF EXISTS {table_name}_select ON public.{table_name};
CREATE POLICY {table_name}_select ON public.{table_name}
  FOR SELECT TO authenticated
  USING (
    public.is_super_admin() OR
    auth.uid() = ANY(assigned_user_ids)
  );
```

### Pattern 4: Client-Based Access

```sql
-- For tables owned by clients (Fever, etc.)
DROP POLICY IF EXISTS {table_name}_select_by_client ON public.{table_name};
CREATE POLICY {table_name}_select_by_client ON public.{table_name}
  FOR SELECT TO authenticated
  USING (
    public.is_super_admin() OR
    client_id IN (
      SELECT client_id FROM client_users WHERE user_id = auth.uid()
    )
  );
```

---

## Debugging RLS Issues

### Check Current Policies

```sql
-- View all policies for a table
SELECT policyname, cmd, roles, qual, with_check
FROM pg_policies
WHERE tablename = 'TABLE_NAME'
ORDER BY cmd, policyname;

-- View policy count per table
SELECT tablename, COUNT(*) as policy_count
FROM pg_policies
WHERE schemaname = 'public'
GROUP BY tablename
ORDER BY policy_count DESC;
```

### Check if RLS is Enabled

```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND tablename = 'TABLE_NAME';
```

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| "infinite recursion detected" | Policy queries table with RLS that queries back | Use denormalized arrays or service_role bypass |
| "permission denied for table" | RLS blocking access | Check is_super_admin() bypass exists |
| "policy does not exist" | Typo or not created | Run DROP IF EXISTS + CREATE |
| Empty results for super admin | is_super_admin() not first in USING | Move is_super_admin() OR to start |

---

## Storage Bucket RLS Policies

Storage buckets in Supabase require RLS policies on `storage.objects`. These are **different from table RLS** - they control file access, upload, and deletion.

### Storage Bucket Concepts

- **Bucket**: Container for files (e.g., `dancer-media`, `venue-documents`)
- **Public Bucket**: Anyone can read files (no RLS for SELECT)
- **Private Bucket**: Requires signed URLs for access (RLS applies)
- **storage.objects**: System table that stores file metadata
- **Signed URLs**: Temporary authenticated URLs for private files

### Storage Bucket Constants

Use centralized constants from `@kit/shared/storage`:

```typescript
import { StorageBuckets, SignedUrlExpiry } from '@kit/shared/storage';

// Available buckets
StorageBuckets.DANCER_MEDIA        // 'dancer-media'
StorageBuckets.VENUE_DOCUMENTS     // 'venue-documents'
StorageBuckets.LEGAL_DOCUMENTS     // 'legal-documents'
StorageBuckets.REIMBURSEMENT_DOCUMENTS  // 'reimbursement-documents'
StorageBuckets.REIMBURSEMENTS      // 'reimbursements' (legacy)
StorageBuckets.CONTRACTS           // 'contracts'
StorageBuckets.PRODUCTION_DOCUMENTS // 'production-documents'
StorageBuckets.INVOICE_PDFS        // 'invoice-pdfs'

// Expiry times (in seconds)
SignedUrlExpiry.IMMEDIATE_DISPLAY  // 3600 (1 hour)
SignedUrlExpiry.DOWNLOAD           // 86400 (24 hours)
SignedUrlExpiry.PROFILE_PHOTO      // 604800 (7 days)
SignedUrlExpiry.ADMIN_REVIEW       // 86400 (24 hours)
SignedUrlExpiry.MAX                // 604800 (7 days - Supabase limit)
SignedUrlExpiry.MIN                // 60 (1 minute)
```

### Creating a Storage Bucket

```sql
-- Create a private bucket (requires signed URLs)
INSERT INTO storage.buckets (id, name, public)
VALUES ('my-bucket', 'my-bucket', false);

-- Create a public bucket (anyone can read)
INSERT INTO storage.buckets (id, name, public)
VALUES ('public-assets', 'public-assets', true);
```

### Pattern 1: Account-Based Storage (Filename = Account UUID)

Use when files are named with account UUIDs (e.g., profile photos):

```sql
-- Uses kit.get_storage_filename_as_uuid() to extract UUID from filename
CREATE POLICY account_image ON storage.objects FOR ALL USING (
  bucket_id = 'account_image'
  AND (
    -- Super admin can access all files
    public.is_super_admin()
    OR
    -- File belongs to user's account
    kit.get_storage_filename_as_uuid(name) = auth.uid()
    OR
    -- User has role on the account
    public.has_role_on_account(kit.get_storage_filename_as_uuid(name))
  )
)
WITH CHECK (
  bucket_id = 'account_image'
  AND (
    -- Super admin can upload/modify
    public.is_super_admin()
    OR
    -- User owns the account
    kit.get_storage_filename_as_uuid(name) = auth.uid()
    OR
    -- User has permission on the account
    public.has_permission(
      auth.uid(),
      kit.get_storage_filename_as_uuid(name),
      'settings.manage'
    )
  )
);
```

### Pattern 2: User-Based Storage (Path includes user_id)

Use when file paths include user ID (e.g., `{user_id}/photos/image.jpg`):

```sql
-- Extract user_id from the first path segment
CREATE POLICY dancer_media ON storage.objects FOR ALL USING (
  bucket_id = 'dancer-media'
  AND (
    public.is_super_admin()
    OR
    -- First segment of path is user's UUID
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
)
WITH CHECK (
  bucket_id = 'dancer-media'
  AND (
    public.is_super_admin()
    OR
    (string_to_array(name, '/'))[1]::uuid = auth.uid()
  )
);
```

### Pattern 3: Entity-Based Storage (Linked to DB record)

Use when files are linked to database records via foreign key:

```sql
-- Example: venue documents linked to venues table
CREATE POLICY venue_documents ON storage.objects FOR ALL USING (
  bucket_id = 'venue-documents'
  AND (
    public.is_super_admin()
    OR
    -- Extract venue_id from path and check access
    EXISTS (
      SELECT 1 FROM venues v
      WHERE v.id = (string_to_array(name, '/'))[1]::uuid
      AND public.has_role_on_account(v.account_id)
    )
  )
)
WITH CHECK (
  bucket_id = 'venue-documents'
  AND (
    public.is_super_admin()
    OR
    EXISTS (
      SELECT 1 FROM venues v
      WHERE v.id = (string_to_array(name, '/'))[1]::uuid
      AND public.has_permission(auth.uid(), v.account_id, 'venues.manage')
    )
  )
);
```

### Pattern 4: Super Admin Only Storage

Use for sensitive documents only admins should access:

```sql
CREATE POLICY admin_only_documents ON storage.objects FOR ALL USING (
  bucket_id = 'admin-documents'
  AND public.is_super_admin()
)
WITH CHECK (
  bucket_id = 'admin-documents'
  AND public.is_super_admin()
);
```

### Signed URL Best Practices

**NEVER use `getPublicUrl()` for private buckets:**

```typescript
// ❌ WRONG - Returns 403 for private buckets
const { data } = client.storage.from('private-bucket').getPublicUrl(path);

// ✅ CORRECT - Use signed URLs for private buckets
const { data } = await client.storage
  .from(StorageBuckets.INVOICE_PDFS)
  .createSignedUrl(path, SignedUrlExpiry.DOWNLOAD);
```

**Use StorageUrlService for consistent URL generation:**

```typescript
import { createStorageUrlService, StorageBuckets, SignedUrlExpiry } from '@kit/shared/storage';

const storageService = createStorageUrlService(client);

// Single URL
const result = await storageService.getSignedUrl(
  StorageBuckets.VENUE_DOCUMENTS,
  'venue-123/photo.jpg',
  { expiresIn: SignedUrlExpiry.IMMEDIATE_DISPLAY }
);

// Batch URLs (more efficient)
const results = await storageService.getBatchSignedUrls(
  StorageBuckets.VENUE_DOCUMENTS,
  ['path1.jpg', 'path2.jpg', 'path3.jpg'],
  { expiresIn: SignedUrlExpiry.DOWNLOAD }
);

// Enrich array with URLs
const docsWithUrls = await storageService.enrichWithSignedUrls(
  StorageBuckets.VENUE_DOCUMENTS,
  documents,
  (doc) => doc.storage_path,
  (doc, url) => ({ ...doc, signedUrl: url }),
  { expiresIn: SignedUrlExpiry.DOWNLOAD }
);
```

### Storage Debugging Commands

```sql
-- List all storage buckets
SELECT id, name, public, created_at
FROM storage.buckets
ORDER BY name;

-- View storage policies
SELECT policyname, cmd, roles, qual, with_check
FROM pg_policies
WHERE schemaname = 'storage' AND tablename = 'objects'
ORDER BY policyname;

-- Check which bucket a policy applies to
SELECT policyname, qual
FROM pg_policies
WHERE schemaname = 'storage'
AND qual LIKE '%bucket_id%';

-- Find files in a bucket
SELECT id, name, bucket_id, created_at
FROM storage.objects
WHERE bucket_id = 'my-bucket'
ORDER BY created_at DESC
LIMIT 10;
```

### Storage Policy Migration Template

```sql
/**
 * Migration: Update {bucket_name} storage RLS policy
 *
 * Purpose: Add super admin bypass to {bucket_name} bucket
 */

-- Drop existing policy
DROP POLICY IF EXISTS {bucket_name} ON storage.objects;

-- Create new policy with super admin bypass
CREATE POLICY {bucket_name} ON storage.objects FOR ALL USING (
  bucket_id = '{bucket_name}'
  AND (
    -- Super admin can access all files
    public.is_super_admin()
    OR
    -- Your access conditions here
    {your_using_condition}
  )
)
WITH CHECK (
  bucket_id = '{bucket_name}'
  AND (
    -- Super admin can manage all files
    public.is_super_admin()
    OR
    -- Your write conditions here
    {your_with_check_condition}
  )
);
```

### Common Storage Issues

| Error | Cause | Fix |
|-------|-------|-----|
| "Object not found" | File doesn't exist or RLS blocking | Check path and RLS policy |
| "new row violates row-level security policy" | WITH CHECK failing | Add is_super_admin() bypass |
| "Bucket not found" | Bucket doesn't exist | Create bucket in storage.buckets |
| Signed URL returns 403 | Expired or wrong bucket | Check expiry time and bucket name |
| Public URL returns 403 | Bucket is private | Use signed URLs instead |

---

## Quick Reference: Full Table Setup

```sql
-- =====================================================================
-- RLS Policies for {table_name}
-- =====================================================================

-- Enable RLS
ALTER TABLE "public".{table_name} ENABLE ROW LEVEL SECURITY;

-- service_role bypass (ALWAYS include this)
DROP POLICY IF EXISTS {table_name}_service_role_bypass ON public.{table_name};
CREATE POLICY {table_name}_service_role_bypass ON public.{table_name}
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

-- SELECT
DROP POLICY IF EXISTS {table_name}_select ON public.{table_name};
CREATE POLICY {table_name}_select ON public.{table_name}
  FOR SELECT TO authenticated
  USING (public.is_super_admin() OR {your_condition});

-- INSERT
DROP POLICY IF EXISTS {table_name}_insert ON public.{table_name};
CREATE POLICY {table_name}_insert ON public.{table_name}
  FOR INSERT TO authenticated
  WITH CHECK (public.is_super_admin() OR {your_condition});

-- UPDATE
DROP POLICY IF EXISTS {table_name}_update ON public.{table_name};
CREATE POLICY {table_name}_update ON public.{table_name}
  FOR UPDATE TO authenticated
  USING (public.is_super_admin() OR {your_condition})
  WITH CHECK (public.is_super_admin() OR {your_condition});

-- DELETE
DROP POLICY IF EXISTS {table_name}_delete ON public.{table_name};
CREATE POLICY {table_name}_delete ON public.{table_name}
  FOR DELETE TO authenticated
  USING (public.is_super_admin());
```

---

## Current Production State (2025-11-27)

### Policy Counts

| Metric | Staging | Production |
|--------|---------|------------|
| Total policies | 311 | 314 |
| Missing in prod | 0 | - |
| Extra in prod | - | 3 (expected) |

### Critical Tables Aligned

| Table | Staging | Production | Status |
|-------|---------|------------|--------|
| productions | 9 | 9 | ✅ |
| events | 16 | 16 | ✅ |
| cast_assignments | 7 | 7 | ✅ |
| event_participants | 9 | 9 | ✅ |
| invoices | 6 | 6 | ✅ |
| hire_orders | 12 | 12 | ✅ |
| profiles | 4 | 4 | ✅ |
| venues | 8 | 8 | ✅ |
| ratings | 7 | 7 | ✅ |
| accounts | 6 | 6 | ✅ |

### Production-Only Policies (Expected)

1. `cast_roles.cast_roles_update_authenticated` - Client user access
2. `seasons.seasons_select_authenticated` - Seasons table (prod only)
3. `seasons.seasons_super_admin_all` - Seasons table (prod only)

---

## Cleanup Guidelines

### Policies to Remove (Dangerous)

```sql
-- "Allow all" policies are SECURITY RISKS
DROP POLICY IF EXISTS "Allow all operations for everyone" ON public.{table};
```

### Duplicate Policies to Consolidate

When you see both:
- `{table}_select` AND `{table}_select_restricted`
- `{table}_delete_own` AND `{table}_delete_restricted`

Keep the more complete one (usually has `is_super_admin()` bypass).

### Legacy Naming to Update

| Old Name | New Name |
|----------|----------|
| "Users can read own..." | `{table}_select` |
| "Super admins can manage..." | `{table}_super_admin_all` |
| `{table}_select_restricted` | `{table}_select` |

---

## Reference Files

- Migrations: `apps/web/supabase/migrations/`
- Database docs: `docs/08-DATABASE_ARCHITECTURE.md`
- Auth docs: `docs/14-AUTHENTICATION_AUTHORIZATION.md`
- is_super_admin function: Check `apps/web/supabase/schemas/`

---

## Changelog

### v2.2.0 (2025-12-15)
- **CRITICAL: Added Personal vs Team Accounts Architecture section**
  - Documented MakerKit dual-account system
  - Explained why personal accounts have no `accounts_memberships` records
  - Added common bug pattern and correct fix
  - Added checklist for `accounts_memberships` usage
  - Listed tables with correct handling vs user-level access
  - Added quick reference account access patterns
- Fixed storage RLS policies for personal accounts (production hotfix)

### v2.1.0 (2025-12-11)
- **Added comprehensive Storage Bucket RLS section**
  - Storage bucket concepts and constants
  - Four storage RLS patterns (account-based, user-based, entity-based, admin-only)
  - Signed URL best practices with StorageUrlService
  - Storage debugging commands
  - Migration template for storage policies
  - Common storage issues table
- Updated skill description to include storage

### v2.0.0 (2025-11-27)
- Added infinite recursion prevention section
- Added environment synchronization commands
- Added security audit queries
- Added CLI database access commands
- Updated policy naming conventions
- Added current production state
- Added cleanup guidelines
- Removed deprecated patterns

### v1.0.0 (Initial)
- Basic RLS patterns and examples

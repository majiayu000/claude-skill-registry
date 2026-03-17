---
name: supabase-expert
description: This skill should be used when working with Supabase database operations in the MyJKKN project, including creating modules, updating schemas, writing RLS policies, creating database functions, implementing Auth SSR, or developing Edge Functions. Automatically triggers when user mentions 'database', 'table', 'SQL', 'Supabase', 'migration', 'RLS', 'policy', or 'Edge Function'.
---

# Supabase Expert

## Overview

This skill provides comprehensive guidance for working with Supabase in the MyJKKN education management system. It enforces critical file management rules, security patterns, and performance optimizations to maintain a clean, organized database structure.

## Critical Rules (NEVER VIOLATE)

### 🔴 SQL File Management
1. **NEVER create duplicate SQL files** - Always update existing files
2. **ALWAYS use Supabase MCP to check REAL-TIME database state FIRST**
   - SQL files might be outdated - MCP shows actual database
   - Use `mcp__supabase__list_tables` to see current schema
   - Use `mcp__supabase__execute_sql` to query structure
   - **NEVER rely on SQL files alone** - they may not match reality
3. **Update ONLY existing files** in `supabase/setup/` directory:
   - Tables → `supabase/setup/01_tables.sql`
   - Functions → `supabase/setup/02_functions.sql`
   - Policies → `supabase/setup/03_policies.sql`
   - Triggers → `supabase/setup/04_triggers.sql`
   - Views → `supabase/setup/05_views.sql`
4. **Add dated comments** for all changes with reason
5. **Update SQL_FILE_INDEX.md** after making changes
6. **DO NOT use CLI commands** - Use Supabase MCP tools exclusively

### 🔴 Authentication SSR Rules
**NEVER USE (DEPRECATED - BREAKS APPLICATION):**
- Individual cookie methods: `get()`, `set()`, `remove()`
- Package: `@supabase/auth-helpers-nextjs`

**ALWAYS USE:**
- Package: `@supabase/ssr`
- Cookie methods: `getAll()` and `setAll()` ONLY
- Middleware MUST call `getUser()` to refresh session
- Middleware MUST return `supabaseResponse` object

### 🔴 RLS Policy Rules
- Always wrap functions in SELECT: `(SELECT auth.uid())` not `auth.uid()`
- **SELECT**: USING only (no WITH CHECK)
- **INSERT**: WITH CHECK only (no USING)
- **UPDATE**: Both USING and WITH CHECK
- **DELETE**: USING only (no WITH CHECK)
- Always specify `TO authenticated` or `TO anon`
- Create indexes on ALL columns used in policies
- NEVER use `FOR ALL` - create 4 separate policies (SELECT, INSERT, UPDATE, DELETE)

### 🔴 Database Function Rules
- **DEFAULT**: Use `SECURITY INVOKER` (safer than DEFINER)
- **ALWAYS**: Set `search_path = ''` for security
- **USE**: Fully qualified names (`public.table_name`)
- **SPECIFY**: Correct volatility (IMMUTABLE/STABLE/VOLATILE)
- **AVOID**: `SECURITY DEFINER` unless absolutely required

### 🔴 Edge Function Rules
- **USE**: `Deno.serve` (not old serve import)
- **IMPORTS**: Always use `npm:/jsr:/node:` prefix with version numbers
- **SHARED**: Place shared code in `_shared/` folder
- **FILES**: Write only to `/tmp` directory
- **NEVER**: Use bare specifiers or cross-function dependencies

## Workflow Decision Tree

```
User mentions database/SQL work?
├─> YES: Query real-time database with Supabase MCP FIRST
│   ├─> Creating new module?
│   │   └─> Use: Module Creation Workflow
│   ├─> Updating existing table?
│   │   └─> Use: Schema Update Workflow
│   ├─> Creating RLS policies?
│   │   └─> Use: RLS Policy Workflow
│   ├─> Creating database function?
│   │   └─> Use: Database Function Workflow
│   ├─> Creating Edge Function?
│   │   └─> Use: Edge Function Workflow
│   └─> Debugging database issue?
│       └─> Use: Debug Workflow
└─> NO: Skill not applicable

⚠️  CRITICAL: Always use MCP to query real-time database state
    SQL files may be outdated - MCP shows actual database reality
```

## Module Creation Workflow

**When to use:** User asks to create a new module, add new tables, or build new database feature.

**Process:**

1. **Query REAL-TIME database state with Supabase MCP (ALWAYS FIRST)**
   ```
   Use Supabase MCP to check current database schema:
   mcp__supabase__list_tables

   Verify table doesn't exist:
   mcp__supabase__execute_sql
   SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE '%keyword%';

   Check related tables:
   mcp__supabase__execute_sql
   SELECT * FROM information_schema.tables WHERE table_schema = 'public';
   ```

2. **Check SQL_FILE_INDEX.md (for documentation reference only)**
   ```
   Read supabase/SQL_FILE_INDEX.md
   NOTE: This may be outdated - trust MCP query results over file contents
   ```

3. **Design tables following MyJKKN conventions**
   - id (UUID PRIMARY KEY)
   - institution_id (for multi-tenant)
   - created_at, updated_at (TIMESTAMPTZ)
   - created_by (UUID reference to profiles)
   - Use snake_case for all identifiers
   - Add comments on all tables

4. **Update ONLY `supabase/setup/01_tables.sql`**
   - Add section comment with date
   - Follow exact template from `references/sql-templates.md`
   - Enable RLS
   - Create indexes
   - Add triggers
   - NOTE: Update the file to match what will be in database

5. **Create RLS policies in `supabase/setup/03_policies.sql`**
   - Use templates from `references/rls-policy-patterns.md`
   - Follow performance optimization rules

6. **Create TypeScript types** in `types/[module_name].ts`

7. **Create service layer** in `lib/services/[module_name]/`

8. **Create React Query hooks** in `hooks/[module_name]/`

9. **Update SQL_FILE_INDEX.md** with new tables

**⚠️  IMPORTANT:** Always verify with MCP that tables don't already exist before creating.

**See `references/module-creation-template.md` for complete example.**

## Schema Update Workflow

**When to use:** User asks to add column, modify table, or update existing schema.

**Process:**

1. **Query REAL-TIME table structure with Supabase MCP (ALWAYS FIRST)**
   ```
   Use Supabase MCP to get current schema:
   mcp__supabase__execute_sql
   SELECT column_name, data_type, is_nullable, column_default
   FROM information_schema.columns
   WHERE table_schema = 'public' AND table_name = 'your_table'
   ORDER BY ordinal_position;

   Check constraints:
   mcp__supabase__execute_sql
   SELECT constraint_name, constraint_type
   FROM information_schema.table_constraints
   WHERE table_schema = 'public' AND table_name = 'your_table';

   Check indexes:
   mcp__supabase__execute_sql
   SELECT indexname, indexdef
   FROM pg_indexes
   WHERE schemaname = 'public' AND tablename = 'your_table';
   ```

2. **Apply migration using Supabase MCP**
   ```
   Use Supabase MCP: mcp__supabase__apply_migration
   Name: add_[column]_to_[table]
   Query: ALTER TABLE public.table_name ADD COLUMN column_name TYPE;
   ```

3. **Update `supabase/setup/01_tables.sql` to match database reality**
   ```sql
   -- Updated: YYYY-MM-DD - Added [column_name] for [reason]
   ALTER TABLE public.table_name ADD COLUMN column_name TYPE;

   NOTE: This file now documents what IS in the database (via MCP query)
   ```

4. **Update TypeScript types** in relevant type file

5. **Update SQL_FILE_INDEX.md** with changes

6. **Verify with MCP that change was applied successfully**
   ```
   mcp__supabase__execute_sql
   SELECT column_name FROM information_schema.columns
   WHERE table_name = 'your_table' AND column_name = 'new_column';
   ```

**⚠️  IMPORTANT:** Always query MCP first to see current state, then apply migration, then update SQL files.

## RLS Policy Creation Workflow

**When to use:** User asks to create policies, secure table, or implement access control.

**Critical Performance Rules:**
- Wrap ALL functions in SELECT
- Index ALL columns used in policies
- Specify target roles (TO authenticated/anon)
- Use PERMISSIVE policies (avoid RESTRICTIVE)

**Process:**

1. **Read `references/rls-policy-patterns.md`** for templates

2. **Choose correct pattern:**
   - Institution-based access (most common in MyJKKN)
   - User-owned records
   - Role-based access
   - Public read, authenticated write
   - MFA-protected operations

3. **Update `supabase/setup/03_policies.sql`**
   ```sql
   -- =====================================================
   -- [TABLE_NAME] RLS POLICIES
   -- =====================================================
   -- Created: YYYY-MM-DD
   -- Performance: Indexed on [columns]

   CREATE POLICY "policy_name"
   ON public.table_name
   FOR SELECT
   TO authenticated
   USING ((SELECT auth.has_institution_access(institution_id)));
   ```

4. **Create required indexes**
   ```sql
   CREATE INDEX IF NOT EXISTS idx_[table]_[column]
   ON public.table_name(column_name);
   ```

5. **Test with different user roles**

## Database Function Creation Workflow

**When to use:** User asks to create stored procedure, trigger function, or database logic.

**Process:**

1. **Read `references/sql-templates.md`** for function templates

2. **Choose security mode:**
   - **SECURITY INVOKER** (default - use this)
   - **SECURITY DEFINER** (only for auth functions)

3. **Choose volatility:**
   - **IMMUTABLE**: Pure function, same input = same output
   - **STABLE**: Can change between statements
   - **VOLATILE**: Can change within statement

4. **Update `supabase/setup/02_functions.sql`**
   ```sql
   -- =====================================================
   -- FUNCTION: function_name
   -- Purpose: [description]
   -- Created: YYYY-MM-DD
   -- Security: INVOKER (runs with caller permissions)
   -- =====================================================

   CREATE OR REPLACE FUNCTION public.function_name(
       p_param1 TYPE
   )
   RETURNS return_type
   LANGUAGE plpgsql
   SECURITY INVOKER
   SET search_path = ''
   AS $$
   BEGIN
       -- Use fully qualified names
       SELECT column_name
       INTO v_result
       FROM public.table_name
       WHERE condition = p_param1;

       RETURN v_result;
   END;
   $$;
   ```

5. **Grant appropriate permissions**
   ```sql
   GRANT EXECUTE ON FUNCTION public.function_name TO authenticated;
   ```

**See `references/function-templates.md` for complete examples.**

## Edge Function Creation Workflow

**When to use:** User asks to create serverless function, API endpoint, or background task.

**Process:**

1. **Read `references/edge-function-templates.md`** for templates

2. **Choose function type:**
   - Basic function with CORS
   - Function with Supabase client
   - Function with multiple routes (Express/Hono)
   - Function with background tasks
   - Function with file operations
   - Function with AI embeddings

3. **Create function directory**
   ```
   supabase/functions/[function-name]/index.ts
   ```

4. **Use correct import format**
   ```typescript
   import express from "npm:express@4.18.2"
   import { createClient } from "npm:@supabase/supabase-js@2"
   ```

5. **Use Deno.serve (not old serve)**
   ```typescript
   Deno.serve(async (req: Request) => {
     // Handler logic
   })
   ```

6. **Add CORS headers for browser requests**

7. **Deploy function**
   ```bash
   supabase functions deploy function-name
   ```

**See `references/edge-function-templates.md` for complete examples.**

## Auth SSR Implementation

**When to use:** User working with authentication, cookies, or middleware.

**Browser Client (`lib/supabase/client.ts`):**
```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

**Server Client (`lib/supabase/server.ts`):**
```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Ignore if called from Server Component
          }
        },
      },
    }
  )
}
```

**Middleware (`middleware.ts`):**
```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return request.cookies.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // CRITICAL: Must call getUser() to refresh session
  const { data: { user } } = await supabase.auth.getUser()

  if (!user && !request.nextUrl.pathname.startsWith('/login')) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  return supabaseResponse  // MUST return supabaseResponse
}
```

**See `references/auth-ssr-patterns.md` for complete patterns.**

## Debug Workflow

**When to use:** User reports database error, performance issue, or unexpected behavior.

**Process:**

1. **Query REAL-TIME database state with Supabase MCP (ALWAYS FIRST)**
   ```
   Get actual data:
   mcp__supabase__execute_sql
   SELECT * FROM public.table_name WHERE condition;

   Check table structure:
   mcp__supabase__execute_sql
   \d public.table_name

   Get table statistics:
   mcp__supabase__execute_sql
   SELECT COUNT(*), status FROM public.table_name GROUP BY status;
   ```

2. **Check RLS policies using MCP**
   ```
   Query actual policies in database:
   mcp__supabase__execute_sql
   SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
   FROM pg_policies
   WHERE tablename = 'your_table';

   Check if RLS is enabled:
   mcp__supabase__execute_sql
   SELECT tablename, rowsecurity
   FROM pg_tables
   WHERE schemaname = 'public' AND tablename = 'your_table';
   ```

3. **Verify user permissions using MCP**
   ```
   mcp__supabase__execute_sql
   SELECT auth.jwt()->>'role' as user_role;

   mcp__supabase__execute_sql
   SELECT auth.has_institution_access('institution-id-here'::uuid);
   ```

4. **Check foreign key constraints using MCP**
   ```
   mcp__supabase__execute_sql
   SELECT
       tc.constraint_name,
       tc.table_name,
       kcu.column_name,
       ccu.table_name AS foreign_table_name,
       ccu.column_name AS foreign_column_name
   FROM information_schema.table_constraints AS tc
   JOIN information_schema.key_column_usage AS kcu
       ON tc.constraint_name = kcu.constraint_name
   JOIN information_schema.constraint_column_usage AS ccu
       ON ccu.constraint_name = tc.constraint_name
   WHERE tc.constraint_type = 'FOREIGN KEY'
       AND tc.table_name = 'your_table';
   ```

5. **Check indexes using MCP**
   ```
   mcp__supabase__execute_sql
   SELECT indexname, indexdef
   FROM pg_indexes
   WHERE schemaname = 'public' AND tablename = 'your_table';
   ```

6. **Test query performance using MCP**
   ```
   mcp__supabase__execute_sql
   EXPLAIN ANALYZE
   SELECT * FROM public.table_name WHERE condition;
   ```

**⚠️  IMPORTANT:** NEVER read SQL files for debugging - always query MCP for current database state.

## PostgreSQL Style Guide

**Core Conventions:**
- **lowercase** for all SQL keywords
- **snake_case** for tables and columns
- **Plural** table names (users, orders, products)
- **Singular** column names (user_id, order_date)
- **Schema prefix** in all queries (public.users)
- **Comments** on all tables
- **ISO 8601** dates (yyyy-mm-ddThh:mm:ss.sssss)

**Query Formatting:**
```sql
-- Simple queries: compact
select * from public.users where is_active = true;

-- Complex queries: expanded
select
  users.first_name,
  users.last_name,
  count(orders.id) as total_orders
from
  public.users
left join
  public.orders on users.id = orders.user_id
where
  users.is_active = true
group by
  users.id
order by
  total_orders desc;
```

## Naming Conventions

### Tables and Columns
```sql
-- ✅ CORRECT
CREATE TABLE public.students (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  institution_id UUID NOT NULL,
  first_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ❌ WRONG
CREATE TABLE Student (  -- Should be lowercase plural
  ID INT,              -- Should be UUID
  FirstName VARCHAR    -- Should be snake_case
);
```

### Indexes, Triggers, Functions
- Indexes: `idx_[table]_[column]`
- Triggers: `trg_[table]_[action]`
- Functions: `verb_noun` (get_student_attendance)

## Multi-Tenant Pattern

All MyJKKN tables follow multi-tenant pattern:

```sql
CREATE TABLE public.module_table (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  institution_id UUID NOT NULL REFERENCES public.institutions(id),
  -- other columns
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES public.profiles(id)
);

-- Always filter by institution
SELECT * FROM public.module_table
WHERE institution_id = (
  SELECT auth.jwt() -> 'app_metadata' ->> 'institution_id'
)::uuid;
```

## Pre-Flight Checklist

Before ANY Supabase work:

- [ ] **FIRST: Query real-time database with Supabase MCP** (mcp__supabase__list_tables or execute_sql)
- [ ] Verified table/object doesn't already exist in database
- [ ] Checked current table structure with MCP (if updating)
- [ ] Identified correct file to update (setup/*.sql)
- [ ] Added dated comments for changes
- [ ] Following naming conventions
- [ ] Enabled RLS where needed
- [ ] Created proper indexes
- [ ] Updated SQL_FILE_INDEX.md after changes
- [ ] **NEVER used CLI commands** - only Supabase MCP tools
- [ ] **NEVER trusted SQL files** - always verified with MCP

**⚠️  CRITICAL RULE:** SQL files may be outdated. ALWAYS use MCP to query the actual database state first.

## Resources

### References (Load as needed)
- `references/sql-templates.md` - Complete SQL templates for all object types
- `references/rls-policy-patterns.md` - Performance-optimized RLS policy templates
- `references/auth-ssr-patterns.md` - Complete Auth SSR implementation patterns
- `references/edge-function-templates.md` - Edge function templates and patterns
- `references/module-creation-template.md` - Step-by-step module creation guide

### Scripts (Execute without loading to context)
- `scripts/validate_sql_files.py` - Check for duplicate SQL files
- `scripts/check_index.py` - Verify SQL_FILE_INDEX.md is up to date

### Assets (Templates for output)
- `assets/table-template.sql` - Base table creation template
- `assets/migration-template.sql` - Migration file template

## Quick Commands

### For New Module
```
Create [MODULE_NAME] module with [ENTITIES]. Follow supabase-expert skill:
FIRST query MCP for existing tables, then update setup/01_tables.sql only,
add RLS policies, create types/services/hooks, update index.
```

### For Schema Update
```
Update [TABLE]: add [COLUMNS]. Follow supabase-expert skill:
FIRST query MCP for current structure, apply migration via MCP,
then update SQL files to match database reality.
```

### For RLS Policies
```
Create RLS policies for [TABLE]. Follow supabase-expert skill:
query MCP for existing policies, use performance-optimized patterns,
wrap functions in SELECT, create indexes.
```

### For Edge Function
```
Create Edge Function [NAME] for [PURPOSE]. Follow supabase-expert skill:
use Deno.serve, npm: imports with versions, proper CORS headers.
```

### For Debugging
```
Debug [ISSUE]. Follow supabase-expert skill:
query MCP for real-time database state, check policies with MCP,
verify constraints and indexes via MCP queries.
```

## Common Mistakes to Avoid

1. ❌ **Not querying MCP first** - ALWAYS check real-time database state before any work
2. ❌ **Trusting SQL files** - Files may be outdated, MCP shows reality
3. ❌ **Using CLI commands** - Use Supabase MCP tools exclusively
4. ❌ Creating new SQL files instead of updating existing ones
5. ❌ Using auth.uid() without wrapping in SELECT
6. ❌ Forgetting to create indexes on policy columns
7. ❌ Using SECURITY DEFINER by default
8. ❌ Mixing individual cookie methods (get/set/remove)
9. ❌ Using bare import specifiers in Edge Functions
10. ❌ Forgetting to update SQL_FILE_INDEX.md
11. ❌ Not adding dated comments for changes

**🔴 MOST CRITICAL:** Always use `mcp__supabase__execute_sql` or `mcp__supabase__list_tables` to query database BEFORE reading any SQL files.

## Essential MCP Queries

These are the most useful MCP queries for checking real-time database state:

### List All Tables
```
mcp__supabase__list_tables
```

### Get Table Structure
```
mcp__supabase__execute_sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'your_table'
ORDER BY ordinal_position;
```

### Check if Table Exists
```
mcp__supabase__execute_sql
SELECT EXISTS (
  SELECT FROM information_schema.tables
  WHERE table_schema = 'public' AND table_name = 'your_table'
);
```

### Get All Indexes on Table
```
mcp__supabase__execute_sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'your_table';
```

### Get All Policies on Table
```
mcp__supabase__execute_sql
SELECT policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'your_table';
```

### Check Foreign Keys
```
mcp__supabase__execute_sql
SELECT
    tc.constraint_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name = 'your_table';
```

### Check if RLS is Enabled
```
mcp__supabase__execute_sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND tablename = 'your_table';
```

### Get Table Row Count
```
mcp__supabase__execute_sql
SELECT COUNT(*) FROM public.your_table;
```

### Search for Tables by Pattern
```
mcp__supabase__execute_sql
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public' AND tablename LIKE '%keyword%';
```

**💡 TIP:** Save these queries for quick access during development.

## Integration with Other Tools

**With Memory Server:**
```
Remember: ALWAYS query Supabase MCP for real-time database state FIRST
Remember: SQL files may be outdated - MCP shows reality
Remember: NEVER use CLI commands - only Supabase MCP tools
Remember: MyJKKN uses institution_id for multi-tenancy
Remember: RLS policies need (SELECT auth.uid()) wrapping
Remember: Update SQL files to match database reality (from MCP queries)
```

**With Sequential Thinking:**
```
Use sequential thinking to:
1. Plan complex module creation
2. Debug multi-table issues
3. Design RLS policy hierarchy
4. Optimize database performance
```

**With Task Agents:**
```
Use Task tool with general-purpose agent:
"Follow supabase-expert skill to create [MODULE] module.
FIRST query Supabase MCP for real-time database state.
NEVER create duplicate files. Update SQL files to match database reality."
```

---

**Skill Version:** 1.1.0
**Last Updated:** 2025-01-27
**Tested On:** MyJKKN v1.0 (Supabase, Next.js 15, TypeScript)

**Version 1.1.0 Changes:**
- **CRITICAL:** Added MCP-first approach - ALWAYS query real-time database before reading SQL files
- Removed CLI command usage - exclusively use Supabase MCP tools
- Added Essential MCP Queries section with common database inspection queries
- Updated all workflows to prioritize MCP queries over file reading
- Emphasized that SQL files may be outdated and MCP shows database reality

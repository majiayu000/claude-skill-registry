---
name: database-migrations
description: |
  PostgreSQL migration patterns with RLS, Better Auth integration, and TIMESTAMPTZ.
  Covers main tables, meta tables, child entities, and sample data.
  Use this skill when creating migrations, validating SQL, or generating sample data.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.0.0
---

# Database Migrations Skill

Patterns and tools for PostgreSQL database migrations with RLS, Better Auth, and strict conventions.

## Architecture Overview

```
core/migrations/
├── 001_better_auth_and_functions.sql  # Base auth (DO NOT MODIFY)
├── 002_auth_tables.sql                # Auth tables (DO NOT MODIFY)
├── XXX_[entity]_table.sql             # Main entity table
├── XXX_[entity]_metas.sql             # Meta table (optional)
├── XXX_[entity]_sample_data.sql       # Sample data (optional)
└── XXX_[parent]_[child]_table.sql     # Child entities
```

> **📍 Context-Aware Paths:** Paths shown assume monorepo development. In consumer projects,
> create migrations in `contents/themes/{theme}/migrations/` instead (use sequence 1001+). Core is read-only.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Creating new entity migrations
- Adding meta tables for entities
- Creating child entity relationships
- Validating migration conventions
- Generating sample data

## Core Principles

### 1. Better Auth Integration

**Better Auth uses TEXT for IDs, not UUID type:**

```sql
-- ✅ CORRECT
id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
"userId" TEXT NOT NULL REFERENCES public."users"(id) ON DELETE CASCADE,

-- ❌ WRONG
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
```

**Use existing functions (NEVER redefine):**
- `get_auth_user_id()` - Get current authenticated user ID
- `set_updated_at()` - Auto-update timestamp trigger

### 2. Field Ordering (MANDATORY)

Fields MUST follow this exact order:

```sql
CREATE TABLE IF NOT EXISTS public."EntityName" (
  -- 1. Primary Key (always first)
  id            TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,

  -- 2. Relational Fields (foreign keys)
  "userId"      TEXT NOT NULL REFERENCES public."users"(id) ON DELETE CASCADE,
  "teamId"      TEXT REFERENCES public."teams"(id) ON DELETE CASCADE,

  -- 3. Entity-specific Fields (business logic)
  title         TEXT NOT NULL,
  description   TEXT,
  content       JSONB,
  priority      INTEGER DEFAULT 0,

  -- 4. System Fields (always last)
  status        TEXT DEFAULT 'draft',
  "createdAt"   TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt"   TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3. TIMESTAMPTZ Requirement (CRITICAL)

**ALL timestamps MUST use `TIMESTAMPTZ`, never plain `TIMESTAMP`:**

```sql
-- ✅ CORRECT
"createdAt"  TIMESTAMPTZ NOT NULL DEFAULT now(),
"updatedAt"  TIMESTAMPTZ NOT NULL DEFAULT now(),
"expiresAt"  TIMESTAMPTZ,

-- ❌ FORBIDDEN
"createdAt"  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
```

### 4. CASCADE Rules

```sql
-- ✅ Main entity tables - ALWAYS use CASCADE
DROP TABLE IF EXISTS public."EntityName" CASCADE;

-- ✅ Meta tables - NO DROP (removed by parent CASCADE)
CREATE TABLE IF NOT EXISTS public."EntityName_metas" (...);

-- ✅ Foreign Keys - Use CASCADE for parent-child
REFERENCES public."Parent"(id) ON DELETE CASCADE
```

## RLS Patterns (4 Cases)

### Case 1: Private to Owner
```sql
CREATE POLICY "Entity owner can do all"
ON public."Entity"
FOR ALL TO authenticated
USING ("userId" = public.get_auth_user_id())
WITH CHECK ("userId" = public.get_auth_user_id());
```

### Case 2: Team-Based Access
```sql
CREATE POLICY "Entity team can do all"
ON public."Entity"
FOR ALL TO authenticated
USING (
  "teamId" IN (
    SELECT "teamId" FROM public."members"
    WHERE "userId" = public.get_auth_user_id()
  )
)
WITH CHECK (...);
```

### Case 3: Shared Among Authenticated
```sql
CREATE POLICY "Entity any auth can do all"
ON public."Entity"
FOR ALL TO authenticated
USING (true)
WITH CHECK (true);
```

### Case 4: Public Read with Auth Write
```sql
-- Anonymous can read published
CREATE POLICY "Entity public can select"
ON public."Entity"
FOR SELECT TO anon
USING (published = TRUE);

-- Authenticated can manage all
CREATE POLICY "Entity auth can do all"
ON public."Entity"
FOR ALL TO authenticated
USING (true)
WITH CHECK (true);
```

## Meta Tables Pattern

**CRITICAL: Always use `"entityId"` for foreign key (never `"postId"`, `"userId"`, etc.)**

```sql
CREATE TABLE IF NOT EXISTS public."EntityName_metas" (
  id             TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "entityId"     TEXT NOT NULL REFERENCES public."EntityName"(id) ON DELETE CASCADE,
  "metaKey"      TEXT NOT NULL,
  "metaValue"    JSONB NOT NULL DEFAULT '{}'::jsonb,
  "dataType"     TEXT,
  "isPublic"     BOOLEAN NOT NULL DEFAULT FALSE,
  "isSearchable" BOOLEAN NOT NULL DEFAULT FALSE,
  "createdAt"    TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt"    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT entity_metas_unique_key UNIQUE ("entityId", "metaKey")
);
```

## Child Entities Pattern

**CRITICAL: Always use `"parentId"` for foreign key (never `"clientId"`, `"orderId"`, etc.)**

```sql
CREATE TABLE IF NOT EXISTS public."parent_children" (
  id              TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "parentId"      TEXT NOT NULL REFERENCES public."parent"(id) ON DELETE CASCADE,

  -- Child-specific fields (NO userId - inherited via parent)
  name            TEXT NOT NULL,
  description     TEXT,

  -- System fields
  "createdAt"     TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt"     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RLS inherits parent access
CREATE POLICY "Child inherit parent access"
ON public."parent_children"
FOR ALL TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM public."parent" p
    WHERE p.id = "parentId"
      AND p."userId" = public.get_auth_user_id()
  )
)
WITH CHECK (...);
```

## Scripts

### Validate Migration Conventions
```bash
# Validate a specific migration file
python3 .claude/skills/database-migrations/scripts/validate-migration.py \
  --file core/migrations/017_scheduled_actions_table.sql

# Validate all migrations
python3 .claude/skills/database-migrations/scripts/validate-migration.py \
  --path core/migrations/

# Strict mode (exit with error if issues found)
python3 .claude/skills/database-migrations/scripts/validate-migration.py \
  --path core/migrations/ \
  --strict
```

### Generate Sample Data
```bash
# Generate sample data for an entity
python3 .claude/skills/database-migrations/scripts/generate-sample-data.py \
  --entity posts \
  --count 20

# With custom team and user IDs
python3 .claude/skills/database-migrations/scripts/generate-sample-data.py \
  --entity tasks \
  --count 10 \
  --user-id "user-sample-1" \
  --team-id "team-tmt-001"

# Preview without writing
python3 .claude/skills/database-migrations/scripts/generate-sample-data.py \
  --entity products \
  --dry-run
```

## Required Indexes

```sql
-- ============================================
-- INDEXES
-- ============================================
-- Primary relationships
CREATE INDEX IF NOT EXISTS idx_entity_user_id          ON public."entity"("userId");
CREATE INDEX IF NOT EXISTS idx_entity_team_id          ON public."entity"("teamId");

-- Common query patterns
CREATE INDEX IF NOT EXISTS idx_entity_status           ON public."entity"(status);
CREATE INDEX IF NOT EXISTS idx_entity_created_at       ON public."entity"("createdAt" DESC);

-- Conditional indexes
CREATE INDEX IF NOT EXISTS idx_entity_published        ON public."entity"(published) WHERE published = TRUE;

-- JSONB indexes
CREATE INDEX IF NOT EXISTS idx_entity_payload_gin      ON public."entity" USING GIN (payload);
```

## Trigger Pattern

**Always use existing Better Auth function:**

```sql
-- ============================================
-- TRIGGER updatedAt (uses Better Auth function)
-- ============================================
DROP TRIGGER IF EXISTS entity_set_updated_at ON public."entity";
CREATE TRIGGER entity_set_updated_at
BEFORE UPDATE ON public."entity"
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
```

## Naming Conventions

| Convention | Example |
|------------|---------|
| Table names | camelCase: `"scheduledActions"` |
| Column names | camelCase: `"createdAt"`, `"userId"` |
| Index names | snake_case: `idx_entity_user_id` |
| Policy names | "Entity action description" |
| Constraint names | snake_case: `entity_metas_unique_key` |

## Anti-Patterns

```sql
-- ❌ NEVER: Plain TIMESTAMP
"createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- ❌ NEVER: UUID type (Better Auth uses TEXT)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- ❌ NEVER: Redefine auth functions
CREATE OR REPLACE FUNCTION public.get_auth_user_id()...

-- ❌ NEVER: Wrong meta FK naming
"postId" TEXT NOT NULL REFERENCES public."posts"(id)
-- ✅ CORRECT: "entityId"

-- ❌ NEVER: Wrong child FK naming
"clientId" TEXT NOT NULL REFERENCES public."clients"(id)
-- ✅ CORRECT: "parentId"

-- ❌ NEVER: Business logic in DB triggers
CREATE FUNCTION calculate_order_totals()...
```

## Checklist

Before finalizing a migration:

- [ ] Uses TEXT for all ID fields (not UUID type)
- [ ] References `public."users"` for user relationships
- [ ] Uses `get_auth_user_id()` in RLS (not redefined)
- [ ] Uses `set_updated_at()` in triggers (not redefined)
- [ ] ALL timestamps use `TIMESTAMPTZ` (not `TIMESTAMP`)
- [ ] Uses `now()` (not `CURRENT_TIMESTAMP`)
- [ ] Fields follow strict ordering (id → FK → business → system)
- [ ] Main tables use `DROP ... CASCADE`
- [ ] Meta tables use `"entityId"` (not entity-specific name)
- [ ] Child tables use `"parentId"` (not parent-specific name)
- [ ] Appropriate RLS policies for access pattern
- [ ] Required indexes created
- [ ] Sample data uses `ON CONFLICT` clause

---
name: create-migration
description: |
  Créer une migration Supabase avec RLS.
  TRIGGERS : migration, créer table, modifier schema, nouvelle table, alter table
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Create Migration Supabase

## Procédure

### 1. Vérifier les migrations existantes
```bash
ls -la supabase/migrations/
```

### 2. Créer le fichier migration

Nom : `{timestamp}_{description}.sql`

```sql
-- Migration: {nom}
-- Description: {description}

-- ============================================
-- TABLE
-- ============================================
create table if not exists {table_name} (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- ============================================
-- RLS (OBLIGATOIRE)
-- ============================================
alter table {table_name} enable row level security;

-- SELECT: USING uniquement
create policy "{table_name}_select_own"
on {table_name} for select
to authenticated
using ((select auth.uid()) = user_id);

-- INSERT: WITH CHECK uniquement
create policy "{table_name}_insert_own"
on {table_name} for insert
to authenticated
with check ((select auth.uid()) = user_id);

-- UPDATE: USING + WITH CHECK
create policy "{table_name}_update_own"
on {table_name} for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

-- DELETE: USING uniquement
create policy "{table_name}_delete_own"
on {table_name} for delete
to authenticated
using ((select auth.uid()) = user_id);

-- ============================================
-- INDEXES
-- ============================================
create index if not exists idx_{table_name}_user_id
on {table_name}(user_id);

create index if not exists idx_{table_name}_created_at
on {table_name}(created_at desc);
```

### 3. Règles RLS

| Opération | USING | WITH CHECK |
|-----------|-------|------------|
| SELECT | ✅ | ❌ |
| INSERT | ❌ | ✅ |
| UPDATE | ✅ | ✅ |
| DELETE | ✅ | ❌ |

**Important** : Utiliser `(select auth.uid())` (pas `auth.uid()` direct) pour la performance.

### 4. Appliquer

Utiliser **MCP Supabase** pour appliquer la migration (jamais CLI directe).

### 5. Mettre à jour le PRD module

Documenter dans `modules/{module}/prd/{module}.md`.

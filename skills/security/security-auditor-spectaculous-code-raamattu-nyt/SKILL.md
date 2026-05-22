---
name: security-auditor
description: |
  Comprehensive Supabase security auditor for RLS policies, table privileges (GRANTs), and access control validation.

  Use when:
  - Auditing database security (RLS + GRANTs)
  - Generating access matrix (who can SELECT/INSERT/UPDATE/DELETE which tables)
  - Finding security gaps (missing RLS, overly permissive GRANTs)
  - Validating PostgREST access patterns
  - Creating security documentation for Docs/context/
  - Creating RLS policies for new or existing tables
  - Validating user data protection
  - Checking admin access patterns
  - Identifying security vulnerabilities

  Triggers: "security audit", "access matrix", "who can update", "missing RLS", "check grants", "security gaps", "table permissions", "RLS policy", "row level security", "validate security", "user data protection", "admin access"
---

# Security Auditor

Audit Supabase security combining RLS policies and table-level GRANTs.

## Key Concept: Layered Security

PostgREST access requires BOTH:
1. **GRANT** - Table-level privilege (can the role attempt the operation?)
2. **RLS Policy** - Row-level security (which rows are allowed?)

```
Client Request → GRANT check → RLS check → Data
                 (can try?)    (which rows?)
```

A table with `GRANT UPDATE` but no RLS UPDATE policy = **security gap**.

## Quick Audit Commands

### 1. Generate Full Access Matrix

Run the audit script to generate `Docs/context/security-matrix.md`:

```bash
python .claude/skills/security-auditor/scripts/audit_security.py
```

### 2. Quick SQL Checks

**Tables with RLS disabled:**
```sql
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
  AND tablename NOT IN (
    SELECT tablename FROM pg_class c
    JOIN pg_namespace n ON c.relnamespace = n.oid
    WHERE c.relrowsecurity = true
      AND n.nspname IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
  );
```

**GRANTs without matching RLS policies:**
```sql
SELECT DISTINCT tp.table_schema, tp.table_name, tp.privilege_type
FROM information_schema.table_privileges tp
WHERE tp.grantee = 'authenticated'
  AND tp.privilege_type IN ('UPDATE', 'DELETE', 'INSERT')
  AND tp.table_schema IN ('public', 'bible_schema')
  AND NOT EXISTS (
    SELECT 1 FROM pg_policies pp
    WHERE pp.schemaname = tp.table_schema
      AND pp.tablename = tp.table_name
      AND (pp.cmd = tp.privilege_type OR pp.cmd = 'ALL')
  );
```

**Risky FOR ALL policies (should be explicit per-operation):**
```sql
SELECT schemaname, tablename, policyname, roles::text,
  CASE WHEN with_check IS NULL THEN 'MISSING WITH CHECK!' ELSE 'OK' END as with_check_status
FROM pg_policies
WHERE cmd = 'ALL'
  AND schemaname IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback');
```

**Policies using `TO public` (should be role-specific):**
```sql
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies
WHERE roles::text = '{public}'
  AND schemaname IN ('public', 'bible_schema');
```

**UPDATE/INSERT policies missing WITH CHECK:**
```sql
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies
WHERE cmd IN ('UPDATE', 'INSERT')
  AND with_check IS NULL
  AND schemaname IN ('public', 'bible_schema');
```

**Check specific table security:**
```sql
SELECT
  'RLS Status' as check_type,
  CASE WHEN c.relrowsecurity THEN 'Enabled' ELSE 'DISABLED!' END as status
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE c.relname = 'your_table' AND n.nspname = 'public'

UNION ALL

SELECT 'Policy: ' || policyname, cmd || ' for ' || roles::text
FROM pg_policies
WHERE tablename = 'your_table';
```

## Access Matrix Format

The audit generates markdown tables like:

| Table | anon | authenticated | Admin Required |
|-------|------|---------------|----------------|
| verses | R | R | - |
| profiles | R | RU (own) | - |
| ai_features | R | CRUD | Yes (write) |

Legend: R=Read, C=Create, U=Update, D=Delete, (own)=user's own rows only

## Common Security Patterns

### Pattern 1: Public Read, Admin Write
```sql
GRANT SELECT ON table TO anon, authenticated;
GRANT INSERT, UPDATE, DELETE ON table TO authenticated;

CREATE POLICY "anon_read" ON table FOR SELECT TO anon USING (true);
CREATE POLICY "auth_read" ON table FOR SELECT TO authenticated USING (true);
-- Explicit per-operation policies (avoid FOR ALL):
CREATE POLICY "admin_insert" ON table FOR INSERT TO authenticated
  WITH CHECK (schema.is_admin());
CREATE POLICY "admin_update" ON table FOR UPDATE TO authenticated
  USING (schema.is_admin()) WITH CHECK (schema.is_admin());
CREATE POLICY "admin_delete" ON table FOR DELETE TO authenticated
  USING (schema.is_admin());
```

### Pattern 2: User-Owned Data
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON table TO authenticated;

CREATE POLICY "user_crud" ON table FOR ALL TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());
```

### Pattern 3: Service Role Only (Edge Functions)
```sql
-- No GRANTs to anon/authenticated
-- Access only via SECURITY DEFINER functions or service_role
```

## Security Checklist

### For Each Table:
- [ ] RLS enabled (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`)
- [ ] GRANTs match intended access (no excess privileges)
- [ ] RLS policies exist for each granted operation
- [ ] UPDATE policies have both USING and WITH CHECK
- [ ] DELETE policies have USING clause
- [ ] Admin operations check `has_role(auth.uid(), 'admin')` or schema-specific `is_admin()`
- [ ] Indexes exist on RLS-referenced columns (user_id, created_by, status)

### Red Flags:
- `GRANT UPDATE` without UPDATE RLS policy
- `GRANT DELETE` without DELETE RLS policy
- RLS policies with `USING (true)` for write operations
- `TO public` grants (allows unauthenticated access)
- **`FOR ALL` policies** - Avoid these; use explicit per-operation policies instead
- **Policies targeting `public` role** - Use explicit `TO anon` or `TO authenticated`
- **Missing `WITH CHECK`** on UPDATE/INSERT policies

## Fixing Security Gaps

### Missing RLS Policy for GRANT

```sql
-- Option 1: Add restrictive policy
CREATE POLICY "admin_update" ON schema.table
FOR UPDATE TO authenticated
USING (public.has_role(auth.uid(), 'admin'))
WITH CHECK (public.has_role(auth.uid(), 'admin'));

-- Option 2: Revoke the grant if not needed
REVOKE UPDATE ON schema.table FROM authenticated;
```

### Missing USING/WITH CHECK

UPDATE policies need both:
```sql
CREATE POLICY "user_update" ON table
FOR UPDATE TO authenticated
USING (user_id = auth.uid())      -- Which rows can be read for update
WITH CHECK (user_id = auth.uid()); -- What the updated row must satisfy
```

## RLS Policy Patterns Reference

For detailed policy templates, testing procedures, and SECURITY DEFINER patterns, see:
**[references/rls-patterns.md](references/rls-patterns.md)**

Contents:
- User-owned data (full CRUD example)
- Public read, admin write
- Admin-only tables (audit logs)
- Role-based access
- `has_role()` function
- SECURITY DEFINER functions
- Testing RLS policies
- Common vulnerabilities table
- Validation checklists

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| Database migrations | `supabase-migration-writer` |
| Edge Function security | `edge-function-generator` |

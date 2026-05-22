---
name: supabase-rls
description: Apply when implementing multi-tenant data isolation, user-specific data access, or any scenario requiring row-level authorization in Supabase.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://supabase.com/docs/guides/auth/row-level-security
  - https://supabase.com/docs/guides/database/postgres/row-level-security
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [supabase, security, database, rls]
---

## When to Use

Apply when implementing multi-tenant data isolation, user-specific data access, or any scenario requiring row-level authorization in Supabase.

## Patterns

### Pattern 1: User Owns Row
```sql
-- Source: https://supabase.com/docs/guides/auth/row-level-security
CREATE POLICY "Users can view own data"
ON todos FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own data"
ON todos FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### Pattern 2: Role-Based Access
```sql
-- Source: https://supabase.com/docs/guides/auth/row-level-security#policies-with-joins
CREATE POLICY "Admins full access"
ON todos FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role = 'admin'
  )
);
```

### Pattern 3: Organization/Tenant Isolation
```sql
-- Source: https://supabase.com/docs/guides/auth/row-level-security
CREATE POLICY "Org members access"
ON projects FOR SELECT
USING (
  org_id IN (
    SELECT org_id FROM org_members
    WHERE user_id = auth.uid()
  )
);
```

### Pattern 4: Public Read, Auth Write
```sql
-- Source: https://supabase.com/docs/guides/auth/row-level-security
CREATE POLICY "Public read" ON posts
FOR SELECT USING (true);

CREATE POLICY "Auth users write" ON posts
FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
```

## Anti-Patterns

- **No RLS on sensitive tables** - Always enable: `ALTER TABLE x ENABLE ROW LEVEL SECURITY`
- **Using service_role in client** - Bypasses RLS; use only server-side
- **Complex JOINs in policies** - Causes performance issues; denormalize if needed
- **Forgetting FOR clause** - Specify SELECT/INSERT/UPDATE/DELETE explicitly

## Verification Checklist

- [ ] RLS enabled on table: `ALTER TABLE x ENABLE ROW LEVEL SECURITY`
- [ ] Policies exist for all needed operations (SELECT, INSERT, UPDATE, DELETE)
- [ ] Tested with `auth.uid()` returning expected user
- [ ] Service role operations stay server-side only
- [ ] No N+1 queries in policy JOINs

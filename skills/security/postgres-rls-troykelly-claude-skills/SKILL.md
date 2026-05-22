---
name: postgres-rls
description: MANDATORY when touching auth tables, tenant isolation, RLS policies, or multi-tenant database code - enforces Row Level Security best practices and catches common bypass vulnerabilities
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__github__*
model: opus
---

# PostgreSQL Row Level Security

## Overview

Row Level Security (RLS) provides defense-in-depth for data isolation. When implemented correctly, it prevents data leaks even if application code misses a filter. When implemented incorrectly, it creates false security confidence while data bleeds between tenants.

**Core principle:** RLS is your last line of defense, not your only one. Get it wrong and you have a data breach.

**Announce at start:** "I'm applying postgres-rls to verify Row Level Security implementation."

## When This Skill Applies

This skill is MANDATORY when ANY of these patterns are touched:

| Pattern | Examples |
|---------|----------|
| `**/migrations/**/*tenant*` | migrations/001_add_tenant_id.sql |
| `**/migrations/**/*rls*` | migrations/005_enable_rls.sql |
| `**/migrations/**/*policy*` | migrations/010_create_policies.sql |
| `**/*policy*.sql` | db/policies.sql |
| `**/auth/**` | src/auth/context.ts |
| `**/*tenant*` | lib/tenant.ts, services/tenantService.ts |
| `**/*multi-tenant*` | docs/multi-tenant-architecture.md |

Check with:
```bash
git diff --name-only HEAD~1 | grep -iE '(tenant|rls|policy|auth.*sql|multi.?tenant)'
```

## The Critical Vulnerabilities

### 1. Superuser Bypass (CRITICAL)

Superusers and roles with `BYPASSRLS` ignore ALL policies.

```sql
-- DANGEROUS: Testing as superuser shows RLS "working" when it's bypassed
SET ROLE postgres;
SELECT * FROM orders;  -- Returns ALL rows, RLS ignored

-- CORRECT: Test as application role
SET ROLE app_user;
SELECT * FROM orders;  -- Returns only permitted rows
```

**Checklist:**
- [ ] Application connects as non-superuser role
- [ ] No roles have `BYPASSRLS` attribute
- [ ] Tests run as application role, NOT superuser

### 2. Table Owner Bypass (CRITICAL)

Table owners bypass RLS unless `FORCE ROW LEVEL SECURITY` is set.

```sql
-- INCOMPLETE: Owners bypass this
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- COMPLETE: Everyone including owners must obey policies
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

**Checklist:**
- [ ] All RLS tables have both ENABLE and FORCE
- [ ] Migration includes both statements

### 3. View Bypass (CRITICAL)

Views run with creator's privileges by default. Views owned by superusers bypass RLS entirely.

```sql
-- DANGEROUS: View owned by superuser bypasses RLS
CREATE VIEW all_orders AS SELECT * FROM orders;

-- SAFE (PostgreSQL 15+): Security invoker respects caller's RLS
CREATE VIEW user_orders
WITH (security_invoker = true)
AS SELECT * FROM orders;
```

**Checklist:**
- [ ] All views on RLS tables use `security_invoker = true` (PG15+)
- [ ] Views not owned by superuser roles
- [ ] Materialized views documented as bypassing RLS

### 4. USING vs WITH CHECK Mismatch (HIGH)

`USING` filters reads; `WITH CHECK` validates writes. Missing `WITH CHECK` allows inserting data you can't see.

```sql
-- INCOMPLETE: User can INSERT rows they can't SELECT
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- COMPLETE: Both read and write protected
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

**Checklist:**
- [ ] All policies have both USING and WITH CHECK
- [ ] WITH CHECK logic matches security intent

### 5. Thread-Local Context Leakage (HIGH)

Connection pooling can leak tenant context between requests.

```sql
-- DANGEROUS: Context persists across pooled connections
SET app.tenant_id = 'tenant-123';

-- SAFE: Use SET LOCAL inside transaction (auto-resets)
BEGIN;
SET LOCAL app.tenant_id = 'tenant-123';
-- ... queries ...
COMMIT;  -- Context automatically cleared
```

**Application pattern:**
```typescript
// DANGEROUS: Leaks between requests
await db.query(`SET app.tenant_id = '${tenantId}'`);

// SAFE: Transaction-scoped context
await db.transaction(async (trx) => {
  await trx.raw(`SET LOCAL app.tenant_id = ?`, [tenantId]);
  // ... queries ...
});
```

**Checklist:**
- [ ] Always use `SET LOCAL` not `SET`
- [ ] Context set inside transactions
- [ ] Post-request handler resets context (defense in depth)

### 6. SQL Injection in Policy Functions (HIGH)

Functions used in policies can be injection vectors.

```sql
-- DANGEROUS: If current_tenant() uses user input unsafely
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_tenant());

-- The function itself must be injection-safe:
CREATE OR REPLACE FUNCTION current_tenant()
RETURNS uuid AS $$
BEGIN
  -- SAFE: Casts to UUID, not string concatenation
  RETURN current_setting('app.tenant_id')::uuid;
END;
$$ LANGUAGE plpgsql STABLE;
```

### 7. Materialized Views and Data Export (MEDIUM)

Materialized views don't respect source table RLS. Data exports may bypass policies.

```sql
-- DANGEROUS: Contains ALL tenants' data
CREATE MATERIALIZED VIEW order_stats AS
SELECT tenant_id, count(*) FROM orders GROUP BY tenant_id;

-- Background jobs with superuser access can export all data
```

**Checklist:**
- [ ] Materialized views documented as security-sensitive
- [ ] Export jobs run as application role
- [ ] Audit log for bulk data access

## Performance Considerations

### Index Policy Columns

```sql
-- Without index: Sequential scan on every query
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Add index for policy column
CREATE INDEX idx_orders_tenant_id ON orders(tenant_id);
```

### Wrap Functions in Subqueries

Functions called per-row are expensive. Wrap in subquery for single evaluation:

```sql
-- SLOW: Function called per row
CREATE POLICY access_check ON documents
  USING (user_has_access(auth.uid(), id));

-- FASTER: Evaluated once, cached
CREATE POLICY access_check ON documents
  USING ((SELECT auth.uid()) = owner_id);
```

### Use SECURITY DEFINER for Complex Checks

Avoid RLS policy chains with SECURITY DEFINER functions:

```sql
-- SLOW: RLS on permissions table also evaluated
CREATE POLICY access_check ON documents
  USING (id IN (SELECT document_id FROM permissions WHERE user_id = auth.uid()));

-- FASTER: Bypass RLS chain with SECURITY DEFINER
CREATE OR REPLACE FUNCTION user_document_ids(uid uuid)
RETURNS SETOF uuid AS $$
  SELECT document_id FROM permissions WHERE user_id = uid;
$$ LANGUAGE sql STABLE SECURITY DEFINER;

CREATE POLICY access_check ON documents
  USING (id IN (SELECT * FROM user_document_ids(auth.uid())));
```

### Denormalize for Performance

Store tenant_id on every table, even if "obvious" from joins:

```sql
-- SLOW: Must join to get tenant context
CREATE POLICY order_items_policy ON order_items
  USING (order_id IN (
    SELECT id FROM orders WHERE tenant_id = current_setting('app.tenant_id')::uuid
  ));

-- FAST: Direct column check
ALTER TABLE order_items ADD COLUMN tenant_id uuid;
CREATE POLICY order_items_policy ON order_items
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Migration Pattern

### Safe RLS Migration

```sql
-- Step 1: Add column (if needed)
ALTER TABLE orders ADD COLUMN IF NOT EXISTS tenant_id uuid;

-- Step 2: Backfill data (batched for large tables)
UPDATE orders SET tenant_id = (
  SELECT tenant_id FROM customers WHERE customers.id = orders.customer_id
) WHERE tenant_id IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE orders ALTER COLUMN tenant_id SET NOT NULL;

-- Step 4: Create index
CREATE INDEX CONCURRENTLY idx_orders_tenant_id ON orders(tenant_id);

-- Step 5: Enable RLS (both statements!)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Step 6: Create policies
CREATE POLICY tenant_isolation ON orders
  FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

-- Step 7: Grant appropriate permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO app_role;
```

## Testing RLS

### Required Tests

```typescript
describe('RLS Policies', () => {
  it('tenant A cannot see tenant B data', async () => {
    // Insert as tenant A
    await setTenantContext('tenant-a');
    await db('orders').insert({ id: 1, tenant_id: 'tenant-a', amount: 100 });

    // Switch to tenant B
    await setTenantContext('tenant-b');

    // Should not see tenant A's data
    const orders = await db('orders').select();
    expect(orders).toHaveLength(0);
  });

  it('cannot insert data for other tenant', async () => {
    await setTenantContext('tenant-a');

    await expect(
      db('orders').insert({ tenant_id: 'tenant-b', amount: 100 })
    ).rejects.toThrow(/violates row-level security/);
  });

  it('superuser role is not used in application', async () => {
    const result = await db.raw('SELECT current_user');
    expect(result.rows[0].current_user).not.toBe('postgres');
  });
});
```

### Test as Non-Superuser

```bash
# Create test role
CREATE ROLE test_app_user;
GRANT app_role TO test_app_user;

# Run tests as this role
psql -U test_app_user -d testdb -f tests/rls_tests.sql
```

## RLS Policy Artifact

When implementing RLS, post this artifact to the issue:

```markdown
<!-- RLS_IMPLEMENTATION:START -->
## Row Level Security Implementation

### Tables with RLS Enabled

| Table | ENABLE | FORCE | Policies | Index |
|-------|--------|-------|----------|-------|
| orders | ✅ | ✅ | tenant_isolation | idx_orders_tenant_id |
| order_items | ✅ | ✅ | tenant_isolation | idx_order_items_tenant_id |
| customers | ✅ | ✅ | tenant_isolation | idx_customers_tenant_id |

### Policy Details

| Table | Policy | USING | WITH CHECK |
|-------|--------|-------|------------|
| orders | tenant_isolation | tenant_id = current_tenant() | tenant_id = current_tenant() |

### Security Verification

- [ ] Application connects as non-superuser role
- [ ] All RLS tables have FORCE ROW LEVEL SECURITY
- [ ] All policies have WITH CHECK clause
- [ ] Context uses SET LOCAL (transaction-scoped)
- [ ] Views use security_invoker = true
- [ ] Policy columns are indexed
- [ ] Cross-tenant tests written and passing

### Application Role
- Role name: `app_service`
- BYPASSRLS: `false`
- Superuser: `false`

**Verified At:** [timestamp]
<!-- RLS_IMPLEMENTATION:END -->
```

## Checklist

Before completing RLS implementation:

- [ ] All tables have ENABLE and FORCE ROW LEVEL SECURITY
- [ ] All policies have both USING and WITH CHECK
- [ ] Application connects as non-superuser, non-BYPASSRLS role
- [ ] Context set with SET LOCAL inside transactions
- [ ] Views use security_invoker = true (PG15+)
- [ ] Policy columns indexed
- [ ] Cross-tenant isolation tests passing
- [ ] RLS artifact posted to issue

## Integration

This skill is triggered by:
- Changes to migration files with tenant/rls/policy patterns
- Changes to auth-related database code
- Multi-tenant architecture changes

This skill integrates with:
- `security-review` - RLS is part of broader security review
- `database-architecture` - RLS decisions are architectural
- `local-service-testing` - Must test RLS against real Postgres

## References

- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Common RLS Footguns](https://www.bytebase.com/blog/postgres-row-level-security-footguns/)
- [RLS Performance Optimization](https://scottpierce.dev/posts/optimizing-postgres-rls/)
- [AWS Multi-tenant RLS](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/)

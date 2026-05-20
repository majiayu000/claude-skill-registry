---
name: supabase
description: Supabase CLI, Postgres performance, and schema patterns. Use for database operations, queries, RLS, and migrations.
triggers:
  - db
  - supabase
  - postgres
  - rls
  - migration
  - schema
  - table
  - database
  - edge function
allowed-tools: Bash
model: opus
user-invocable: true
---

# Supabase

Use CLI instead of MCP - more reliable, fewer permission issues.

## Common Commands

```bash
# Apply migrations (limit output)
supabase db push --project-ref PROJECT_ID 2>&1 | tail -10

# Run SQL directly
supabase db execute --sql "SELECT * FROM table LIMIT 5" --project-ref PROJECT_ID

# Deploy edge functions
supabase functions deploy FUNCTION_NAME --project-ref PROJECT_ID

# Deploy all functions
supabase functions deploy --project-ref PROJECT_ID

# List projects
supabase projects list

# Check status
supabase status --project-ref PROJECT_ID
```

## Context-Efficient Patterns

```bash
# Limit output to reduce context
supabase db push 2>&1 | tail -5

# Check if migration exists before applying
supabase db execute --sql "SELECT 1 FROM table LIMIT 1" 2>&1 | grep -q "1" && echo "exists"

# Run in background for long operations
Bash({ command: "supabase functions deploy --project-ref X", run_in_background: true })
```

## Project IDs

Get from CLAUDE.md or:
```bash
supabase projects list 2>&1 | grep -E "^\w"
```

## Multi-Org Auth

CLI only supports one token at a time. System env var may not match the current project — always check. A 401 means wrong token, do not retry.

```bash
# Option 1: Inline token (best for multi-org)
SUPABASE_ACCESS_TOKEN=$SUPABASE_TOKEN_REELR supabase db push --project-ref XXX

# Option 2: Source project's .env.local first
# .env.local is auto-loaded by session-start hook - no need to source
supabase db push --project-ref $SUPABASE_PROJECT_ID

# Option 3: Use --db-url with connection string (bypasses auth)
supabase db execute --db-url "postgresql://postgres:PASSWORD@db.XXX.supabase.co:5432/postgres" --sql "..."
```

**Project .env.local should have:**
```env
SUPABASE_ACCESS_TOKEN=sbp_xxx
SUPABASE_PROJECT_ID=xxx
SUPABASE_DB_PASSWORD=xxx
```

## Direct psql (Most Reliable)

**Use Pooler URL (IPv4 compatible), not direct connection:**
```bash
# Pooler - IPv4 compatible (use this)
psql "postgresql://postgres.REF:PASS@aws-0-REGION.pooler.supabase.com:6543/postgres" -c "SELECT 1"
```

Get pooler URL: Dashboard > Connect > Connection String > Session Pooler

---

## Postgres Performance

### Missing Indexes (Critical)
```sql
-- BAD: Full table scan
SELECT * FROM orders WHERE customer_id = 123;

-- GOOD: Add index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### N+1 Queries (Critical)
```sql
-- BAD: N+1 queries
SELECT * FROM orders WHERE id = 1;
SELECT * FROM customers WHERE id = (order.customer_id); -- repeated

-- GOOD: Single join
SELECT o.*, c.*
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.id = 1;
```

### RLS Performance (Critical)
```sql
-- BAD: Function call in RLS (slow)
CREATE POLICY "users" ON profiles
  USING (user_id = get_current_user_id());

-- GOOD: Use auth.uid() directly
CREATE POLICY "users" ON profiles
  USING (user_id = auth.uid());
```

### Connection Pooling
```
Supabase default: Transaction mode (pgbouncer)
- Use for serverless/edge functions
- Prepared statements require session mode
- Set pool size based on: max_connections / num_instances
```

### Foreign Key Indexes
```sql
-- Always index foreign keys!
ALTER TABLE orders ADD CONSTRAINT fk_customer
  FOREIGN KEY (customer_id) REFERENCES customers(id);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### Priority Reference

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Query Performance | High - Missing indexes, composite indexes |
| 2 | Connection Management | High - Pooling, limits, idle timeout |
| 3 | Security & RLS | High - RLS basics, RLS performance |
| 4 | Schema Design | HIGH - Data types, PKs, FK indexes, partitioning |
| 5 | Concurrency & Locking | MEDIUM-HIGH - Short transactions, deadlock prevention |
| 6 | Data Access Patterns | MEDIUM - N+1, pagination, batch inserts, upsert |

### Detailed References

| File | When to Load |
|------|--------------|
| `references/query-missing-indexes.md` | Query optimization |
| `references/conn-pooling.md` | Connection issues |
| `references/security-rls-performance.md` | Slow RLS policies |
| `references/security-rls-basics.md` | Setting up RLS |
| `references/data-n-plus-one.md` | Multiple query issues |
| `references/monitor-explain-analyze.md` | Query debugging |

---

## Schema & RLS Patterns

### Standard Table Template

```sql
CREATE TABLE IF NOT EXISTS public.[table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Always enable RLS
ALTER TABLE public.[table_name] ENABLE ROW LEVEL SECURITY;

-- User owns row
CREATE POLICY "Users access own data"
  ON public.[table_name] FOR ALL
  USING (auth.uid() = user_id);
```

### Profiles Table (Standard)

```sql
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-create on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### CLI Workflow

```bash
# View schema
npx supabase db dump --schema public | head -200

# Create migration
npx supabase migration new create_[table_name]

# Apply migration
npx supabase db push
```

### Safety Rules

**Do:**
- Enable RLS on every table
- Use migrations for schema changes
- Include ON DELETE CASCADE for FKs
- Add created_at/updated_at columns

**Avoid:**
- Disable RLS in production
- Hardcode secrets in migrations
- Delete tables without confirmation

### Detailed Rules

| Rule | When to Load |
|------|--------------|
| `rules/rls-patterns.md` | RLS policy examples |
| `rules/security-patterns.md` | Security hardening |
| `rules/multi-account.md` | Multi-account CLI setup |

Source: [supabase/agent-skills](https://github.com/supabase/agent-skills)

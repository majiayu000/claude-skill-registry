---
name: arcanea-supabase-patterns
description: Supabase + PostgreSQL patterns for Arcanea. Use when writing SQL queries, designing database schemas, implementing Row Level Security, managing connections, optimizing Supabase queries, or working with Supabase Auth, Realtime, or Storage. Triggers on: supabase, postgres, SQL, RLS, row level security, schema, migration, database, auth, realtime, storage. Sourced from Supabase Engineering's official postgres-best-practices skill.
license: MIT (source: supabase/agent-skills)
metadata:
  author: Arcanea (adapted from Supabase Engineering)
  version: "1.0.0"
  stack: Supabase (PostgreSQL + Auth + Realtime + Storage), Next.js 16
---

# Arcanea Supabase & PostgreSQL Patterns

> *"Lyssandria guards the Foundation Gate at 174 Hz — Earth, stability. Your database is the Foundation. Build it with the permanence of stone."*

Adapted from Supabase Engineering's official Postgres best practices (8 categories, prioritized by impact).

## Rule Categories by Priority

| Priority | Category | Impact | Focus |
|----------|----------|--------|-------|
| 1 | Query Performance | CRITICAL | Indexes, query plans |
| 2 | Connection Management | CRITICAL | Pooling, serverless |
| 3 | Security & RLS | CRITICAL | Row Level Security |
| 4 | Schema Design | HIGH | Types, constraints |
| 5 | Concurrency & Locking | MEDIUM-HIGH | Deadlocks, transactions |
| 6 | Data Access Patterns | MEDIUM | Joins, pagination |
| 7 | Monitoring | LOW-MEDIUM | EXPLAIN, pg_stat |
| 8 | Advanced Features | LOW | JSONB, full-text |

---

## 1. Query Performance (CRITICAL)

### Index every foreign key and filter column
```sql
-- Arcanea schema: always index FK columns
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_gate ON user_progress(gate_name);
CREATE INDEX idx_prompts_collection_id ON prompts(collection_id);
CREATE INDEX idx_prompts_created_by ON prompts(created_by);

-- Partial index for hot paths (unlocked gates only)
CREATE INDEX idx_unlocked_gates ON user_progress(user_id, gate_name)
WHERE status = 'unlocked';

-- Composite for frequent WHERE + ORDER BY
CREATE INDEX idx_prompts_collection_created ON prompts(collection_id, created_at DESC);
```

### Check EXPLAIN ANALYZE before shipping queries
```sql
-- Always run before shipping any non-trivial query
EXPLAIN ANALYZE
SELECT g.name, g.gate, g.frequency_hz, gb.name as godbeast
FROM guardians g
JOIN godbeasts gb ON gb.guardian_id = g.id
WHERE g.element = 'Fire'
ORDER BY g.frequency_hz;

-- Seq Scan = missing index. Index Scan = good.
-- Actual rows vs estimated rows gap > 10x = stale statistics → ANALYZE
```

### Avoid N+1 queries — use joins or select with relations
```typescript
// BAD — N+1 in Supabase
const { data: guardians } = await supabase.from('guardians').select()
for (const g of guardians) {
  const { data: godbeast } = await supabase // N queries!
    .from('godbeasts').select().eq('guardian_id', g.id).single()
}

// GOOD — single query with relation
const { data } = await supabase
  .from('guardians')
  .select(`
    id, name, gate, frequency_hz,
    godbeast:godbeasts(id, name, element, description)
  `)
  .eq('element', 'Fire')
```

### Use `.limit()` and pagination — never load entire tables
```typescript
// Arcanea pattern: cursor-based pagination for large datasets
const PAGE_SIZE = 20

const { data, error } = await supabase
  .from('prompts')
  .select('id, title, created_at, element')
  .order('created_at', { ascending: false })
  .limit(PAGE_SIZE)
  .range(offset, offset + PAGE_SIZE - 1)
```

---

## 2. Connection Management (CRITICAL)

### Use Supabase SSR client in Next.js — never direct postgres
```typescript
// lib/supabase-server.ts — for Server Components and Route Handlers
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import type { Database } from '@/types/supabase'

export async function createSupabaseServer() {
  const cookieStore = await cookies() // Next.js 16: async cookies
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookies) => cookies.forEach(({ name, value, options }) =>
          cookieStore.set(name, value, options)
        ),
      },
    }
  )
}
```

### Browser client — singleton pattern
```typescript
// lib/supabase-browser.ts — one instance per browser session
import { createBrowserClient } from '@supabase/ssr'
import type { Database } from '@/types/supabase'

let client: ReturnType<typeof createBrowserClient<Database>> | null = null

export function getSupabaseBrowser() {
  if (!client) {
    client = createBrowserClient<Database>(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    )
  }
  return client
}
```

### Serverless: use Supabase's built-in pooling (pgbouncer mode)
```
# .env — Supabase provides both direct and pooler URLs
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true
# Use pgbouncer=true URL for serverless (Vercel functions)
# Use direct URL only for migrations
```

---

## 3. Security & Row Level Security (CRITICAL)

### Enable RLS on every user-data table
```sql
-- NEVER ship a user-data table without RLS
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE prompts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_collections ENABLE ROW LEVEL SECURITY;

-- Basic user-scoped policy
CREATE POLICY "Users can read own progress"
  ON user_progress FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
  ON user_progress FOR UPDATE
  USING (auth.uid() = user_id);

-- Public read for lore content (no auth required)
CREATE POLICY "Lore is publicly readable"
  ON guardians FOR SELECT
  USING (true); -- anon can read

-- Prompts: owner CRUD, public read if published
CREATE POLICY "Prompts: owner full access"
  ON prompts FOR ALL
  USING (auth.uid() = created_by);

CREATE POLICY "Prompts: public read if published"
  ON prompts FOR SELECT
  USING (is_published = true);
```

### Use service role ONLY in server-side trusted code
```typescript
// NEVER expose service role key to client
// ONLY in Server Actions or Route Handlers for admin operations

import { createClient } from '@supabase/supabase-js'

// lib/supabase-admin.ts — server-only (never imported in 'use client' files)
export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // NOT NEXT_PUBLIC_
  { auth: { persistSession: false } }
)
```

### Always validate user ownership before mutations
```typescript
// Server Action pattern
'use server'
export async function deletePrompt(promptId: string) {
  const supabase = await createSupabaseServer()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('Unauthorized')
  
  // RLS handles this, but explicit check is defense-in-depth
  const { data: prompt } = await supabase
    .from('prompts').select('created_by').eq('id', promptId).single()
  if (prompt?.created_by !== user.id) throw new Error('Forbidden')
  
  await supabase.from('prompts').delete().eq('id', promptId)
}
```

---

## 4. Schema Design (HIGH)

### Arcanea canonical schema patterns
```sql
-- Standard Arcanea table structure
CREATE TABLE guardians (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  gate        TEXT NOT NULL UNIQUE, -- 'foundation', 'flow', 'fire'...
  name        TEXT NOT NULL,        -- 'Lyssandria', 'Leyla', 'Draconia'...
  element     TEXT NOT NULL,        -- 'earth', 'water', 'fire', 'wind', 'void'
  frequency_hz INTEGER NOT NULL,    -- 174, 285, 396...
  description TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Use ENUM for constrained domains
CREATE TYPE gate_element AS ENUM ('earth', 'water', 'fire', 'wind', 'void', 'spirit');
CREATE TYPE magic_rank AS ENUM ('apprentice', 'mage', 'master', 'archmage', 'luminor');
CREATE TYPE gate_name AS ENUM (
  'foundation', 'flow', 'fire', 'heart', 'voice', 
  'sight', 'crown', 'shift', 'unity', 'source'
);

-- Always add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER guardians_updated_at
  BEFORE UPDATE ON guardians
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### User progress table — core Arcanea schema
```sql
CREATE TABLE user_progress (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  gate        gate_name NOT NULL,
  status      TEXT NOT NULL DEFAULT 'locked' CHECK (status IN ('locked', 'unlocked', 'mastered')),
  unlocked_at TIMESTAMPTZ,
  score       INTEGER DEFAULT 0 CHECK (score >= 0 AND score <= 100),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(user_id, gate) -- one row per user per gate
);

ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_user_progress_user ON user_progress(user_id);
CREATE INDEX idx_user_progress_gate ON user_progress(gate);
```

---

## 5. Concurrency & Locking (MEDIUM-HIGH)

### Use transactions for multi-step mutations
```typescript
// When updating multiple tables atomically
const { data, error } = await supabase.rpc('unlock_gate_transaction', {
  p_user_id: user.id,
  p_gate: 'flow',
  p_score: 87,
})

-- In Supabase SQL editor / migration:
CREATE OR REPLACE FUNCTION unlock_gate_transaction(
  p_user_id UUID,
  p_gate gate_name,
  p_score INTEGER
) RETURNS JSONB LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  v_result JSONB;
BEGIN
  -- Update gate status
  UPDATE user_progress
  SET status = 'unlocked', score = p_score, unlocked_at = now()
  WHERE user_id = p_user_id AND gate = p_gate;
  
  -- Update rank if needed (computed from unlocked gates count)
  UPDATE profiles
  SET rank = compute_rank(p_user_id)
  WHERE id = p_user_id;
  
  RETURN jsonb_build_object('success', true, 'gate', p_gate);
EXCEPTION WHEN OTHERS THEN
  RAISE; -- rollback automatically
END;
$$;
```

---

## 6. Data Access Patterns (MEDIUM)

### Full-text search for Lore content
```sql
-- Add tsvector column for lore search
ALTER TABLE lore_texts ADD COLUMN search_vector TSVECTOR;
CREATE INDEX idx_lore_search ON lore_texts USING GIN(search_vector);

UPDATE lore_texts SET search_vector = 
  to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Search query
SELECT title, element, gate, ts_rank(search_vector, query) as rank
FROM lore_texts, to_tsquery('english', 'guardian & fire') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;
```

### JSONB for flexible prompt metadata
```typescript
// Prompts can have arbitrary metadata
const { data } = await supabase
  .from('prompts')
  .select('id, title, metadata')
  .contains('metadata', { element: 'fire', gate: 'fire' }) // JSONB contains
  .order('created_at', { ascending: false })
```

```sql
-- JSONB index for prompt metadata
CREATE INDEX idx_prompts_metadata ON prompts USING GIN(metadata);
```

### Realtime subscriptions — Arcanea patterns
```typescript
// apps/web — subscribe to user progress changes
const channel = supabase
  .channel(`user-progress-${user.id}`)
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'user_progress',
      filter: `user_id=eq.${user.id}`,
    },
    (payload) => {
      // Animate gate unlock in UI
      setGateStatus(prev => ({ ...prev, [payload.new.gate]: payload.new.status }))
    }
  )
  .subscribe()

// Always cleanup
return () => { supabase.removeChannel(channel) }
```

---

## 7. Monitoring (LOW-MEDIUM)

### Key queries to run periodically in Supabase SQL editor
```sql
-- Find tables without indexes on FKs
SELECT tc.table_name, kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND NOT EXISTS (
  SELECT 1 FROM pg_indexes 
  WHERE tablename = tc.table_name AND indexdef LIKE '%' || kcu.column_name || '%'
);

-- Slow queries (requires pg_stat_statements)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100 -- ms
ORDER BY total_exec_time DESC
LIMIT 20;

-- Table sizes
SELECT schemaname, tablename, 
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## TypeScript Types

### Generate and use Supabase types
```bash
# Generate types from your Supabase schema
npx supabase gen types typescript --project-id [ref] > apps/web/types/supabase.ts
```

```typescript
// Always type your Supabase client
import type { Database } from '@/types/supabase'
import { createBrowserClient } from '@supabase/ssr'

const supabase = createBrowserClient<Database>(url, key)

// Now fully typed:
const { data } = await supabase
  .from('guardians') // autocomplete
  .select('id, name, gate, frequency_hz')
// data is typed as Database['public']['Tables']['guardians']['Row'][]
```

---

## Quick Checklist

Before any Supabase/database work in Arcanea:

- [ ] RLS enabled on all user-data tables with appropriate policies
- [ ] Service role key never in NEXT_PUBLIC_ env vars
- [ ] FK columns have indexes
- [ ] EXPLAIN ANALYZE run on non-trivial queries (no Seq Scan surprises)
- [ ] No N+1 queries — use Supabase select with relations
- [ ] Multi-table mutations use RPC transactions
- [ ] Realtime subscriptions cleaned up in useEffect return
- [ ] Types generated from schema: `npx supabase gen types`
- [ ] `params` and `cookies` awaited in Next.js 16 server context

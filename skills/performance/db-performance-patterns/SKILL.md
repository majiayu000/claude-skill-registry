---
name: db-performance-patterns
description: "Patterns for optimizing database queries and preventing connection pool exhaustion. Use when writing batch operations, debugging slow queries, or reviewing code for performance."
---

# Database Performance Patterns

Patterns and guidelines for preventing connection pool exhaustion and optimizing database queries in Ballee.

## When to Use This Skill

- Writing cron jobs or batch operations
- Creating services that query multiple entities
- Debugging slow queries or connection issues
- Reviewing code for performance issues

## Critical Connection Settings

Production Supabase has **60 max connections**. These settings prevent pool exhaustion:

```sql
-- Applied to both production and staging (2025-12-18)
ALTER DATABASE postgres SET idle_session_timeout = '300000';           -- 5 min
ALTER DATABASE postgres SET idle_in_transaction_session_timeout = '60000'; -- 1 min
```

## Anti-Patterns to Avoid

### 1. N+1 Query Pattern (FORBIDDEN)

```typescript
// BAD: 3 queries per item = 150 queries for 50 items
for (const item of items) {
  const { count: countA } = await supabase.from('table').select('id', { count: 'exact' }).eq('item_id', item.id).eq('status', 'a');
  const { count: countB } = await supabase.from('table').select('id', { count: 'exact' }).eq('item_id', item.id).eq('status', 'b');
  const { count: countC } = await supabase.from('table').select('id', { count: 'exact' }).eq('item_id', item.id).eq('status', 'c');
}

// GOOD: 1 query total, aggregate in memory
const { data: allRecords } = await supabase
  .from('table')
  .select('item_id, status')
  .in('status', ['a', 'b', 'c']);

const countsByItem = new Map();
for (const record of allRecords || []) {
  // Aggregate in memory
}
```

### 2. Sequential Independent Queries (FORBIDDEN)

```typescript
// BAD: Sequential queries (3x latency)
const production = await supabase.from('productions').select('*').eq('id', id).single();
const roles = await supabase.from('cast_roles').select('*').eq('production_id', id);
const events = await supabase.from('events').select('*').eq('production_id', id);

// GOOD: Parallel queries (1x latency)
const [productionResult, rolesResult, eventsResult] = await Promise.all([
  supabase.from('productions').select('*').eq('id', id).single(),
  supabase.from('cast_roles').select('*').eq('production_id', id),
  supabase.from('events').select('*').eq('production_id', id),
]);
```

### 3. Individual Inserts/Updates in Loops (FORBIDDEN)

```typescript
// BAD: N inserts = N queries
for (const item of items) {
  await supabase.from('table').insert({ ...item });
}

// GOOD: 1 batch insert
await supabase.from('table').insert(items);

// BAD: N updates
for (const id of ids) {
  await supabase.from('table').update({ status: 'done' }).eq('id', id);
}

// GOOD: 1 batch update
await supabase.from('table').update({ status: 'done' }).in('id', ids);
```

## Required Index Patterns

### Always Index Foreign Keys

```sql
-- Every FK column should have an index
CREATE INDEX idx_table_foreign_id ON table(foreign_id);

-- Use partial indexes for nullable FKs
CREATE INDEX idx_table_optional_fk ON table(optional_fk) WHERE optional_fk IS NOT NULL;
```

### Index Frequently Filtered Columns

```sql
-- Boolean flags queried often
CREATE INDEX idx_feature_flags_is_active ON feature_flags(is_active) WHERE is_active = true;

-- Status columns
CREATE INDEX idx_events_status ON events(status);

-- Composite indexes for common query patterns
CREATE INDEX idx_events_status_date ON events(status, event_date DESC);
```

### Check for Missing Indexes

```sql
-- Find tables with high sequential scans (missing indexes)
SELECT relname, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_scan DESC;

-- Find missing FK indexes
SELECT c.relname, a.attname
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(con.conkey)
WHERE con.contype = 'f'
AND NOT EXISTS (
  SELECT 1 FROM pg_index i
  WHERE i.indrelid = c.oid AND a.attnum = ANY(i.indkey)
);
```

## Cron Job Best Practices

### Structure for Batch Operations

```typescript
export async function GET(request: Request) {
  // 1. Single query to get all entities
  const { data: entities } = await client.from('entities').select('id, status').eq('status', 'pending');

  // 2. Single query to get related data for all entities
  const entityIds = entities.map(e => e.id);
  const { data: relatedData } = await client.from('related').select('*').in('entity_id', entityIds);

  // 3. Group related data by entity in memory
  const relatedByEntity = new Map();
  for (const item of relatedData || []) {
    // Group in memory
  }

  // 4. Process and prepare batch operations
  const toInsert = [];
  const toUpdate = [];

  for (const entity of entities) {
    const related = relatedByEntity.get(entity.id);
    // Process and add to batch arrays
  }

  // 5. Single batch insert
  if (toInsert.length > 0) {
    await client.from('results').insert(toInsert);
  }

  // 6. Single batch update (if needed)
  if (toUpdate.length > 0) {
    await client.from('entities').update({ status: 'processed' }).in('id', toUpdate);
  }
}
```

## Connection Pool Monitoring

### Check Current Connections

```sql
SELECT state, count(*) FROM pg_stat_activity WHERE datname = 'postgres' GROUP BY state;
```

### Monitor Slow Queries

```sql
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

## Supabase Dashboard Monitoring

1. **Database Reports** → Query Performance
2. **Database Reports** → Connection Pooler
3. Set alerts for:
   - Connection count > 50 (of 60 max)
   - Query time > 100ms average

## Quick Reference: Query Reduction

| Pattern | Before | After | Reduction |
|---------|--------|-------|-----------|
| Status counts | 3 queries | 1 query + memory | 66% |
| Per-item metrics | N×3 queries | 1 query + memory | 99% |
| Batch reports | N×3 queries | 3 queries | 99% |
| Sequential inserts | N queries | 1 query | 99% |

## Fix Templates (Copy-Paste Ready)

### Template 1: N+1 → Batch Fetch + Map Lookup

**Before (N+1):**
```typescript
const results = [];
for (const item of items) {
  const { data } = await supabase
    .from('related_table')
    .select('*')
    .eq('item_id', item.id)
    .single();
  results.push({ ...item, related: data });
}
```

**After (1 query):**
```typescript
// 1. Collect all IDs
const itemIds = items.map(item => item.id);

// 2. Batch fetch all related data
const { data: allRelated } = await supabase
  .from('related_table')
  .select('*')
  .in('item_id', itemIds);

// 3. Create lookup Map for O(1) access
const relatedMap = new Map(
  (allRelated ?? []).map(r => [r.item_id, r])
);

// 4. Use Map in loop (no queries)
const results = items.map(item => ({
  ...item,
  related: relatedMap.get(item.id),
}));
```

---

### Template 2: Multiple Counts → Single Query + Aggregation

**Before (3 queries):**
```typescript
const { count: acceptedCount } = await supabase
  .from('assignments')
  .select('id', { count: 'exact', head: true })
  .eq('status', 'accepted');

const { count: pendingCount } = await supabase
  .from('assignments')
  .select('id', { count: 'exact', head: true })
  .eq('status', 'pending');

const { count: declinedCount } = await supabase
  .from('assignments')
  .select('id', { count: 'exact', head: true })
  .eq('status', 'declined');
```

**After (1 query):**
```typescript
// 1. Single query fetching all statuses
const { data: assignments } = await supabase
  .from('assignments')
  .select('status')
  .in('status', ['accepted', 'pending', 'declined']);

// 2. Aggregate in memory
const counts = { accepted: 0, pending: 0, declined: 0 };
for (const a of assignments ?? []) {
  if (a.status in counts) {
    counts[a.status as keyof typeof counts]++;
  }
}

const { accepted: acceptedCount, pending: pendingCount, declined: declinedCount } = counts;
```

---

### Template 3: Sequential Queries → Promise.all

**Before (sequential - 3x latency):**
```typescript
const { data: production } = await supabase
  .from('productions')
  .select('*')
  .eq('id', productionId)
  .single();

const { data: roles } = await supabase
  .from('cast_roles')
  .select('*')
  .eq('production_id', productionId);

const { data: events } = await supabase
  .from('events')
  .select('*')
  .eq('production_id', productionId);
```

**After (parallel - 1x latency):**
```typescript
const [productionResult, rolesResult, eventsResult] = await Promise.all([
  supabase.from('productions').select('*').eq('id', productionId).single(),
  supabase.from('cast_roles').select('*').eq('production_id', productionId),
  supabase.from('events').select('*').eq('production_id', productionId),
]);

const production = productionResult.data;
const roles = rolesResult.data;
const events = eventsResult.data;
```

---

### Template 4: Loop Inserts → Batch Insert

**Before (N inserts):**
```typescript
for (const item of items) {
  await supabase.from('notifications').insert({
    user_id: item.userId,
    message: item.message,
    type: 'reminder',
  });
}
```

**After (1 insert):**
```typescript
const toInsert = items.map(item => ({
  user_id: item.userId,
  message: item.message,
  type: 'reminder',
}));

if (toInsert.length > 0) {
  await supabase.from('notifications').insert(toInsert);
}
```

---

### Template 5: Loop Updates → Batch Update

**Before (N updates):**
```typescript
for (const id of completedIds) {
  await supabase
    .from('tasks')
    .update({ status: 'done', completed_at: new Date().toISOString() })
    .eq('id', id);
}
```

**After (1 update):**
```typescript
if (completedIds.length > 0) {
  await supabase
    .from('tasks')
    .update({ status: 'done', completed_at: new Date().toISOString() })
    .in('id', completedIds);
}
```

---

### Template 6: Cron Job Batch Pattern

**Complete pattern for cron jobs:**
```typescript
export async function GET(request: Request) {
  const client = getSupabaseRouteHandlerClient({ admin: true });

  // 1. Fetch all eligible entities in ONE query
  const { data: entities } = await client
    .from('entities')
    .select('id, user_id, status')
    .eq('status', 'pending')
    .lt('created_at', oneHourAgo);

  if (!entities?.length) {
    return NextResponse.json({ processed: 0 });
  }

  // 2. Collect IDs for batch queries
  const entityIds = entities.map(e => e.id);
  const userIds = [...new Set(entities.map(e => e.user_id))];

  // 3. Batch fetch ALL related data in PARALLEL
  const [relatedResult, usersResult, existingResult] = await Promise.all([
    client.from('related').select('*').in('entity_id', entityIds),
    client.from('profiles').select('id, email').in('id', userIds),
    client.from('processed').select('entity_id').in('entity_id', entityIds),
  ]);

  // 4. Create lookup Maps
  const relatedByEntity = new Map<string, typeof relatedResult.data>();
  for (const r of relatedResult.data ?? []) {
    if (!relatedByEntity.has(r.entity_id)) {
      relatedByEntity.set(r.entity_id, []);
    }
    relatedByEntity.get(r.entity_id)!.push(r);
  }

  const usersMap = new Map((usersResult.data ?? []).map(u => [u.id, u]));
  const alreadyProcessed = new Set((existingResult.data ?? []).map(e => e.entity_id));

  // 5. Process and build batch operations (NO QUERIES IN LOOP)
  const toInsert = [];
  const toUpdate = [];

  for (const entity of entities) {
    if (alreadyProcessed.has(entity.id)) continue;

    const related = relatedByEntity.get(entity.id) ?? [];
    const user = usersMap.get(entity.user_id);

    // Process logic here...
    toInsert.push({ entity_id: entity.id, processed_at: new Date().toISOString() });
    toUpdate.push(entity.id);
  }

  // 6. Batch insert
  if (toInsert.length > 0) {
    await client.from('processed').insert(toInsert);
  }

  // 7. Batch update
  if (toUpdate.length > 0) {
    await client.from('entities').update({ status: 'done' }).in('id', toUpdate);
  }

  return NextResponse.json({ processed: toInsert.length });
}
```

---

### Template 7: Grouped Updates by Value

**Before (N updates with different values):**
```typescript
for (const item of items) {
  await supabase
    .from('table')
    .update({ reminder_count: item.count })
    .eq('id', item.id);
}
```

**After (grouped by value):**
```typescript
// Group IDs by their target value
const byCount = new Map<number, string[]>();
for (const item of items) {
  if (!byCount.has(item.count)) {
    byCount.set(item.count, []);
  }
  byCount.get(item.count)!.push(item.id);
}

// One update per unique value
for (const [count, ids] of byCount) {
  await supabase.from('table').update({ reminder_count: count }).in('id', ids);
}
```

## Related Files

- Migration: `supabase/migrations/20251218200640_add_performance_indexes.sql`
- Optimized service: `app/admin/_lib/services/reporting.service.ts`
- Optimized crons: `app/api/cron/feedback-*/route.ts`

## Related Skills

- `db-anti-patterns` - Detection rules for finding issues
- `/db-perf` command - Automated scanning and fixing

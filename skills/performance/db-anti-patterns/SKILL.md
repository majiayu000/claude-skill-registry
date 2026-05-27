---
name: db-anti-patterns
description: "Detection rules and grep patterns for database performance anti-patterns. Use when scanning codebase for N+1 queries, sequential queries, or connection pool issues."
---

# Database Anti-Patterns Detection

Detection rules and grep patterns for identifying database performance anti-patterns in code.

## When to Use This Skill

- Scanning codebase for performance issues
- Code review for database patterns
- Used by `db-performance-agent` for automated detection

## Anti-Pattern Categories

### 1. N+1 Query Patterns (CRITICAL)

Queries executed inside loops - causes O(n) database calls.

**Detection Patterns:**

```typescript
// Pattern 1: await inside for loop
for (const item of items) {
  await supabase.from('table')...  // N+1!
}

// Pattern 2: await inside forEach
items.forEach(async (item) => {
  await supabase.from('table')...  // N+1!
});

// Pattern 3: await inside map
await Promise.all(items.map(async (item) => {
  await supabase.from('table')...  // N+1 even with Promise.all!
}));

// Pattern 4: count queries in loop
for (const item of items) {
  const { count } = await supabase.from('x').select('id', { count: 'exact' })...
}
```

**Grep Patterns:**

```bash
# For loops with await supabase
grep -Pzo 'for\s*\([^)]+\)\s*\{[^}]*await[^}]*\.from\(' --include="*.ts"

# forEach with async
grep -n 'forEach\s*\(\s*async' --include="*.ts"

# map with nested await from()
grep -n '\.map\s*\(\s*async.*await.*\.from\(' --include="*.ts"
```

**Severity:** CRITICAL
**Impact:** 50-500+ queries per request
**Auto-fixable:** Yes - batch fetch + Map lookup

---

### 2. Sequential Independent Queries (HIGH)

Multiple await statements that could run in parallel.

**Detection Pattern:**

```typescript
// Sequential (BAD)
const a = await supabase.from('table_a').select()...;
const b = await supabase.from('table_b').select()...;
const c = await supabase.from('table_c').select()...;

// Should be parallel (GOOD)
const [a, b, c] = await Promise.all([
  supabase.from('table_a').select()...,
  supabase.from('table_b').select()...,
  supabase.from('table_c').select()...,
]);
```

**Detection Heuristic:**

Look for 2+ consecutive lines matching:
- `const/let X = await supabase.from(...)`
- With no data dependency between them

**Severity:** HIGH
**Impact:** 2-5x latency increase
**Auto-fixable:** Yes - wrap in Promise.all()

---

### 3. Unbounded Data Fetches (MEDIUM)

Queries without `.limit()` on tables that can grow large.

**Large Tables to Check:**

```typescript
const LARGE_TABLES = [
  'events',
  'cast_assignments',
  'invoices',
  'invoice_line_items',
  'notifications',
  'notification_deliveries',
  'airtable_sync_changes',
  'audit_logs',
  'feedback_requests',
  'reimbursements',
  'reimbursement_line_items',
];
```

**Detection Pattern:**

```typescript
// Missing limit (BAD for large tables)
await supabase.from('events').select('*')

// Should have limit or be filtered (GOOD)
await supabase.from('events').select('*').limit(100)
await supabase.from('events').select('*').eq('user_id', userId)
```

**Grep Pattern:**

```bash
# Selects on large tables without limit
grep -n "\.from\(['\"]events['\"]\)" --include="*.ts" | grep -v "\.limit\|\.eq\|\.in\|\.single"
```

**Severity:** MEDIUM
**Impact:** Memory exhaustion, slow queries
**Auto-fixable:** Partial - add .limit(), may need review

---

### 4. Individual Insert/Update in Loops (HIGH)

Single-row operations that should be batched.

**Detection Pattern:**

```typescript
// Individual inserts (BAD)
for (const item of items) {
  await supabase.from('table').insert({ ...item });
}

// Individual updates (BAD)
for (const id of ids) {
  await supabase.from('table').update({ status: 'done' }).eq('id', id);
}

// Batch operations (GOOD)
await supabase.from('table').insert(items);
await supabase.from('table').update({ status: 'done' }).in('id', ids);
```

**Grep Pattern:**

```bash
# Insert in loop
grep -Pzo 'for\s*\([^)]+\)\s*\{[^}]*\.insert\(' --include="*.ts"

# Update in loop
grep -Pzo 'for\s*\([^)]+\)\s*\{[^}]*\.update\(' --include="*.ts"
```

**Severity:** HIGH
**Impact:** N database round-trips
**Auto-fixable:** Yes - batch operations

---

### 5. Count Queries Instead of Aggregation (MEDIUM)

Using multiple COUNT queries instead of fetching once and aggregating.

**Detection Pattern:**

```typescript
// Multiple count queries (BAD)
const { count: countA } = await supabase.from('x').select('id', { count: 'exact' }).eq('status', 'a');
const { count: countB } = await supabase.from('x').select('id', { count: 'exact' }).eq('status', 'b');
const { count: countC } = await supabase.from('x').select('id', { count: 'exact' }).eq('status', 'c');

// Single fetch + aggregate (GOOD)
const { data } = await supabase.from('x').select('status').in('status', ['a', 'b', 'c']);
const counts = { a: 0, b: 0, c: 0 };
for (const item of data) counts[item.status]++;
```

**Grep Pattern:**

```bash
# Multiple count queries (look for pattern of consecutive count selects)
grep -n "count: 'exact'" --include="*.ts"
```

**Severity:** MEDIUM
**Impact:** 2-10x more queries than necessary
**Auto-fixable:** Yes - single query + in-memory aggregation

---

### 6. Missing Promise.all for Related Lookups (MEDIUM)

Fetching the same related entity type multiple times sequentially.

**Detection Pattern:**

```typescript
// Sequential related lookups (BAD)
const user1 = await getUser(id1);
const user2 = await getUser(id2);
const user3 = await getUser(id3);

// Batch lookup (GOOD)
const users = await getUsers([id1, id2, id3]);
```

**Severity:** MEDIUM
**Impact:** Increased latency
**Auto-fixable:** Sometimes - depends on function signature

---

## Quick Reference: Detection Commands

```bash
# Find all N+1 patterns (for loops with await from)
grep -rn "for.*{" apps/web --include="*.ts" | xargs -I {} sh -c 'grep -l "await.*\.from\(" {}'

# Find sequential queries (consecutive await from lines)
grep -n "await.*\.from\(" apps/web --include="*.ts" | sort | uniq -c | sort -rn

# Find unbounded selects on large tables
for table in events cast_assignments invoices notifications; do
  grep -rn "\.from(['\"]$table['\"])" apps/web --include="*.ts" | grep -v "\.limit\|\.single\|\.eq\|\.in"
done

# Find insert/update in loops
grep -rn "for\s*(" apps/web --include="*.ts" -A 5 | grep -E "\.(insert|update)\("

# Find multiple count queries in same file
grep -l "count: 'exact'" apps/web --include="*.ts" -r | xargs -I {} grep -c "count: 'exact'" {} | grep -v ":1$"
```

## Severity Levels

| Severity | Impact | Fix Priority |
|----------|--------|--------------|
| CRITICAL | 10x+ queries, pool exhaustion risk | Immediate |
| HIGH | 3-10x queries/latency | Same sprint |
| MEDIUM | 2-3x queries/latency | Next sprint |
| LOW | Minor inefficiency | Backlog |

## Files Commonly Affected

High-risk file patterns to prioritize scanning:

1. **Cron jobs**: `app/api/cron/*/route.ts`
2. **Services with batch ops**: `**/services/*.service.ts`
3. **Admin list pages**: `app/admin/**/actions.ts`
4. **Report generators**: `**/reporting*.ts`

## Related Skills

- `db-performance-patterns` - Correct patterns and fixes
- `db-performance-agent` - Automated scanning and fixing

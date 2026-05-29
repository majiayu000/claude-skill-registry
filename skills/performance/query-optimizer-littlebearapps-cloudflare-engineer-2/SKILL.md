---
name: query-optimizer
description: Static analysis of D1 queries to prevent the #1 billing trap - unindexed queries causing row read explosion (5M daily free limit). Use this skill when reviewing D1 usage, analysing query patterns, unexpected D1 costs, row reads, slow queries, unindexed columns, SELECT * issues, N+1 problems, pagination, or Drizzle ORM queries.
---

# D1 Query Optimizer Skill

Prevent the #1 Cloudflare billing trap for solo developers: unindexed queries causing row read explosion. D1's free tier allows 5 billion row reads/month, but a single unindexed query on a 100K row table can burn through this in days.

## Why This Matters

**Real-World Horror Story**: One developer hit the 5 million daily read limit just by browsing their own site during development - each page load triggered a full table scan.

| Query Type | Table Size | Requests/Day | Daily Rows Read | Days to Exceed Free Tier |
|------------|-----------|--------------|-----------------|--------------------------|
| Unindexed WHERE | 100K | 1000 | 100M | 1.6 days |
| Indexed WHERE | 100K | 1000 | 1000 | Never (free tier covers it) |
| SELECT * list | 50K | 500 | 25M | 6.6 days |
| Paginated list | 50K | 500 | 50K | Never |

## Static Analysis Patterns

### QUERY001: SELECT * Without LIMIT (HIGH)

**Pattern**: Fetching all columns and all rows from a table.

```typescript
// EXPENSIVE: Returns ALL rows, ALL columns
const users = await db.prepare('SELECT * FROM users').all();
// If users table has 100K rows = 100K row reads per request

// OPTIMIZED: Limit results and select only needed columns
const users = await db
  .prepare('SELECT id, name, email FROM users LIMIT 50')
  .all();
// Fixed 50 row reads per request
```

**Detection**:
- Grep for `SELECT \*` without `LIMIT` clause
- Check for missing pagination on list endpoints

**Cost Formula**:
```
rows_read_per_request = table_size (if no LIMIT)
monthly_cost = rows_read × requests/month × $0.25 / 1B
```

---

### QUERY002: SQL in Loop (N+1) (CRITICAL)

**Pattern**: Database query inside iteration block.

```typescript
// DISASTER: 1000 users = 1000 D1 queries
for (const user of users) {
  const orders = await db
    .prepare('SELECT * FROM orders WHERE user_id = ?')
    .bind(user.id)
    .all();
}
// Cost: 1000 × orders_per_user row reads

// OPTIMIZED: Single batch query
const userIds = users.map(u => u.id);
const placeholders = userIds.map(() => '?').join(',');
const orders = await db
  .prepare(`SELECT * FROM orders WHERE user_id IN (${placeholders})`)
  .bind(...userIds)
  .all();
// Cost: 1 query, rows = total matching orders
```

**Detection Patterns**:
- `for.*\.prepare\(` or `for.*\.run\(`
- `while.*\.prepare\(` or `while.*\.run\(`
- `forEach.*\.prepare\(` or `forEach.*\.run\(`
- `.map\(.*\.prepare\(` or `.map\(.*\.run\(`

**Cost Formula**:
```
n_plus_one_cost = iterations × avg_rows_per_query × $0.25 / 1B
vs
batched_cost = total_matching_rows × $0.25 / 1B
```

---

### QUERY003: Query on Unindexed Column (CRITICAL)

**Pattern**: WHERE clause on column without index causes full table scan.

```sql
-- EXPENSIVE: Full table scan (no index on 'status')
SELECT * FROM users WHERE status = 'active';
-- If users table has 1M rows = 1M row reads

-- OPTIMIZED: Create index first
CREATE INDEX idx_users_status ON users(status);
SELECT * FROM users WHERE status = 'active';
-- Now reads only matching rows (~10K if 1% active)
```

**Detection**:
1. Extract column names from WHERE clauses
2. Check migrations for corresponding CREATE INDEX
3. Flag if no index exists

**Verify with EXPLAIN QUERY PLAN**:
```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE status = 'active';
-- BAD: "SCAN TABLE users" (full scan)
-- GOOD: "SEARCH TABLE users USING INDEX idx_users_status" (index lookup)
```

**MCP Probe**:
```javascript
// Check for table scans
mcp__cloudflare-bindings__d1_database_query({
  database_id: "...",
  sql: "EXPLAIN QUERY PLAN SELECT * FROM users WHERE status = ?"
});
// Look for "SCAN TABLE" in output
```

---

### QUERY004: List Endpoint Without Pagination (MEDIUM)

**Pattern**: API endpoint returns unbounded list.

```typescript
// EXPENSIVE: Returns entire table
app.get('/api/users', async (c) => {
  const users = await db.prepare('SELECT * FROM users').all();
  return c.json(users);
});

// OPTIMIZED: Cursor-based pagination
app.get('/api/users', async (c) => {
  const cursor = c.req.query('cursor') || '0';
  const limit = Math.min(parseInt(c.req.query('limit') || '50'), 100);

  const users = await db
    .prepare('SELECT id, name FROM users WHERE id > ? ORDER BY id LIMIT ?')
    .bind(cursor, limit)
    .all();

  const nextCursor = users.results.length === limit
    ? users.results[users.results.length - 1].id
    : null;

  return c.json({
    data: users.results,
    nextCursor,
    hasMore: nextCursor !== null,
  });
});
```

**Detection**:
- List endpoints (GET with path like `/api/:resource`) without LIMIT in query
- Routes returning `db.prepare(...).all()` without pagination parameters

---

### QUERY005: Drizzle .all() Without .limit() (HIGH)

**Pattern**: Drizzle ORM query without limit constraint.

```typescript
// EXPENSIVE: Returns all matching rows
const users = await db.select().from(users);
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.status, 'active'));

// OPTIMIZED: Always use .limit()
const users = await db.select().from(users).limit(50);
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.status, 'active'))
  .limit(50)
  .offset(page * 50);
```

**Drizzle-Specific Patterns to Flag**:
- `.select().from(...).all()` without `.limit()`
- `.findMany()` without `limit` option
- `.query.*.findMany()` without limit

---

## Cost Projection Formulas

### Per-Request Cost

```
cost_per_request = rows_read × $0.25 / 1,000,000,000

Example (unindexed query on 100K table):
cost = 100,000 × $0.25 / 1B = $0.000025 per request
At 1000 req/day = $0.75/month

Example (indexed query returning 10 rows):
cost = 10 × $0.25 / 1B = $0.0000000025 per request
At 1000 req/day = $0.000075/month (essentially free)
```

### Free Tier Burn Rate

```
Free tier: 5B rows/month = ~166M rows/day

Time to exceed free tier = 166M / (rows_per_request × requests_per_day)

Example: 100K rows/request × 1000 requests/day = 100M rows/day
Days to exceed = 166M / 100M = 1.66 days
```

### Write Cost Comparison

| Operation | Cost | Free Tier |
|-----------|------|-----------|
| Row reads | $0.25 / billion | 5B/month |
| Row writes | $1.00 / million | 5M/month |
| Storage | $0.75 / GB | 5GB |

---

## Caching Decision Tree

Not all D1 queries need caching. Use this decision tree:

```
Is the data personalized to the user?
│
├─ YES: Is it frequently accessed?
│   │
│   ├─ YES: Use user-scoped KV cache
│   │       Key: `user:{userId}:{dataType}`
│   │       TTL: 60-300 seconds
│   │
│   └─ NO: No cache needed (occasional personalized reads are cheap)
│
└─ NO: Is it static/reference data?
    │
    ├─ YES: Use KV-cache-first pattern
    │       Key: `data:{dataType}:{id}`
    │       TTL: 3600-86400 seconds
    │       See: @skills/patterns/kv-cache-first.md
    │
    └─ NO: Is it search/list results?
        │
        ├─ YES: Use Cache API with short TTL
        │       Key: Request URL
        │       TTL: 10-60 seconds
        │
        └─ NO: Direct D1 query (ensure indexed)
```

### KV Cache Pattern

```typescript
// User-scoped cache for personalized data
async function getUserDashboard(userId: string, env: Env) {
  const cacheKey = `dashboard:${userId}`;

  // Try cache first
  const cached = await env.CACHE.get(cacheKey, 'json');
  if (cached) return cached;

  // Cache miss: query D1
  const dashboard = await env.DB
    .prepare(`
      SELECT * FROM dashboards
      WHERE user_id = ?
      LIMIT 1
    `)
    .bind(userId)
    .first();

  // Cache for next request
  await env.CACHE.put(cacheKey, JSON.stringify(dashboard), {
    expirationTtl: 60,  // 1 minute for user data
  });

  return dashboard;
}
```

### Cache API Pattern for Lists

```typescript
// Cache search results at the edge
async function searchProducts(query: string, env: Env, ctx: ExecutionContext) {
  const cache = caches.default;
  const cacheKey = new Request(`https://cache/search?q=${encodeURIComponent(query)}`);

  // Try edge cache
  const cached = await cache.match(cacheKey);
  if (cached) return cached;

  // Cache miss: query D1
  const products = await env.DB
    .prepare(`
      SELECT id, name, price
      FROM products
      WHERE name LIKE ?
      LIMIT 50
    `)
    .bind(`%${query}%`)
    .all();

  const response = new Response(JSON.stringify(products.results), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'max-age=30',  // Short TTL for search
    },
  });

  // Store in edge cache (non-blocking)
  ctx.waitUntil(cache.put(cacheKey, response.clone()));

  return response;
}
```

---

## Query Audit Workflow

### Step 1: Identify Hot Paths

Scan routes for D1 usage:

```bash
# Find all D1 query patterns
grep -rn "\.prepare\|\.run\|\.first\|\.all" src/
```

### Step 2: Analyse Each Query

For each query found:

1. **Check for index coverage**:
   ```sql
   -- List all indexes
   SELECT name, sql FROM sqlite_master WHERE type='index';

   -- Check query plan
   EXPLAIN QUERY PLAN <your_query>;
   ```

2. **Estimate row reads**:
   - `SCAN TABLE` = full table size
   - `SEARCH USING INDEX` = estimated matching rows

3. **Calculate cost impact**:
   - Multiply by expected daily requests
   - Compare against free tier

### Step 3: Prioritise Fixes

| Priority | Pattern | Severity | Action |
|----------|---------|----------|--------|
| P0 | SCAN on hot endpoint | CRITICAL | Add index immediately |
| P0 | SQL in loop | CRITICAL | Rewrite to batch query |
| P1 | SELECT * without LIMIT | HIGH | Add pagination |
| P1 | Drizzle .findMany() | HIGH | Add .limit() |
| P2 | Unindexed JOIN | MEDIUM | Create composite index |
| P2 | Missing cache | MEDIUM | Add KV cache layer |

---

## Drizzle ORM Best Practices

### Safe Query Patterns

```typescript
import { drizzle } from 'drizzle-orm/d1';
import { eq, lt, desc } from 'drizzle-orm';
import { users, orders } from './schema';

// SAFE: Always include limit
const recentUsers = await db
  .select()
  .from(users)
  .orderBy(desc(users.createdAt))
  .limit(50);

// SAFE: Pagination with offset
const page = 1;
const pageSize = 20;
const pagedUsers = await db
  .select({
    id: users.id,
    name: users.name,
  })
  .from(users)
  .limit(pageSize)
  .offset(page * pageSize);

// SAFE: Indexed lookup (ensure index exists)
const user = await db
  .select()
  .from(users)
  .where(eq(users.email, email))
  .limit(1);

// SAFE: Batch query instead of loop
const userOrders = await db
  .select()
  .from(orders)
  .where(inArray(orders.userId, userIds));
```

### Drizzle Index Definition

```typescript
// schema.ts
import { sqliteTable, text, integer, index } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  email: text('email').notNull(),
  status: text('status').notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }),
}, (table) => ({
  // Create indexes for WHERE clause columns
  emailIdx: index('idx_users_email').on(table.email),
  statusIdx: index('idx_users_status').on(table.status),
  // Composite index for common query patterns
  statusCreatedIdx: index('idx_users_status_created')
    .on(table.status, table.createdAt),
}));
```

---

## New Validation Rules Summary

| ID | Severity | Check |
|----|----------|-------|
| QUERY001 | HIGH | SELECT * without LIMIT |
| QUERY002 | CRITICAL | SQL in loop (N+1) |
| QUERY003 | MEDIUM | Query on potentially unindexed column |
| QUERY004 | LOW | List endpoint without pagination |
| QUERY005 | HIGH | Drizzle .all() without .limit() |

---

## New Cost Traps

### TRAP-D1-005: Unbounded SELECT * (HIGH)

**Pattern**: SELECT * on table without row limit.

**Detection**: `SELECT \*` without `LIMIT` clause.

**Guardian Rule**: `BUDGET007`

---

### TRAP-D1-006: Drizzle findMany Without Limit (MEDIUM)

**Pattern**: Drizzle ORM query returning unbounded results.

**Detection**: `.findMany()` or `.select().from()` without `.limit()`.

**Guardian Rule**: `QUERY005`

---

## Related Skills

- **patterns/kv-cache-first**: D1 + KV caching pattern
- **guardian**: BUDGET007 enforcement for D1 row reads
- **cost-analyzer**: Live D1 usage analysis
- **loop-breaker**: N+1 query prevention with QueryBatcher

---

*Added in v1.5.0 - Query Optimization + D1 Row Read Guard*

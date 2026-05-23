# Database Anti-Patterns

Detection and fix patterns for common database performance issues.

> **Template Usage:** Customize the code patterns and grep commands for your ORM (Prisma, Drizzle, TypeORM, Sequelize, etc.).

## N+1 Query Detection

### What is N+1?

```typescript
// BAD: N+1 Query - 1 query for users + N queries for posts
const users = await db.user.findMany(); // 1 query

for (const user of users) {
  // N queries - one per user!
  user.posts = await db.post.findMany({
    where: { userId: user.id }
  });
}
```

### Detection Patterns (grep/search)

```bash
# Pattern 1: Query inside forEach/map
grep -rn "\.forEach.*await.*\.(find|select|query)" src/
grep -rn "\.map.*await.*\.(find|select|query)" src/

# Pattern 2: Query inside for loop
grep -rn "for.*of.*\n.*await.*\.(find|select|query)" src/

# Pattern 3: Query inside loop with common ORMs
# Prisma
grep -rn "for.*\n.*await.*prisma\." src/
grep -rn "\.forEach.*await.*prisma\." src/

# Drizzle
grep -rn "for.*\n.*await.*db\.(select|query)" src/

# TypeORM
grep -rn "for.*\n.*await.*\.find\(.*where" src/
```

### Fix Patterns

```typescript
// GOOD: Batch query + in-memory join
const users = await db.user.findMany();
const userIds = users.map(u => u.id);

// Single query for all posts
const posts = await db.post.findMany({
  where: { userId: { in: userIds } }
});

// Join in memory
const postsByUser = new Map<string, Post[]>();
for (const post of posts) {
  const userPosts = postsByUser.get(post.userId) || [];
  userPosts.push(post);
  postsByUser.set(post.userId, userPosts);
}

const usersWithPosts = users.map(user => ({
  ...user,
  posts: postsByUser.get(user.id) || [],
}));
```

```typescript
// ALSO GOOD: Use ORM includes/joins
// Prisma
const users = await db.user.findMany({
  include: { posts: true }
});

// Drizzle
const users = await db.query.users.findMany({
  with: { posts: true }
});

// TypeORM
const users = await userRepo.find({
  relations: ['posts']
});
```

## Sequential Queries Detection

### What is it?

```typescript
// BAD: Sequential queries that could be parallel
const user = await db.user.findUnique({ where: { id } });
const posts = await db.post.findMany({ where: { userId: id } });
const comments = await db.comment.findMany({ where: { userId: id } });
// Total time: user + posts + comments
```

### Detection Patterns

```bash
# Multiple awaits in sequence (same function)
grep -rn "await.*\n.*await.*\n.*await" src/

# Look for patterns like:
# const a = await ...
# const b = await ...
# const c = await ...
```

### Fix Pattern

```typescript
// GOOD: Parallel queries with Promise.all
const [user, posts, comments] = await Promise.all([
  db.user.findUnique({ where: { id } }),
  db.post.findMany({ where: { userId: id } }),
  db.comment.findMany({ where: { userId: id } }),
]);
// Total time: max(user, posts, comments)
```

## Unbounded Fetches Detection

### What is it?

```typescript
// BAD: No limit - could return millions of rows
const allUsers = await db.user.findMany();
const allPosts = await db.post.findMany({
  where: { status: 'published' }
});
```

### Detection Patterns

```bash
# findMany without take/limit
grep -rn "findMany\(\s*\)" src/
grep -rn "findMany\(\s*{[^}]*}\s*\)" src/ | grep -v "take:"

# SELECT without LIMIT
grep -rn "SELECT.*FROM" src/ | grep -v -i "limit"
```

### Fix Pattern

```typescript
// GOOD: Always use pagination
const PAGE_SIZE = 50;

const users = await db.user.findMany({
  take: PAGE_SIZE,
  skip: page * PAGE_SIZE,
  orderBy: { createdAt: 'desc' },
});

// For processing all records, use cursor pagination
async function* getAllUsers() {
  let cursor: string | undefined;

  while (true) {
    const batch = await db.user.findMany({
      take: 100,
      skip: cursor ? 1 : 0,
      cursor: cursor ? { id: cursor } : undefined,
      orderBy: { id: 'asc' },
    });

    if (batch.length === 0) break;

    yield* batch;
    cursor = batch[batch.length - 1].id;
  }
}
```

## Missing Index Detection

### Symptoms

```typescript
// Queries on non-indexed columns are slow
await db.user.findMany({
  where: { email: 'test@example.com' }  // Is email indexed?
});

await db.post.findMany({
  where: { status: 'published', createdAt: { gte: lastWeek } }
  // Composite index on (status, createdAt)?
});
```

### Detection

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Find missing indexes (columns frequently in WHERE)
SELECT
  schemaname,
  relname as table,
  seq_scan,
  idx_scan,
  seq_scan - idx_scan as diff
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY diff DESC;
```

### Fix Pattern

```sql
-- Add indexes for frequently queried columns
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Composite index for multi-column queries
CREATE INDEX CONCURRENTLY idx_posts_status_created
ON posts(status, created_at DESC);

-- Partial index for filtered queries
CREATE INDEX CONCURRENTLY idx_posts_published
ON posts(created_at DESC)
WHERE status = 'published';
```

## Connection Pool Exhaustion

### What is it?

```typescript
// BAD: Creating new connections instead of using pool
async function getUser(id: string) {
  const client = new DatabaseClient(); // New connection each time!
  const user = await client.query('SELECT * FROM users WHERE id = $1', [id]);
  await client.close();
  return user;
}

// BAD: Long-running transactions holding connections
await db.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } });
  await sendEmail(user.email); // Slow external call inside transaction!
  await tx.user.update({ where: { id }, data: { notified: true } });
});
```

### Detection Patterns

```bash
# New client creation in functions
grep -rn "new.*Client\(\)" src/
grep -rn "createConnection\(\)" src/

# External calls inside transactions
grep -rn "\$transaction.*await.*fetch\|axios\|sendEmail" src/
```

### Fix Pattern

```typescript
// GOOD: Use singleton/pooled connection
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}

// GOOD: Keep transactions short
const user = await db.user.findUnique({ where: { id } });
await sendEmail(user.email); // Outside transaction

await db.user.update({
  where: { id },
  data: { notified: true }
});
```

## Select Only What You Need

### Detection

```typescript
// BAD: Selecting all columns
const users = await db.user.findMany(); // Returns all columns

// BAD: SELECT * in raw queries
const users = await db.$queryRaw`SELECT * FROM users`;
```

### Fix Pattern

```typescript
// GOOD: Select only needed columns
const users = await db.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
    // Don't select: passwordHash, internalNotes, etc.
  }
});

// GOOD: Explicit columns in raw queries
const users = await db.$queryRaw`
  SELECT id, name, email FROM users
`;
```

## Anti-Pattern Scanning Script

```bash
#!/bin/bash
# scan-db-antipatterns.sh

echo "🔍 Scanning for database anti-patterns..."

echo ""
echo "=== N+1 Queries ==="
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(forEach|map|for\s+\(.*of).*\n.*await.*(find|select|query|prisma)" src/ || echo "✅ None found"

echo ""
echo "=== Unbounded Fetches ==="
grep -rn --include="*.ts" --include="*.tsx" \
  "findMany\(\s*\)" src/ || echo "✅ None found"

echo ""
echo "=== SELECT * ==="
grep -rn --include="*.ts" --include="*.tsx" \
  "SELECT \*" src/ || echo "✅ None found"

echo ""
echo "=== New DB Connections ==="
grep -rn --include="*.ts" --include="*.tsx" \
  -E "new.*(PrismaClient|Pool|Client)\(" src/ | grep -v "lib/db" || echo "✅ None found"

echo ""
echo "Done!"
```

## Checklist

### Query Patterns
- [ ] No queries inside loops (N+1)
- [ ] Independent queries use Promise.all
- [ ] All list queries have LIMIT/take
- [ ] Only needed columns selected
- [ ] Proper indexes on filtered columns

### Connection Management
- [ ] Using connection pooling
- [ ] Singleton pattern for DB client
- [ ] Transactions are short
- [ ] No external calls inside transactions

### Performance
- [ ] Slow queries identified and optimized
- [ ] EXPLAIN ANALYZE on complex queries
- [ ] Proper indexes for common queries
- [ ] Monitoring in place for query times

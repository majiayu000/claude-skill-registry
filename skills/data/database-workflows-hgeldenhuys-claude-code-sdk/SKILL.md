---
name: database-workflows
description: Database workflows - schema design, migrations, query optimization. Use when designing schemas, reviewing migrations, optimizing queries, preventing N+1 problems, or working with ORMs like Prisma, Drizzle, and TypeORM.
version: 1.0.0
author: Claude Code SDK
tags: [database, schema, migrations, sql]
---

# Database Workflows

Quick reference for database work with Claude Code - schema design, migrations, query optimization, and ORM patterns.

## Quick Reference

| Task | Key Action |
|------|------------|
| Schema design | Normalize to 3NF, add indexes for queries |
| Migration review | Check reversibility, data preservation |
| Query optimization | Explain analyze, check indexes |
| N+1 prevention | Eager load relations, use joins |
| Index selection | Composite for multi-column WHERE |

## When to Use This Skill

- Designing new database schemas
- Reviewing migration files before running
- Optimizing slow queries
- Debugging N+1 query problems
- Adding or reviewing indexes
- Working with Prisma, Drizzle, or TypeORM

## Schema Design Checklist

Before creating or modifying schemas:

- [ ] Tables have singular names (`user` not `users`)
- [ ] Primary keys are `id` (auto-increment or UUID)
- [ ] Foreign keys follow `{table}_id` pattern
- [ ] Timestamps include `created_at`, `updated_at`
- [ ] Nullable columns are intentional
- [ ] Indexes cover common query patterns
- [ ] No redundant data (normalized to 3NF minimum)

See [SCHEMA-DESIGN.md](./SCHEMA-DESIGN.md) for detailed patterns.

## Migration Workflow

### Before Creating Migrations

```bash
# Prisma
bunx prisma migrate dev --create-only --name descriptive_name

# Drizzle
bunx drizzle-kit generate:pg --name descriptive_name

# TypeORM
bunx typeorm migration:generate -n DescriptiveName
```

### Migration Review Checklist

- [ ] Migration is reversible (has down/rollback)
- [ ] No data loss on rollback
- [ ] Large tables use batched operations
- [ ] Indexes created CONCURRENTLY (if supported)
- [ ] Foreign key constraints don't lock tables
- [ ] Default values for new NOT NULL columns

See [MIGRATIONS.md](./MIGRATIONS.md) for strategies.

## Query Optimization Quick Guide

### Identify Slow Queries

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

### Analyze Queries

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- MySQL
EXPLAIN ANALYZE SELECT ...;
```

### Common Optimizations

| Problem | Solution |
|---------|----------|
| Full table scan | Add index on WHERE columns |
| Filesort | Add index matching ORDER BY |
| Using temporary | Optimize GROUP BY, add composite index |
| Seq Scan on large table | Add covering index |

See [QUERIES.md](./QUERIES.md) for detailed optimization.

## N+1 Query Prevention

### Problem Pattern

```typescript
// BAD: N+1 queries
const users = await db.user.findMany();
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } });
}
```

### Solution Pattern

```typescript
// GOOD: Single query with relation
const users = await db.user.findMany({
  include: { posts: true }
});
```

### Detection

```typescript
// Prisma: Enable query logging
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
});

// Drizzle: Use query builder with joins
const result = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.userId));
```

## Index Quick Reference

### When to Add Indexes

| Query Pattern | Index Type |
|---------------|------------|
| `WHERE col = ?` | B-tree on col |
| `WHERE col1 = ? AND col2 = ?` | Composite (col1, col2) |
| `WHERE col LIKE 'prefix%'` | B-tree on col |
| `WHERE col @@ to_tsquery(?)` | GIN full-text |
| `ORDER BY col` | B-tree on col |
| `WHERE col IN (...)` | B-tree on col |

### When NOT to Add Indexes

- Small tables (< 1000 rows)
- Columns with low cardinality
- Write-heavy tables with rare reads
- Columns rarely used in WHERE/ORDER BY

### Index Commands

```sql
-- PostgreSQL: Create without locking
CREATE INDEX CONCURRENTLY idx_name ON table(column);

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Find missing indexes
SELECT relname, seq_scan, idx_scan,
       seq_scan - idx_scan AS difference
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY difference DESC;
```

## ORM Patterns

### Prisma

```typescript
// Schema definition
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
  @@index([email])
}

// Efficient query with select
const users = await prisma.user.findMany({
  select: { id: true, email: true },
  where: { email: { contains: '@company.com' } },
  take: 10,
});
```

### Drizzle

```typescript
// Schema definition
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
}, (table) => ({
  emailIdx: index('email_idx').on(table.email),
}));

// Efficient query with joins
const result = await db
  .select({ id: users.id, email: users.email })
  .from(users)
  .where(like(users.email, '%@company.com'))
  .limit(10);
```

### TypeORM

```typescript
// Entity definition
@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  @Index()
  email: string;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;

  @OneToMany(() => Post, post => post.user)
  posts: Post[];
}

// Efficient query with QueryBuilder
const users = await userRepository
  .createQueryBuilder('user')
  .select(['user.id', 'user.email'])
  .where('user.email LIKE :email', { email: '%@company.com' })
  .take(10)
  .getMany();
```

## Database-Specific Patterns

### PostgreSQL

```sql
-- UPSERT
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name, updated_at = NOW();

-- Array columns
ALTER TABLE users ADD COLUMN tags TEXT[];
CREATE INDEX idx_users_tags ON users USING GIN(tags);
SELECT * FROM users WHERE 'admin' = ANY(tags);

-- JSON columns
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}';
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
SELECT * FROM users WHERE metadata->>'role' = 'admin';
```

### MySQL

```sql
-- UPSERT
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON DUPLICATE KEY UPDATE name = VALUES(name), updated_at = NOW();

-- Full-text search
ALTER TABLE posts ADD FULLTEXT INDEX ft_content (title, content);
SELECT * FROM posts WHERE MATCH(title, content) AGAINST('search term');
```

### SQLite

```sql
-- UPSERT
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON CONFLICT(email)
DO UPDATE SET name = excluded.name, updated_at = datetime('now');

-- Enable foreign keys (per connection)
PRAGMA foreign_keys = ON;

-- WAL mode for better concurrency
PRAGMA journal_mode = WAL;
```

## Workflow: Schema Review

### Prerequisites

- [ ] Schema file or migration to review
- [ ] Understanding of query patterns

### Steps

1. **Check Normalization**
   - [ ] No repeated groups
   - [ ] All columns depend on primary key
   - [ ] No transitive dependencies

2. **Validate Relationships**
   - [ ] Foreign keys defined correctly
   - [ ] Cascade rules appropriate
   - [ ] Junction tables for many-to-many

3. **Review Indexes**
   - [ ] Indexes on foreign keys
   - [ ] Indexes on commonly queried columns
   - [ ] Composite indexes in correct order

4. **Check Constraints**
   - [ ] NOT NULL where required
   - [ ] UNIQUE where appropriate
   - [ ] CHECK constraints for valid ranges

### Validation

- [ ] No N+1 patterns in expected queries
- [ ] Indexes support all common queries
- [ ] Schema can evolve without data loss

## Workflow: Query Optimization

### Prerequisites

- [ ] Slow query identified
- [ ] Access to EXPLAIN ANALYZE

### Steps

1. **Analyze Query Plan**
   - [ ] Run EXPLAIN ANALYZE
   - [ ] Identify sequential scans
   - [ ] Check join strategies

2. **Identify Issues**
   - [ ] Missing indexes
   - [ ] Incorrect join order
   - [ ] Unnecessary columns in SELECT

3. **Apply Fixes**
   - [ ] Add appropriate indexes
   - [ ] Rewrite query if needed
   - [ ] Use query hints if necessary

4. **Verify Improvement**
   - [ ] Re-run EXPLAIN ANALYZE
   - [ ] Compare execution times
   - [ ] Test under load

### Validation

- [ ] Query uses indexes effectively
- [ ] Execution time acceptable
- [ ] No regression in related queries

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No index on foreign key | Add index on FK columns |
| SELECT * in production | Select only needed columns |
| N+1 in loops | Use eager loading or joins |
| Missing timestamps | Add created_at, updated_at |
| Nullable by default | Explicitly define NOT NULL |
| No migration rollback | Always write down migration |

## Reference Files

| File | Contents |
|------|----------|
| [SCHEMA-DESIGN.md](./SCHEMA-DESIGN.md) | Schema patterns, normalization, relationships |
| [MIGRATIONS.md](./MIGRATIONS.md) | Migration strategies, rollback, versioning |
| [QUERIES.md](./QUERIES.md) | Query optimization, N+1 prevention, performance |

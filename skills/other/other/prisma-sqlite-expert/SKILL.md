---
name: prisma-sqlite-expert
description: Expert guidance for Prisma ORM with SQLite databases. Use when designing schemas, writing migrations, optimizing queries, working with FTS5 full-text search, or troubleshooting SQLite-specific issues in Node.js/TypeScript applications.
---

# Prisma + SQLite Expert

Comprehensive guidance for building production applications with Prisma ORM and SQLite. Covers schema design, query optimization, migrations, FTS5 full-text search, and SQLite-specific patterns.

For detailed code examples and reference patterns, see [references/patterns.md](references/patterns.md).

## SQLite Connection Configuration

Always configure these PRAGMAs on connection. SQLite defaults are conservative — these are production-proven settings:

```typescript
// After Prisma client initialization
await prisma.$executeRaw`PRAGMA journal_mode = WAL`
await prisma.$executeRaw`PRAGMA synchronous = NORMAL`
await prisma.$executeRaw`PRAGMA foreign_keys = ON`
await prisma.$executeRaw`PRAGMA busy_timeout = 5000`
await prisma.$executeRaw`PRAGMA temp_store = MEMORY`
await prisma.$executeRaw`PRAGMA cache_size = -64000`
await prisma.$executeRaw`PRAGMA mmap_size = 268435456`
```

**Why each matters:**
- `journal_mode = WAL`: Readers never block writers. Critical for concurrent access. Without this, any read blocks all writes.
- `synchronous = NORMAL`: Safe with WAL mode. Only WAL checkpoints wait for fsync, not every write.
- `foreign_keys = ON`: SQLite does NOT enforce foreign keys by default. This is a common source of data integrity bugs.
- `busy_timeout = 5000`: Wait 5s for write locks instead of failing immediately. Prevents `SQLITE_BUSY` errors under load.
- `temp_store = MEMORY`: Keep temp tables in memory instead of disk.
- `cache_size = -64000`: 64MB page cache (negative = KB). Reduces disk reads.
- `mmap_size = 268435456`: Memory-map up to 256MB for faster reads.

**Prisma 7+ with driver adapter** (preferred — gives you direct PRAGMA control):
```typescript
import Database from 'better-sqlite3'
import { PrismaBetterSQLite3 } from '@prisma/adapter-better-sqlite3'

const db = new Database('./app.db')
db.pragma('journal_mode = WAL')
db.pragma('foreign_keys = ON')
db.pragma('synchronous = NORMAL')
db.pragma('busy_timeout = 5000')
db.pragma('temp_store = MEMORY')
db.pragma('cache_size = -64000')

const adapter = new PrismaBetterSQLite3(db)
const prisma = new PrismaClient({ adapter })
```

## Schema Design Principles

### Data Types
- **No native Enum**: Use `String` with application-level validation
- **No arrays**: Use junction tables or JSON strings (`@default("[]")`)
- **No DECIMAL**: Store money as `Int` (cents) — SQLite has no fixed-point type
- **BigInt for file sizes**: Use `BigInt` for values that may exceed 2^53, but remember to convert to string before JSON serialization
- **JSON fields**: Stored as TEXT. Use `Json` type in Prisma. Queryable with `json_extract()` in raw SQL (SQLite 3.38+)

### Timestamps
Every table should have:
```prisma
createdAt DateTime @default(now())
updatedAt DateTime @updatedAt
```
Store all timestamps in UTC.

### Primary Keys
- Use `Int @id @default(autoincrement())` for simple tables
- Use `String @id @default(uuid())` for distributed or sync scenarios
- Composite PKs (`@@id([field1, field2])`) for multi-tenant or multi-instance data

### Soft Deletes
For data that syncs from external sources:
```prisma
deletedAt DateTime?
```
Always filter: `WHERE deletedAt IS NULL` in every query.

### Indexes
```prisma
model Entity {
  id        String   @id
  status    String
  createdAt DateTime @default(now())
  parentId  String

  parent    Parent   @relation(fields: [parentId], references: [id])

  @@index([parentId])                          // ALWAYS index foreign keys
  @@index([status, createdAt(sort: Desc)])     // Composite: most selective first
  @@index([deletedAt, createdAt(sort: Desc)])  // Soft delete + sort pattern
}
```

**Index rules:**
- Always index foreign key columns (Prisma does NOT auto-create these)
- Composite index column order: equality columns first, then range/sort columns
- Most selective (highest cardinality) column first in composites
- Partial indexes (via raw migration SQL) for hot subsets: `CREATE INDEX idx_active ON "User"(email) WHERE status = 'active'`
- Every index slows writes — only index columns you actually query on

### Relations
- Always use explicit `@relation` with `fields:` and `references:`
- Set `onDelete:` strategy deliberately: `Cascade` for owned data, `Restrict` for referenced data, `SetNull` for optional references
- Junction tables for many-to-many — avoid implicit many-to-many without explicit join tables

## Query Optimization

### Avoid N+1 Queries (the #1 ORM performance problem)
```typescript
// BAD: N+1
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } })
}

// GOOD: eager load
const users = await prisma.user.findMany({
  include: { posts: true }
})

// BETTER: select only what you need
const users = await prisma.user.findMany({
  select: {
    id: true, name: true,
    posts: { select: { id: true, title: true }, where: { published: true }, take: 5 }
  }
})
```

### Select Only Needed Fields
```typescript
// BAD: fetches every column
const users = await prisma.user.findMany()

// GOOD: minimal data transfer
const users = await prisma.user.findMany({
  select: { id: true, email: true, name: true }
})
```

### Use _count for Relation Counts
```typescript
const users = await prisma.user.findMany({
  select: {
    name: true,
    _count: { select: { posts: { where: { published: true } }, followers: true } }
  }
})
```

### Pagination: Prefer Cursor-Based
```typescript
// OFFSET pagination (fine for small datasets, degrades at depth)
const page = await prisma.post.findMany({ skip: offset, take: limit, orderBy: { id: 'asc' } })

// CURSOR pagination (constant time at any depth)
const page = await prisma.post.findMany({
  take: 20, skip: 1, cursor: { id: lastSeenId }, orderBy: { id: 'asc' }
})
```

### Batch Operations
```typescript
// BAD: individual creates in a loop
for (const item of items) { await prisma.item.create({ data: item }) }

// GOOD: batch
await prisma.item.createMany({ data: items })
```

**SQLite caveat:** `createMany` does NOT support `skipDuplicates`. Use individual upserts:
```typescript
await Promise.all(items.map(item =>
  prisma.item.upsert({ where: { id: item.id }, create: item, update: {} })
))
```

### Raw SQL for Complex Queries
Use `$queryRaw` with tagged template literals — they auto-parameterize and prevent SQL injection:
```typescript
const results = await prisma.$queryRaw`
  SELECT u.name, COUNT(p.id) as postCount
  FROM User u LEFT JOIN Post p ON p.authorId = u.id
  WHERE u.status = ${status}
  GROUP BY u.id, u.name
`
```

**For dynamic identifiers (table/column names), whitelist — never interpolate user input:**
```typescript
const ALLOWED_SORT = ['createdAt', 'name', 'email'] as const
if (!ALLOWED_SORT.includes(sortBy)) throw new Error(`Invalid sort: ${sortBy}`)
```

### Use EXPLAIN QUERY PLAN to Verify Index Usage
```typescript
const plan = await prisma.$queryRaw`EXPLAIN QUERY PLAN SELECT * FROM User WHERE email = ${email}`
```
Look for `USING INDEX` — if you see `SCAN TABLE`, your query is doing a full table scan.

## Transactions

### Simple Batch (array of operations)
```typescript
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'alice@example.com' } }),
  prisma.post.create({ data: { title: 'Hello', authorId: 1 } })
])
```

### Interactive (for dependent operations)
```typescript
await prisma.$transaction(async (tx) => {
  const sender = await tx.account.update({
    where: { id: senderId },
    data: { balance: { decrement: amount } }
  })
  if (sender.balance < 0) throw new Error('Insufficient funds') // rolls back everything
  await tx.account.update({
    where: { id: recipientId },
    data: { balance: { increment: amount } }
  })
}, { timeout: 30000 })
```

**SQLite-specific:** Keep write transactions short. SQLite locks the entire database file during writes. Do all data preparation outside the transaction.

### TransactionClient Type
```typescript
type TransactionClient = Omit<PrismaClient,
  '$connect' | '$disconnect' | '$on' | '$transaction' | '$use' | '$extends'>
```

## FTS5 Full-Text Search

Prisma cannot manage FTS5 virtual tables — handle via raw SQL in manual migrations.

### Setup (in migration SQL)
```sql
CREATE VIRTUAL TABLE IF NOT EXISTS entity_fts USING fts5(
    id, title, details,
    content='SourceTable',
    content_rowid='rowid',
    tokenize='porter unicode61 remove_diacritics 2',
    prefix='2,3'
);
```

### Sync Triggers (required for content tables)
```sql
CREATE TRIGGER entity_fts_insert AFTER INSERT ON SourceTable BEGIN
    INSERT INTO entity_fts(rowid, id, title, details)
    VALUES (NEW.rowid, NEW.id, NEW.title, NEW.details);
END;

CREATE TRIGGER entity_fts_delete AFTER DELETE ON SourceTable BEGIN
    INSERT INTO entity_fts(entity_fts, rowid, id, title, details)
    VALUES ('delete', OLD.rowid, OLD.id, OLD.title, OLD.details);
END;

CREATE TRIGGER entity_fts_update AFTER UPDATE ON SourceTable BEGIN
    INSERT INTO entity_fts(entity_fts, rowid, id, title, details)
    VALUES ('delete', OLD.rowid, OLD.id, OLD.title, OLD.details);
    INSERT INTO entity_fts(rowid, id, title, details)
    VALUES (NEW.rowid, NEW.id, NEW.title, NEW.details);
END;
```

### Querying FTS5
```typescript
const results = await prisma.$queryRaw`
  SELECT s.*, bm25(entity_fts) as relevance
  FROM entity_fts
  INNER JOIN SourceTable s ON entity_fts.id = s.id
  WHERE entity_fts MATCH ${query}
    AND s.deletedAt IS NULL
  ORDER BY relevance
  LIMIT ${limit}
`
```

**Always implement a LIKE fallback** — FTS5 can fail on special characters:
```typescript
try {
  return await ftsSearch(query, limit)
} catch {
  return await prisma.sourceTable.findMany({
    where: { deletedAt: null, OR: [{ title: { contains: query } }, { code: { contains: query } }] },
    take: limit,
  })
}
```

### FTS5 Query Syntax
- `rust AND async` — both terms
- `rust OR go` — either term
- `rust NOT unsafe` — exclude
- `"exact phrase"` — phrase match
- `rust*` — prefix match
- `title:rust` — search specific column

### FTS Maintenance
```sql
-- Optimize index (merge segments) — run periodically
INSERT INTO entity_fts(entity_fts) VALUES('optimize');
-- Rebuild index (after bulk operations or corruption)
INSERT INTO entity_fts(entity_fts) VALUES('rebuild');
```

## Migration Workflow

### Standard Prisma Migrations (no FTS tables)
```bash
npx prisma migrate dev --name descriptive_name    # Development
npx prisma migrate deploy                          # Production
```

### Manual Migrations (required when FTS tables exist)
Prisma's introspection sees FTS virtual tables as "schema drift" and wants to reset. Bypass this:

```bash
# 1. Create migration directory
mkdir -p prisma/migrations/YYYYMMDD000000_descriptive_name

# 2. Write SQL manually
# prisma/migrations/YYYYMMDD000000_descriptive_name/migration.sql

# 3. Update schema.prisma to match the SQL changes

# 4. Regenerate client
npx prisma generate

# 5. Apply (does NOT introspect — just runs the SQL)
npx prisma migrate deploy
```

**Never use `prisma migrate dev`** in projects with FTS tables. It will detect "drift" and request a database reset.

### Safe Migration Patterns
- **Add columns as nullable first**, backfill, then make required (if needed)
- **SQLite cannot:** drop columns (pre-3.35), change column types, alter primary keys, add constraints to existing columns
- **For any of those, use the copy-table pattern:**
  1. `CREATE TABLE new_table (...)` with desired schema
  2. `INSERT INTO new_table SELECT ... FROM old_table`
  3. `DROP TABLE old_table`
  4. `ALTER TABLE new_table RENAME TO old_table`
  5. Recreate indexes and triggers
- Use `PRAGMA foreign_keys=OFF` during table recreation, re-enable after
- Use `CREATE INDEX IF NOT EXISTS` for idempotent index creation

## SQLite Limitations & Workarounds

| Limitation | Workaround |
|---|---|
| No `skipDuplicates` in `createMany` | Use individual upserts in `Promise.all` |
| No `ALTER TABLE` for PKs/constraints | Copy-table pattern (create, copy, drop, rename) |
| No `UPDATE ... FROM` (JOINed updates) | Use CASE expressions or subqueries |
| 999 parameter limit | Use JOIN-based filtering instead of `WHERE id NOT IN (...)` with large arrays |
| Single writer (file-level lock) | Keep write transactions short; use WAL mode; sequential writes when order matters |
| No concurrent schema migrations | Run migrations serially, never in parallel |
| `RANDOM()` integer overflow | Use modular arithmetic: `ABS((seed * 3266489917 + id * 277803737) % 4294967291)` |
| BigInt not JSON-serializable | Convert to string before sending to client |
| FTS tables cause Prisma drift detection | Use manual migrations with `prisma migrate deploy` only |
| `LIKE '%term%'` cannot use indexes | Use FTS5 for text search; only `LIKE 'term%'` (prefix) can use indexes |

## Database Maintenance

```typescript
// Run on connection open or periodically
await prisma.$executeRaw`PRAGMA optimize`

// After bulk data changes
await prisma.$executeRaw`ANALYZE`

// Reclaim space (locks entire DB — run during low traffic)
const [{ freelist_count }] = await prisma.$queryRaw`PRAGMA freelist_count`
if (freelist_count > 1000) {
  await prisma.$executeRaw`VACUUM`
}
```

### Backup
```typescript
// Atomic backup using VACUUM INTO (safe during writes)
await prisma.$executeRawUnsafe(`VACUUM INTO '${validatedBackupPath}'`)
```
Always validate the backup path to prevent path traversal. Never interpolate user input.

### WAL Checkpoint Management
If WAL file grows large (checkpoint starvation from long-running reads):
```typescript
await prisma.$executeRaw`PRAGMA wal_checkpoint(RESTART)`
```

## Checklist

Before shipping database changes:
- [ ] Foreign keys indexed
- [ ] Composite index column order matches query patterns
- [ ] `PRAGMA foreign_keys = ON` set on connection
- [ ] WAL mode enabled
- [ ] Migrations tested on a copy of production data
- [ ] FTS triggers updated if FTS-indexed columns changed
- [ ] No `$queryRawUnsafe` with user input
- [ ] BigInt fields converted to string in API responses
- [ ] `deletedAt IS NULL` filter on all soft-delete table queries
- [ ] Write transactions are short and do prep work outside

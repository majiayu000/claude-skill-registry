---
name: "Database Design"
description: "Schema design, normalization, query optimization, and data modeling patterns"
applyTo: "**/*database*,**/*schema*,**/*sql*,**/*postgres*,**/*mongo*,**/*prisma*,**/*drizzle*"
---

# Database Design Skill

> Model data to match access patterns. Normalize for integrity, denormalize for performance.

---

## Choosing a Database

### Decision Matrix

| Factor | SQL (Relational) | NoSQL (Document) | Key-Value | Graph |
|--------|------------------|------------------|-----------|-------|
| **Schema** | Fixed, strict | Flexible | None | Nodes/edges |
| **Transactions** | ACID built-in | Eventually consistent (usually) | Limited | Varies |
| **Joins** | Native support | Expensive/manual | N/A | Native (relationships) |
| **Scale** | Vertical → Horizontal | Horizontal native | Horizontal native | Specialized |
| **Best for** | Structured data, complex queries | Rapid iteration, varied shape | Cache, sessions | Relationships |

### Common Choices (2026)

| Database | Type | Best For |
|----------|------|----------|
| **PostgreSQL** | Relational | General purpose, full-featured |
| **SQLite** | Relational | Embedded, serverless |
| **MongoDB** | Document | Rapid prototyping, flexible schema |
| **Redis** | Key-Value | Caching, sessions, pub/sub |
| **Cosmos DB** | Multi-model | Azure-native, global distribution |
| **DynamoDB** | Key-Value/Document | AWS-native, massive scale |
| **Neo4j** | Graph | Social networks, recommendations |

---

## Schema Design Principles

### Normalization Levels

| Form | Rule | Trade-off |
|------|------|-----------|
| **1NF** | No repeating groups | Basic structure |
| **2NF** | No partial dependencies | Remove redundancy |
| **3NF** | No transitive dependencies | Data integrity |
| **BCNF** | Every determinant is a key | Strict integrity |

### When to Denormalize

- Read-heavy workloads
- Complex queries hitting many tables
- When consistency can be eventual
- Reporting/analytics tables

### Example: E-Commerce Schema

```sql
-- Normalized (3NF)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) NOT NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

-- Denormalized for reporting
CREATE TABLE order_summary (
    order_id INTEGER PRIMARY KEY,
    customer_email VARCHAR(255),
    customer_name VARCHAR(255),
    total_amount DECIMAL(10,2),
    item_count INTEGER,
    created_at TIMESTAMP
);
```

---

## Modern ORM Patterns

### Prisma (TypeScript)

```prisma
// schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

```typescript
// Usage - type-safe queries
const user = await prisma.user.findUnique({
  where: { email: 'alex@example.com' },
  include: { posts: true }
});
```

### Drizzle (TypeScript)

```typescript
// schema.ts
import { pgTable, serial, varchar, integer, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).unique().notNull(),
  name: varchar('name', { length: 255 }),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  authorId: integer('author_id').references(() => users.id),
});

// Usage
const result = await db.select().from(users).where(eq(users.email, 'alex@example.com'));
```

### Entity Framework (.NET)

```csharp
public class User
{
    public int Id { get; set; }
    public string Email { get; set; } = null!;
    public string? Name { get; set; }
    public ICollection<Post> Posts { get; } = new List<Post>();
}

// Usage
var user = await context.Users
    .Include(u => u.Posts)
    .FirstOrDefaultAsync(u => u.Email == "alex@example.com");
```

---

## Query Optimization

### The EXPLAIN Plan

```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id
ORDER BY post_count DESC
LIMIT 10;
```

### Reading Execution Plans

| Operation | Meaning | Concern |
|-----------|---------|---------|
| Seq Scan | Full table scan | Consider index |
| Index Scan | Using index | Good |
| Nested Loop | For each row... | OK for small sets |
| Hash Join | Build hash table | Good for large sets |
| Sort | In-memory sort | Check work_mem |

### Index Strategy

```sql
-- Single column (most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite (column order matters!)
CREATE INDEX idx_posts_author_date ON posts(author_id, created_at DESC);

-- Partial (when you query a subset)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering (includes all needed columns)
CREATE INDEX idx_posts_covering ON posts(author_id) INCLUDE (title, created_at);
```

### Query Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `SELECT *` | Fetches unnecessary data | List specific columns |
| N+1 queries | Loop makes N queries | Use JOIN or eager loading |
| Missing index on WHERE | Full table scan | Add appropriate index |
| OR in WHERE | Can't use index efficiently | UNION ALL or restructure |
| Functions on columns | `WHERE YEAR(date) = 2026` | `WHERE date >= '2026-01-01'` |

---

## Data Modeling Patterns

### Soft Deletes

```sql
-- Instead of DELETE, update a flag
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 123;
```

### Audit Trails

```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger for automatic auditing (PostgreSQL)
CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
    VALUES (TG_TABLE_NAME, COALESCE(NEW.id, OLD.id), TG_OP, 
            to_jsonb(OLD), to_jsonb(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Temporal Tables

```sql
-- PostgreSQL example
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    valid_from TIMESTAMP DEFAULT NOW(),
    valid_to TIMESTAMP DEFAULT 'infinity'
);

-- Query current data
SELECT * FROM products WHERE valid_to = 'infinity';

-- Query historical data (what was the price on Jan 1?)
SELECT * FROM products 
WHERE valid_from <= '2026-01-01' AND valid_to > '2026-01-01';
```

---

## NoSQL Patterns

### Document Modeling (MongoDB)

```javascript
// ❌ Relational thinking (too normalized)
{ _id: 1, userId: 'u1', productId: 'p1' }  // separate collection

// ✅ Document thinking (embed when 1:few or frequent access together)
{
  _id: 'order123',
  customer: {
    id: 'c1',
    name: 'Alex',
    email: 'alex@example.com'
  },
  items: [
    { productId: 'p1', name: 'Widget', price: 9.99, quantity: 2 },
    { productId: 'p2', name: 'Gadget', price: 19.99, quantity: 1 }
  ],
  total: 39.97,
  createdAt: ISODate('2026-02-11')
}
```

### Embedding vs Referencing

| Embed When | Reference When |
|------------|----------------|
| 1:1 or 1:few relationship | 1:many or many:many |
| Data accessed together | Data accessed independently |
| Data doesn't change often | Data changes frequently |
| Size is bounded | Unbounded growth |

---

## Migration Strategies

### Schema Migration Best Practices

1. **Forward-only migrations** — Don't modify existing migrations
2. **Small, incremental changes** — One concern per migration
3. **Backward compatible** — Add before remove
4. **Test migrations** — Run against production copy

### Zero-Downtime Schema Changes

```sql
-- Phase 1: Add new column (nullable)
ALTER TABLE users ADD COLUMN new_email VARCHAR(255);

-- Phase 2: Backfill data (in batches)
UPDATE users SET new_email = email WHERE new_email IS NULL LIMIT 1000;

-- Phase 3: Update application to write to both columns

-- Phase 4: Make new column required
ALTER TABLE users ALTER COLUMN new_email SET NOT NULL;

-- Phase 5: Update application to read from new column

-- Phase 6: Drop old column
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN new_email TO email;
```

---

## Connection Management

### Connection Pooling

```typescript
// Prisma with connection pool
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Pool settings in URL: ?connection_limit=10&pool_timeout=30
}

// Node postgres pool
const pool = new Pool({
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Connection Pool Sizing

Rule of thumb for PostgreSQL:
```
connections = (core_count * 2) + spindle_count
```

For cloud: Start with 10-20, monitor and adjust.

---

## Implementation Checklist

### New Database

- [ ] Choose appropriate database type
- [ ] Design initial schema (3NF or justified denormalization)
- [ ] Define primary keys and foreign keys
- [ ] Plan indexes for known query patterns
- [ ] Set up connection pooling
- [ ] Configure backups and point-in-time recovery
- [ ] Set up monitoring (query performance, connections)

### Production Readiness

- [ ] Indexes for all WHERE/JOIN columns
- [ ] No N+1 query patterns
- [ ] Connection pool sized appropriately
- [ ] Query timeouts configured
- [ ] Slow query logging enabled
- [ ] Backup restoration tested

---

## Related Skills

- **performance-profiling** — Query-level performance analysis
- **api-design** — Data shapes for API responses
- **infrastructure-as-code** — Database provisioning
- **security-review** — Access control, encryption

---

*Design for today's queries, but plan for tomorrow's scale.*

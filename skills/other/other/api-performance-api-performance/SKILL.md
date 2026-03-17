---
name: api-performance-api-performance
description: Query optimization, caching, indexing
---

# Backend Performance Optimization

> **Quick Guide:** Optimize backend performance through database query optimization (indexes, prepared statements, avoiding N+1), caching strategies (Redis cache-aside, write-through), connection pooling, and non-blocking async patterns. Always measure before optimizing.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always release database connections back to the pool using `finally` blocks)**

**(You MUST use `.with()` or eager loading to prevent N+1 queries - never lazy load in loops)**

**(You MUST set TTL on all cached data to prevent stale data and memory exhaustion)**

**(You MUST offload CPU-intensive work to Worker Threads - blocking the event loop degrades all requests)**

</critical_requirements>

---

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [caching.md](examples/caching.md) - Redis caching patterns and strategies
  - [database.md](examples/database.md) - Query optimization, indexing, connection pooling
  - [async.md](examples/async.md) - Event loop, worker threads, CPU-bound tasks
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

**Auto-detection:** Redis, connection pool, query optimization, database index, N+1, caching, cache invalidation, prepared statement, worker threads, event loop, CPU-bound, latency, throughput, performance tuning

**When to use:**

- Database queries taking > 100ms
- High-traffic endpoints with repeated data fetches
- API responses with multiple related entities (N+1 risk)
- CPU-intensive operations blocking request handling
- Need to reduce database load or API costs

**When NOT to use:**

- Premature optimization without measuring first
- Simple CRUD with low traffic (adds complexity without benefit)
- Data that changes frequently and must be fresh (caching adds staleness)
- Development/debugging (caching obscures issues)

**Key patterns covered:**

- Database indexing strategies (composite, partial, covering)
- Connection pooling (node-postgres, external poolers)
- N+1 query prevention (eager loading, DataLoader)
- Redis caching (cache-aside, write-through, invalidation)
- Event loop optimization (async patterns, setImmediate)
- Worker threads for CPU-bound operations
- Prepared statements for repeated queries

---

<philosophy>

## Philosophy

Backend performance optimization follows one core principle: **measure first, optimize second**. Premature optimization wastes development time and adds complexity without evidence of benefit.

**The Three Pillars of Backend Performance:**

1. **Database Optimization** - Indexes, query planning, N+1 prevention
2. **Caching** - Reduce repeated expensive operations
3. **Async Efficiency** - Never block the event loop

**When to optimize:**

- Response times exceed SLA thresholds
- Database CPU/memory approaching limits
- Metrics show specific bottlenecks
- Load testing reveals scaling issues

**When NOT to optimize:**

- "It might be slow someday" (premature)
- Following blog post advice without context
- Optimizing cold paths (rarely executed code)
- Before profiling identifies the actual bottleneck

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Database Connection Pooling

Connection pooling reuses database connections instead of creating new ones per request. A PostgreSQL handshake takes 20-30ms - pooling eliminates this overhead.

#### Configuration

```typescript
// Good Example - Proper connection pooling with node-postgres
import { Pool } from "pg";

const POOL_MAX_CONNECTIONS = 20;
const POOL_IDLE_TIMEOUT_MS = 30000;
const POOL_CONNECTION_TIMEOUT_MS = 5000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: POOL_MAX_CONNECTIONS,
  idleTimeoutMillis: POOL_IDLE_TIMEOUT_MS,
  connectionTimeoutMillis: POOL_CONNECTION_TIMEOUT_MS,
});

// Listen for pool errors (idle clients can still emit errors)
pool.on("error", (err) => {
  console.error("Unexpected pool error:", err);
});

// For simple queries - auto-manages connection lifecycle
async function getUsers() {
  const result = await pool.query("SELECT * FROM users WHERE active = $1", [
    true,
  ]);
  return result.rows;
}

// For transactions - manual checkout with guaranteed release
async function createUserWithProfile(
  userData: UserData,
  profileData: ProfileData,
) {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const userResult = await client.query(
      "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
      [userData.name, userData.email],
    );
    await client.query("INSERT INTO profiles (user_id, bio) VALUES ($1, $2)", [
      userResult.rows[0].id,
      profileData.bio,
    ]);
    await client.query("COMMIT");
    return userResult.rows[0];
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release(); // CRITICAL: Always release back to pool
  }
}

// Graceful shutdown
async function shutdown() {
  await pool.end();
}

export { pool, getUsers, createUserWithProfile, shutdown };
```

**Why good:** Named constants document configuration, `pool.query()` auto-manages simple queries, `finally` block guarantees connection release preventing pool exhaustion, error listener catches backend failures, graceful shutdown prevents connection leaks

```typescript
// Bad Example - Connection leak and missing error handling
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function createUser(data) {
  const client = await pool.connect();
  await client.query("INSERT INTO users (name) VALUES ($1)", [data.name]);
  // Missing client.release() - connection leaked!
  // Missing error handling - transaction left open on failure
}
```

**Why bad:** Missing `client.release()` causes connection pool exhaustion, no try/catch means failed queries leave connections checked out forever, no transaction handling means partial writes possible

---

### Pattern 2: N+1 Query Prevention

The N+1 problem occurs when fetching N records triggers N additional queries for related data. Use eager loading or batching instead.

#### Eager Loading with ORM

```typescript
// Good Example - Single query with eager loading (Drizzle)
import { db } from "./database";
import { and, eq, isNull } from "drizzle-orm";

async function getJobsWithCompanies() {
  // Single SQL query fetches jobs + companies + locations
  const jobs = await db.query.jobs.findMany({
    where: and(eq(jobs.isActive, true), isNull(jobs.deletedAt)),
    with: {
      company: {
        with: {
          locations: true,
        },
      },
      jobSkills: {
        with: {
          skill: true,
        },
      },
    },
  });

  return jobs;
}
```

**Why good:** `.with()` generates a single SQL query with JOINs, eliminates N+1 problem entirely, fully typed result prevents runtime errors

```typescript
// Bad Example - N+1 query anti-pattern
async function getJobsWithCompanies() {
  const jobs = await db.query.jobs.findMany({
    where: eq(jobs.isActive, true),
  });

  // N+1: One query per job to get company!
  for (const job of jobs) {
    job.company = await db.query.companies.findFirst({
      where: eq(companies.id, job.companyId),
    });
  }

  return jobs;
}
```

**Why bad:** 1 query for jobs + N queries for companies = N+1 total queries, latency grows linearly with data size, database gets hammered with many small queries

#### DataLoader Pattern (GraphQL/REST)

```typescript
// Good Example - DataLoader for batching
import DataLoader from "dataloader";

// Create loader once per request (caches within request lifecycle)
function createCompanyLoader() {
  return new DataLoader<string, Company>(async (companyIds) => {
    // Single query for all requested companies
    const companies = await db.query.companies.findMany({
      where: inArray(companies.id, [...companyIds]),
    });

    // Return in same order as requested IDs
    const companyMap = new Map(companies.map((c) => [c.id, c]));
    return companyIds.map((id) => companyMap.get(id) ?? null);
  });
}

// Usage in resolver or handler
async function resolveJob(job: Job, context: Context) {
  // DataLoader batches all .load() calls in same tick
  const company = await context.loaders.company.load(job.companyId);
  return { ...job, company };
}
```

**Why good:** DataLoader batches multiple `.load()` calls into single query, caches results within request preventing duplicate fetches, works with any data source (DB, API, etc.)

---

### Pattern 3: Database Indexing

Indexes speed up queries by avoiding full table scans. Index columns used in WHERE, JOIN, and ORDER BY clauses.

#### Index Strategies

```typescript
// Good Example - Strategic indexes (Drizzle schema)
import {
  pgTable,
  uuid,
  varchar,
  timestamp,
  boolean,
  index,
} from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

export const jobs = pgTable(
  "jobs",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    companyId: uuid("company_id").notNull(),
    title: varchar("title", { length: 255 }).notNull(),
    country: varchar("country", { length: 100 }),
    employmentType: varchar("employment_type", { length: 50 }),
    isActive: boolean("is_active").default(true),
    createdAt: timestamp("created_at").defaultNow(),
    deletedAt: timestamp("deleted_at"),
  },
  (table) => ({
    // Composite index for common filter combination
    countryEmploymentIdx: index("jobs_country_employment_idx").on(
      table.country,
      table.employmentType,
    ),

    // Partial index - only indexes active non-deleted jobs
    activeJobsIdx: index("jobs_active_idx")
      .on(table.isActive, table.createdAt)
      .where(sql`${table.deletedAt} IS NULL`),

    // Foreign key index for JOIN performance
    companyIdIdx: index("jobs_company_id_idx").on(table.companyId),

    // Text search index
    titleIdx: index("jobs_title_idx").on(table.title),
  }),
);
```

**Why good:** Composite index matches common query patterns (country + employmentType), partial index reduces index size by excluding deleted records, foreign key index speeds up JOINs, column order in composite index matches query filter order

**Index Decision Framework:**

| Column Usage                | Index Type       | When to Use                                    |
| --------------------------- | ---------------- | ---------------------------------------------- |
| WHERE equality              | B-tree (default) | High-selectivity columns                       |
| WHERE range (>, <, BETWEEN) | B-tree           | Date ranges, numeric ranges                    |
| WHERE multiple columns      | Composite        | Queries always filter by same columns together |
| WHERE on subset             | Partial          | Most queries filter on active/non-deleted      |
| Full-text search            | GIN/GiST         | Text search with LIKE, tsvector                |
| JSON field access           | GIN              | JSONB column queries                           |

</patterns>

---

## Additional Patterns

The following patterns are documented with full examples in [examples/](examples/):

- **Redis Caching** - Cache-aside, write-through, invalidation, TTL - see [caching.md](examples/caching.md)
- **Prepared Statements** - Reuse query plans for repeated queries - see [database.md](examples/database.md)
- **Event Loop Optimization** - Async patterns, setImmediate chunking - see [async.md](examples/async.md)
- **Worker Threads** - CPU-bound operations without blocking - see [async.md](examples/async.md)

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST always release database connections back to the pool using `finally` blocks)**

**(You MUST use `.with()` or eager loading to prevent N+1 queries - never lazy load in loops)**

**(You MUST set TTL on all cached data to prevent stale data and memory exhaustion)**

**(You MUST offload CPU-intensive work to Worker Threads - blocking the event loop degrades all requests)**

**Failure to follow these rules will cause connection pool exhaustion, N+1 performance degradation, memory leaks from unbounded caches, and blocked event loops affecting all concurrent requests.**

</critical_reminders>

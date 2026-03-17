---
name: api-database-drizzle
description: Drizzle ORM, queries, migrations
---

# Database with Drizzle ORM + Neon

> **Quick Guide:** Use Drizzle ORM for type-safe queries, Neon serverless Postgres for edge-compatible connections. Schema-first design with automatic TypeScript types. Use RQB v2 with `defineRelations()` and object-based `where` syntax. Relational queries with `.with()` avoid N+1 problems. Use transactions for atomic operations.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set `casing: 'snake_case'` in Drizzle config to map camelCase JS to snake_case SQL)**

**(You MUST use `tx` parameter (NOT `db`) inside transaction callbacks to ensure atomicity)**

**(You MUST use `.with()` for relational queries to avoid N+1 problems - fetches all data in single SQL query)**

**(You MUST use `defineRelations()` for RQB v2 - the old `relations()` per-table syntax is deprecated)**

</critical_requirements>

---

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Connection setup and schema definition (always loaded)
  - [queries.md](examples/queries.md) - Relational queries and query builder
  - [relations-v2.md](examples/relations-v2.md) - RQB v2 with defineRelations() (NEW)
  - [transactions.md](examples/transactions.md) - Atomic operations
  - [migrations.md](examples/migrations.md) - Drizzle Kit workflow
  - [seeding.md](examples/seeding.md) - Development data population (includes drizzle-seed)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

**Auto-detection:** drizzle-orm, @neondatabase/serverless, neon-http, db.query, db.transaction, drizzle-kit, pgTable, defineRelations, drizzle-seed

**When to use:**

- Serverless functions needing type-safe database queries
- Schema-first development with migrations
- Building Next.js apps with API routes

**When NOT to use:**

- Simple apps using Next.js server actions directly (overhead not justified)
- Apps needing traditional TCP connection pooling only (use standard Postgres clients)
- Non-TypeScript projects (lose primary benefit of type safety)
- Edge functions requiring WebSocket connections (not supported in edge runtime)

**Key patterns covered:**

- Neon serverless connection (HTTP and WebSocket)
- Drizzle schema design (tables, relations, enums)
- RQB v2 with `defineRelations()` and object-based syntax (NEW)
- Relational queries with `.with()` (single SQL query)
- Query builder for complex filters
- Many-to-many with `.through()` (eliminates junction table boilerplate)
- Transactions for atomic operations
- Database migrations with Drizzle Kit
- drizzle-seed for deterministic test data
- Performance optimization (indexes, prepared statements, batch API)

---

<philosophy>

## Philosophy

**Drizzle ORM** provides SQL-like queries with TypeScript safety and zero runtime overhead. **Neon Serverless** offers PostgreSQL over HTTP/WebSocket for edge compatibility.

**When to use this stack:**

- Serverless functions (Vercel, Cloudflare Workers, Edge)
- Need type-safe database queries
- Want schema-first development with migrations
- Building Next.js apps with API routes

**When NOT to use:**

- Simple apps using Next.js server actions directly
- Apps needing traditional TCP connection pooling only
- Non-TypeScript projects

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Database Connection (Neon HTTP)

Configure Drizzle with Neon for serverless/edge compatibility.

#### Configuration

```typescript
// Good Example - Proper Neon HTTP setup
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "./db/schema";

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable is not set");
}

// Use neon() for HTTP-based queries (edge-compatible)
export const sql = neon(process.env.DATABASE_URL);

// Initialize Drizzle with schema and snake_case mapping
export const db = drizzle(sql, {
  schema,
  casing: "snake_case", // Maps camelCase JS to snake_case SQL
});

// Export tables for direct query access
export const { jobs, companies, companyLocations, skills, jobSkills } = schema;
```

**Why good:** Environment variable validation prevents runtime errors, `casing: "snake_case"` ensures JS camelCase maps correctly to SQL snake_case preventing field name mismatches, HTTP connection works in all serverless environments

#### Drizzle Kit Configuration

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./lib/db/schema.ts",
  out: "./drizzle", // Migration files output
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

For more connection examples (WebSocket, error handling), see [examples/core.md](examples/core.md).

---

### Pattern 2: Schema Definition

Define tables with TypeScript types using Drizzle's schema builder.

#### Constants and Enums

```typescript
import {
  pgTable,
  uuid,
  varchar,
  text,
  timestamp,
  boolean,
  integer,
  pgEnum,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Define enums for constrained values
export const employmentTypeEnum = pgEnum("employment_type", [
  "full_time",
  "part_time",
  "contract",
  "internship",
  "freelance",
]);

export const seniorityLevelEnum = pgEnum("seniority_level", [
  "intern",
  "junior",
  "mid",
  "senior",
  "lead",
  "principal",
]);
```

#### Table Definitions

```typescript
// Good Example - Well-structured table with constraints
export const companies = pgTable("companies", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: varchar("name", { length: 255 }).notNull(),
  slug: varchar("slug", { length: 255 }).unique(),
  description: text("description"),
  logoUrl: text("logo_url"),
  websiteUrl: text("website_url"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
  deletedAt: timestamp("deleted_at"), // Soft delete
});
```

**Why good:** `uuid().defaultRandom()` generates secure unique IDs, `.notNull()` enforces required fields preventing null errors, enums constrain values to valid options, `deletedAt` enables soft deletes preserving data history, `createdAt`/`updatedAt` track record lifecycle

For complete schema examples (relations, junction tables), see [examples/core.md](examples/core.md).

---

### Pattern 3: Relational Queries with `.with()`

Fetch related data efficiently in a single SQL query.

```typescript
// Good Example - Efficient relational query
import { and, eq, desc, asc, isNull } from "drizzle-orm";

const job = await db.query.jobs.findFirst({
  where: and(
    eq(jobs.id, jobId),
    eq(jobs.isActive, true),
    isNull(jobs.deletedAt),
  ),
  with: {
    company: {
      with: {
        locations: {
          orderBy: [
            desc(companyLocations.isHeadquarters),
            asc(companyLocations.name),
          ],
        },
      },
    },
    jobSkills: {
      where: eq(jobSkills.isRequired, true),
      with: {
        skill: true,
      },
    },
  },
});

// Result is fully typed and nested
if (job) {
  console.log(job.title); // string
  console.log(job.company.name); // string
  console.log(job.company.locations); // CompanyLocation[]
  console.log(job.jobSkills[0].skill.name); // string
}
```

**Why good:** Single SQL query eliminates N+1 problem, nested `.with()` loads deep relations efficiently, soft delete check prevents returning deleted records, ordering nested results provides predictable output, fully typed results catch errors at compile time

**When to use:** Need related data across tables, want to avoid N+1 queries, prefer type-safe queries over raw SQL

**When not to use:** Simple queries without relations (use `db.select()`), need custom JOINs with complex conditions (use query builder)

For more query examples (N+1 anti-pattern, complex filtering), see [examples/queries.md](examples/queries.md).

</patterns>

---

## Additional Patterns

The following patterns are documented with full examples in [examples/](examples/):

- **Query Builder** - Complex filters, dynamic conditions, custom JOINs - see [queries.md](examples/queries.md)
- **Transactions** - Atomic operations, error handling, rollback - see [transactions.md](examples/transactions.md)
- **Database Migrations** - Drizzle Kit workflow, `generate` vs `push` - see [migrations.md](examples/migrations.md)
- **Database Seeding** - Development data, safe cleanup - see [seeding.md](examples/seeding.md)

Performance optimization (indexes, prepared statements, pagination) is documented in [reference.md](reference.md#performance-optimization).

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST set `casing: 'snake_case'` in Drizzle config to map camelCase JS to snake_case SQL)**

**(You MUST use `tx` parameter (NOT `db`) inside transaction callbacks to ensure atomicity)**

**(You MUST use `.with()` for relational queries to avoid N+1 problems - fetches all data in single SQL query)**

**(You MUST use `defineRelations()` for RQB v2 - the old `relations()` per-table syntax is deprecated)**

**Failure to follow these rules will cause field name mismatches, break transaction atomicity, create N+1 performance issues, and use deprecated APIs.**

</critical_reminders>

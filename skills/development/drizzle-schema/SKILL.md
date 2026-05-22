---
name: drizzle-schema
description: Database schema patterns using Drizzle ORM with PostgreSQL
disable-model-invocation: true
---

# Drizzle ORM Schema Patterns

## Schema Files

- Main schema: `shared/schema.ts`
- MLOps schema: `shared/mlops-schema.ts`

## Core Tables

### Tenants (Multi-tenant)
All data is scoped to a tenant. Every query must include tenant filtering.

### Users
- Roles: `admin`, `operator`, `viewer`, `platform_admin`
- Linked to tenant via `tenantId`
- Password hashed with bcryptjs

### Sessions
- PostgreSQL-backed session store
- Used with `connect-pg-simple`

## Patterns

### Define a table:
```typescript
import { pgTable, text, serial, integer, timestamp } from "drizzle-orm/pg-core";

export const myTable = pgTable("my_table", {
  id: serial("id").primaryKey(),
  tenantId: integer("tenant_id").notNull().references(() => tenants.id),
  name: text("name").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});
```

### Create Zod schemas:
```typescript
import { createInsertSchema, createSelectSchema } from "drizzle-zod";

export const insertMyTableSchema = createInsertSchema(myTable);
export const selectMyTableSchema = createSelectSchema(myTable);
```

### Query with tenant isolation:
```typescript
import { eq, and } from "drizzle-orm";

const results = await db
  .select()
  .from(myTable)
  .where(and(eq(myTable.tenantId, tenantId), eq(myTable.id, id)));
```

## Configuration

- `drizzle.config.ts` — migration config
- Push schema: `npm run db:push`
- Connection via `DATABASE_URL` env variable

---
name: db-migration
description: Create Drizzle ORM database migrations for the Encore.ts backend. Use when adding or modifying database tables, columns, or indexes.
metadata:
  author: traceway
  version: "1.0.0"
---

# Create Database Migration

Use this skill when the user asks to add/modify database tables, columns, indexes, or any schema changes.

## How it works

Traceway uses **Drizzle ORM** with **PostgreSQL**. Schema is defined in TypeScript, migrations are auto-generated.

## Step 1: Modify the schema

Edit `backend/app/core/schema.ts`. All tables are defined using `drizzle-orm/pg-core`:

```typescript
import * as p from "drizzle-orm/pg-core";

export const myEntities = p.pgTable(
  "my_entities",  // SQL table name (snake_case)
  {
    // Columns
    id: p.uuid().primaryKey(),
    orgId: p.uuid("org_id").notNull()
      .references(() => organizations.id, { onDelete: "cascade" }),
    projectId: p.uuid("project_id").notNull()
      .references(() => projects.id, { onDelete: "cascade" }),
    name: p.text().notNull(),
    description: p.text(),                    // nullable by default
    status: p.text().notNull().default("active"),
    metadata: p.jsonb(),                      // JSON column
    count: p.integer().notNull().default(0),
    isActive: p.boolean("is_active").notNull().default(true),
    createdAt: p.timestamp("created_at", { withTimezone: true }).notNull(),
    updatedAt: p.timestamp("updated_at", { withTimezone: true }).notNull(),
  },
  // Indexes and constraints (third argument)
  (table) => [
    p.index("my_entities_org_project_idx").on(table.orgId, table.projectId),
    p.unique("my_entities_org_slug_unique").on(table.orgId, table.name),
  ]
);
```

### Column naming convention

- TypeScript field: `camelCase` (e.g., `orgId`, `createdAt`)
- SQL column: `snake_case` passed as string (e.g., `"org_id"`, `"created_at"`)
- Drizzle maps between them automatically when you provide the SQL name

### Common column types

| Drizzle type | SQL type | Notes |
|---|---|---|
| `p.uuid()` | `uuid` | Use for IDs, foreign keys |
| `p.text()` | `text` | Strings |
| `p.integer()` | `integer` | Whole numbers |
| `p.boolean()` | `boolean` | True/false |
| `p.timestamp("col", { withTimezone: true })` | `timestamptz` | Always use `withTimezone: true` |
| `p.jsonb()` | `jsonb` | JSON data |
| `p.real()` | `real` | Floating point |

### Foreign key pattern

Always reference parent tables and use `onDelete: "cascade"` for org/project scoping:

```typescript
orgId: p.uuid("org_id").notNull()
  .references(() => organizations.id, { onDelete: "cascade" }),
```

## Step 2: Generate the migration

```bash
cd backend/app && npx drizzle-kit generate
```

This creates a new SQL file in `backend/app/core/migrations/` with an auto-generated name.

## Step 3: Verify

1. Review the generated SQL migration file
2. Run typecheck: `cd backend/app && npm run typecheck`
3. The migration runs automatically when Encore starts (`encore run`)

## Adding columns to existing tables

Just add the new column to the existing table definition in `schema.ts` and regenerate:

```typescript
// Add to existing table
export const existingTable = p.pgTable("existing_table", {
  // ... existing columns ...
  newColumn: p.text("new_column"),  // Add this
});
```

Then: `cd backend/app && npx drizzle-kit generate`

## Key conventions

- Every table with user data needs `orgId` + `projectId` for multi-tenant scoping
- Always include `createdAt` and `updatedAt` timestamps
- Use `uuid` type for all IDs (generated with `crypto.randomUUID()`)
- Foreign keys should cascade on delete from org/project
- Index columns that are frequently queried (especially org_id + project_id)
- Migration files are checked into git — never edit them after they've been applied

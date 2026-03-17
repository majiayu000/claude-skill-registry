---
name: add-table
description: Add a Drizzle database table with migration and seed data for x4-mono
---

# Add Table Skill

Add or modify database tables in the x4-mono Drizzle ORM setup.

## Arguments

The user describes the table or schema change they want. If unclear, ask for:

- Table name (snake_case)
- Columns with types
- Relations to existing tables
- Whether seed data is needed

## Schema Conventions

All tables in `packages/database/src/schema.ts` must follow these patterns:

### Standard Columns (always include)

```typescript
id: uuid("id").primaryKey().defaultRandom(),
createdAt: timestamp("created_at").default(sql`now()`).notNull(),
updatedAt: timestamp("updated_at")
  .default(sql`now()`)
  .notNull()
  .$onUpdate(() => new Date()),
```

### Column Naming

- TypeScript: camelCase (`userId`, `createdAt`)
- SQL: snake_case via explicit names (`uuid("user_id")`, `timestamp("created_at")`)
- Always use explicit SQL column names

### Foreign Keys

```typescript
userId: uuid("user_id")
  .notNull()
  .references(() => users.id, { onDelete: "cascade" }),
```

### Indexes

```typescript
(table) => [index('idx_tablename_column').on(table.column)];
```

### Relations

```typescript
export const tableRelations = relations(tableName, ({ one, many }) => ({
  owner: one(users, { fields: [tableName.ownerId], references: [users.id] }),
  items: many(otherTable),
}));
```

## Workflow

1. **Read current schema**: Read `packages/database/src/schema.ts`
2. **Add table definition**: Add `pgTable()` with standard columns + custom columns
3. **Add relations**: Define relations if foreign keys exist
4. **Add Zod schema**: Create corresponding Zod schemas in `packages/shared/`
5. **Generate migration**: Run `bun db:generate`
6. **Push to dev DB**: Run `bun db:push`
7. **Add seed data**: Update `packages/database/seed.ts` if needed
8. **Type check**: Run `bun turbo type-check` to verify

## Available Column Types

```typescript
import {
  pgTable,
  uuid,
  varchar,
  text,
  timestamp,
  boolean,
  integer,
  numeric,
  pgEnum,
  index,
  jsonb,
  serial,
} from 'drizzle-orm/pg-core';
```

## Important Notes

- Schema `status: text("status")` returns `string` not union type at runtime
- Nullable columns return `string | null` not `string | undefined`
- Output Zod schemas must match DB return types
- Use `db.select().from()` SQL-like API, not `db.query` relational API
- Better Auth expects singular model names (`user` not `users`) — the existing `export const user = users;` alias handles this

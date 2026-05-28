---
name: drizzle-schema-guide
description: Modify Drizzle ORM database schema safely. Use when user mentions "add table", "new column", "database schema", "migration", or "drizzle".
allowed-tools: Read, Grep, Glob
---

# Drizzle Schema Modifications

This project uses Drizzle ORM with Neon Serverless Postgres.

## Project Files

- Schema: `db/schema.ts`
- Config: `drizzle.config.ts`
- Connection: `db/index.ts`

## Current Schema

```typescript
// x_account_cache - Caches X account analysis
export const xAccountCache = pgTable('x_account_cache', {
  id: uuid('id').primaryKey().defaultRandom(),
  xHandle: text('x_handle').unique().notNull(),
  searchResponse: jsonb('search_response').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
  expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
});

// usage_tracking - Tracks premium image quota
export const usageTracking = pgTable('usage_tracking', {
  id: uuid('id').primaryKey().defaultRandom(),
  userIdentifier: text('user_identifier').unique().notNull(),
  premiumImagesCount: integer('premium_images_count').default(0),
  lastResetAt: timestamp('last_reset_at', { withTimezone: true }).defaultNow(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow(),
});
```

## Instructions

1. **Adding a new table**:
```typescript
import { pgTable, uuid, text, timestamp, integer, index } from 'drizzle-orm/pg-core';

export const newTable = pgTable('new_table', {
  id: uuid('id').primaryKey().defaultRandom(),
  // columns here
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
}, (table) => [
  index('idx_name').on(table.column),  // optional indexes
]);

// Type exports
export type NewTable = typeof newTable.$inferSelect;
export type InsertNewTable = typeof newTable.$inferInsert;
```

2. **Update db/index.ts** to export the new table:
```typescript
export { db } from './index';
export { xAccountCache, usageTracking, newTable } from './schema';
```

3. **Apply schema changes**:
   - Development: `npm run db:push` (direct push, no migration files)
   - Production: `npm run db:generate` then `npm run db:migrate`

4. **Inspect database**: `npm run db:studio` opens Drizzle Studio

## Common Column Types

```typescript
uuid('id').primaryKey().defaultRandom()
text('name').notNull()
text('email').unique()
integer('count').default(0)
boolean('active').default(true)
jsonb('data').notNull()
timestamp('created_at', { withTimezone: true }).defaultNow()
```

## Examples

- "Add a feedback table" → Add table definition to `db/schema.ts`, export in `db/index.ts`
- "Add email column to usage" → Modify `usageTracking` in schema

## Guardrails

- READ-ONLY by default - review changes before applying
- Never run `db:push` against production
- Always generate migrations for production changes
- Backup data before destructive migrations
- Confirm with user before running any db commands
- Add NOT NULL columns with defaults to avoid breaking existing rows

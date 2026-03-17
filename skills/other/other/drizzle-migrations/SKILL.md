---
name: drizzle-migrations
description: Manage database schema with Drizzle ORM and SQLite migrations. Use when adding tables, modifying columns, creating indexes, or running migrations. Activates for database schema changes, migration generation, and Drizzle query patterns.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*)
category: Data & Analytics
tags:
  - database
  - drizzle
  - migrations
---

# Drizzle ORM Migrations

This skill helps you manage database schema changes using Drizzle ORM with SQLite.

## When to Use

✅ **USE this skill for:**
- Adding new tables or modifying existing columns
- Generating and running database migrations
- Drizzle-specific query patterns and relations
- SQLite schema best practices with Drizzle
- Setting up Drizzle configuration

❌ **DO NOT use for:**
- Supabase/PostgreSQL → use `supabase-admin` skill
- Raw SQL without Drizzle → use standard SQL resources
- Prisma ORM → different syntax and patterns
- General database design theory → use database architecture resources

## Project Setup

**Configuration**: `drizzle.config.ts`
```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
  dbCredentials: {
    url: './data/app.db',
  },
});
```

**Commands**:
```bash
npm run db:generate  # Generate migration files
npm run db:push      # Push schema directly (dev only)
npm run db:studio    # Open Drizzle Studio GUI
```

## Schema Definition

Location: `src/db/schema.ts`

### Table Definition

```typescript
import { sqliteTable, text, integer, real, blob } from 'drizzle-orm/sqlite-core';
import { relations } from 'drizzle-orm';

// Basic table
export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  username: text('username').notNull(),
  passwordHash: text('password_hash'),
  createdAt: text('created_at').notNull().default(sql`CURRENT_TIMESTAMP`),
  updatedAt: text('updated_at'),
});

// Table with foreign key
export const checkIns = sqliteTable('check_ins', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id, {
    onDelete: 'cascade',
  }),
  mood: integer('mood').notNull(),
  cravingLevel: integer('craving_level').notNull(),
  sleepHours: real('sleep_hours'),
  notes: text('notes'),
  createdAt: text('created_at').notNull().default(sql`CURRENT_TIMESTAMP`),
});

// Table with composite index
export const auditLog = sqliteTable('audit_log', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull(),
  action: text('action').notNull(),
  targetType: text('target_type'),
  targetId: text('target_id'),
  details: text('details'),  // JSON string
  createdAt: text('created_at').notNull().default(sql`CURRENT_TIMESTAMP`),
}, (table) => ({
  userActionIdx: index('idx_audit_user_action').on(table.userId, table.action),
  createdAtIdx: index('idx_audit_created').on(table.createdAt),
}));
```

### Relations

```typescript
export const usersRelations = relations(users, ({ many }) => ({
  checkIns: many(checkIns),
  sessions: many(sessions),
  journalEntries: many(journalEntries),
}));

export const checkInsRelations = relations(checkIns, ({ one }) => ({
  user: one(users, {
    fields: [checkIns.userId],
    references: [users.id],
  }),
}));
```

## Column Types

### SQLite Types in Drizzle

```typescript
import {
  sqliteTable,
  text,           // TEXT - strings, JSON, dates
  integer,        // INTEGER - numbers, booleans (0/1)
  real,           // REAL - floating point
  blob,           // BLOB - binary data
} from 'drizzle-orm/sqlite-core';

const examples = sqliteTable('examples', {
  // Strings
  name: text('name').notNull(),
  description: text('description'),

  // Numbers
  count: integer('count').notNull().default(0),
  rating: real('rating'),

  // Booleans (stored as 0/1)
  isActive: integer('is_active', { mode: 'boolean' }).default(true),

  // Dates (stored as ISO strings)
  createdAt: text('created_at').notNull().default(sql`CURRENT_TIMESTAMP`),
  expiresAt: text('expires_at'),

  // JSON (stored as TEXT)
  metadata: text('metadata', { mode: 'json' }),

  // Enums (stored as TEXT)
  status: text('status', { enum: ['pending', 'active', 'archived'] }),
});
```

## Migration Strategies

### Strategy 1: Push (Development Only)

```bash
npm run db:push
```

- Directly applies schema changes
- Fast for development
- **Never use in production**

### Strategy 2: Generate & Migrate (Production)

```bash
# 1. Generate migration file
npm run db:generate

# 2. Review generated SQL in /drizzle folder

# 3. Apply migration (in code or manually)
```

### Applying Migrations in Code

```typescript
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { migrate } from 'drizzle-orm/better-sqlite3/migrator';
import Database from 'better-sqlite3';

const sqlite = new Database('./data/app.db');
const db = drizzle(sqlite);

// Run migrations
migrate(db, { migrationsFolder: './drizzle' });
```

## Common Schema Changes

### Adding a New Table

```typescript
// 1. Add to schema.ts
export const newFeature = sqliteTable('new_feature', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id),
  name: text('name').notNull(),
  createdAt: text('created_at').notNull().default(sql`CURRENT_TIMESTAMP`),
});

// 2. Add relations
export const newFeatureRelations = relations(newFeature, ({ one }) => ({
  user: one(users, {
    fields: [newFeature.userId],
    references: [users.id],
  }),
}));

// 3. Generate migration
// npm run db:generate
```

### Adding a Column

```typescript
// In schema.ts, add the new column
export const users = sqliteTable('users', {
  // existing columns...
  newColumn: text('new_column'),  // Add this
});

// Generate migration
// npm run db:generate
```

### Adding an Index

```typescript
export const messages = sqliteTable('messages', {
  id: text('id').primaryKey(),
  conversationId: text('conversation_id').notNull(),
  createdAt: text('created_at').notNull(),
}, (table) => ({
  // Add index
  convCreatedIdx: index('idx_messages_conv_created')
    .on(table.conversationId, table.createdAt),
}));
```

### Renaming (Requires Manual SQL)

SQLite doesn't support direct column renames in older versions. For complex changes:

```sql
-- drizzle/XXXX_rename_column.sql
-- Manual migration for column rename

-- 1. Create new table with desired schema
CREATE TABLE users_new (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,  -- renamed from username
  created_at TEXT NOT NULL
);

-- 2. Copy data
INSERT INTO users_new SELECT id, email, username, created_at FROM users;

-- 3. Drop old table
DROP TABLE users;

-- 4. Rename new table
ALTER TABLE users_new RENAME TO users;
```

## Query Patterns

### Basic Queries

```typescript
import { db } from '@/db';
import { eq, and, or, desc, asc, like, gte, lte } from 'drizzle-orm';
import { users, checkIns } from '@/db/schema';

// Select all
const allUsers = await db.select().from(users);

// Select with conditions
const activeUsers = await db
  .select()
  .from(users)
  .where(eq(users.isActive, true));

// Select specific columns
const userEmails = await db
  .select({ id: users.id, email: users.email })
  .from(users);

// Complex where clause
const results = await db
  .select()
  .from(checkIns)
  .where(
    and(
      eq(checkIns.userId, userId),
      gte(checkIns.createdAt, startDate),
      lte(checkIns.createdAt, endDate)
    )
  )
  .orderBy(desc(checkIns.createdAt))
  .limit(30);
```

### Insert

```typescript
// Single insert
const [newUser] = await db
  .insert(users)
  .values({
    id: generateId(),
    email: 'user@example.com',
    username: 'newuser',
  })
  .returning();

// Bulk insert
await db.insert(checkIns).values([
  { id: '1', userId, mood: 7, cravingLevel: 2 },
  { id: '2', userId, mood: 8, cravingLevel: 1 },
]);

// Upsert (insert or update)
await db
  .insert(users)
  .values({ id: 'user-1', email: 'new@example.com' })
  .onConflictDoUpdate({
    target: users.id,
    set: { email: 'new@example.com' },
  });
```

### Update

```typescript
await db
  .update(users)
  .set({ username: 'newname', updatedAt: new Date().toISOString() })
  .where(eq(users.id, userId));
```

### Delete

```typescript
// Always use WHERE clause!
await db
  .delete(checkIns)
  .where(eq(checkIns.id, checkInId));

// Delete with multiple conditions
await db
  .delete(sessions)
  .where(
    and(
      eq(sessions.userId, userId),
      lte(sessions.expiresAt, new Date().toISOString())
    )
  );
```

### Joins

```typescript
const userWithCheckIns = await db
  .select({
    user: users,
    checkIn: checkIns,
  })
  .from(users)
  .leftJoin(checkIns, eq(users.id, checkIns.userId))
  .where(eq(users.id, userId));
```

### Aggregations

```typescript
import { count, avg, sum, max, min } from 'drizzle-orm';

const stats = await db
  .select({
    totalCheckIns: count(),
    avgMood: avg(checkIns.mood),
    maxStreak: max(checkIns.streak),
  })
  .from(checkIns)
  .where(eq(checkIns.userId, userId));
```

## Best Practices

1. **Always use transactions for related changes**
```typescript
await db.transaction(async (tx) => {
  await tx.insert(users).values(userData);
  await tx.insert(profiles).values(profileData);
});
```

2. **Always include WHERE on DELETE/UPDATE**
3. **Use indexes for frequently queried columns**
4. **Store dates as ISO strings for SQLite**
5. **Use `returning()` to get inserted/updated rows**
6. **Generate migrations, don't push to production**

## References

- [Drizzle ORM Docs](https://orm.drizzle.team/docs/overview)
- [Drizzle SQLite](https://orm.drizzle.team/docs/get-started-sqlite)
- [Drizzle Migrations](https://orm.drizzle.team/docs/migrations)

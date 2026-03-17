---
name: drizzle-patterns
description: Drizzle ORM best practices including schema design with relationships, database migrations, prepared statements for performance, transactions, indexes, Turso SQLite database operations, type safety patterns, query optimization, and database workflow for ree-board project
model: sonnet
---

# Drizzle ORM Patterns

## When to Use This Skill

Activate this skill when working on:

- Designing or modifying database schema
- Creating database migrations
- Writing database queries
- Optimizing query performance
- Managing Turso database operations
- Implementing transactions
- Adding indexes
- Schema type safety and validation

## Core Patterns

### Schema Definition with Relationships

**Primary Keys:** All tables use Nano IDs for primary keys

**Schema Pattern:**

```typescript
// db/schema.ts
import { sqliteTable, text, integer, index } from "drizzle-orm/sqlite-core";
import { relations } from "drizzle-orm";
import { nanoid } from "nanoid";

export const boardTable = sqliteTable(
  "board",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => nanoid()),
    name: text("name").notNull(),
    userId: text("user_id").notNull(),
    createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
      () => new Date()
    ),
  },
  (table) => ({
    userIdIndex: index("board_user_id_index").on(table.userId),
  })
);

export const postTable = sqliteTable(
  "post",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => nanoid()),
    boardId: text("board_id")
      .notNull()
      .references(() => boardTable.id, { onDelete: "cascade" }),
    userId: text("user_id").notNull(),
    content: text("content").notNull(),
    type: text("type", {
      enum: ["went_well", "to_improve", "action_items"],
    }).notNull(),
    voteCount: integer("vote_count").default(0),
  },
  (table) => ({
    boardIdIndex: index("post_board_id_index").on(table.boardId),
    userIdIndex: index("post_user_id_index").on(table.userId),
  })
);

// Define relationships
export const boardRelations = relations(boardTable, ({ many }) => ({
  posts: many(postTable),
  members: many(memberTable),
}));

export const postRelations = relations(postTable, ({ one, many }) => ({
  board: one(boardTable, {
    fields: [postTable.boardId],
    references: [boardTable.id],
  }),
  votes: many(voteTable),
}));
```

### Migration Workflow

**Step-by-Step Process:**

1. **Modify Schema** (`db/schema.ts`)
2. **Generate Migration:**

   ```bash
   pnpm generate
   ```

3. **Review Generated SQL** (in `drizzle/` folder)
4. **Apply to Development:**

   ```bash
   pnpm push:dev
   ```

5. **Test Thoroughly**
6. **Apply to Production:**

   ```bash
   pnpm push
   ```

**Example Migration:**

```typescript
// After adding a new column to schema.ts:
export const boardTable = sqliteTable("board", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"), // ✅ New field
  // ...
});
```

### Prepared Statements for Performance

**Critical:** Use prepared statements for repeated queries

**Pattern:**

```typescript
// lib/db/post.ts
import { db } from "@/db";
import { postTable } from "@/db/schema";
import { eq, sql } from "drizzle-orm";

// ✅ Prepared statement for repeated queries
export const prepareFetchPostsByBoardID = db
  .select()
  .from(postTable)
  .where(eq(postTable.boardId, sql.placeholder("boardId")))
  .prepare();

// Usage
export async function getPostsByBoardId(boardId: string) {
  return prepareFetchPostsByBoardID.execute({ boardId });
}
```

**When to Use Prepared Statements:**

- Queries executed multiple times with different parameters
- High-frequency operations (fetching posts, votes)
- Performance-critical paths

### Transaction Patterns

**Use for Multi-Table Operations:**

```typescript
import { db } from "@/db";

export async function createBoardWithMember(name: string, userId: string) {
  return db.transaction(async (tx) => {
    // Create board
    const [board] = await tx
      .insert(boardTable)
      .values({
        id: nanoid(),
        name,
        userId,
      })
      .returning();

    // Add owner as member
    await tx.insert(memberTable).values({
      id: nanoid(),
      boardId: board.id,
      userId,
      role: "owner",
    });

    return board;
  });
}
```

**Transaction Best Practices:**

- Keep transactions small and fast
- Handle errors appropriately
- Use for data consistency requirements
- Avoid long-running operations in transactions

### Index Strategy

**Index All Foreign Keys and Frequently Queried Columns:**

```typescript
export const postTable = sqliteTable(
  "post",
  {
    id: text("id").primaryKey(),
    boardId: text("board_id").notNull(),
    userId: text("user_id").notNull(),
    type: text("type"),
  },
  (table) => ({
    // ✅ Index foreign keys
    boardIdIndex: index("post_board_id_index").on(table.boardId),
    userIdIndex: index("post_user_id_index").on(table.userId),
    // ✅ Index frequently filtered columns
    typeIndex: index("post_type_index").on(table.type),
  })
);
```

**Indexing Guidelines:**

- Always index foreign keys
- Index columns used in WHERE clauses
- Index columns used in JOIN conditions
- Monitor query performance to identify missing indexes

### Query Optimization

**Efficient Queries:**

```typescript
import { db } from "@/db";
import { postTable, voteTable } from "@/db/schema";
import { eq, and, count, inArray, sql } from "drizzle-orm";

// ✅ Select only needed columns
export async function getBoardPostSummary(boardId: string) {
  return db
    .select({
      id: postTable.id,
      content: postTable.content,
      voteCount: postTable.voteCount,
    })
    .from(postTable)
    .where(eq(postTable.boardId, boardId));
}

// ✅ Use aggregations efficiently
export async function getVoteCountForPost(postId: string) {
  const [result] = await db
    .select({ count: count() })
    .from(voteTable)
    .where(eq(voteTable.postId, postId));

  return result.count;
}

// ✅ Batch operations
export async function updatePostVotes(postIds: string[]) {
  return db
    .update(postTable)
    .set({ voteCount: sql`vote_count + 1` })
    .where(inArray(postTable.id, postIds));
}
```

## Anti-Patterns

### ❌ Not Using Prepared Statements for Repeated Queries

**Bad:**

```typescript
export async function getPostsByBoardId(boardId: string) {
  // ❌ Query parsed every time
  return db.select().from(postTable).where(eq(postTable.boardId, boardId));
}
```

**Good:**

```typescript
const preparedQuery = db
  .select()
  .from(postTable)
  .where(eq(postTable.boardId, sql.placeholder("boardId")))
  .prepare();

export async function getPostsByBoardId(boardId: string) {
  // ✅ Prepared statement reused
  return preparedQuery.execute({ boardId });
}
```

### ❌ Missing Indexes on Foreign Keys

**Bad:**

```typescript
export const postTable = sqliteTable("post", {
  id: text("id").primaryKey(),
  boardId: text("board_id").notNull(),
  // ❌ No index on foreign key
});
```

**Good:**

```typescript
export const postTable = sqliteTable(
  "post",
  {
    id: text("id").primaryKey(),
    boardId: text("board_id").notNull(),
  },
  (table) => ({
    // ✅ Index on foreign key
    boardIdIndex: index("post_board_id_index").on(table.boardId),
  })
);
```

### ❌ Not Using Transactions for Multi-Table Operations

**Bad:**

```typescript
// ❌ Two separate operations - potential inconsistency
await db.insert(boardTable).values(board);
await db.insert(memberTable).values(member); // Could fail leaving orphaned board
```

**Good:**

```typescript
// ✅ Transaction ensures atomicity
await db.transaction(async (tx) => {
  await tx.insert(boardTable).values(board);
  await tx.insert(memberTable).values(member);
});
```

### ❌ Selecting All Columns When Only Few Needed

**Bad:**

```typescript
// ❌ Fetches all columns
const posts = await db
  .select()
  .from(postTable)
  .where(eq(postTable.boardId, boardId));
```

**Good:**

```typescript
// ✅ Select only needed columns
const posts = await db
  .select({
    id: postTable.id,
    content: postTable.content,
  })
  .from(postTable)
  .where(eq(postTable.boardId, boardId));
```

### ❌ Modifying Schema Without Migration

**Bad:**

```typescript
// ❌ Directly modifying schema and pushing without generating migration
// Changes schema.ts
// Runs: pnpm push
```

**Good:**

```typescript
// ✅ Proper migration workflow
// 1. Modify schema.ts
// 2. Run: pnpm generate
// 3. Review generated SQL
// 4. Run: pnpm push:dev (test)
// 5. Run: pnpm push (production)
```

## Integration with Other Skills

- **[nextjs-app-router](../nextjs-app-router/SKILL.md):** Data fetching in server components and actions
- **[rbac-security](../rbac-security/SKILL.md):** Database operations require authentication
- **[testing-patterns](../testing-patterns/SKILL.md):** Test database operations and queries
- **[signal-state-management](../signal-state-management/SKILL.md):** Sync database state with signals

## Project-Specific Context

### Key Files

- `db/schema.ts` - Complete database schema with all tables and relationships
- `db/index.ts` - Database connection configuration
- `lib/db/` - Prepared statements and query utilities by entity
- `drizzle.config.ts` - Drizzle configuration for migrations
- `drizzle/` - Generated migration files

### Database Configuration

**Development:**

```typescript
// Uses local SQLite file
DATABASE_URL=file:test.db
```

**Production:**

```env
# Uses Turso Cloud
TURSO_DATABASE_URL=<TURSO_DATABASE_URL>
TURSO_AUTH_TOKEN=<TURSO_AUTH_TOKEN>
```

### Project Conventions

1. **Nano IDs** for all primary keys
2. **Foreign key indexes** on all relationships
3. **Prepared statements** for repeated queries
4. **Transactions** for multi-table operations
5. **Cascade deletes** where appropriate (posts delete with board)
6. **Vote count optimization** denormalized in post table

### Common Queries

**Fetch Board with Posts:**

```typescript
const board = await db.query.boardTable.findFirst({
  where: eq(boardTable.id, boardId),
  with: {
    posts: true,
    members: true,
  },
});
```

**Update Vote Count:**

```typescript
await db
  .update(postTable)
  .set({ voteCount: sql`vote_count + 1` })
  .where(eq(postTable.id, postId));
```

---

**Last Updated:** 2026-01-10

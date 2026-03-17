---
name: drizzle-orm
description: Drizzle ORM for TypeScript - type-safe SQL queries, schema definitions, migrations, and relations. Use when building database layers in Next.js or Node.js applications.
---

# Drizzle ORM Skill

Type-safe SQL ORM for TypeScript with excellent DX and performance.

## Quick Start

### Installation

```bash
# npm
npm install drizzle-orm
npm install -D drizzle-kit

# pnpm
pnpm add drizzle-orm
pnpm add -D drizzle-kit

# yarn
yarn add drizzle-orm
yarn add -D drizzle-kit

# bun
bun add drizzle-orm
bun add -D drizzle-kit
```

### Database Drivers

```bash
# PostgreSQL (Neon)
npm install @neondatabase/serverless

# PostgreSQL (node-postgres)
npm install pg

# PostgreSQL (postgres.js)
npm install postgres

# MySQL
npm install mysql2

# SQLite
npm install better-sqlite3
```

## Project Structure

```
src/
├── db/
│   ├── index.ts          # DB connection
│   ├── schema.ts         # All schemas
│   └── migrations/       # Generated migrations
├── drizzle.config.ts     # Drizzle Kit config
└── .env
```

## Key Concepts

| Concept | Guide |
|---------|-------|
| **Schema Definition** | [reference/schema.md](reference/schema.md) |
| **Queries** | [reference/queries.md](reference/queries.md) |
| **Relations** | [reference/relations.md](reference/relations.md) |
| **Migrations** | [reference/migrations.md](reference/migrations.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **CRUD Operations** | [examples/crud.md](examples/crud.md) |
| **Complex Queries** | [examples/complex-queries.md](examples/complex-queries.md) |
| **Transactions** | [examples/transactions.md](examples/transactions.md) |
| **With Better Auth** | [examples/better-auth.md](examples/better-auth.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/schema.ts](templates/schema.ts) | Schema template |
| [templates/db.ts](templates/db.ts) | Database connection |
| [templates/drizzle.config.ts](templates/drizzle.config.ts) | Drizzle Kit config |

## Database Connection

### Neon (Serverless)

```typescript
// src/db/index.ts
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### Neon (With Connection Pooling)

```typescript
import { Pool } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-serverless";
import * as schema from "./schema";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

### Node Postgres

```typescript
import { Pool } from "pg";
import { drizzle } from "drizzle-orm/node-postgres";
import * as schema from "./schema";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

## Schema Definition

```typescript
// src/db/schema.ts
import {
  pgTable,
  serial,
  text,
  boolean,
  timestamp,
  integer,
  varchar,
  index,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Users table
export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  name: text("name"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Tasks table
export const tasks = pgTable(
  "tasks",
  {
    id: serial("id").primaryKey(),
    title: varchar("title", { length: 200 }).notNull(),
    description: text("description"),
    completed: boolean("completed").default(false).notNull(),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
  },
  (table) => ({
    userIdIdx: index("tasks_user_id_idx").on(table.userId),
  })
);

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  tasks: many(tasks),
}));

export const tasksRelations = relations(tasks, ({ one }) => ({
  user: one(users, {
    fields: [tasks.userId],
    references: [users.id],
  }),
}));

// Types
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Task = typeof tasks.$inferSelect;
export type NewTask = typeof tasks.$inferInsert;
```

## Drizzle Kit Config

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./src/db/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

## Migrations

```bash
# Generate migration
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema directly (development)
npx drizzle-kit push

# Open Drizzle Studio
npx drizzle-kit studio
```

## CRUD Operations

### Create

```typescript
import { db } from "@/db";
import { tasks } from "@/db/schema";

// Insert one
const task = await db
  .insert(tasks)
  .values({
    title: "New task",
    userId: user.id,
  })
  .returning();

// Insert many
const newTasks = await db
  .insert(tasks)
  .values([
    { title: "Task 1", userId: user.id },
    { title: "Task 2", userId: user.id },
  ])
  .returning();
```

### Read

```typescript
import { eq, and, desc } from "drizzle-orm";

// Get all tasks for user
const userTasks = await db
  .select()
  .from(tasks)
  .where(eq(tasks.userId, user.id))
  .orderBy(desc(tasks.createdAt));

// Get single task
const task = await db
  .select()
  .from(tasks)
  .where(and(eq(tasks.id, taskId), eq(tasks.userId, user.id)))
  .limit(1);

// With relations
const tasksWithUser = await db.query.tasks.findMany({
  where: eq(tasks.userId, user.id),
  with: {
    user: true,
  },
});
```

### Update

```typescript
const updated = await db
  .update(tasks)
  .set({
    completed: true,
    updatedAt: new Date(),
  })
  .where(and(eq(tasks.id, taskId), eq(tasks.userId, user.id)))
  .returning();
```

### Delete

```typescript
await db
  .delete(tasks)
  .where(and(eq(tasks.id, taskId), eq(tasks.userId, user.id)));
```

## Query Helpers

```typescript
import { eq, ne, gt, lt, gte, lte, like, ilike, and, or, not, isNull, isNotNull, inArray, between, sql } from "drizzle-orm";

// Comparison
eq(tasks.id, 1)              // =
ne(tasks.id, 1)              // !=
gt(tasks.id, 1)              // >
gte(tasks.id, 1)             // >=
lt(tasks.id, 1)              // <
lte(tasks.id, 1)             // <=

// String
like(tasks.title, "%test%")   // LIKE
ilike(tasks.title, "%test%")  // ILIKE (case-insensitive)

// Logical
and(eq(tasks.userId, id), eq(tasks.completed, false))
or(eq(tasks.status, "pending"), eq(tasks.status, "active"))
not(eq(tasks.completed, true))

// Null checks
isNull(tasks.description)
isNotNull(tasks.description)

// Arrays
inArray(tasks.status, ["pending", "active"])

// Range
between(tasks.createdAt, startDate, endDate)

// Raw SQL
sql`${tasks.title} || ' - ' || ${tasks.description}`
```

## Transactions

```typescript
await db.transaction(async (tx) => {
  const [task] = await tx
    .insert(tasks)
    .values({ title: "New task", userId: user.id })
    .returning();

  await tx.insert(taskHistory).values({
    taskId: task.id,
    action: "created",
  });
});
```

## Server Actions (Next.js)

```typescript
// app/actions/tasks.ts
"use server";

import { db } from "@/db";
import { tasks } from "@/db/schema";
import { eq, and } from "drizzle-orm";
import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";

export async function createTask(formData: FormData) {
  const session = await auth();
  if (!session?.user) throw new Error("Unauthorized");

  const title = formData.get("title") as string;

  await db.insert(tasks).values({
    title,
    userId: session.user.id,
  });

  revalidatePath("/tasks");
}

export async function toggleTask(taskId: number) {
  const session = await auth();
  if (!session?.user) throw new Error("Unauthorized");

  const [task] = await db
    .select()
    .from(tasks)
    .where(and(eq(tasks.id, taskId), eq(tasks.userId, session.user.id)));

  if (!task) throw new Error("Task not found");

  await db
    .update(tasks)
    .set({ completed: !task.completed })
    .where(eq(tasks.id, taskId));

  revalidatePath("/tasks");
}
```

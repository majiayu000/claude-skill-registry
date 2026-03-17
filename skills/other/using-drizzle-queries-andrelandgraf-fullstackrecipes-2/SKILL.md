---
name: using-drizzle-queries
description: Write type-safe database queries with Drizzle ORM. Covers select, insert, update, delete, relational queries, and adding new tables.
---

# Working with Drizzle

Write type-safe database queries with Drizzle ORM. Covers select, insert, update, delete, relational queries, and adding new tables.

## Implement Working with Drizzle

Write type-safe database queries with Drizzle ORM. Covers select, insert, update, delete, relational queries, and adding new tables.

**See:**

- Resource: `using-drizzle-queries` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-drizzle-queries

---

### Writing Queries

Use Drizzle's query API for type-safe database operations:

```typescript
import { db } from "@/lib/db/client";
import { chats } from "@/lib/chat/schema";
import { eq, desc } from "drizzle-orm";

// Select all
const allChats = await db.select().from(chats);

// Select with filter
const userChats = await db
  .select()
  .from(chats)
  .where(eq(chats.userId, userId))
  .orderBy(desc(chats.createdAt));

// Select single record
const chat = await db
  .select()
  .from(chats)
  .where(eq(chats.id, chatId))
  .limit(1)
  .then((rows) => rows[0]);
```

### Inserting Data

```typescript
import { db } from "@/lib/db/client";
import { chats } from "@/lib/chat/schema";

// Insert single record
const [newChat] = await db
  .insert(chats)
  .values({
    userId,
    title: "New Chat",
  })
  .returning();

// Insert multiple records
await db.insert(messages).values([
  { chatId, role: "user", content: "Hello" },
  { chatId, role: "assistant", content: "Hi there!" },
]);
```

### Updating Data

```typescript
import { db } from "@/lib/db/client";
import { chats } from "@/lib/chat/schema";
import { eq } from "drizzle-orm";

await db
  .update(chats)
  .set({ title: "Updated Title" })
  .where(eq(chats.id, chatId));
```

### Deleting Data

```typescript
import { db } from "@/lib/db/client";
import { chats } from "@/lib/chat/schema";
import { eq } from "drizzle-orm";

await db.delete(chats).where(eq(chats.id, chatId));
```

### Using Relational Queries

For queries with relations, use the query API:

```typescript
import { db } from "@/lib/db/client";

const chatWithMessages = await db.query.chats.findFirst({
  where: eq(chats.id, chatId),
  with: {
    messages: {
      orderBy: (messages, { asc }) => [asc(messages.createdAt)],
    },
  },
});
```

### Adding New Tables

1. Create the schema in the feature's library folder:

```typescript
// src/lib/feature/schema.ts
import { pgTable, text, uuid, timestamp } from "drizzle-orm/pg-core";

export const items = pgTable("items", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

1. Import the schema in `src/lib/db/client.ts`:

```typescript
import * as itemSchema from "@/lib/feature/schema";

const schema = {
  ...authSchema,
  ...chatSchema,
  ...itemSchema,
};
```

1. Generate and run migrations:

```bash
bun run db:generate
bun run db:migrate
```

---

## References

- [Drizzle ORM Select](https://orm.drizzle.team/docs/select)
- [Drizzle ORM Insert](https://orm.drizzle.team/docs/insert)
- [Drizzle ORM Relational Queries](https://orm.drizzle.team/docs/rqb)

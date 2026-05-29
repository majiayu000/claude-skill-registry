---
name: bknd-seed-data
description: Use when populating a Bknd database with initial or test data. Covers the seed function in options, ctx.em.mutator() for insertOne/insertMany, conditional seeding, environment-based data, and common patterns for dev/test fixtures.
---

# Seed Data

Populate your Bknd database with initial, test, or development data using the built-in seed function.

## Prerequisites

- Bknd project initialized
- At least one entity defined
- Code-first configuration (seed is code-only)

## When to Use

- Populating initial data on first startup
- Creating test fixtures for development
- Setting up demo data for presentations
- Bootstrapping admin users or default records

**Note:** Seed function is code-only—no UI equivalent. For one-off data entry, use the admin panel Data section directly.

## Code Approach

### Step 1: Add Seed Function to Options

The seed function lives in the `options` section of your config:

```typescript
import { type BunBkndConfig, serve } from "bknd/adapter/bun";
import { em, entity, text, boolean } from "bknd";

const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean({ default_value: false }),
  }),
});

const config: BunBkndConfig = {
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
  },
  options: {
    seed: async (ctx) => {
      // Seed logic here
    },
  },
};

serve(config);
```

### Step 2: Insert Data with ctx.em.mutator()

Use `ctx.em.mutator(entity)` for server-side inserts:

```typescript
options: {
  seed: async (ctx) => {
    // Insert single record
    await ctx.em.mutator("todos").insertOne({
      title: "Welcome task",
      done: false,
    });

    // Insert multiple records
    await ctx.em.mutator("todos").insertMany([
      { title: "Learn Bknd basics", done: false },
      { title: "Create first entity", done: true },
      { title: "Set up authentication", done: false },
    ]);
  },
}
```

### Step 3: Seed Related Entities

Insert parent records first, then children:

```typescript
options: {
  seed: async (ctx) => {
    // Create users first
    const users = await ctx.em.mutator("users").insertMany([
      { email: "admin@example.com", name: "Admin" },
      { email: "user@example.com", name: "User" },
    ]);

    // Create posts referencing users
    await ctx.em.mutator("posts").insertMany([
      { title: "First Post", author_id: users[0].id },
      { title: "Second Post", author_id: users[1].id },
    ]);
  },
}
```

### Step 4: Conditional Seeding

Check if data exists before seeding to avoid duplicates:

```typescript
options: {
  seed: async (ctx) => {
    // Check if already seeded
    const existing = await ctx.em.repo("users").findOne({
      where: { email: { $eq: "admin@example.com" } },
    });

    if (existing) {
      console.log("Database already seeded");
      return;
    }

    // Seed data
    await ctx.em.mutator("users").insertOne({
      email: "admin@example.com",
      name: "Admin",
    });
  },
}
```

## Full Example

```typescript
import { type BunBkndConfig, serve } from "bknd/adapter/bun";
import { em, entity, text, boolean, number, date } from "bknd";

const schema = em({
  users: entity("users", {
    email: text().required().unique(),
    name: text(),
    role: text({ default_value: "user" }),
  }),
  posts: entity("posts", {
    title: text().required(),
    content: text(),
    published: boolean({ default_value: false }),
    view_count: number({ default_value: 0 }),
    created_at: date({ default_value: "now" }),
  }),
  tags: entity("tags", {
    name: text().required().unique(),
  }),
});

type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}

const config: BunBkndConfig = {
  connection: { url: "file:data.db" },
  config: {
    data: schema.toJSON(),
  },
  options: {
    seed: async (ctx) => {
      // Check if already seeded
      const count = await ctx.em.repo("users").count();
      if (count > 0) {
        console.log("Skipping seed: data exists");
        return;
      }

      console.log("Seeding database...");

      // Seed users
      const [admin, author] = await ctx.em.mutator("users").insertMany([
        { email: "admin@example.com", name: "Admin", role: "admin" },
        { email: "author@example.com", name: "Author", role: "author" },
      ]);

      // Seed tags
      const tags = await ctx.em.mutator("tags").insertMany([
        { name: "javascript" },
        { name: "typescript" },
        { name: "bknd" },
      ]);

      // Seed posts
      await ctx.em.mutator("posts").insertMany([
        {
          title: "Getting Started with Bknd",
          content: "Learn the basics...",
          published: true,
          author_id: author.id,
        },
        {
          title: "Advanced Patterns",
          content: "Deep dive into...",
          published: false,
          author_id: admin.id,
        },
      ]);

      console.log("Seed complete!");
    },
  },
};

serve(config);
```

## React/Browser Adapter

For browser-based apps using `BkndBrowserApp`:

```tsx
import { BkndBrowserApp } from "bknd/adapter/browser";

function App() {
  return (
    <BkndBrowserApp
      config={{
        data: schema.toJSON(),
      }}
      options={{
        seed: async (ctx) => {
          await ctx.em.mutator("todos").insertMany([
            { title: "Sample task 1", done: false },
            { title: "Sample task 2", done: true },
          ]);
        },
      }}
    >
      <YourApp />
    </BkndBrowserApp>
  );
}
```

## Environment-Based Seeding

Different data for dev vs production:

```typescript
options: {
  seed: async (ctx) => {
    const isDev = process.env.NODE_ENV !== "production";

    // Always seed admin
    await ctx.em.mutator("users").insertOne({
      email: "admin@example.com",
      name: "Admin",
      role: "admin",
    });

    // Dev-only test data
    if (isDev) {
      await ctx.em.mutator("users").insertMany([
        { email: "test1@example.com", name: "Test User 1" },
        { email: "test2@example.com", name: "Test User 2" },
      ]);

      // Generate bulk test data
      const testPosts = Array.from({ length: 50 }, (_, i) => ({
        title: `Test Post ${i + 1}`,
        content: `Content for test post ${i + 1}`,
        published: i % 2 === 0,
      }));

      await ctx.em.mutator("posts").insertMany(testPosts);
    }
  },
}
```

## Seed Execution Behavior

| Scenario | Seed Runs? |
|----------|------------|
| First startup (empty DB) | Yes |
| Subsequent startups | Yes (every time) |
| After schema sync | Yes |
| Production deployment | Yes (use guards!) |

**Important:** The seed function runs on every startup. Always add existence checks to prevent duplicate data.

## Mutator Methods Reference

| Method | Description | Example |
|--------|-------------|---------|
| `insertOne(data)` | Insert single record | `mutator("users").insertOne({ email: "..." })` |
| `insertMany(data[])` | Insert multiple records | `mutator("users").insertMany([...])` |

## Common Patterns

### Idempotent Seeding

```typescript
async function seedIfNotExists(ctx, entity: string, where: object, data: object) {
  const existing = await ctx.em.repo(entity).findOne({ where });
  if (!existing) {
    return ctx.em.mutator(entity).insertOne(data);
  }
  return existing;
}

// Usage
options: {
  seed: async (ctx) => {
    await seedIfNotExists(ctx, "users",
      { email: { $eq: "admin@example.com" } },
      { email: "admin@example.com", name: "Admin", role: "admin" }
    );
  },
}
```

### Factory Functions

```typescript
function createTestUser(overrides = {}) {
  return {
    email: `user${Date.now()}@test.com`,
    name: "Test User",
    role: "user",
    ...overrides,
  };
}

function createTestPost(authorId: number, overrides = {}) {
  return {
    title: "Test Post",
    content: "Lorem ipsum...",
    published: false,
    author_id: authorId,
    ...overrides,
  };
}

// Usage
options: {
  seed: async (ctx) => {
    const user = await ctx.em.mutator("users").insertOne(
      createTestUser({ role: "admin" })
    );

    await ctx.em.mutator("posts").insertMany([
      createTestPost(user.id, { title: "Post 1", published: true }),
      createTestPost(user.id, { title: "Post 2" }),
    ]);
  },
}
```

### Seeding with Faker Data

```typescript
import { faker } from "@faker-js/faker";

options: {
  seed: async (ctx) => {
    const users = Array.from({ length: 10 }, () => ({
      email: faker.internet.email(),
      name: faker.person.fullName(),
      role: faker.helpers.arrayElement(["user", "author", "admin"]),
    }));

    await ctx.em.mutator("users").insertMany(users);
  },
}
```

## Common Pitfalls

### Duplicate Data on Restart

**Problem:** Seed runs every startup, creating duplicates.

**Fix:** Check for existing data:

```typescript
seed: async (ctx) => {
  const count = await ctx.em.repo("users").count();
  if (count > 0) return; // Already seeded

  // Seed logic...
}
```

### Foreign Key Order

**Problem:** `Foreign key constraint failed` error.

**Fix:** Insert parent records before children:

```typescript
// ❌ Wrong order
await ctx.em.mutator("posts").insertOne({ author_id: 1, ... }); // User doesn't exist!
await ctx.em.mutator("users").insertOne({ id: 1, ... });

// ✅ Correct order
const user = await ctx.em.mutator("users").insertOne({ ... });
await ctx.em.mutator("posts").insertOne({ author_id: user.id, ... });
```

### Missing Required Fields

**Problem:** `NOT NULL constraint failed` error.

**Fix:** Include all required fields:

```typescript
// ❌ Missing required field
await ctx.em.mutator("users").insertOne({ name: "Admin" });
// Error: email is required

// ✅ Include all required fields
await ctx.em.mutator("users").insertOne({
  email: "admin@example.com",  // required
  name: "Admin"
});
```

### Seed in Production

**Problem:** Test data appears in production.

**Fix:** Guard with environment check:

```typescript
seed: async (ctx) => {
  if (process.env.NODE_ENV === "production") {
    // Only seed essential data in production
    const adminExists = await ctx.em.repo("users").findOne({
      where: { role: { $eq: "admin" } },
    });
    if (!adminExists) {
      await ctx.em.mutator("users").insertOne({
        email: process.env.ADMIN_EMAIL,
        name: "Admin",
        role: "admin",
      });
    }
    return;
  }

  // Full dev seed...
}
```

## Verification

After seeding, verify data was inserted:

```typescript
seed: async (ctx) => {
  // ... insert data ...

  // Verify
  const userCount = await ctx.em.repo("users").count();
  const postCount = await ctx.em.repo("posts").count();

  console.log(`Seeded: ${userCount} users, ${postCount} posts`);
}
```

Or via API after startup:

```typescript
const api = app.getApi();
const { data } = await api.data.readMany("users");
console.log("Users:", data.length);
```

## DOs and DON'Ts

**DO:**
- Check for existing data before inserting
- Insert parent records before children (FK order)
- Use environment checks for dev vs prod data
- Log seed progress for debugging
- Keep seed functions idempotent

**DON'T:**
- Seed sensitive data (real passwords, API keys)
- Assume seed runs only once
- Hardcode production admin credentials in code
- Skip required fields
- Ignore foreign key relationships

## Related Skills

- **bknd-crud-create** - Create records via API/SDK
- **bknd-bulk-operations** - Bulk insert/update/delete at runtime
- **bknd-create-entity** - Define entities before seeding
- **bknd-define-relationship** - Set up relations for seeding linked data

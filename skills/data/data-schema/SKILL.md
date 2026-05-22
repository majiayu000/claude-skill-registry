---
name: data-schema
description: Use when defining Bknd entities, fields, relationships, and indices. Covers entity definition with em(), field types (text, number, boolean, date, enumm, json, jsonschema), field configuration (required, default_value, validation), relationship types (many-to-one, one-to-one, many-to-many, polymorphic), and index creation (simple, composite, unique).
---

# Data Schema

Define your data model with entities, fields, and relationships. Bknd uses a declarative API similar to Drizzle/Prisma but with fewer boilerplate.

## What You'll Learn

- Define entities with `em()` and `entity()`
- Use all field types with proper configuration
- Create relationships between entities
- Add indices for performance
- Follow naming conventions and best practices

## Entity Definition

### Basic Entity

Use `em()` to define multiple entities:

```typescript
import { em, entity, text, boolean } from "bknd";

const schema = em({
  todos: entity("todos", {
    title: text().required(),
    done: boolean(),
  }),
});
```

**Auto-generated fields:**
- `id` (primary key) - automatically added to every entity
- Format depends on database: SQLite uses integer, PostgreSQL uses UUID

### Multiple Entities

```typescript
const schema = em({
  users: entity("users", {
    email: text().required(),
    name: text(),
  }),
  posts: entity("posts", {
    title: text().required(),
    content: text(),
  }),
});
```

## Field Types

### Primary Field

Primary key is automatically added to every entity:

```typescript
entity("users", {
  email: text().required(),
})
// Auto-generated: id (integer or UUID)
```

**Customize primary key format:**

```typescript
entity("users", {
  email: text().required(),
}, {
  primary_format: "uuid",  // "integer" | "uuid" (default: "integer")
})
```

**Note:** Use the timestamps plugin for automatic created_at/updated_at fields.

### Enum Field

```typescript
import { enumm } from "bknd";

entity("users", {
  role: enumm({
    enum: ["admin", "user", "guest"],
  }).required(),
  status: enumm({
    enum: {
      ACTIVE: "active",
      INACTIVE: "inactive",
      PENDING: "pending",
    },
    default_value: "PENDING",
  }),
})
```

### JSON Field

```typescript
import { json } from "bknd";

entity("users", {
  metadata: json<{ theme: string; notifications: boolean }>(),
  preferences: json<string[]>({
    default_value: [],
  }),
})
```

### JSON Schema Field

For validated JSON with schema enforcement:

```typescript
import { jsonschema } from "bknd";

entity("events", {
  payload: jsonschema({
    type: "object",
    properties: {
      type: { type: "string" },
      data: { type: "object" },
    },
    required: ["type", "data"],
  }),
})
```

## Relationships

### Many-to-One

Posts belong to one user:

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
    }),
    posts: entity("posts", {
      title: text().required(),
    }),
  },
  ({ relation }, { users, posts }) => {
    relation(posts).manyToOne(users);
  }
);
```

**Auto-generated:** `user_id` foreign key on `posts` table

### One-to-One

User has one settings profile:

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
    }),
    settings: entity("settings", {
      theme: text(),
    }),
  },
  ({ relation }, { users, settings }) => {
    relation(settings).oneToOne(users);
  }
);
```

**Note:** One-to-one cannot use `$set` operator for updates (maintains exclusivity).

### Many-to-Many

Posts have many tags:

```typescript
const schema = em(
  {
    posts: entity("posts", {
      title: text().required(),
    }),
    tags: entity("tags", {
      name: text().required(),
    }),
  },
  ({ relation }, { posts, tags }) => {
    relation(posts).manyToMany(tags);
  }
);
```

**Auto-generated:** Junction table `posts_tags` with `post_id` and `tag_id`

### Many-to-Many with Custom Fields

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
    }),
    courses: entity("courses", {
      title: text().required(),
    }),
  },
  ({ relation }, { users, courses }) => {
    relation(users).manyToMany(courses, {
      connectionTable: "user_courses",
    }, {
      enrolled_at: date(),
      completed_at: date(),
    });
  }
);
```

### Self-Referencing

Categories can have parent/child relationships:

```typescript
const schema = em(
  {
    categories: entity("categories", {
      name: text().required(),
    }),
  },
  ({ relation }, { categories }) => {
    relation(categories).manyToOne(categories, {
      inversedBy: "children",
      mappedBy: "parent",
    });
  }
);
```

## Indices

### Simple Index

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
    }),
  },
  ({ index }, { users }) => {
    index(users).on(["email"]);
  }
);
```

### Unique Index

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
      username: text().required(),
    }),
  },
  ({ index }, { users }) => {
    index(users).on(["email"], true); // Second parameter = unique
  }
);
```

### Composite Index

```typescript
const schema = em(
  {
    posts: entity("posts", {
      author_id: number(),
      published: boolean(),
      created_at: date(),
    }),
  },
  ({ index }, { posts }) => {
    index(posts).on(["author_id", "published"]);
  }
);
```

### Chained Index Definition

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required(),
      username: text().required(),
    }),
  },
  ({ index }, { users }) => {
    index(users)
      .on(["email"], true)  // Unique index on email
      .on(["username"], true) // Unique index on username
      .on(["created_at"]);  // Non-unique index
  }
);
```

## Field Validation

### Built-in Validation

Fields validate data on insert/update:

```typescript
entity("users", {
  age: number({
    minimum: 18,
    maximum: 120,
  }),
  email: text({
    pattern: "^[^@]+@[^@]+\\.[^@]+$", // Basic email regex
  }),
})
```

### Validation Errors

For server-side mutations, use the API:

```typescript
const result = await api.data.createOne("users", {
  email: "invalid-email", // Fails pattern validation
  age: 15,               // Fails minimum validation
});

if (result.error) {
  console.log(result.error); // Validation error details
}
```

## Naming Conventions

### Entity Names

Use plural, lowercase entity names:

```typescript
// ✅ Good
entity("users", { ... })
entity("posts", { ... })

// ❌ Bad
entity("User", { ... })
entity("user", { ... })
```

### Field Names

Use snake_case for database compatibility:

```typescript
// ✅ Good
entity("users", {
  first_name: text(),
  last_name: text(),
  created_at: date(),
})

// ❌ Bad (works but inconsistent)
entity("users", {
  firstName: text(),  // Stored as firstName in DB
  lastName: text(),
})
```

## Type Generation

Extract types from schema for type safety:

```typescript
const schema = em({
  users: entity("users", {
    email: text().required(),
    name: text(),
  }),
});

type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}
```

**Generate with CLI:**
```bash
npx bknd types
```

## DOs and DON'Ts

**DO:**
- Use plural entity names (users, posts, comments)
- Use snake_case for field names (created_at, user_id)
- Add unique indices for fields used in lookups (email, username)
- Use composite indices for frequently filtered combinations
- Generate types with `npx bknd types` for full type safety
- Use timestamps plugin for created_at/updated_at fields
- Index foreign key fields (user_id, post_id)

**DON'T:**
- Define the same entity twice in `em()`
- Forget `.required()` for non-nullable fields
- Skip indices on frequently queried fields (you'll see warnings)
- Use PascalCase for entity or field names
- Store large binary data in JSON fields (use media fields instead)
- Overuse jsonschema unless you need runtime validation

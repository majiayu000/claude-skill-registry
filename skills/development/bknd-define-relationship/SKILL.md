---
name: bknd-define-relationship
description: Use when defining relationships between Bknd entities. Covers many-to-one, one-to-one, many-to-many, self-referencing relationships, junction tables, options like mappedBy and inversedBy, and UI vs code approaches.
---

# Define Entity Relationships

Create relationships between entities in Bknd (foreign keys, references, associations).

## Prerequisites

- At least two entities exist (see `bknd-create-entity`)
- For code mode: Access to your schema file

## Relationship Types

| Type | Use Case | Example |
|------|----------|---------|
| Many-to-One | Child belongs to one parent | Posts → User (author) |
| One-to-One | Exclusive 1:1 pairing | User → Profile |
| Many-to-Many | Both sides have multiple | Posts ↔ Tags |
| Self-Referencing | Entity references itself | Categories → Parent Category |

## When to Use UI vs Code

### Use UI Mode When
- Quick prototyping
- Visual learners
- Non-developers setting up relationships

### Use Code Mode When
- Version control needed
- Reproducible schema
- Custom options (mappedBy, connectionTable)
- Team collaboration

## UI Approach

### Step 1: Access Data Section

1. Start server: `npx bknd run`
2. Open `http://localhost:1337`
3. Navigate to **Data** section

### Step 2: Add Relation Field

1. Click on the **child** entity (e.g., `posts`)
2. Click **+ Add Field**
3. Select **Relation** field type
4. Choose the target entity (e.g., `users`)
5. Select relationship type:
   - **Many-to-One**: Multiple posts can belong to one user
   - **One-to-One**: One post has exactly one user
   - **Many-to-Many**: Posts can have many tags, tags can have many posts

### Step 3: Configure Options

- **Field Name**: Name for the foreign key (e.g., `author` creates `author_id`)
- **Required**: Toggle if relationship is mandatory

### Step 4: Save and Sync

1. Click **Save Field**
2. Click **Sync Database** to apply changes

## Code Approach

Relationships are defined in the second argument to `em()`:

```typescript
const schema = em(
  {
    // Entity definitions (first argument)
  },
  ({ relation, index }, entities) => {
    // Relationship definitions (second argument)
  }
);
```

### Many-to-One

Child belongs to one parent. Most common relationship type.

```typescript
import { em, entity, text } from "bknd";

const schema = em(
  {
    users: entity("users", { email: text().required() }),
    posts: entity("posts", { title: text().required() }),
  },
  ({ relation }, { users, posts }) => {
    relation(posts).manyToOne(users);
  }
);
```

**Auto-generated:** `users_id` foreign key column on `posts` table

**Custom field name with `mappedBy`:**

```typescript
({ relation }, { users, posts }) => {
  relation(posts).manyToOne(users, {
    mappedBy: "author",  // Creates author_id instead of users_id
  });
}
```

### One-to-One

Exclusive 1:1 relationship. Each child belongs to exactly one parent.

```typescript
const schema = em(
  {
    users: entity("users", { email: text().required() }),
    profiles: entity("profiles", { bio: text() }),
  },
  ({ relation }, { users, profiles }) => {
    relation(profiles).oneToOne(users);
  }
);
```

**Note:** One-to-one relationships cannot use `$set` operator (maintains exclusivity).

### Many-to-Many

Both entities can have multiple of the other. Junction table created automatically.

```typescript
const schema = em(
  {
    posts: entity("posts", { title: text().required() }),
    tags: entity("tags", { name: text().required() }),
  },
  ({ relation }, { posts, tags }) => {
    relation(posts).manyToMany(tags);
  }
);
```

**Auto-generated:** `posts_tags` junction table with `posts_id` and `tags_id` columns

**Custom junction table name:**

```typescript
({ relation }, { posts, tags }) => {
  relation(posts).manyToMany(tags, {
    connectionTable: "post_tags",  // Custom junction table name
  });
}
```

**Extra fields on junction table:**

```typescript
({ relation }, { users, courses }) => {
  relation(users).manyToMany(courses, {
    connectionTable: "enrollments",
  }, {
    // Extra fields on junction table
    enrolled_at: date(),
    completed: boolean(),
    grade: number(),
  });
}
```

### Self-Referencing

Entity references itself. Common for hierarchies (categories, comments, org charts).

```typescript
const schema = em(
  {
    categories: entity("categories", { name: text().required() }),
  },
  ({ relation }, { categories }) => {
    relation(categories).manyToOne(categories, {
      mappedBy: "parent",      // FK field: parent_id
      inversedBy: "children",  // Reverse navigation
    });
  }
);
```

**Usage:**
- `category.parent_id` → Points to parent category
- Query children: `api.data.readMany("categories", { where: { parent_id: 5 } })`

## Alternative: Direct Foreign Key

Instead of `relation()`, use `.references()` on a number field:

```typescript
const schema = em({
  users: entity("users", { email: text().required() }),
  posts: entity("posts", {
    title: text().required(),
    author_id: number().references("users.id"),
  }),
});
```

**Difference:** `.references()` is simpler but doesn't create inverse navigation or support many-to-many.

## Relation Options

### ManyToOne / OneToOne Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mappedBy` | string | Target entity name | FK field name (e.g., `author` → `author_id`) |
| `inversedBy` | string | Source entity name | Reverse navigation name |
| `required` | boolean | false | Relationship is mandatory |

### ManyToMany Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `connectionTable` | string | `{source}_{target}` | Junction table name |

## Querying Relations

### Load Related Data (with)

```typescript
const api = app.getApi();

// Load posts with their author
const posts = await api.data.readMany("posts", {
  with: {
    users: { select: ["email", "name"] },
  },
});
// Result: [{ id: 1, title: "...", users: { email: "...", name: "..." } }]
```

### Filter by Relation

```typescript
// Posts by specific author
const posts = await api.data.readMany("posts", {
  where: { author_id: 5 },
});

// Using join for complex filters
const posts = await api.data.readMany("posts", {
  join: {
    users: { where: { email: "john@example.com" } },
  },
});
```

### Many-to-Many Operations

```typescript
// Attach tags to post
await api.data.updateOne("posts", 1, {
  tags: { $attach: [1, 2, 3] },  // Tag IDs
});

// Detach tags
await api.data.updateOne("posts", 1, {
  tags: { $detach: [2] },
});

// Replace all tags
await api.data.updateOne("posts", 1, {
  tags: { $set: [4, 5] },
});
```

### Many-to-One Operations

```typescript
// Set author on post
await api.data.updateOne("posts", 1, {
  users: { $set: 5 },  // User ID
});
```

## Common Patterns

### Blog with Authors and Tags

```typescript
const schema = em(
  {
    users: entity("users", {
      email: text().required().unique(),
      name: text(),
    }),
    posts: entity("posts", {
      title: text().required(),
      content: text(),
      published: boolean(),
    }),
    tags: entity("tags", {
      name: text().required().unique(),
    }),
  },
  ({ relation }, { users, posts, tags }) => {
    // Post has one author
    relation(posts).manyToOne(users, { mappedBy: "author" });

    // Posts have many tags
    relation(posts).manyToMany(tags);
  }
);
```

### E-commerce Orders

```typescript
const schema = em(
  {
    customers: entity("customers", { email: text().required() }),
    orders: entity("orders", { total: number() }),
    products: entity("products", { name: text().required(), price: number() }),
  },
  ({ relation }, { customers, orders, products }) => {
    // Order belongs to customer
    relation(orders).manyToOne(customers);

    // Order has many products (with quantity)
    relation(orders).manyToMany(products, {
      connectionTable: "order_items",
    }, {
      quantity: number().required(),
      unit_price: number().required(),
    });
  }
);
```

### Nested Categories

```typescript
const schema = em(
  {
    categories: entity("categories", {
      name: text().required(),
      slug: text().required().unique(),
    }),
  },
  ({ relation }, { categories }) => {
    relation(categories).manyToOne(categories, {
      mappedBy: "parent",
      inversedBy: "children",
    });
  }
);

// Usage: Get all children of category 5
const children = await api.data.readMany("categories", {
  where: { parent_id: 5 },
});
```

## Common Pitfalls

### Entity Not Found

**Error:** `Entity "user" not found`

**Fix:** Entity names are plural by convention. Use `users` not `user`.

```typescript
// Wrong
relation(posts).manyToOne(user);

// Correct
relation(posts).manyToOne(users);
```

### Circular Reference Error

**Error:** `Circular dependency detected`

**Fix:** For self-referencing, use proper options:

```typescript
// Correct self-reference
relation(categories).manyToOne(categories, {
  mappedBy: "parent",
  inversedBy: "children",
});
```

### Foreign Key Naming Conflict

**Error:** `Field "users_id" already exists`

**Fix:** Use `mappedBy` to specify a different field name:

```typescript
// If you already have users_id, use a different name
relation(posts).manyToOne(users, { mappedBy: "author" });  // Creates author_id
```

### Many-to-Many $set on One-to-One

**Error:** `Cannot use $set on one-to-one relation`

**Fix:** One-to-one maintains exclusivity differently. Use `$create` instead:

```typescript
// For one-to-one
await api.data.updateOne("users", 1, {
  profiles: { $create: { bio: "Hello" } },
});
```

### Missing Entity in Destructure

**Error:** `Cannot read property 'manyToOne' of undefined`

**Fix:** Ensure entity is destructured from second callback parameter:

```typescript
// Wrong - missing users in destructure
({ relation }, { posts }) => {
  relation(posts).manyToOne(users);  // users is undefined
}

// Correct
({ relation }, { users, posts }) => {
  relation(posts).manyToOne(users);
}
```

### Relation Changes Not Applying

**Problem:** Added relation but not seeing FK column.

**Fixes:**
1. Restart server (schema syncs on startup)
2. Verify relation is in second `em()` argument
3. Check for syntax errors

## Verification

### Check Foreign Key Created

```bash
npx bknd debug paths
# Look for the FK field in entity output
```

### Test Relation in Code

```typescript
const api = app.getApi();

// Create parent
const user = await api.data.createOne("users", { email: "test@example.com" });

// Create child with relation
const post = await api.data.createOne("posts", {
  title: "Test Post",
  author_id: user.data.id,
});

// Load with relation
const loaded = await api.data.readOne("posts", post.data.id, {
  with: { users: true },
});
console.log(loaded.data.users);  // { id: 1, email: "test@example.com" }
```

## DOs and DON'Ts

**DO:**
- Use plural entity names (`users`, `posts`)
- Use `mappedBy` for semantic field names (`author` instead of `users`)
- Define relations in the second `em()` argument
- Use `.references()` for simple FK without navigation

**DON'T:**
- Use singular entity names in relations
- Create manual FK fields when using `relation()` (it creates them automatically)
- Use `$set` on one-to-one relations
- Forget to destructure entities in the callback

## Related Skills

- **bknd-create-entity** - Create entities before defining relationships
- **bknd-add-field** - Add fields including `.references()` for simple FKs
- **bknd-crud-read** - Query related data with `with` and `join`
- **bknd-crud-update** - Use `$attach`, `$detach`, `$set` for relation updates
- **bknd-query-filter** - Advanced filtering on relations

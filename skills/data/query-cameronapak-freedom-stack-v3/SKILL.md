---
name: query
description: Use when querying Bknd data, building filters with WhereBuilder, sorting results, pagination, auto-joining relationships, and optimizing query performance. Covers Repository API, WhereQuery operators, RepoQuery configuration, and relationship preloading.
---

# Query System

Bknd provides a type-safe query builder built on top of Kysely. All queries start from a Repository and use WhereBuilder for filters.

**Important:** The `em()` function is used for schema definition in Code Mode. For runtime queries, use:
- **API endpoints** (Code Mode recommended): `api.data.readMany()`, `api.data.createOne()`, etc.
- **Direct database access** (Hybrid Mode): `app.em.repo()`, `app.em.mutator()` after `app.build()`

## What You'll Learn

- Get a Repository from EntityManager
- Build filter conditions with WhereBuilder
- Use auto-join for relationship filtering
- Configure pagination, sorting, and field selection
- Eagerly load relations with `with`
- Optimize query performance with indices

## Repository - Query Entry Point

**For Code Mode (recommended):**

Use the TypeScript SDK via API endpoints:

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:3000" });

// Three main query methods
await api.data.readOne("users", 1);              // Find single by primary key
await api.data.readOneBy("users", { id: 1 });   // Find single by conditions
await api.data.readMany("users", { limit: 10 });  // Find multiple
```

**For Hybrid Mode (direct database access):**

Get a Repository through EntityManager after `app.build()`:

```typescript
const app = createApp(config);
await app.build();

const userRepo = app.em.repo('User'); // Shorthand for app.em.repository('User')

// Three main query methods
await userRepo.findId(1);              // Find single by primary key
await userRepo.findOne({ id: 1 });     // Find single by conditions
await userRepo.findMany({ limit: 10 }); // Find multiple
```

## WhereBuilder - Filter Conditions

### Basic Operators

```typescript
// Equal (direct value or use $eq)
{ id: 1 }                    // id = 1
{ id: { $eq: 1 } }           // id = 1

// Not equal
{ status: { $ne: 'active' } }  // status != 'active'

// Comparisons
{ age: { $gt: 18 } }         // age > 18
{ age: { $gte: 18 } }        // age >= 18
{ age: { $lt: 65 } }         // age < 65
{ age: { $lte: 65 } }        // age <= 65

// Range
{ createdAt: { $between: ['2024-01-01', '2024-12-31'] } }

// Null checks
{ deletedAt: { $isnull: true } }   // IS NULL
{ deletedAt: { $isnull: false } }  // IS NOT NULL

// Arrays
{ status: { $in: ['active', 'pending'] } }     // IN ('active', 'pending')
{ status: { $notin: ['deleted'] } }            // NOT IN ('deleted')

// Fuzzy search
{ name: { $like: 'John*' } }  // LIKE 'John%' (supports * wildcard)
```

### Auto-Join Filtering

Filter by related entity fields using **dot notation** - Bknd automatically adds necessary joins:

```typescript
// Filter comments by post title (auto-joins posts table)
const comments = await api.data.readMany("comments", {
  where: { 'posts.title': 'My Post' }
});

// Filter posts by author username
const posts = await api.data.readMany("posts", {
  where: { 'author.username': 'john' }
});

// Filter by multiple related fields
const comments = await api.data.readMany("comments", {
  where: {
    'posts.title': { $like: '*Tutorial*' },
    'author.status': 'active'
  }
});
```

**Auto-join rules:**
- Related entity exists and has a defined relationship
- Field exists on the related entity
- Use dot notation: `"{relationName}.{fieldName}"`

**Performance warning:** If related field is not indexed, you'll see a warning.

### Compound Conditions

```typescript
// AND (multiple fields default to AND)
{ 
  status: 'active',
  age: { $gte: 18 }
}
// WHERE status = 'active' AND age >= 18

// OR
{
  $or: {
    status: 'active',
    role: 'admin'
  }
}
// WHERE status = 'active' OR role = 'admin'
```

## RepoQuery - Complete Query Configuration

```typescript
interface RepoQuery {
  limit?: number;      // Default 10
  offset?: number;     // Default 0
  
  sort?: string | { by: string; dir: 'asc' | 'desc' };
  // 'id'              → ORDER BY id ASC
  // '-id'             → ORDER BY id DESC
  
  select?: string[];   // ['id', 'title', 'createdAt']
  
  with?: Record<string, RepoQuery>;  // Eager load relations (supports nesting)
  
  join?: string[];     // Explicit join tables (advanced)
  
  where?: WhereQuery;
}
```

## Practical Examples

### Basic Queries

```typescript
// Find active users, sorted by creation time descending
const users = await api.data.readMany("users", {
  where: { status: 'active' },
  sort: '-createdAt',
  limit: 20
});

// Find users aged 18-65
const adults = await api.data.readMany("users", {
  where: { age: { $between: [18, 65] }
});

// Fuzzy search
const results = await api.data.readMany("posts", {
  where: { title: { $like: '*tutorial*' } },
  limit: 10
});
```

### Relation Queries (with)

```typescript
// Find users with their posts (max 5 per user)
const usersWithPosts = await api.data.readMany("users", {
  limit: 10,
  with: {
    posts: {
      limit: 5,
      sort: '-createdAt',
      where: { status: 'published' }
    }
  }
});

// Nested relations: User → Posts → Comments
const deepQuery = await api.data.readMany("users", {
  with: {
    posts: {
      with: {
        comments: {
          limit: 10,
          where: { approved: { $isnull: false } }
        }
      }
    }
  }
});
```

### Field Selection

```typescript
// Query only needed fields
const lightUsers = await api.data.readMany("users", {
  select: ['id', 'name', 'email'],
  limit: 100
});
```

### Combined Queries

```typescript
// Find active users from 2024, sorted by post count
const activeUsers = await api.data.readMany("users", {
  where: {
    status: 'active',
    createdAt: { $gte: '2024-01-01' }
  },
  sort: { by: 'postsCount', dir: 'desc' },
  select: ['id', 'name', 'postsCount', 'lastLoginAt'],
  limit: 20,
  offset: 0
});
```

## Performance Considerations

### Auto-Join Performance

Auto-join is convenient but may load unnecessary data:

```typescript
// Auto-join: Simple but loads all columns
const comments = await api.data.readMany("comments", {
  where: { 'posts.title': 'My Post' }
});

// Explicit join: Use select to load only needed columns
const commentsOptimized = await api.data.readMany("comments", {
  join: ['posts'],
  select: ['id', 'content', 'posts.title'],
  where: { 'posts.title': 'My Post' }
});
```

### Indexing for Filters

Always index fields used in filters and joins:

```typescript
const users = entity('users', {
  email: text().unique().index(),  // Index for login queries
  status: text().index(),           // Index for status filters
  createdAt: timestamp().index(),   // Index for date range queries
});
```

### Pagination

Use reasonable limits:

```typescript
// Good: Reasonable page size
const page1 = await api.data.readMany("posts", {
  limit: 20,
  offset: 0
});

// Avoid: Large limits slow down queries
const allPosts = await api.data.readMany("posts", {
  limit: 10000  // ⚠️ Performance risk
});
```

## DOs and DON'Ts

**DO:**
- Index fields used in `where` clauses and auto-join filters
- Use `select` to limit returned columns when joining large tables
- Use `with` to eagerly load relations instead of N+1 queries
- Set reasonable `limit` values (typically 20-100)
- Use dot notation for auto-join filtering (`'posts.title'`)
- Generate types with `npx bknd types` for full type safety

**DON'T:**
- Auto-join on non-indexed fields without adding indices first
- Use `limit` values larger than 100 without pagination
- Forget to sort by indexed fields for consistent performance
- Query unnecessary columns with `select: ['*']` (use specific fields)
- Use auto-join deeply nested relations (use explicit joins instead)
- Overlook performance warnings in development logs

## Common Issues

**"Field not found" type errors:**
- Ensure the field exists on the entity definition
- Check for correct case sensitivity (snake_case fields)

**Slow auto-join queries:**
- Add index to the related field
- Consider using explicit `join` with `select` for large tables

**Incorrect results with $like:**
- Use `*` wildcard, not `%` (Bknd normalizes `%` to `*`)
- Pattern matching is case-sensitive

## Next Steps

- **[Data Schema](data-schema)** - Define entities with indices for better queries
- **[Auth](auth)** - Integrate authentication with query filters
- **[Permissions](permissions)** - Apply row-level security to queries

---
name: bknd-crud-read
description: Use when querying and retrieving data from Bknd entities via SDK or REST API. Covers readOne, readMany, readOneBy, filtering (where clause), sorting, field selection, loading relations (with/join), and response handling.
---

# CRUD Read

Query and retrieve data from your Bknd database using the SDK or REST API.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists with data (use `bknd-create-entity`, `bknd-crud-create`)
- SDK configured or API endpoint known

## When to Use UI Mode

- Browsing data manually
- Quick lookups during development
- Verifying data after operations

**UI steps:** Admin Panel > Data > Select Entity > Browse/search records

## When to Use Code Mode

- Application data display
- Search/filter functionality
- Building lists, tables, detail pages
- API integrations

## Code Approach

### Step 1: Set Up SDK Client

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",
});

// If auth required:
api.updateToken("your-jwt-token");
```

### Step 2: Read Single Record by ID

Use `readOne(entity, id, query?)`:

```typescript
const { ok, data, error } = await api.data.readOne("posts", 1);

if (ok) {
  console.log("Post:", data.title);
} else {
  console.error("Not found or error:", error.message);
}
```

### Step 3: Read Single Record by Query

Use `readOneBy(entity, query)` to find by field value:

```typescript
const { data } = await api.data.readOneBy("users", {
  where: { email: { $eq: "user@example.com" } },
});

if (data) {
  console.log("Found user:", data.id);
}
```

### Step 4: Read Multiple Records

Use `readMany(entity, query?)`:

```typescript
const { ok, data, meta } = await api.data.readMany("posts", {
  where: { status: { $eq: "published" } },
  sort: { created_at: "desc" },
  limit: 20,
  offset: 0,
});

console.log(`Found ${meta.total} total, showing ${data.length}`);
```

### Step 5: Handle Response

The response object structure:

```typescript
type ReadResponse = {
  ok: boolean;
  data?: T | T[];         // Single object or array
  meta?: {                // For readMany
    total: number;        // Total matching records
    limit: number;        // Current page size
    offset: number;       // Current offset
  };
  error?: {
    message: string;
    code: string;
  };
};
```

## Filtering (Where Clause)

### Comparison Operators

```typescript
// Equality (implicit or explicit)
{ where: { status: "published" } }
{ where: { status: { $eq: "published" } } }

// Not equal
{ where: { status: { $ne: "deleted" } } }

// Numeric comparisons
{ where: { age: { $gt: 18 } } }    // Greater than
{ where: { age: { $gte: 18 } } }   // Greater or equal
{ where: { price: { $lt: 100 } } } // Less than
{ where: { price: { $lte: 100 } } } // Less or equal
```

### String Operators

```typescript
// LIKE patterns (% = wildcard)
{ where: { title: { $like: "%hello%" } } }      // Contains (case-sensitive)
{ where: { title: { $ilike: "%hello%" } } }     // Contains (case-insensitive)

// Convenience methods
{ where: { name: { $startswith: "John" } } }
{ where: { email: { $endswith: "@gmail.com" } } }
{ where: { bio: { $contains: "developer" } } }
```

### Array Operators

```typescript
// In array
{ where: { id: { $in: [1, 2, 3] } } }

// Not in array
{ where: { type: { $nin: ["archived", "deleted"] } } }
```

### Null Checks

```typescript
// Is NULL
{ where: { deleted_at: { $isnull: true } } }

// Is NOT NULL
{ where: { published_at: { $isnull: false } } }
```

### Logical Operators

```typescript
// AND (implicit - multiple fields)
{
  where: {
    status: { $eq: "published" },
    category: { $eq: "news" },
  }
}

// OR
{
  where: {
    $or: [
      { status: { $eq: "published" } },
      { featured: { $eq: true } },
    ]
  }
}

// Combined AND/OR
{
  where: {
    category: { $eq: "news" },
    $or: [
      { status: { $eq: "published" } },
      { author_id: { $eq: currentUserId } },
    ]
  }
}
```

## Sorting

```typescript
// Object syntax (preferred)
{ sort: { created_at: "desc" } }
{ sort: { name: "asc", created_at: "desc" } }  // Multi-sort

// String syntax (- prefix = descending)
{ sort: "-created_at" }
{ sort: "name,-created_at" }
```

## Field Selection

Reduce payload by selecting specific fields:

```typescript
const { data } = await api.data.readMany("users", {
  select: ["id", "email", "name"],
});
// data[0] only has id, email, name
```

## Loading Relations

### With Clause (Separate Queries)

```typescript
// Simple - load relations
{ with: "author" }
{ with: ["author", "comments"] }
{ with: "author,comments" }

// Nested with subquery options
{
  with: {
    author: {
      select: ["id", "name", "avatar"],
    },
    comments: {
      where: { approved: { $eq: true } },
      sort: { created_at: "desc" },
      limit: 10,
      with: ["user"],  // Nested loading
    },
  }
}
```

Result structure:

```typescript
const { data } = await api.data.readOne("posts", 1, {
  with: ["author", "comments"],
});

console.log(data.author.name);      // Nested object
console.log(data.comments[0].text); // Nested array
```

### Join Clause (SQL JOIN)

Use `join` to filter by related fields:

```typescript
const { data } = await api.data.readMany("posts", {
  join: ["author"],
  where: {
    "author.role": { $eq: "admin" },  // Filter by joined field
  },
  sort: "-author.created_at",         // Sort by joined field
});
```

### With vs Join

| Feature | `with` | `join` |
|---------|--------|--------|
| Query method | Separate queries | SQL JOIN |
| Return structure | Nested objects | Flat (unless also with) |
| Use case | Load related data | Filter by related fields |
| Performance | Multiple queries | Single query |

## Pagination

```typescript
// Page 1 (records 0-19)
{ limit: 20, offset: 0 }

// Page 2 (records 20-39)
{ limit: 20, offset: 20 }

// Generic page formula
{ limit: pageSize, offset: (page - 1) * pageSize }
```

Default limit is 10 if not specified.

### Pagination Helper

```typescript
async function paginate<T>(
  entity: string,
  page: number,
  pageSize: number,
  query: object = {}
) {
  const { data, meta } = await api.data.readMany(entity, {
    ...query,
    limit: pageSize,
    offset: (page - 1) * pageSize,
  });

  return {
    data,
    page,
    pageSize,
    total: meta.total,
    totalPages: Math.ceil(meta.total / pageSize),
    hasNext: page * pageSize < meta.total,
    hasPrev: page > 1,
  };
}
```

## REST API Approach

### Read Many

```bash
# Basic
curl http://localhost:7654/api/data/posts

# With query params
curl "http://localhost:7654/api/data/posts?limit=20&offset=0&sort=-created_at"

# With where clause
curl "http://localhost:7654/api/data/posts?where=%7B%22status%22%3A%22published%22%7D"
```

### Read One by ID

```bash
curl http://localhost:7654/api/data/posts/1
```

### Complex Query (POST)

For complex queries, use POST to `/api/data/:entity/query`:

```bash
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{
    "where": {"status": {"$eq": "published"}},
    "sort": {"created_at": "desc"},
    "limit": 20,
    "with": ["author"]
  }'
```

### Read Related Records

```bash
# Get user's posts
curl http://localhost:7654/api/data/users/1/posts
```

## React Integration

### Basic List

```tsx
import { useApp } from "bknd/react";
import { useEffect, useState } from "react";

function PostsList() {
  const { api } = useApp();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.data.readMany("posts", {
      where: { status: { $eq: "published" } },
      sort: { created_at: "desc" },
      limit: 20,
    }).then(({ data }) => {
      setPosts(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### With SWR

```tsx
import { useApp } from "bknd/react";
import useSWR from "swr";

function PostsList() {
  const { api } = useApp();

  const { data: posts, isLoading, error } = useSWR(
    "posts-published",
    () => api.data.readMany("posts", {
      where: { status: { $eq: "published" } },
      sort: { created_at: "desc" },
    }).then((r) => r.data)
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading posts</div>;

  return (
    <ul>
      {posts?.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Detail Page

```tsx
function PostDetail({ postId }: { postId: number }) {
  const { api } = useApp();

  const { data: post, isLoading } = useSWR(
    `post-${postId}`,
    () => api.data.readOne("posts", postId, {
      with: ["author", "comments"],
    }).then((r) => r.data)
  );

  if (isLoading) return <div>Loading...</div>;
  if (!post) return <div>Post not found</div>;

  return (
    <article>
      <h1>{post.title}</h1>
      <p>By {post.author?.name}</p>
      <div>{post.content}</div>
      <h2>Comments ({post.comments?.length})</h2>
    </article>
  );
}
```

### Search with Debounce

```tsx
import { useState, useMemo } from "react";
import { useApp } from "bknd/react";
import useSWR from "swr";
import { useDebouncedValue } from "@mantine/hooks"; // or custom hook

function SearchPosts() {
  const { api } = useApp();
  const [search, setSearch] = useState("");
  const [debouncedSearch] = useDebouncedValue(search, 300);

  const { data: results, isLoading } = useSWR(
    debouncedSearch ? `search-${debouncedSearch}` : null,
    () => api.data.readMany("posts", {
      where: { title: { $ilike: `%${debouncedSearch}%` } },
      limit: 10,
    }).then((r) => r.data)
  );

  return (
    <div>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search posts..."
      />
      {isLoading && <p>Searching...</p>}
      <ul>
        {results?.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Full Example

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// Get single post with relations
const { data: post } = await api.data.readOne("posts", 1, {
  with: {
    author: { select: ["id", "name"] },
    tags: true,
  },
});
console.log(post.title, "by", post.author.name);

// Find user by email
const { data: user } = await api.data.readOneBy("users", {
  where: { email: { $eq: "admin@example.com" } },
});

// List published posts with pagination
const { data: posts, meta } = await api.data.readMany("posts", {
  where: {
    status: { $eq: "published" },
    deleted_at: { $isnull: true },
  },
  sort: { created_at: "desc" },
  limit: 10,
  offset: 0,
  with: ["author"],
});
console.log(`Page 1 of ${Math.ceil(meta.total / 10)}`);

// Complex query: posts by admin authors in category
const { data: adminPosts } = await api.data.readMany("posts", {
  join: ["author"],
  where: {
    "author.role": { $eq: "admin" },
    category: { $eq: "announcements" },
    $or: [
      { status: { $eq: "published" } },
      { featured: { $eq: true } },
    ],
  },
  select: ["id", "title", "created_at"],
  sort: "-created_at",
});
```

## Common Patterns

### Count Records

```typescript
const { data } = await api.data.count("posts", {
  status: { $eq: "published" },
});
console.log(`${data.count} published posts`);
```

### Check Existence

```typescript
const { data } = await api.data.exists("users", {
  email: { $eq: "test@example.com" },
});
if (data.exists) {
  console.log("Email already registered");
}
```

### Soft Delete Filter

```typescript
// Always exclude soft-deleted
const { data } = await api.data.readMany("posts", {
  where: { deleted_at: { $isnull: true } },
});
```

### Get User's Related Data

```typescript
// Using readManyByReference
const { data: userPosts } = await api.data.readManyByReference(
  "users", userId, "posts",
  { sort: { created_at: "desc" }, limit: 10 }
);
```

## Common Pitfalls

### Not Checking Response

**Problem:** Assuming data exists.

**Fix:** Always check `ok` or handle undefined:

```typescript
// Wrong
const { data } = await api.data.readOne("posts", 999);
console.log(data.title);  // Error if not found!

// Correct
const { ok, data } = await api.data.readOne("posts", 999);
if (!ok || !data) {
  console.log("Post not found");
  return;
}
console.log(data.title);
```

### Wrong Operator Syntax

**Problem:** Using operators incorrectly.

**Fix:** Wrap values in operator object:

```typescript
// Wrong
{ where: { age: ">18" } }

// Correct
{ where: { age: { $gt: 18 } } }
```

### Missing Join for Related Filter

**Problem:** Filtering by related field without join.

**Fix:** Add `join` clause:

```typescript
// Wrong - won't work
{ where: { "author.role": { $eq: "admin" } } }

// Correct - add join
{
  join: ["author"],
  where: { "author.role": { $eq: "admin" } }
}
```

### N+1 Query Problem

**Problem:** Loading relations in a loop.

**Fix:** Use `with` to load relations in batch:

```typescript
// Wrong - N+1 queries
const { data: posts } = await api.data.readMany("posts");
for (const post of posts) {
  const { data: author } = await api.data.readOne("users", post.author_id);
}

// Correct - single batch query
const { data: posts } = await api.data.readMany("posts", {
  with: ["author"],
});
posts.forEach(p => console.log(p.author.name));
```

### Case-Sensitive Search

**Problem:** `$like` is case-sensitive.

**Fix:** Use `$ilike` for case-insensitive:

```typescript
// Case-sensitive (may miss results)
{ where: { title: { $like: "%React%" } } }

// Case-insensitive
{ where: { title: { $ilike: "%react%" } } }
```

## Verification

Test queries in admin panel first:

1. Admin Panel > Data > Select Entity
2. Use filters/search UI
3. Check returned data matches expectations

Or log response in code:

```typescript
const response = await api.data.readMany("posts", query);
console.log("Response:", JSON.stringify(response, null, 2));
```

## DOs and DON'Ts

**DO:**
- Check `ok` before accessing `data`
- Use `with` for loading relations
- Use `join` when filtering by related fields
- Use `$ilike` for case-insensitive text search
- Use pagination for large datasets
- Use `select` to reduce payload size

**DON'T:**
- Assume queries always return data
- Load relations in a loop (N+1 problem)
- Forget `join` when filtering by relation fields
- Use `$like` when case-insensitive needed
- Request all fields when only few needed
- Skip pagination for potentially large datasets

## Related Skills

- **bknd-crud-create** - Insert records to query
- **bknd-crud-update** - Modify queried records
- **bknd-crud-delete** - Remove queried records
- **bknd-query-filter** - Advanced filtering techniques
- **bknd-pagination** - Pagination strategies
- **bknd-define-relationship** - Set up relations to load with `with`

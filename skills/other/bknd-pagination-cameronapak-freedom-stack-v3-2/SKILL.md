---
name: bknd-pagination
description: Use when implementing paginated data retrieval in Bknd. Covers limit/offset pagination, page calculation, pagination metadata (total, hasNext, hasPrev), pagination helper functions, infinite scroll, and React integration patterns.
---

# Pagination

Implement paginated data retrieval for lists, tables, and infinite scroll using Bknd's limit/offset pagination.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists with data (use `bknd-create-entity`, `bknd-seed-data`)
- SDK configured or API endpoint known

## When to Use UI Mode

- Browsing data in admin panel
- Quick data exploration
- Testing pagination manually

**UI steps:** Admin Panel > Data > Select Entity > Use pagination controls at bottom

## When to Use Code Mode

- Building paginated lists/tables
- Implementing "Load More" buttons
- Creating infinite scroll
- Server-side pagination APIs

## Pagination Basics

Bknd uses **offset-based pagination** with two parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | number | 10 | Records per page |
| `offset` | number | 0 | Records to skip |

### Page Formula

```typescript
// Page N (1-indexed) with pageSize records:
{
  limit: pageSize,
  offset: (page - 1) * pageSize
}

// Examples:
// Page 1: { limit: 20, offset: 0 }   -> records 0-19
// Page 2: { limit: 20, offset: 20 }  -> records 20-39
// Page 3: { limit: 20, offset: 40 }  -> records 40-59
```

## Code Approach

### Step 1: Basic Paginated Query

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

const page = 1;
const pageSize = 20;

const { ok, data, meta } = await api.data.readMany("posts", {
  where: { status: { $eq: "published" } },
  sort: { created_at: "desc" },
  limit: pageSize,
  offset: (page - 1) * pageSize,
});

console.log(`Page ${page}: ${data.length} records`);
console.log(`Total: ${meta.total}`);
```

### Step 2: Handle Response Metadata

The `meta` object contains pagination info:

```typescript
type PaginationMeta = {
  total: number;   // Total matching records
  limit: number;   // Current page size
  offset: number;  // Current offset
};

const { data, meta } = await api.data.readMany("posts", {
  limit: 20,
  offset: 0,
});

const totalPages = Math.ceil(meta.total / meta.limit);
const currentPage = Math.floor(meta.offset / meta.limit) + 1;
const hasNextPage = meta.offset + meta.limit < meta.total;
const hasPrevPage = meta.offset > 0;

console.log(`Page ${currentPage} of ${totalPages}`);
console.log(`Has next: ${hasNextPage}, Has prev: ${hasPrevPage}`);
```

### Step 3: Create Pagination Helper

```typescript
type PaginationResult<T> = {
  data: T[];
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
};

async function paginate<T>(
  entity: string,
  page: number,
  pageSize: number,
  query: object = {}
): Promise<PaginationResult<T>> {
  const { data, meta } = await api.data.readMany(entity, {
    ...query,
    limit: pageSize,
    offset: (page - 1) * pageSize,
  });

  return {
    data: data as T[],
    page,
    pageSize,
    total: meta.total,
    totalPages: Math.ceil(meta.total / pageSize),
    hasNext: page * pageSize < meta.total,
    hasPrev: page > 1,
  };
}

// Usage
const result = await paginate("posts", 1, 20, {
  where: { status: { $eq: "published" } },
  sort: { created_at: "desc" },
});

console.log(result.data);         // Posts array
console.log(result.totalPages);   // Total pages
console.log(result.hasNext);      // true/false
```

### Step 4: Paginate with Filters

Combine pagination with where clause:

```typescript
async function paginatedSearch(
  entity: string,
  page: number,
  pageSize: number,
  filters: object,
  sort: object = {}
) {
  const { data, meta } = await api.data.readMany(entity, {
    where: filters,
    sort,
    limit: pageSize,
    offset: (page - 1) * pageSize,
  });

  return {
    data,
    pagination: {
      page,
      pageSize,
      total: meta.total,
      totalPages: Math.ceil(meta.total / pageSize),
      hasNext: page * pageSize < meta.total,
      hasPrev: page > 1,
    },
  };
}

// Search with pagination
const result = await paginatedSearch(
  "posts",
  2,        // page 2
  10,       // 10 per page
  {
    status: { $eq: "published" },
    title: { $ilike: "%react%" },
  },
  { created_at: "desc" }
);
```

## REST API Approach

### Query Parameters

```bash
# Page 1, 20 per page
curl "http://localhost:7654/api/data/posts?limit=20&offset=0"

# Page 2
curl "http://localhost:7654/api/data/posts?limit=20&offset=20"

# With sorting
curl "http://localhost:7654/api/data/posts?limit=20&offset=0&sort=-created_at"

# With filters (URL-encoded JSON)
curl "http://localhost:7654/api/data/posts?limit=20&offset=0&where=%7B%22status%22%3A%22published%22%7D"
```

### POST for Complex Queries

```bash
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{
    "where": {"status": {"$eq": "published"}},
    "sort": {"created_at": "desc"},
    "limit": 20,
    "offset": 0
  }'
```

### Response Format

```json
{
  "ok": true,
  "data": [...],
  "meta": {
    "total": 150,
    "limit": 20,
    "offset": 0
  }
}
```

## React Integration

### Basic Paginated List

```tsx
import { useApp } from "bknd/react";
import { useState, useEffect } from "react";

function PaginatedPosts() {
  const { api } = useApp();
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const pageSize = 10;

  useEffect(() => {
    setLoading(true);
    api.data.readMany("posts", {
      sort: { created_at: "desc" },
      limit: pageSize,
      offset: (page - 1) * pageSize,
    }).then(({ data, meta }) => {
      setPosts(data);
      setTotalPages(Math.ceil(meta.total / pageSize));
      setLoading(false);
    });
  }, [page]);

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {posts.map((post) => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      )}

      <div className="pagination">
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button
          disabled={page >= totalPages}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

### With SWR (Recommended)

```tsx
import { useApp } from "bknd/react";
import { useState } from "react";
import useSWR from "swr";

function PaginatedPosts() {
  const { api } = useApp();
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const { data: result, isLoading } = useSWR(
    ["posts", page, pageSize],
    () => api.data.readMany("posts", {
      sort: { created_at: "desc" },
      limit: pageSize,
      offset: (page - 1) * pageSize,
    })
  );

  const posts = result?.data ?? [];
  const total = result?.meta?.total ?? 0;
  const totalPages = Math.ceil(total / pageSize);

  return (
    <div>
      {isLoading ? <p>Loading...</p> : (
        <ul>
          {posts.map((post) => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      )}

      <Pagination
        page={page}
        totalPages={totalPages}
        onPageChange={setPage}
      />
    </div>
  );
}

function Pagination({ page, totalPages, onPageChange }) {
  return (
    <div className="flex gap-2">
      <button
        disabled={page === 1}
        onClick={() => onPageChange(page - 1)}
      >
        Prev
      </button>

      {/* Page numbers */}
      {Array.from({ length: totalPages }, (_, i) => i + 1)
        .filter(p => Math.abs(p - page) <= 2 || p === 1 || p === totalPages)
        .map((p, i, arr) => (
          <>
            {i > 0 && arr[i - 1] !== p - 1 && <span>...</span>}
            <button
              key={p}
              onClick={() => onPageChange(p)}
              className={p === page ? "active" : ""}
            >
              {p}
            </button>
          </>
        ))}

      <button
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
}
```

### Load More / Infinite Scroll

```tsx
import { useApp } from "bknd/react";
import { useState, useCallback } from "react";

function InfinitePostsList() {
  const { api } = useApp();
  const [posts, setPosts] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const pageSize = 20;

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const { data, meta } = await api.data.readMany("posts", {
      sort: { created_at: "desc" },
      limit: pageSize,
      offset: posts.length,  // Use current length as offset
    });

    setPosts((prev) => [...prev, ...data]);
    setHasMore(posts.length + data.length < meta.total);
    setLoading(false);
  }, [posts.length, loading, hasMore]);

  // Initial load
  useEffect(() => {
    loadMore();
  }, []);

  return (
    <div>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>

      {hasMore && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? "Loading..." : "Load More"}
        </button>
      )}

      {!hasMore && <p>No more posts</p>}
    </div>
  );
}
```

### Infinite Scroll with Intersection Observer

```tsx
import { useApp } from "bknd/react";
import { useState, useEffect, useRef, useCallback } from "react";

function InfiniteScrollPosts() {
  const { api } = useApp();
  const [posts, setPosts] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const loaderRef = useRef(null);
  const pageSize = 20;

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const { data, meta } = await api.data.readMany("posts", {
      sort: { created_at: "desc" },
      limit: pageSize,
      offset: posts.length,
    });

    setPosts((prev) => [...prev, ...data]);
    setHasMore(posts.length + data.length < meta.total);
    setLoading(false);
  }, [posts.length, loading, hasMore]);

  // Intersection Observer for auto-load
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (loaderRef.current) {
      observer.observe(loaderRef.current);
    }

    return () => observer.disconnect();
  }, [loadMore]);

  // Initial load
  useEffect(() => {
    loadMore();
  }, []);

  return (
    <div>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>

      <div ref={loaderRef} style={{ height: 20 }}>
        {loading && <p>Loading...</p>}
        {!hasMore && <p>End of list</p>}
      </div>
    </div>
  );
}
```

### URL-Synced Pagination

```tsx
import { useApp } from "bknd/react";
import { useSearchParams } from "react-router-dom";
import useSWR from "swr";

function URLPaginatedPosts() {
  const { api } = useApp();
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parseInt(searchParams.get("page") || "1", 10);
  const pageSize = 20;

  const { data: result, isLoading } = useSWR(
    ["posts", page],
    () => api.data.readMany("posts", {
      limit: pageSize,
      offset: (page - 1) * pageSize,
    })
  );

  const setPage = (newPage: number) => {
    setSearchParams({ page: String(newPage) });
  };

  const totalPages = result
    ? Math.ceil(result.meta.total / pageSize)
    : 0;

  return (
    <div>
      {/* ... render posts ... */}
      <Pagination
        page={page}
        totalPages={totalPages}
        onPageChange={setPage}
      />
    </div>
  );
}
```

## Common Patterns

### Configurable Default Limit

Configure default page size in SDK:

```typescript
const api = new Api({
  host: "http://localhost:7654",
  data: {
    defaultQuery: {
      limit: 25,  // Default if not specified
    },
  },
});
```

### Server-Side Pagination (Next.js)

```typescript
// app/posts/page.tsx
export default async function PostsPage({
  searchParams,
}: {
  searchParams: { page?: string };
}) {
  const page = parseInt(searchParams.page || "1", 10);
  const pageSize = 20;

  const response = await fetch(
    `${process.env.BKND_URL}/api/data/posts?` +
    `limit=${pageSize}&offset=${(page - 1) * pageSize}&sort=-created_at`
  );
  const { data, meta } = await response.json();

  const totalPages = Math.ceil(meta.total / pageSize);

  return (
    <>
      <PostsList posts={data} />
      <PaginationLinks
        page={page}
        totalPages={totalPages}
        basePath="/posts"
      />
    </>
  );
}
```

### Paginate with Relations

```typescript
const result = await paginate("posts", page, pageSize, {
  where: { status: { $eq: "published" } },
  sort: { created_at: "desc" },
  with: {
    author: { select: ["id", "name", "avatar"] },
  },
});
```

### Count Total Without Data

If you only need count (e.g., for showing total):

```typescript
const { data } = await api.data.count("posts", {
  status: { $eq: "published" },
});
console.log(`${data.count} total posts`);
```

## Common Pitfalls

### Forgetting Pagination

**Problem:** Loading all records causes performance issues.

**Fix:** Always paginate large datasets:

```typescript
// Wrong - loads everything
const { data } = await api.data.readMany("posts");

// Correct - paginate
const { data } = await api.data.readMany("posts", {
  limit: 20,
  offset: 0,
});
```

### Off-by-One Page Calculation

**Problem:** Using 0-indexed pages.

**Fix:** Use 1-indexed pages with correct offset formula:

```typescript
// Wrong (if page is 1-indexed)
offset: page * pageSize  // Skips first page!

// Correct
offset: (page - 1) * pageSize
```

### Not Tracking Total

**Problem:** Can't show "Page X of Y" without total.

**Fix:** Always use `meta.total` from response:

```typescript
const { data, meta } = await api.data.readMany("posts", query);
const totalPages = Math.ceil(meta.total / pageSize);
```

### Duplicate Items in Infinite Scroll

**Problem:** Same items appear multiple times when data changes.

**Fix:** Use unique keys and deduplicate:

```typescript
setPosts((prev) => {
  const ids = new Set(prev.map(p => p.id));
  const newPosts = data.filter(p => !ids.has(p.id));
  return [...prev, ...newPosts];
});
```

### Page Exceeds Total

**Problem:** Navigating to non-existent page.

**Fix:** Clamp page number:

```typescript
const safePage = Math.min(page, totalPages);
const safeOffset = (safePage - 1) * pageSize;
```

## Verification

1. Check first page returns correct count:
   ```typescript
   const { data, meta } = await api.data.readMany("posts", { limit: 10 });
   console.log(data.length, "of", meta.total);
   ```

2. Verify last page doesn't error:
   ```typescript
   const lastPage = Math.ceil(meta.total / pageSize);
   const { data } = await api.data.readMany("posts", {
     limit: pageSize,
     offset: (lastPage - 1) * pageSize,
   });
   ```

3. Test empty results:
   ```typescript
   const { data } = await api.data.readMany("posts", {
     where: { title: { $eq: "nonexistent" } },
     limit: 10,
   });
   console.log("Empty:", data.length === 0);
   ```

## DOs and DON'Ts

**DO:**
- Always paginate large datasets
- Use `meta.total` for page calculations
- Handle edge cases (empty, last page)
- Use SWR/React Query for caching
- Sync pagination with URL when appropriate
- Pre-fetch next page for smoother UX

**DON'T:**
- Load all records at once
- Use 0-indexed pages (convention is 1-indexed)
- Forget to handle loading states
- Ignore empty state UI
- Skip pagination in admin/debug views (still paginate!)
- Assume data won't change between pages

## Related Skills

- **bknd-crud-read** - Basic read operations
- **bknd-query-filter** - Combine pagination with filtering
- **bknd-bulk-operations** - Paginate bulk operations
- **bknd-client-setup** - Configure SDK with default pagination

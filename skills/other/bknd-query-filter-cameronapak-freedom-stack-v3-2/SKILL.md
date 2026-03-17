---
name: bknd-query-filter
description: Use when building advanced queries with complex filtering conditions in Bknd. Covers all filter operators ($eq, $ne, $gt, $lt, $like, $ilike, $in, $nin, $isnull, $between), logical operators ($or, $and), nested conditions, combining filters, and dynamic query building.
---

# Advanced Query Filtering

Build complex queries with multiple conditions, logical operators, and dynamic filters in Bknd.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists with data
- SDK configured or API endpoint known
- Basic understanding of `readMany` (see `bknd-crud-read`)

## When to Use UI Mode

- Testing filter combinations before coding
- Exploring data patterns
- Quick ad-hoc queries

**UI steps:** Admin Panel > Data > Select Entity > Use filter controls

## When to Use Code Mode

- Complex multi-condition queries
- Dynamic user-driven filters (search, facets)
- Reusable query builders
- API integrations

## Code Approach

### Step 1: Understand Operator Categories

Bknd supports these filter operators:

| Category | Operators |
|----------|-----------|
| Equality | `$eq`, `$ne` |
| Comparison | `$gt`, `$gte`, `$lt`, `$lte` |
| Range | `$between` |
| Pattern | `$like`, `$ilike` |
| Array | `$in`, `$nin` (alias: `$notin`) |
| Null | `$isnull` |
| Logical | `$or`, `$and` (implicit) |

### Step 2: Use Comparison Operators

```typescript
import { Api } from "bknd";
const api = new Api({ host: "http://localhost:7654" });

// Equality (implicit $eq)
const { data } = await api.data.readMany("products", {
  where: { status: "active" },  // Same as { status: { $eq: "active" } }
});

// Not equal
const { data } = await api.data.readMany("products", {
  where: { status: { $ne: "deleted" } },
});

// Numeric comparisons
const { data } = await api.data.readMany("products", {
  where: {
    price: { $gte: 10 },   // price >= 10
    stock: { $gt: 0 },     // stock > 0
  },
});

// Date comparisons
const { data } = await api.data.readMany("orders", {
  where: {
    created_at: { $gte: "2024-01-01" },
    created_at: { $lt: "2024-02-01" },
  },
});
```

### Step 3: Use Range Operator ($between)

```typescript
// Price between 10 and 100 (inclusive)
const { data } = await api.data.readMany("products", {
  where: {
    price: { $between: [10, 100] },
  },
});

// Date range
const { data } = await api.data.readMany("orders", {
  where: {
    created_at: { $between: ["2024-01-01", "2024-12-31"] },
  },
});
```

### Step 4: Use Pattern Matching

```typescript
// LIKE (case-sensitive) - use % as wildcard
const { data } = await api.data.readMany("posts", {
  where: { title: { $like: "%React%" } },
});

// ILIKE (case-insensitive) - preferred for search
const { data } = await api.data.readMany("posts", {
  where: { title: { $ilike: "%react%" } },
});

// Starts with
const { data } = await api.data.readMany("users", {
  where: { name: { $like: "John%" } },
});

// Ends with
const { data } = await api.data.readMany("users", {
  where: { email: { $like: "%@gmail.com" } },
});

// Wildcard alternative: use * instead of %
const { data } = await api.data.readMany("posts", {
  where: { title: { $like: "*React*" } },  // Converted to %React%
});
```

### Step 5: Use Array Operators

```typescript
// In array - match any value
const { data } = await api.data.readMany("posts", {
  where: { status: { $in: ["published", "featured"] } },
});

// Not in array - exclude values
const { data } = await api.data.readMany("posts", {
  where: { status: { $nin: ["deleted", "archived"] } },
});

// Get specific records by IDs
const { data } = await api.data.readMany("products", {
  where: { id: { $in: [1, 5, 10, 15] } },
});
```

### Step 6: Use Null Checks

```typescript
// Is NULL
const { data } = await api.data.readMany("posts", {
  where: { deleted_at: { $isnull: true } },
});

// Is NOT NULL
const { data } = await api.data.readMany("posts", {
  where: { published_at: { $isnull: false } },
});

// Combine: active records (not deleted, has been published)
const { data } = await api.data.readMany("posts", {
  where: {
    deleted_at: { $isnull: true },
    published_at: { $isnull: false },
  },
});
```

### Step 7: Combine with AND (Implicit)

Multiple fields at same level = AND:

```typescript
// status = "published" AND category = "news" AND views > 100
const { data } = await api.data.readMany("posts", {
  where: {
    status: { $eq: "published" },
    category: { $eq: "news" },
    views: { $gt: 100 },
  },
});
```

### Step 8: Use OR Conditions

```typescript
// status = "published" OR featured = true
const { data } = await api.data.readMany("posts", {
  where: {
    $or: [
      { status: { $eq: "published" } },
      { featured: { $eq: true } },
    ],
  },
});

// Multiple OR conditions
const { data } = await api.data.readMany("users", {
  where: {
    $or: [
      { role: { $eq: "admin" } },
      { role: { $eq: "moderator" } },
      { is_verified: { $eq: true } },
    ],
  },
});
```

### Step 9: Combine AND + OR

```typescript
// category = "news" AND (status = "published" OR author_id = currentUser)
const { data } = await api.data.readMany("posts", {
  where: {
    category: { $eq: "news" },
    $or: [
      { status: { $eq: "published" } },
      { author_id: { $eq: currentUserId } },
    ],
  },
});

// Complex: (price < 50 OR on_sale = true) AND in_stock = true AND category IN ["electronics", "books"]
const { data } = await api.data.readMany("products", {
  where: {
    in_stock: { $eq: true },
    category: { $in: ["electronics", "books"] },
    $or: [
      { price: { $lt: 50 } },
      { on_sale: { $eq: true } },
    ],
  },
});
```

### Step 10: Filter by Related Fields (Join)

Use `join` to filter by fields in related entities:

```typescript
// Posts where author.role = "admin"
const { data } = await api.data.readMany("posts", {
  join: ["author"],
  where: {
    "author.role": { $eq: "admin" },
  },
});

// Orders where customer.country = "US" AND product.category = "electronics"
const { data } = await api.data.readMany("orders", {
  join: ["customer", "product"],
  where: {
    "customer.country": { $eq: "US" },
    "product.category": { $eq: "electronics" },
  },
});

// Combine with regular filters
const { data } = await api.data.readMany("posts", {
  join: ["author"],
  where: {
    status: { $eq: "published" },
    "author.is_verified": { $eq: true },
  },
});
```

## Dynamic Query Building

### Build Queries Programmatically

```typescript
type WhereClause = Record<string, any>;

function buildProductQuery(filters: {
  search?: string;
  minPrice?: number;
  maxPrice?: number;
  categories?: string[];
  inStock?: boolean;
}): WhereClause {
  const where: WhereClause = {};

  if (filters.search) {
    where.name = { $ilike: `%${filters.search}%` };
  }

  if (filters.minPrice !== undefined) {
    where.price = { ...where.price, $gte: filters.minPrice };
  }

  if (filters.maxPrice !== undefined) {
    where.price = { ...where.price, $lte: filters.maxPrice };
  }

  if (filters.categories?.length) {
    where.category = { $in: filters.categories };
  }

  if (filters.inStock !== undefined) {
    where.stock = filters.inStock ? { $gt: 0 } : { $eq: 0 };
  }

  return where;
}

// Usage
const filters = { search: "laptop", minPrice: 500, categories: ["electronics"] };
const { data } = await api.data.readMany("products", {
  where: buildProductQuery(filters),
  sort: { price: "asc" },
  limit: 20,
});
```

### Conditional OR Builder

```typescript
function buildOrConditions(conditions: WhereClause[]): WhereClause {
  const validConditions = conditions.filter(c => Object.keys(c).length > 0);

  if (validConditions.length === 0) return {};
  if (validConditions.length === 1) return validConditions[0];

  return { $or: validConditions };
}

// Search across multiple fields
const searchTerm = "john";
const { data } = await api.data.readMany("users", {
  where: buildOrConditions([
    { name: { $ilike: `%${searchTerm}%` } },
    { email: { $ilike: `%${searchTerm}%` } },
    { username: { $ilike: `%${searchTerm}%` } },
  ]),
});
```

### Faceted Search Pattern

```typescript
type Facets = {
  category?: string;
  brand?: string;
  priceRange?: "budget" | "mid" | "premium";
  rating?: number;
};

const PRICE_RANGES = {
  budget: { $lt: 50 },
  mid: { $between: [50, 200] },
  premium: { $gt: 200 },
};

async function facetedSearch(query: string, facets: Facets) {
  const where: WhereClause = {};

  // Text search
  if (query) {
    where.name = { $ilike: `%${query}%` };
  }

  // Facet filters
  if (facets.category) {
    where.category = { $eq: facets.category };
  }

  if (facets.brand) {
    where.brand = { $eq: facets.brand };
  }

  if (facets.priceRange) {
    where.price = PRICE_RANGES[facets.priceRange];
  }

  if (facets.rating) {
    where.rating = { $gte: facets.rating };
  }

  return api.data.readMany("products", { where, limit: 50 });
}
```

## React Integration

### Search Filter Component

```tsx
import { useState, useCallback } from "react";
import { useApp } from "bknd/react";
import useSWR from "swr";
import { useDebouncedValue } from "@mantine/hooks";

type Filters = {
  search: string;
  status: string;
  minDate: string;
};

function FilteredList() {
  const { api } = useApp();
  const [filters, setFilters] = useState<Filters>({
    search: "",
    status: "",
    minDate: "",
  });
  const [debouncedFilters] = useDebouncedValue(filters, 300);

  const buildWhere = useCallback((f: Filters) => {
    const where: Record<string, any> = {};

    if (f.search) {
      where.title = { $ilike: `%${f.search}%` };
    }
    if (f.status) {
      where.status = { $eq: f.status };
    }
    if (f.minDate) {
      where.created_at = { $gte: f.minDate };
    }

    return where;
  }, []);

  const { data: posts, isLoading } = useSWR(
    ["posts", debouncedFilters],
    () => api.data.readMany("posts", {
      where: buildWhere(debouncedFilters),
      sort: { created_at: "desc" },
      limit: 20,
    }).then(r => r.data)
  );

  return (
    <div>
      <input
        placeholder="Search..."
        value={filters.search}
        onChange={e => setFilters(f => ({ ...f, search: e.target.value }))}
      />
      <select
        value={filters.status}
        onChange={e => setFilters(f => ({ ...f, status: e.target.value }))}
      >
        <option value="">All statuses</option>
        <option value="draft">Draft</option>
        <option value="published">Published</option>
      </select>
      <input
        type="date"
        value={filters.minDate}
        onChange={e => setFilters(f => ({ ...f, minDate: e.target.value }))}
      />

      {isLoading ? <p>Loading...</p> : (
        <ul>
          {posts?.map(post => <li key={post.id}>{post.title}</li>)}
        </ul>
      )}
    </div>
  );
}
```

## REST API Approach

### Query String Format

```bash
# Simple filter
curl "http://localhost:7654/api/data/posts?where=%7B%22status%22%3A%22published%22%7D"

# URL-decoded: where={"status":"published"}
```

### Complex Query via POST

For complex queries, use POST to `/api/data/:entity/query`:

```bash
curl -X POST http://localhost:7654/api/data/posts/query \
  -H "Content-Type: application/json" \
  -d '{
    "where": {
      "category": {"$eq": "news"},
      "$or": [
        {"status": {"$eq": "published"}},
        {"featured": {"$eq": true}}
      ]
    },
    "sort": {"created_at": "desc"},
    "limit": 20
  }'
```

## Full Example

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// 1. Simple equality filter
const published = await api.data.readMany("posts", {
  where: { status: "published" },
});

// 2. Numeric range
const midPriced = await api.data.readMany("products", {
  where: { price: { $between: [50, 200] } },
});

// 3. Text search (case-insensitive)
const searchResults = await api.data.readMany("products", {
  where: { name: { $ilike: "%laptop%" } },
});

// 4. Multiple values
const specificCategories = await api.data.readMany("products", {
  where: { category: { $in: ["electronics", "computers"] } },
});

// 5. Exclude soft-deleted
const activeRecords = await api.data.readMany("posts", {
  where: { deleted_at: { $isnull: true } },
});

// 6. Complex AND + OR
const complexQuery = await api.data.readMany("orders", {
  where: {
    created_at: { $gte: "2024-01-01" },
    status: { $nin: ["cancelled", "refunded"] },
    $or: [
      { total: { $gt: 100 } },
      { is_priority: { $eq: true } },
    ],
  },
  sort: { created_at: "desc" },
  limit: 50,
});

// 7. Filter by related entity
const adminPosts = await api.data.readMany("posts", {
  join: ["author"],
  where: {
    "author.role": { $eq: "admin" },
    status: { $eq: "published" },
  },
});
```

## Common Pitfalls

### Combining Same-Field Operators Wrong

**Problem:** Overwriting previous condition.

```typescript
// Wrong - second assignment overwrites first
where: {
  price: { $gte: 10 },
  price: { $lte: 100 },  // Overwrites!
}

// Correct - use $between or spread
where: {
  price: { $between: [10, 100] },
}
// Or
where: {
  price: { $gte: 10, $lte: 100 },
}
```

### $or at Wrong Level

**Problem:** `$or` must be at top level of where clause.

```typescript
// Wrong - nested $or
where: {
  status: {
    $or: [{ $eq: "a" }, { $eq: "b" }],  // Invalid!
  },
}

// Correct - use $in for same field
where: {
  status: { $in: ["a", "b"] },
}

// Correct - $or at top level for different fields
where: {
  $or: [
    { status: { $eq: "a" } },
    { featured: { $eq: true } },
  ],
}
```

### Missing Join for Related Filter

**Problem:** Filtering by related field without `join`.

```typescript
// Wrong - won't work
where: { "author.role": { $eq: "admin" } }

// Correct - add join
{
  join: ["author"],
  where: { "author.role": { $eq: "admin" } },
}
```

### Case-Sensitive Search

**Problem:** `$like` is case-sensitive.

```typescript
// May miss results
where: { title: { $like: "%React%" } }

// Use $ilike for case-insensitive
where: { title: { $ilike: "%react%" } }
```

### Empty Filter Objects

**Problem:** Empty where returns all records.

```typescript
// Returns everything (no filter)
where: {}

// Always validate filters exist
const where = buildFilters(userInput);
if (Object.keys(where).length === 0) {
  // Handle: show default view or require at least one filter
}
```

## Verification

Test filters in admin panel first:

1. Admin Panel > Data > Select Entity
2. Use filter controls to build query
3. Verify expected results
4. Translate to code

Or log the where clause:

```typescript
const where = buildFilters(input);
console.log("Query:", JSON.stringify(where, null, 2));
const { data } = await api.data.readMany("posts", { where });
```

## DOs and DON'Ts

**DO:**
- Use `$ilike` for user-facing search (case-insensitive)
- Use `$in` instead of multiple `$or` for same field
- Use `$between` for numeric/date ranges
- Build queries dynamically for filter UIs
- Validate/sanitize user input before building queries
- Use `join` when filtering by related fields

**DON'T:**
- Use `$like` for user search (case-sensitive issues)
- Nest `$or` inside field conditions
- Forget `join` for related field filters
- Trust user input directly in queries
- Build excessively complex nested conditions
- Forget that empty where = return all

## Related Skills

- **bknd-crud-read** - Basic read operations
- **bknd-pagination** - Paginate filtered results
- **bknd-define-relationship** - Set up relations for join filters
- **bknd-row-level-security** - Apply automatic filters via policies

---
name: add-query-filter
description: Add custom query parameter filters to entity endpoints. Use when extending search/filter capabilities beyond the base pagination. Triggers on "add filter", "query parameter", "search filter", "filter by".
---

# Add Query Filter

Adds custom query parameter filters to entity schemas and repository implementations.

## Quick Reference

**Files to modify**:

1. `src/schemas/{entity}.schema.ts` - Add filter to query params schema
2. `src/repositories/mockdb/{entity}.mockdb.repository.ts` - Implement filter logic
3. `src/repositories/mongodb/{entity}.mongodb.repository.ts` - Implement filter logic
4. `tests/schemas/{entity}.schema.test.ts` - Test new filter
5. `tests/repositories/{entity}.*.repository.test.ts` - Test filter behavior

## Prerequisites

- Entity schema exists with `{entity}QueryParamsSchema`
- Repository implementations exist

## Instructions

### Step 1: Add Filter to Query Params Schema

Update `src/schemas/{entity}.schema.ts`:

```typescript
import { z } from "zod";
import { queryParamsSchema } from "@/schemas/shared.schema";

// Extend the base query params with entity-specific filters
export const {entity}QueryParamsSchema = queryParamsSchema.extend({
  // Existing filters...
  createdBy: z.string().optional(),

  // Add new filter
  {filterName}: z.string().optional(),
  // OR for enum filter
  status: z.enum(["draft", "published", "archived"]).optional(),
  // OR for boolean filter (from query string)
  isActive: z.coerce.boolean().optional(),
  // OR for date range
  createdAfter: z.coerce.date().optional(),
  createdBefore: z.coerce.date().optional(),
  // OR for numeric range
  minPrice: z.coerce.number().optional(),
  maxPrice: z.coerce.number().optional(),
});

export type {Entity}QueryParamsType = z.infer<typeof {entity}QueryParamsSchema>;
```

### Step 2: Implement Filter in MockDB Repository

Update `src/repositories/mockdb/{entity}.mockdb.repository.ts`:

```typescript
async findAll(query: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>> {
  let filtered = [...this.{entities}];

  // Existing filters
  if (query.createdBy) {
    filtered = filtered.filter((item) => item.createdBy === query.createdBy);
  }

  if (query.search) {
    const searchLower = query.search.toLowerCase();
    filtered = filtered.filter((item) =>
      item.content.toLowerCase().includes(searchLower)
    );
  }

  // NEW: Add your filter
  if (query.{filterName}) {
    filtered = filtered.filter((item) => item.{fieldName} === query.{filterName});
  }

  // For enum filter
  if (query.status) {
    filtered = filtered.filter((item) => item.status === query.status);
  }

  // For boolean filter
  if (query.isActive !== undefined) {
    filtered = filtered.filter((item) => item.isActive === query.isActive);
  }

  // For date range
  if (query.createdAfter) {
    filtered = filtered.filter((item) => item.createdAt >= query.createdAfter!);
  }
  if (query.createdBefore) {
    filtered = filtered.filter((item) => item.createdAt <= query.createdBefore!);
  }

  // For numeric range
  if (query.minPrice !== undefined) {
    filtered = filtered.filter((item) => item.price >= query.minPrice!);
  }
  if (query.maxPrice !== undefined) {
    filtered = filtered.filter((item) => item.price <= query.maxPrice!);
  }

  // ... sorting and pagination continue as before
}
```

### Step 3: Implement Filter in MongoDB Repository

Update `src/repositories/mongodb/{entity}.mongodb.repository.ts`:

```typescript
async findAll(query: {Entity}QueryParamsType): Promise<PaginatedResultType<{Entity}Type>> {
  const collection = await this.getCollection();
  const filter: Filter<{Entity}Document> = {};

  // Existing filters
  if (query.createdBy) {
    filter.createdBy = query.createdBy;
  }

  if (query.search) {
    filter.$text = { $search: query.search };
  }

  // NEW: Add your filter
  if (query.{filterName}) {
    filter.{fieldName} = query.{filterName};
  }

  // For enum filter
  if (query.status) {
    filter.status = query.status;
  }

  // For boolean filter
  if (query.isActive !== undefined) {
    filter.isActive = query.isActive;
  }

  // For date range
  if (query.createdAfter || query.createdBefore) {
    filter.createdAt = {};
    if (query.createdAfter) {
      filter.createdAt.$gte = query.createdAfter;
    }
    if (query.createdBefore) {
      filter.createdAt.$lte = query.createdBefore;
    }
  }

  // For numeric range
  if (query.minPrice !== undefined || query.maxPrice !== undefined) {
    filter.price = {};
    if (query.minPrice !== undefined) {
      filter.price.$gte = query.minPrice;
    }
    if (query.maxPrice !== undefined) {
      filter.price.$lte = query.maxPrice;
    }
  }

  // ... continue with sorting, pagination
}
```

### Step 4: Add Schema Tests

Update `tests/schemas/{entity}.schema.test.ts`:

```typescript
describe("{entity}QueryParamsSchema", () => {
  // ... existing tests ...

  it("accepts {filterName} filter", () => {
    const parsed = {entity}QueryParamsSchema.parse({
      {filterName}: "filter-value",
    });
    expect(parsed.{filterName}).toBe("filter-value");
  });

  // For enum filter
  it("accepts valid status values", () => {
    expect({entity}QueryParamsSchema.parse({ status: "draft" }).status).toBe("draft");
    expect({entity}QueryParamsSchema.parse({ status: "published" }).status).toBe("published");
  });

  it("rejects invalid status values", () => {
    expect(() => {entity}QueryParamsSchema.parse({ status: "invalid" })).toThrow();
  });

  // For boolean filter
  it("coerces isActive to boolean", () => {
    expect({entity}QueryParamsSchema.parse({ isActive: "true" }).isActive).toBe(true);
    expect({entity}QueryParamsSchema.parse({ isActive: "false" }).isActive).toBe(false);
  });

  // For date filter
  it("coerces date strings to Date objects", () => {
    const parsed = {entity}QueryParamsSchema.parse({
      createdAfter: "2024-01-01",
    });
    expect(parsed.createdAfter).toBeInstanceOf(Date);
  });

  // For numeric filter
  it("coerces price filters to numbers", () => {
    const parsed = {entity}QueryParamsSchema.parse({
      minPrice: "10",
      maxPrice: "100",
    });
    expect(parsed.minPrice).toBe(10);
    expect(parsed.maxPrice).toBe(100);
  });
});
```

### Step 5: Add Repository Tests

Update repository test files:

```typescript
describe("findAll", () => {
  // ... existing tests ...

  it("filters by {filterName}", async () => {
    await repo.create({ content: "A", {fieldName}: "value1" }, userId);
    await repo.create({ content: "B", {fieldName}: "value2" }, userId);
    await repo.create({ content: "C", {fieldName}: "value1" }, userId);

    const result = await repo.findAll({ {filterName}: "value1" });

    expect(result.data.length).toBe(2);
    expect(result.data.every((item) => item.{fieldName} === "value1")).toBe(true);
  });

  // For enum filter
  it("filters by status", async () => {
    await repo.create({ content: "A", status: "draft" }, userId);
    await repo.create({ content: "B", status: "published" }, userId);

    const result = await repo.findAll({ status: "published" });

    expect(result.data.length).toBe(1);
    expect(result.data[0].status).toBe("published");
  });

  // For date range
  it("filters by date range", async () => {
    // Create items with different dates
    const old = await repo.create({ content: "Old" }, userId);
    await new Promise((r) => setTimeout(r, 10));
    const recent = await repo.create({ content: "Recent" }, userId);

    const result = await repo.findAll({
      createdAfter: old.createdAt,
    });

    expect(result.data.length).toBeGreaterThanOrEqual(1);
  });

  // For numeric range
  it("filters by price range", async () => {
    await repo.create({ content: "Cheap", price: 10 }, userId);
    await repo.create({ content: "Mid", price: 50 }, userId);
    await repo.create({ content: "Expensive", price: 100 }, userId);

    const result = await repo.findAll({ minPrice: 20, maxPrice: 80 });

    expect(result.data.length).toBe(1);
    expect(result.data[0].content).toBe("Mid");
  });
});
```

## Common Filter Patterns

### String Exact Match

```typescript
// Schema
categoryId: z.string().optional(),

// MockDB
if (query.categoryId) {
  filtered = filtered.filter((item) => item.categoryId === query.categoryId);
}

// MongoDB
if (query.categoryId) {
  filter.categoryId = query.categoryId;
}
```

### String Array (IN query)

```typescript
// Schema
tags: z.array(z.string()).optional(),
// OR from comma-separated string
tags: z.string().transform(s => s.split(",")).optional(),

// MockDB
if (query.tags?.length) {
  filtered = filtered.filter((item) =>
    query.tags!.some(tag => item.tags.includes(tag))
  );
}

// MongoDB
if (query.tags?.length) {
  filter.tags = { $in: query.tags };
}
```

### Partial Text Match

```typescript
// Schema
title: z.string().optional(),

// MockDB
if (query.title) {
  const titleLower = query.title.toLowerCase();
  filtered = filtered.filter((item) =>
    item.title.toLowerCase().includes(titleLower)
  );
}

// MongoDB (requires text index for $text, or use regex)
if (query.title) {
  filter.title = { $regex: query.title, $options: "i" };
}
```

### Null/Not Null Check

```typescript
// Schema
hasParent: z.coerce.boolean().optional(),

// MockDB
if (query.hasParent !== undefined) {
  if (query.hasParent) {
    filtered = filtered.filter((item) => item.parentId != null);
  } else {
    filtered = filtered.filter((item) => item.parentId == null);
  }
}

// MongoDB
if (query.hasParent !== undefined) {
  if (query.hasParent) {
    filter.parentId = { $ne: null };
  } else {
    filter.parentId = null;
  }
}
```

## Adding MongoDB Indexes for Filters

If a filter is frequently used, add an index:

```typescript
// In MongoDB repository constructor or initialization
async ensureIndexes() {
  const collection = await this.getCollection();

  // Single field index
  await collection.createIndex({ status: 1 });

  // Compound index for common filter combinations
  await collection.createIndex({ createdBy: 1, status: 1 });

  // For date range queries
  await collection.createIndex({ createdAt: -1 });
}
```

## Filter Validation Tips

### Coercion for Query Strings

Query parameters are always strings. Use `z.coerce` for non-string types:

```typescript
// Numbers
minPrice: z.coerce.number().optional(),

// Booleans
isActive: z.coerce.boolean().optional(),

// Dates
createdAfter: z.coerce.date().optional(),
```

### Default Values

```typescript
// With default
status: z.enum(["all", "active", "inactive"]).default("all"),

// Optional without default
status: z.enum(["draft", "published"]).optional(),
```

### Validation Constraints

```typescript
// Positive numbers only
minPrice: z.coerce.number().positive().optional(),

// Max length
search: z.string().max(100).optional(),

// Future dates only
eventDate: z.coerce.date().min(new Date()).optional(),
```

## What NOT to Do

- Do NOT forget to add the filter to both MockDB and MongoDB implementations
- Do NOT skip coercion for query string values
- Do NOT use complex filters without indexes in MongoDB
- Do NOT forget to test the filter behavior
- Do NOT filter on fields that don't exist in the schema

## See Also

- `create-schema` - Creating entity schemas
- `create-mockdb-repository` - MockDB repository implementation
- `create-mongodb-repository` - MongoDB repository implementation
- `test-schema` - Testing schema validation
- `test-mockdb-repository` - Testing repository filters

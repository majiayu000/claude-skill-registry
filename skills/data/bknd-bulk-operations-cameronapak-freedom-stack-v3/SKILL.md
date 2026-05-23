---
name: bknd-bulk-operations
description: Use when performing bulk insert, update, or delete operations in Bknd. Covers createMany, updateMany, deleteMany, batch processing with progress, chunking large datasets, error handling strategies, and transaction-like patterns.
---

# Bulk Operations

Perform large-scale insert, update, and delete operations efficiently using Bknd's bulk APIs.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists (use `bknd-create-entity` first)
- SDK configured or API endpoint known

## When to Use UI Mode

UI mode not recommended for bulk operations. Use Admin Panel only for:
- Importing small CSV files (<100 records)
- Manual data cleanup

## When to Use Code Mode

- Migrating data from another system
- Seeding large datasets
- Batch updates (publish all drafts, archive old records)
- Mass deletion (cleanup, GDPR requests)
- ETL pipelines

## Code Approach

### Bulk Insert: createMany

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// Insert multiple records in one call
const { ok, data, error } = await api.data.createMany("products", [
  { name: "Product A", price: 10, stock: 100 },
  { name: "Product B", price: 20, stock: 50 },
  { name: "Product C", price: 15, stock: 75 },
]);

if (ok) {
  console.log(`Created ${data.length} products`);
  // data contains array of created records with IDs
}
```

### Bulk Update: updateMany

```typescript
// Update all records matching where clause
const { ok, data } = await api.data.updateMany(
  "posts",
  { status: { $eq: "draft" } },     // where clause (required)
  { status: "archived" }             // update data
);

// Archive old posts
await api.data.updateMany(
  "posts",
  {
    status: { $eq: "published" },
    created_at: { $lt: "2024-01-01" },
  },
  { status: "archived" }
);

// Increment view count for multiple posts
await api.data.updateMany(
  "posts",
  { id: { $in: [1, 2, 3, 4, 5] } },
  { featured: true }
);
```

### Bulk Delete: deleteMany

```typescript
// Delete all records matching where clause
const { ok, data } = await api.data.deleteMany("logs", {
  created_at: { $lt: "2023-01-01" },  // Delete old logs
});

// Delete by IDs
await api.data.deleteMany("temp_files", {
  id: { $in: [10, 11, 12, 13] },
});

// Delete archived items
await api.data.deleteMany("posts", {
  status: { $eq: "archived" },
  deleted_at: { $isnull: false },
});
```

**Warning:** `where` clause is required - prevents accidental delete-all.

## Chunked Processing

For large datasets, process in chunks to avoid timeouts and memory issues:

### Basic Chunking

```typescript
async function bulkInsertChunked(
  api: Api,
  entity: string,
  items: object[],
  chunkSize = 100
): Promise<object[]> {
  const results: object[] = [];

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    const { ok, data, error } = await api.data.createMany(entity, chunk);

    if (!ok) {
      throw new Error(`Chunk ${i / chunkSize + 1} failed: ${error.message}`);
    }

    results.push(...data);
  }

  return results;
}

// Usage
const products = generateProducts(5000);  // Large dataset
const created = await bulkInsertChunked(api, "products", products);
console.log(`Created ${created.length} products`);
```

### With Progress Callback

```typescript
type ProgressCallback = (done: number, total: number, chunk: number) => void;

async function bulkInsertWithProgress(
  api: Api,
  entity: string,
  items: object[],
  onProgress?: ProgressCallback,
  chunkSize = 100
): Promise<{ success: object[]; failed: object[] }> {
  const success: object[] = [];
  const failed: object[] = [];
  const totalChunks = Math.ceil(items.length / chunkSize);

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunkNum = Math.floor(i / chunkSize) + 1;
    const chunk = items.slice(i, i + chunkSize);

    const { ok, data, error } = await api.data.createMany(entity, chunk);

    if (ok) {
      success.push(...data);
    } else {
      failed.push(...chunk);
      console.warn(`Chunk ${chunkNum} failed:`, error.message);
    }

    onProgress?.(Math.min(i + chunkSize, items.length), items.length, chunkNum);
  }

  return { success, failed };
}

// Usage with progress
await bulkInsertWithProgress(
  api,
  "products",
  products,
  (done, total, chunk) => {
    const percent = Math.round((done / total) * 100);
    console.log(`Progress: ${percent}% (chunk ${chunk})`);
  }
);
```

### Parallel Chunk Processing

Process multiple chunks concurrently (use with caution):

```typescript
async function bulkInsertParallel(
  api: Api,
  entity: string,
  items: object[],
  chunkSize = 100,
  concurrency = 3
): Promise<object[]> {
  const chunks: object[][] = [];
  for (let i = 0; i < items.length; i += chunkSize) {
    chunks.push(items.slice(i, i + chunkSize));
  }

  const results: object[] = [];

  // Process in batches of concurrent requests
  for (let i = 0; i < chunks.length; i += concurrency) {
    const batch = chunks.slice(i, i + concurrency);
    const promises = batch.map((chunk) =>
      api.data.createMany(entity, chunk)
    );

    const responses = await Promise.all(promises);
    for (const { ok, data } of responses) {
      if (ok) results.push(...data);
    }
  }

  return results;
}
```

## REST API Approach

### Bulk Insert

```bash
curl -X POST http://localhost:7654/api/data/products \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Product A", "price": 10},
    {"name": "Product B", "price": 20}
  ]'
```

### Bulk Update

```bash
curl -X PATCH http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{
    "where": {"status": {"$eq": "draft"}},
    "data": {"status": "archived"}
  }'
```

### Bulk Delete

```bash
curl -X DELETE http://localhost:7654/api/data/logs \
  -H "Content-Type: application/json" \
  -d '{"where": {"created_at": {"$lt": "2023-01-01"}}}'
```

## Server-Side Seeding

For initial data population, use the seed function:

```typescript
import { App, em, entity, text, number } from "bknd";

const schema = em({
  products: entity("products", {
    name: text().required(),
    price: number().required(),
    stock: number({ default_value: 0 }),
  }),
});

new App({
  ...schema,
  options: {
    seed: async (ctx) => {
      // Check if already seeded
      const { data } = await ctx.em.repo("products").count();
      if (data.count > 0) return;

      // Bulk insert via mutator
      await ctx.em.mutator("products").insertMany([
        { name: "Widget", price: 9.99, stock: 100 },
        { name: "Gadget", price: 19.99, stock: 50 },
        { name: "Gizmo", price: 14.99, stock: 75 },
      ]);

      console.log("Seeded products");
    },
  },
});
```

## Error Handling Strategies

### All-or-Nothing (Fail Fast)

Stop on first error:

```typescript
async function bulkInsertStrict(api: Api, entity: string, items: object[]) {
  for (let i = 0; i < items.length; i += 100) {
    const chunk = items.slice(i, i + 100);
    const { ok, error } = await api.data.createMany(entity, chunk);

    if (!ok) {
      throw new Error(`Failed at chunk ${i / 100 + 1}: ${error.message}`);
    }
  }
}
```

### Best Effort (Continue on Error)

Collect failures, continue processing:

```typescript
async function bulkInsertBestEffort(api: Api, entity: string, items: object[]) {
  const results = { success: [] as object[], failed: [] as object[] };

  for (let i = 0; i < items.length; i += 100) {
    const chunk = items.slice(i, i + 100);
    const { ok, data } = await api.data.createMany(entity, chunk);

    if (ok) {
      results.success.push(...data);
    } else {
      results.failed.push(...chunk);
    }
  }

  return results;
}
```

### Individual Fallback

Fall back to individual inserts on chunk failure:

```typescript
async function bulkInsertWithFallback(api: Api, entity: string, items: object[]) {
  const success: object[] = [];
  const failed: object[] = [];

  for (let i = 0; i < items.length; i += 100) {
    const chunk = items.slice(i, i + 100);
    const { ok, data } = await api.data.createMany(entity, chunk);

    if (ok) {
      success.push(...data);
    } else {
      // Fall back to individual inserts
      for (const item of chunk) {
        const { ok: itemOk, data: itemData } = await api.data.createOne(
          entity,
          item
        );
        if (itemOk) {
          success.push(itemData);
        } else {
          failed.push(item);
        }
      }
    }
  }

  return { success, failed };
}
```

## Common Patterns

### Data Migration

```typescript
async function migrateData(
  sourceApi: Api,
  targetApi: Api,
  entity: string,
  transform?: (record: object) => object
) {
  let offset = 0;
  const limit = 100;
  let total = 0;

  while (true) {
    const { data, meta } = await sourceApi.data.readMany(entity, {
      limit,
      offset,
    });

    if (data.length === 0) break;

    const transformed = transform ? data.map(transform) : data;
    await targetApi.data.createMany(entity, transformed);

    total += data.length;
    offset += limit;

    console.log(`Migrated ${total}/${meta.total} records`);
  }

  return total;
}
```

### Conditional Bulk Update

```typescript
// Publish all posts by specific author
await api.data.updateMany(
  "posts",
  {
    author_id: { $eq: authorId },
    status: { $eq: "draft" },
  },
  { status: "published", published_at: new Date().toISOString() }
);

// Mark inactive users
const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
  .toISOString();

await api.data.updateMany(
  "users",
  { last_login: { $lt: thirtyDaysAgo } },
  { status: "inactive" }
);
```

### Soft Delete Cleanup

```typescript
// Permanently delete soft-deleted records older than 30 days
const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
  .toISOString();

await api.data.deleteMany("posts", {
  deleted_at: { $lt: thirtyDaysAgo, $isnull: false },
});
```

### Bulk Update Relations

```typescript
// Add tag to multiple posts
const postIds = [1, 2, 3, 4, 5];

for (const postId of postIds) {
  await api.data.updateOne("posts", postId, {
    tags: { $add: [newTagId] },
  });
}
```

Note: Bknd doesn't support bulk relation updates in a single call. Loop through records.

### Transaction-like Pattern

Bknd doesn't have explicit transactions. Use this pattern for related operations:

```typescript
async function createOrderWithItems(
  api: Api,
  orderData: object,
  items: object[]
) {
  // Create order
  const { ok, data: order, error } = await api.data.createOne("orders", orderData);
  if (!ok) throw new Error(`Order failed: ${error.message}`);

  // Create order items
  const itemsWithOrder = items.map((item) => ({
    ...item,
    order: { $set: order.id },
  }));

  const { ok: itemsOk, error: itemsError } = await api.data.createMany(
    "order_items",
    itemsWithOrder
  );

  if (!itemsOk) {
    // Rollback: delete the order
    await api.data.deleteOne("orders", order.id);
    throw new Error(`Items failed, order rolled back: ${itemsError.message}`);
  }

  return order;
}
```

## React Integration

### Bulk Import Component

```tsx
import { useApp } from "bknd/react";
import { useState } from "react";

function BulkImport({ entity }: { entity: string }) {
  const { api } = useApp();
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<"idle" | "importing" | "done">("idle");

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    const text = await file.text();
    const items = JSON.parse(text);  // Assume JSON array

    setStatus("importing");
    setProgress(0);

    const chunkSize = 100;
    for (let i = 0; i < items.length; i += chunkSize) {
      const chunk = items.slice(i, i + chunkSize);
      await api.data.createMany(entity, chunk);
      setProgress(Math.round(((i + chunkSize) / items.length) * 100));
    }

    setStatus("done");
  }

  return (
    <div>
      <input type="file" accept=".json" onChange={handleFileUpload} />
      {status === "importing" && <p>Importing... {progress}%</p>}
      {status === "done" && <p>Import complete!</p>}
    </div>
  );
}
```

### Bulk Delete with Confirmation

```tsx
function BulkDeleteButton({
  entity,
  where,
  onComplete,
}: {
  entity: string;
  where: object;
  onComplete: () => void;
}) {
  const { api } = useApp();
  const [loading, setLoading] = useState(false);

  async function handleDelete() {
    // Get count first
    const { data } = await api.data.count(entity, where);
    const confirmed = window.confirm(
      `Delete ${data.count} records? This cannot be undone.`
    );

    if (!confirmed) return;

    setLoading(true);
    await api.data.deleteMany(entity, where);
    setLoading(false);
    onComplete();
  }

  return (
    <button onClick={handleDelete} disabled={loading}>
      {loading ? "Deleting..." : "Delete All Matching"}
    </button>
  );
}
```

## Performance Tips

1. **Optimal chunk size:** 100-500 records per chunk (balance speed vs memory)
2. **Avoid parallel writes** to same entity (can cause locks)
3. **Use server-side seed** for initial large datasets
4. **Index fields** used in bulk update/delete where clauses
5. **Monitor memory** when processing very large datasets client-side

## Common Pitfalls

### Missing Where Clause on deleteMany

**Problem:** Attempt to delete all records blocked.

**Fix:** Always provide where clause:

```typescript
// Wrong - no where clause
await api.data.deleteMany("posts");  // Error!

// Correct
await api.data.deleteMany("posts", { status: { $eq: "archived" } });

// To delete all (intentionally):
await api.data.deleteMany("posts", { id: { $gt: 0 } });
```

### Memory Issues with Large Datasets

**Problem:** Out of memory when processing millions of records.

**Fix:** Process in chunks, avoid loading all at once:

```typescript
// Wrong - loads everything
const { data } = await api.data.readMany("logs", { limit: 1000000 });
await api.data.deleteMany("logs", { id: { $in: data.map((d) => d.id) } });

// Correct - delete directly with where
await api.data.deleteMany("logs", { created_at: { $lt: cutoffDate } });
```

### No Unique Constraint Handling

**Problem:** Bulk insert fails on duplicate key.

**Fix:** Deduplicate before insert or use upsert pattern:

```typescript
// Deduplicate by email before insert
const uniqueItems = [...new Map(items.map((i) => [i.email, i])).values()];
await api.data.createMany("users", uniqueItems);
```

### Timeout on Very Large Operations

**Problem:** Request times out on huge bulk operation.

**Fix:** Use smaller chunks with longer delays:

```typescript
for (let i = 0; i < items.length; i += 50) {
  await api.data.createMany(entity, items.slice(i, i + 50));
  await new Promise((r) => setTimeout(r, 100));  // Small delay
}
```

## DOs and DON'Ts

**DO:**
- Use chunking for large datasets (>100 records)
- Provide where clause for updateMany/deleteMany
- Track progress for user feedback
- Handle partial failures gracefully
- Use server-side seed for initial data

**DON'T:**
- Load millions of records into memory
- Run parallel bulk writes to same entity
- Assume bulk operations are atomic
- Forget to handle unique constraint errors
- Skip confirmation for destructive bulk deletes

## Related Skills

- **bknd-crud-create** - Single record insertion
- **bknd-crud-update** - Single record updates
- **bknd-crud-delete** - Single record deletion
- **bknd-seed-data** - Server-side initial data population
- **bknd-query-filter** - Build where clauses for bulk operations

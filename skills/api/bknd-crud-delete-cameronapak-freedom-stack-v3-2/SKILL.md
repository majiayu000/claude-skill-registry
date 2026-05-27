---
name: bknd-crud-delete
description: Use when deleting records from a Bknd entity via the SDK or REST API. Covers deleteOne, deleteMany, soft delete patterns, cascade considerations, response handling, and common patterns.
---

# CRUD Delete

Delete records from your Bknd database using the SDK or REST API.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists with records to delete
- SDK configured or API endpoint known
- Record ID or filter criteria known
- Understanding of any relationships/dependencies

## When to Use UI Mode

- Quick one-off deletions
- Manual data cleanup
- Visual verification of what's being deleted

**UI steps:** Admin Panel > Data > Select Entity > Click record > Delete button > Confirm

## When to Use Code Mode

- Application logic for user-initiated deletes
- Automated data cleanup/maintenance
- Bulk deletions
- Soft delete implementations

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

### Step 2: Delete Single Record

Use `deleteOne(entity, id)`:

```typescript
const { ok, data, error } = await api.data.deleteOne("posts", 1);

if (ok) {
  console.log("Deleted post:", data.id);
} else {
  console.error("Failed:", error.message);
}
```

### Step 3: Handle Response

The response object:

```typescript
type DeleteResponse = {
  ok: boolean;       // Success/failure
  data?: {           // Deleted record (if ok)
    id: number;
    // ...all fields of deleted record
  };
  error?: {          // Error info (if !ok)
    message: string;
    code: string;
  };
};
```

### Step 4: Delete Multiple Records (Bulk)

Use `deleteMany(entity, where)`:

```typescript
// Delete all archived posts
const { ok, data } = await api.data.deleteMany("posts", {
  status: { $eq: "archived" },
});

// data contains deleted records
console.log("Deleted", data.length, "posts");
```

**Important:** `where` clause is required to prevent accidental delete-all.

```typescript
// Delete old sessions
await api.data.deleteMany("sessions", {
  last_active: { $lt: "2024-01-01" },
});

// Delete by multiple conditions
await api.data.deleteMany("logs", {
  level: { $eq: "debug" },
  created_at: { $lt: "2024-06-01" },
});
```

### Step 5: Verify Before Delete

Always verify record exists or check count before deleting:

```typescript
// Check record exists
const { data: existing } = await api.data.readOne("posts", id);
if (!existing) {
  throw new Error("Post not found");
}
await api.data.deleteOne("posts", id);

// Check count before bulk delete
const { data: countResult } = await api.data.count("logs", {
  level: { $eq: "debug" },
});
console.log(`About to delete ${countResult.count} records`);
```

## REST API Approach

### Delete One

```bash
curl -X DELETE http://localhost:7654/api/data/posts/1
```

### Delete with Auth

```bash
curl -X DELETE http://localhost:7654/api/data/posts/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Delete Many

```bash
# Delete all archived posts
curl -X DELETE "http://localhost:7654/api/data/posts?where=%7B%22status%22%3A%22archived%22%7D"

# URL-decoded where: {"status":"archived"}
```

## React Integration

### Delete Button

```tsx
import { useApp } from "bknd/react";
import { useState } from "react";

function DeleteButton({ postId, onDeleted }: { postId: number; onDeleted?: () => void }) {
  const { api } = useApp();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDelete() {
    if (!confirm("Are you sure you want to delete this post?")) {
      return;
    }

    setLoading(true);
    setError(null);

    const { ok, error: apiError } = await api.data.deleteOne("posts", postId);

    setLoading(false);

    if (ok) {
      onDeleted?.();
    } else {
      setError(apiError.message);
    }
  }

  return (
    <>
      <button onClick={handleDelete} disabled={loading}>
        {loading ? "Deleting..." : "Delete"}
      </button>
      {error && <p className="error">{error}</p>}
    </>
  );
}
```

### With SWR Revalidation

```tsx
import { mutate } from "swr";

function useDeletePost() {
  const { api } = useApp();

  async function deletePost(id: number) {
    const { ok, error } = await api.data.deleteOne("posts", id);

    if (ok) {
      // Revalidate list
      mutate("posts");
    }

    return { ok, error };
  }

  return { deletePost };
}
```

### Optimistic Delete

```tsx
function useOptimisticDelete() {
  const { api } = useApp();
  const [posts, setPosts] = useState<Post[]>([]);

  async function deletePost(id: number) {
    // Optimistic: remove immediately
    const originalPosts = [...posts];
    setPosts((prev) => prev.filter((p) => p.id !== id));

    // Actual delete
    const { ok } = await api.data.deleteOne("posts", id);

    if (!ok) {
      // Rollback on failure
      setPosts(originalPosts);
    }

    return { ok };
  }

  return { posts, deletePost };
}
```

## Full Example

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// Authenticate
await api.auth.login({ email: "admin@example.com", password: "password" });

// Simple delete
const { ok, data } = await api.data.deleteOne("posts", 1);
if (ok) {
  console.log("Deleted:", data.title);
}

// Delete with verification
const postId = 5;
const { data: post } = await api.data.readOne("posts", postId);
if (post) {
  await api.data.deleteOne("posts", postId);
}

// Bulk delete: remove old archived posts
const { data: deleted } = await api.data.deleteMany("posts", {
  status: { $eq: "archived" },
  created_at: { $lt: "2023-01-01" },
});
console.log("Deleted", deleted.length, "old archived posts");

// Cleanup expired sessions
await api.data.deleteMany("sessions", {
  expires_at: { $lt: new Date().toISOString() },
});
```

## Common Patterns

### Soft Delete (Recommended for User Data)

Instead of permanent deletion, mark as deleted:

```typescript
// Soft delete: set timestamp
async function softDelete(api: Api, entity: string, id: number) {
  return api.data.updateOne(entity, id, {
    deleted_at: new Date().toISOString(),
  });
}

// Restore soft-deleted record
async function restore(api: Api, entity: string, id: number) {
  return api.data.updateOne(entity, id, {
    deleted_at: null,
  });
}

// Query non-deleted records
async function findActive(api: Api, entity: string, query = {}) {
  return api.data.readMany(entity, {
    ...query,
    where: {
      ...query.where,
      deleted_at: { $isnull: true },
    },
  });
}

// Permanently delete soft-deleted records older than 30 days
async function purgeDeleted(api: Api, entity: string) {
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  return api.data.deleteMany(entity, {
    deleted_at: { $lt: thirtyDaysAgo.toISOString() },
  });
}
```

### Delete with Confirmation

```typescript
async function deleteWithConfirmation(
  api: Api,
  entity: string,
  id: number,
  confirm: () => Promise<boolean>
) {
  const { data } = await api.data.readOne(entity, id);
  if (!data) {
    return { ok: false, error: { message: "Record not found" } };
  }

  const confirmed = await confirm();
  if (!confirmed) {
    return { ok: false, error: { message: "Cancelled by user" } };
  }

  return api.data.deleteOne(entity, id);
}
```

### Cascade Delete (Manual)

When Bknd doesn't auto-cascade, delete children first:

```typescript
async function cascadeDelete(api: Api, userId: number) {
  // Delete children first
  await api.data.deleteMany("posts", { author_id: { $eq: userId } });
  await api.data.deleteMany("comments", { user_id: { $eq: userId } });
  await api.data.deleteMany("likes", { user_id: { $eq: userId } });

  // Then delete parent
  return api.data.deleteOne("users", userId);
}
```

### Batch Delete with Progress

```typescript
async function batchDelete(
  api: Api,
  entity: string,
  ids: number[],
  onProgress?: (done: number, total: number) => void
) {
  const results = [];

  for (let i = 0; i < ids.length; i++) {
    const result = await api.data.deleteOne(entity, ids[i]);
    results.push(result);
    onProgress?.(i + 1, ids.length);
  }

  return results;
}

// Usage
const idsToDelete = [1, 5, 12, 23];
await batchDelete(api, "posts", idsToDelete, (done, total) => {
  console.log(`Deleted ${done}/${total}`);
});
```

### Archive Before Delete

```typescript
async function archiveAndDelete(
  api: Api,
  sourceEntity: string,
  archiveEntity: string,
  id: number
) {
  // Read current record
  const { data: record } = await api.data.readOne(sourceEntity, id);
  if (!record) {
    return { ok: false, error: { message: "Record not found" } };
  }

  // Create archive copy
  await api.data.createOne(archiveEntity, {
    ...record,
    original_id: record.id,
    archived_at: new Date().toISOString(),
  });

  // Delete original
  return api.data.deleteOne(sourceEntity, id);
}
```

### Conditional Delete

```typescript
async function deleteIf(
  api: Api,
  entity: string,
  id: number,
  condition: (record: any) => boolean
) {
  const { data } = await api.data.readOne(entity, id);
  if (!data) {
    return { ok: false, error: { message: "Record not found" } };
  }

  if (!condition(data)) {
    return { ok: false, error: { message: "Condition not met" } };
  }

  return api.data.deleteOne(entity, id);
}

// Only delete if draft
await deleteIf(api, "posts", 1, (post) => post.status === "draft");
```

## Common Pitfalls

### Record Not Found

**Problem:** Delete returns no data or error.

**Fix:** Check if record exists first:

```typescript
const { data: existing } = await api.data.readOne("posts", id);
if (!existing) {
  console.error("Post not found");
  return;
}
await api.data.deleteOne("posts", id);
```

### Foreign Key Constraint

**Problem:** `FOREIGN KEY constraint failed` when deleting parent.

**Fix:** Delete or unlink children first:

```typescript
// Option 1: Delete children
await api.data.deleteMany("comments", { post_id: { $eq: postId } });
await api.data.deleteOne("posts", postId);

// Option 2: Unlink children (if nullable FK)
await api.data.updateMany(
  "comments",
  { post_id: { $eq: postId } },
  { post_id: null }
);
await api.data.deleteOne("posts", postId);
```

### Not Checking Response

**Problem:** Assuming success without verification.

**Fix:** Always check `ok`:

```typescript
// Wrong
await api.data.deleteOne("posts", id);
console.log("Deleted!");  // Might have failed!

// Correct
const { ok, error } = await api.data.deleteOne("posts", id);
if (!ok) {
  console.error("Delete failed:", error.message);
  return;
}
console.log("Deleted!");
```

### Accidental Mass Delete

**Problem:** Deleting more records than intended.

**Fix:** Always use specific where clause and verify count:

```typescript
// Dangerous - might delete more than expected
await api.data.deleteMany("posts", { status: { $eq: "draft" } });

// Safer - check count first
const { data: count } = await api.data.count("posts", {
  status: { $eq: "draft" }
});
console.log(`About to delete ${count.count} posts`);
if (count.count > 100) {
  throw new Error("Too many records - aborting");
}
```

### Missing Auth

**Problem:** `Unauthorized` error.

**Fix:** Authenticate before deleting:

```typescript
await api.auth.login({ email, password });
// or
api.updateToken(savedToken);

await api.data.deleteOne("posts", id);
```

### No Undo for Hard Delete

**Problem:** Accidentally deleted important data.

**Fix:** Use soft delete for recoverable data:

```typescript
// Instead of hard delete
await api.data.deleteOne("posts", id);

// Use soft delete
await api.data.updateOne("posts", id, {
  deleted_at: new Date().toISOString(),
});
```

### Deleting Without Confirmation

**Problem:** Users accidentally delete data.

**Fix:** Always confirm destructive actions:

```typescript
// In frontend
function handleDelete(id: number) {
  if (!confirm("Delete this post? This cannot be undone.")) {
    return;
  }
  api.data.deleteOne("posts", id);
}
```

## Verification

After deleting, verify the record is gone:

```typescript
const { ok } = await api.data.deleteOne("posts", 1);

if (ok) {
  const { data } = await api.data.readOne("posts", 1);
  console.log("Record exists:", data !== null);  // Should be false
}
```

Or via admin panel: Admin Panel > Data > Select Entity > Search for deleted record.

## DOs and DON'Ts

**DO:**
- Check `ok` before assuming success
- Verify record exists before deleting
- Use soft delete for user data
- Handle foreign key constraints
- Confirm with user before destructive actions
- Check count before bulk deletes
- Consider archiving before permanent delete

**DON'T:**
- Assume deleteOne always succeeds
- Delete parent before children with FK constraints
- Hard delete user data without confirmation
- Forget to revalidate caches after delete
- Use deleteMany without specific where clause
- Delete without authentication on protected entities

## Related Skills

- **bknd-crud-read** - Verify records before deleting
- **bknd-crud-update** - Update instead of delete (soft delete)
- **bknd-crud-create** - Recreate accidentally deleted records
- **bknd-define-relationship** - Understand FK constraints
- **bknd-bulk-operations** - Large-scale delete patterns

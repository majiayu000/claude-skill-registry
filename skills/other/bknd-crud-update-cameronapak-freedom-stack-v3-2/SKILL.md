---
name: bknd-crud-update
description: Use when updating existing records in a Bknd entity via the SDK or REST API. Covers updateOne, updateMany, updating relations ($set, $add, $remove, $unset), partial updates, conditional updates, response handling, and common patterns.
---

# CRUD Update

Update existing records in your Bknd database using the SDK or REST API.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists with records to update
- SDK configured or API endpoint known
- Record ID or filter criteria known

## When to Use UI Mode

- Quick one-off edits
- Manual data corrections
- Visual verification during development

**UI steps:** Admin Panel > Data > Select Entity > Click record > Edit fields > Save

## When to Use Code Mode

- Application logic for user edits
- Form submissions
- Bulk updates
- Automated data maintenance

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

### Step 2: Update Single Record

Use `updateOne(entity, id, data)`:

```typescript
const { ok, data, error } = await api.data.updateOne("posts", 1, {
  title: "Updated Title",
  status: "published",
});

if (ok) {
  console.log("Updated post:", data.id);
} else {
  console.error("Failed:", error.message);
}
```

### Step 3: Handle Response

The response object:

```typescript
type UpdateResponse = {
  ok: boolean;       // Success/failure
  data?: {           // Updated record (if ok)
    id: number;
    // ...all fields with new values
  };
  error?: {          // Error info (if !ok)
    message: string;
    code: string;
  };
};
```

### Step 4: Partial Updates

Only changed fields are required - other fields remain unchanged:

```typescript
// Only update title, keep everything else
await api.data.updateOne("posts", 1, {
  title: "New Title Only",
});

// Update multiple fields
await api.data.updateOne("users", 5, {
  name: "New Name",
  bio: "Updated bio",
  updated_at: new Date().toISOString(),
});
```

### Step 5: Update Relations

#### Change Linked Record (Many-to-One)

```typescript
// Change post author to user ID 2
await api.data.updateOne("posts", 1, {
  author: { $set: 2 },
});
```

#### Unlink Record (Set to NULL)

```typescript
// Remove author link
await api.data.updateOne("posts", 1, {
  author: { $unset: true },
});
```

#### Many-to-Many: Add Relations

```typescript
// Add tags 4 and 5 to existing tags
await api.data.updateOne("posts", 1, {
  tags: { $add: [4, 5] },
});
```

#### Many-to-Many: Remove Relations

```typescript
// Remove tag 2 from post
await api.data.updateOne("posts", 1, {
  tags: { $remove: [2] },
});
```

#### Many-to-Many: Replace All Relations

```typescript
// Replace all tags with new set
await api.data.updateOne("posts", 1, {
  tags: { $set: [1, 3, 5] },
});
```

#### Combined Field and Relation Update

```typescript
await api.data.updateOne("posts", 1, {
  title: "Updated Post",
  status: "published",
  author: { $set: newAuthorId },
  tags: { $add: [newTagId] },
});
```

### Step 6: Update Multiple Records (Bulk)

Use `updateMany(entity, where, data)`:

```typescript
// Archive all draft posts
const { ok, data } = await api.data.updateMany(
  "posts",
  { status: { $eq: "draft" } },     // where clause (required)
  { status: "archived" },            // update values
);

// data contains affected records
console.log("Archived", data.length, "posts");
```

**Important:** `where` clause is required to prevent accidental update-all.

```typescript
// Update posts by author
await api.data.updateMany(
  "posts",
  { author_id: { $eq: userId } },
  { author_id: newUserId },
);

// Update old records
await api.data.updateMany(
  "sessions",
  { last_active: { $lt: "2024-01-01" } },
  { expired: true },
);
```

## REST API Approach

### Update One

```bash
curl -X PATCH http://localhost:7654/api/data/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "status": "published"}'
```

### Update with Auth

```bash
curl -X PATCH http://localhost:7654/api/data/posts/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "Protected Update"}'
```

### Update Relations

```bash
# Change author
curl -X PATCH http://localhost:7654/api/data/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"author": {"$set": 2}}'

# Add tags
curl -X PATCH http://localhost:7654/api/data/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"tags": {"$add": [4, 5]}}'
```

### Update Many

```bash
curl -X PATCH "http://localhost:7654/api/data/posts?where=%7B%22status%22%3A%22draft%22%7D" \
  -H "Content-Type: application/json" \
  -d '{"status": "archived"}'
```

## React Integration

### Edit Form

```tsx
import { useApp } from "bknd/react";
import { useState, useEffect } from "react";

function EditPostForm({ postId }: { postId: number }) {
  const { api } = useApp();
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load existing data
  useEffect(() => {
    api.data.readOne("posts", postId).then(({ data }) => {
      if (data) setTitle(data.title);
    });
  }, [postId]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { ok, error: apiError } = await api.data.updateOne("posts", postId, {
      title,
    });

    setLoading(false);

    if (!ok) {
      setError(apiError.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Post title"
      />
      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
```

### With SWR Revalidation

```tsx
import useSWR, { mutate } from "swr";

function useUpdatePost() {
  const { api } = useApp();

  async function updatePost(id: number, updates: object) {
    const { ok, data, error } = await api.data.updateOne("posts", id, updates);

    if (ok) {
      // Revalidate the post and list
      mutate(`posts/${id}`);
      mutate("posts");
    }

    return { ok, data, error };
  }

  return { updatePost };
}
```

### Optimistic Update

```tsx
function useOptimisticUpdate() {
  const { api } = useApp();
  const [posts, setPosts] = useState<Post[]>([]);

  async function updatePost(id: number, updates: Partial<Post>) {
    // Optimistic: update immediately
    const originalPosts = [...posts];
    setPosts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, ...updates } : p))
    );

    // Actual update
    const { ok } = await api.data.updateOne("posts", id, updates);

    if (!ok) {
      // Rollback on failure
      setPosts(originalPosts);
    }

    return { ok };
  }

  return { posts, updatePost };
}
```

## Full Example

```typescript
import { Api } from "bknd";

const api = new Api({ host: "http://localhost:7654" });

// Authenticate
await api.auth.login({ email: "user@example.com", password: "password" });

// Simple field update
const { ok, data } = await api.data.updateOne("posts", 1, {
  title: "Updated Title",
  updated_at: new Date().toISOString(),
});

// Update with relation changes
await api.data.updateOne("posts", 1, {
  status: "published",
  published_at: new Date().toISOString(),
  category: { $set: 3 },        // Change category
  tags: { $add: [7, 8] },       // Add new tags
});

// Bulk update: mark old drafts as archived
await api.data.updateMany(
  "posts",
  {
    status: { $eq: "draft" },
    created_at: { $lt: "2024-01-01" },
  },
  { status: "archived" }
);

// Toggle boolean field
const post = await api.data.readOne("posts", 1);
if (post.ok) {
  await api.data.updateOne("posts", 1, {
    featured: !post.data.featured,
  });
}
```

## Common Patterns

### Upsert (Update or Insert)

```typescript
async function upsert(
  api: Api,
  entity: string,
  where: object,
  data: object
) {
  const { data: existing } = await api.data.readOneBy(entity, { where });

  if (existing) {
    return api.data.updateOne(entity, existing.id, data);
  }

  return api.data.createOne(entity, data);
}

// Usage
await upsert(
  api,
  "settings",
  { key: { $eq: "theme" } },
  { key: "theme", value: "dark" }
);
```

### Conditional Update

```typescript
async function updateIf(
  api: Api,
  entity: string,
  id: number,
  condition: (record: any) => boolean,
  updates: object
) {
  const { data: current } = await api.data.readOne(entity, id);

  if (!current || !condition(current)) {
    return { ok: false, error: { message: "Condition not met" } };
  }

  return api.data.updateOne(entity, id, updates);
}

// Only update if not published
await updateIf(
  api,
  "posts",
  1,
  (post) => post.status !== "published",
  { title: "New Title" }
);
```

### Increment/Decrement Field

```typescript
async function increment(
  api: Api,
  entity: string,
  id: number,
  field: string,
  amount: number = 1
) {
  const { data: current } = await api.data.readOne(entity, id);
  if (!current) return { ok: false };

  return api.data.updateOne(entity, id, {
    [field]: current[field] + amount,
  });
}

// Increment view count
await increment(api, "posts", 1, "view_count");

// Decrement stock
await increment(api, "products", 5, "stock", -1);
```

### Soft Delete

```typescript
async function softDelete(api: Api, entity: string, id: number) {
  return api.data.updateOne(entity, id, {
    deleted_at: new Date().toISOString(),
  });
}

async function restore(api: Api, entity: string, id: number) {
  return api.data.updateOne(entity, id, {
    deleted_at: null,
  });
}
```

### Batch Update with Progress

```typescript
async function batchUpdate(
  api: Api,
  entity: string,
  updates: Array<{ id: number; data: object }>,
  onProgress?: (done: number, total: number) => void
) {
  const results = [];

  for (let i = 0; i < updates.length; i++) {
    const { id, data } = updates[i];
    const result = await api.data.updateOne(entity, id, data);
    results.push(result);
    onProgress?.(i + 1, updates.length);
  }

  return results;
}

// Usage
await batchUpdate(
  api,
  "products",
  [
    { id: 1, data: { price: 19.99 } },
    { id: 2, data: { price: 29.99 } },
    { id: 3, data: { price: 39.99 } },
  ],
  (done, total) => console.log(`${done}/${total}`)
);
```

## Common Pitfalls

### Record Not Found

**Problem:** Update returns no data or error.

**Fix:** Verify record exists first:

```typescript
const { data: existing } = await api.data.readOne("posts", id);
if (!existing) {
  throw new Error("Post not found");
}
await api.data.updateOne("posts", id, updates);
```

### Invalid Relation ID

**Problem:** `FOREIGN KEY constraint failed`

**Fix:** Verify related record exists:

```typescript
// Wrong - author ID doesn't exist
await api.data.updateOne("posts", 1, { author: { $set: 999 } });

// Correct - verify first
const { data: author } = await api.data.readOne("users", newAuthorId);
if (author) {
  await api.data.updateOne("posts", 1, { author: { $set: newAuthorId } });
}
```

### Unique Constraint Violation

**Problem:** `UNIQUE constraint failed` when updating to existing value.

**Fix:** Check uniqueness before update:

```typescript
// Check if email already taken by another user
const { data: existing } = await api.data.readOneBy("users", {
  where: {
    email: { $eq: newEmail },
    id: { $ne: currentUserId },  // Exclude current user
  },
});

if (existing) {
  throw new Error("Email already in use");
}

await api.data.updateOne("users", currentUserId, { email: newEmail });
```

### Not Checking Response

**Problem:** Assuming success without verification.

**Fix:** Always check `ok`:

```typescript
// Wrong
const { data } = await api.data.updateOne("posts", 1, updates);
console.log(data.title);  // data might be undefined!

// Correct
const { ok, data, error } = await api.data.updateOne("posts", 1, updates);
if (!ok) {
  throw new Error(error.message);
}
console.log(data.title);
```

### Updating Without Auth

**Problem:** `Unauthorized` error.

**Fix:** Authenticate first:

```typescript
await api.auth.login({ email, password });
// or
api.updateToken(savedToken);

await api.data.updateOne("posts", 1, updates);
```

### Using Wrong Relation Operator

**Problem:** Replacing when intending to add.

**Fix:** Use correct operator:

```typescript
// $set replaces ALL relations
await api.data.updateOne("posts", 1, { tags: { $set: [5] } });
// Post now has ONLY tag 5

// $add keeps existing and adds new
await api.data.updateOne("posts", 1, { tags: { $add: [5] } });
// Post keeps existing tags AND adds tag 5
```

### Forgetting updateMany Where Clause

**Problem:** Trying to update all without where.

**Fix:** Always provide where clause:

```typescript
// updateMany requires where clause
await api.data.updateMany(
  "posts",
  { status: { $eq: "draft" } },  // Required
  { status: "archived" }
);

// To update ALL records, use explicit condition
await api.data.updateMany(
  "posts",
  { id: { $gt: 0 } },  // Match all
  { reviewed: true }
);
```

## Verification

After updating, verify changes:

```typescript
const { ok } = await api.data.updateOne("posts", 1, { title: "New Title" });

if (ok) {
  const { data } = await api.data.readOne("posts", 1);
  console.log("Updated title:", data.title);
}
```

Or via admin panel: Admin Panel > Data > Select Entity > Find record > Verify fields.

## DOs and DON'Ts

**DO:**
- Check `ok` before using response data
- Verify record exists before updating
- Use `$add`/`$remove` for incremental relation changes
- Handle unique constraint errors
- Authenticate before updating protected records
- Revalidate caches after updates

**DON'T:**
- Assume updateOne always succeeds
- Use `$set` for relations when meaning `$add`
- Update without where clause in updateMany
- Ignore validation errors
- Forget to refresh UI after updates
- Use non-existent IDs in relation operators

## Related Skills

- **bknd-crud-create** - Create records before updating
- **bknd-crud-read** - Fetch records to get current values
- **bknd-crud-delete** - Remove records instead of updating
- **bknd-define-relationship** - Set up relations for linking
- **bknd-bulk-operations** - Large-scale update patterns

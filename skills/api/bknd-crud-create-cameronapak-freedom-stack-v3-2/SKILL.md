---
name: bknd-crud-create
description: Use when inserting new records into a Bknd entity via the SDK or REST API. Covers createOne, createMany, creating with relations ($set), response handling, error handling, and common patterns for client-side record creation.
---

# CRUD Create

Insert new records into your Bknd database using the SDK or REST API.

## Prerequisites

- Bknd project running (local or deployed)
- Entity exists (use `bknd-create-entity` first)
- SDK configured or API endpoint known

## When to Use UI Mode

- Quick one-off data entry
- Manual testing during development
- Non-technical users adding records

**UI steps:** Admin Panel > Data > Select Entity > Click "+" or "Add" > Fill form > Save

## When to Use Code Mode

- Application logic for user-generated content
- Form submissions
- API integrations
- Automated record creation

## Code Approach

### Step 1: Set Up SDK Client

```typescript
import { Api } from "bknd";

const api = new Api({
  host: "http://localhost:7654",  // Your Bknd server
});

// If auth required:
api.updateToken("your-jwt-token");
```

### Step 2: Create Single Record

Use `createOne(entity, data)`:

```typescript
const { ok, data, error } = await api.data.createOne("posts", {
  title: "My First Post",
  content: "Hello world!",
  published: false,
});

if (ok) {
  console.log("Created post:", data.id);
} else {
  console.error("Failed:", error.message);
}
```

### Step 3: Handle Response

The response object:

```typescript
type CreateResponse = {
  ok: boolean;       // Success/failure
  data?: {           // Created record (if ok)
    id: number;      // Auto-generated ID
    // ...all fields with defaults applied
  };
  error?: {          // Error info (if !ok)
    message: string;
    code: string;
  };
};
```

### Step 4: Create with Relations

Link to existing related records using `$set`:

```typescript
// Link to single related record (many-to-one)
const { data } = await api.data.createOne("posts", {
  title: "New Post",
  author: { $set: 1 },  // Link to user with ID 1
});

// Link to multiple related records (many-to-many)
const { data } = await api.data.createOne("posts", {
  title: "Tagged Post",
  tags: { $set: [1, 2, 3] },  // Link to tag IDs 1, 2, 3
});

// Combine both
const { data } = await api.data.createOne("posts", {
  title: "Complete Post",
  content: "Full content here",
  author: { $set: userId },
  category: { $set: categoryId },
  tags: { $set: [tagId1, tagId2] },
});
```

### Step 5: Create Multiple Records (Bulk)

Use `createMany(entity, data[])`:

```typescript
const { ok, data } = await api.data.createMany("tags", [
  { name: "javascript" },
  { name: "typescript" },
  { name: "bknd" },
]);

// data is array of created records
console.log("Created", data.length, "tags");
```

## REST API Approach

### Create One

```bash
curl -X POST http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "New Post", "content": "Hello!"}'
```

### Create with Auth

```bash
curl -X POST http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "Protected Post"}'
```

### Create Many

```bash
curl -X POST http://localhost:7654/api/data/tags \
  -H "Content-Type: application/json" \
  -d '[{"name": "tag1"}, {"name": "tag2"}]'
```

### Create with Relations

```bash
curl -X POST http://localhost:7654/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Post", "author": {"$set": 1}}'
```

## React Integration

### Basic Form Submit

```tsx
import { useApp } from "bknd/react";

function CreatePostForm() {
  const { api } = useApp();
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { ok, data, error: apiError } = await api.data.createOne("posts", {
      title,
      published: false,
    });

    setLoading(false);

    if (ok) {
      console.log("Created:", data.id);
      setTitle("");
    } else {
      setError(apiError.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Post title"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Post"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
```

### With SWR Revalidation

```tsx
import { useApp } from "bknd/react";
import useSWR, { mutate } from "swr";

function PostsList() {
  const { api } = useApp();

  const { data: posts } = useSWR("posts", () =>
    api.data.readMany("posts").then((r) => r.data)
  );

  async function createPost(title: string) {
    const { ok, data } = await api.data.createOne("posts", { title });

    if (ok) {
      // Revalidate the posts list
      mutate("posts");
    }

    return { ok, data };
  }

  return (
    <div>
      <CreateForm onCreate={createPost} />
      <ul>
        {posts?.map((post) => (
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

// Authenticate first (if required)
await api.auth.login({ email: "user@example.com", password: "password" });

// Create a user
const { data: user } = await api.data.createOne("users", {
  email: "newuser@example.com",
  name: "New User",
  role: "author",
});

// Create a post linked to user
const { data: post } = await api.data.createOne("posts", {
  title: "My First Blog Post",
  content: "This is the content of my post.",
  published: true,
  author: { $set: user.id },
});

// Create tags
const { data: tags } = await api.data.createMany("tags", [
  { name: "intro" },
  { name: "tutorial" },
]);

// Link tags to post (update after creation)
await api.data.updateOne("posts", post.id, {
  tags: { $set: tags.map((t) => t.id) },
});

console.log("Created post:", post.id, "with tags:", tags.length);
```

## Field Default Handling

Bknd applies defaults for omitted fields:

```typescript
// Entity definition
entity("posts", {
  title: text().required(),
  status: text({ default_value: "draft" }),
  view_count: number({ default_value: 0 }),
  created_at: date({ default_value: "now" }),
});

// Create with minimal data
const { data } = await api.data.createOne("posts", {
  title: "Just a title",  // Only required field
});

// Result includes defaults
console.log(data);
// {
//   id: 1,
//   title: "Just a title",
//   status: "draft",           // default applied
//   view_count: 0,             // default applied
//   created_at: "2025-01-20T..." // default applied
// }
```

## Validation Handling

Bknd validates data against schema:

```typescript
// Entity with constraints
entity("users", {
  email: text().required().unique(),
  name: text(),
});

// Missing required field
const { ok, error } = await api.data.createOne("users", {
  name: "No Email",
});
// ok: false, error: { message: "email is required" }

// Duplicate unique field
const { ok, error } = await api.data.createOne("users", {
  email: "existing@example.com",  // Already exists
});
// ok: false, error: { message: "UNIQUE constraint failed" }
```

## Common Patterns

### Create or Find Existing

```typescript
async function createOrFind(
  api: Api,
  entity: string,
  data: object,
  uniqueField: string
) {
  // Try to find existing
  const { data: existing } = await api.data.readOneBy(entity, {
    where: { [uniqueField]: { $eq: data[uniqueField] } },
  });

  if (existing) {
    return { created: false, data: existing };
  }

  // Create new
  const { data: created } = await api.data.createOne(entity, data);
  return { created: true, data: created };
}

// Usage
const { created, data } = await createOrFind(
  api,
  "users",
  { email: "user@example.com", name: "User" },
  "email"
);
```

### Create with Optimistic UI

```typescript
function useCreatePost() {
  const { api } = useApp();
  const [posts, setPosts] = useState<Post[]>([]);

  async function createPost(title: string) {
    // Optimistic: add temp post immediately
    const tempId = `temp-${Date.now()}`;
    const tempPost = { id: tempId, title, status: "creating" };
    setPosts((prev) => [...prev, tempPost]);

    // Actual create
    const { ok, data } = await api.data.createOne("posts", { title });

    if (ok) {
      // Replace temp with real
      setPosts((prev) =>
        prev.map((p) => (p.id === tempId ? data : p))
      );
    } else {
      // Remove temp on failure
      setPosts((prev) => prev.filter((p) => p.id !== tempId));
    }

    return { ok, data };
  }

  return { posts, createPost };
}
```

### Batch Create with Progress

```typescript
async function batchCreate(
  api: Api,
  entity: string,
  items: object[],
  onProgress?: (done: number, total: number) => void
) {
  const results = [];
  const batchSize = 100;

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const { data } = await api.data.createMany(entity, batch);
    results.push(...data);

    onProgress?.(Math.min(i + batchSize, items.length), items.length);
  }

  return results;
}

// Usage
const items = generateItems(500);
await batchCreate(api, "products", items, (done, total) => {
  console.log(`Progress: ${done}/${total}`);
});
```

## Common Pitfalls

### Missing Required Fields

**Problem:** `NOT NULL constraint failed`

**Fix:** Include all required fields:

```typescript
// Entity: email is required
entity("users", { email: text().required(), name: text() });

// Wrong - missing email
await api.data.createOne("users", { name: "Test" });

// Correct
await api.data.createOne("users", { email: "test@example.com", name: "Test" });
```

### Invalid Relation ID

**Problem:** `FOREIGN KEY constraint failed`

**Fix:** Ensure related record exists:

```typescript
// Wrong - author ID doesn't exist
await api.data.createOne("posts", { title: "Post", author: { $set: 999 } });

// Correct - verify first or handle error
const { data: author } = await api.data.readOne("users", authorId);
if (author) {
  await api.data.createOne("posts", { title: "Post", author: { $set: authorId } });
}
```

### Unique Constraint Violation

**Problem:** `UNIQUE constraint failed`

**Fix:** Check before create or handle error:

```typescript
// Option 1: Check first
const { data: exists } = await api.data.exists("users", {
  email: { $eq: email },
});
if (exists.exists) {
  throw new Error("Email already registered");
}
await api.data.createOne("users", { email, name });

// Option 2: Handle error
const { ok, error } = await api.data.createOne("users", { email, name });
if (!ok && error.message.includes("UNIQUE")) {
  throw new Error("Email already registered");
}
```

### Not Handling Response

**Problem:** Assuming success without checking.

**Fix:** Always check `ok`:

```typescript
// Wrong - assumes success
const { data } = await api.data.createOne("posts", { title });
console.log(data.id);  // data might be undefined!

// Correct
const { ok, data, error } = await api.data.createOne("posts", { title });
if (!ok) {
  throw new Error(error.message);
}
console.log(data.id);
```

### Creating Without Auth

**Problem:** `Unauthorized` error.

**Fix:** Authenticate first or check permissions:

```typescript
// Login first
await api.auth.login({ email, password });

// Or set token
api.updateToken(savedToken);

// Then create
await api.data.createOne("posts", { title });
```

## Verification

After creating, verify the record:

```typescript
const { ok, data } = await api.data.createOne("posts", { title: "Test" });

if (ok) {
  // Read back to verify
  const { data: fetched } = await api.data.readOne("posts", data.id);
  console.log("Created and verified:", fetched);
}
```

Or via admin panel: Admin Panel > Data > Select Entity > Find new record.

## DOs and DON'Ts

**DO:**
- Check the `ok` field before using `data`
- Include all required fields
- Verify related records exist before using `$set`
- Handle unique constraint errors gracefully
- Authenticate before creating protected records

**DON'T:**
- Assume createOne always succeeds
- Use non-existent IDs in `$set`
- Ignore validation errors
- Create without auth when permissions require it
- Forget to revalidate caches after create

## Related Skills

- **bknd-seed-data** - Bulk initial data via seed function (server-side)
- **bknd-crud-read** - Query records after creation
- **bknd-crud-update** - Modify created records
- **bknd-define-relationship** - Set up relations for `$set` linking
- **bknd-bulk-operations** - Large-scale record creation

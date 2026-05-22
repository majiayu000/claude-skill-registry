---
name: bknd-delete-entity
description: Use when removing an entity from Bknd. Covers safely deleting entities, handling relationships and dependencies, data backup, the sync workflow with --drop flag, and cleaning up orphaned data.
---

# Delete Entity

Safely remove an entity (table) from Bknd, handling dependencies and avoiding data loss.

## Prerequisites

- Existing Bknd app with entities (see `bknd-create-entity`)
- For code mode: Access to `bknd.config.ts`
- **Critical:** Backup database before deletion

## Warning: Destructive Operation

Deleting an entity:
- Permanently removes the table and ALL its data
- Removes all relationships involving this entity
- May break application code referencing this entity
- Cannot be undone without database restore

## When to Use UI vs Code

### Use UI Mode When
- Quick prototype cleanup
- Development/testing environments
- Exploring what dependencies exist

### Use Code Mode When
- Production changes
- Version control needed
- Team collaboration
- Reproducible deployments

---

## Pre-Deletion Checklist

Before deleting an entity, verify:

### 1. Check for Relationships

Entities may be referenced by other entities via:
- Foreign keys (many-to-one)
- Junction tables (many-to-many)
- Self-references

### 2. Check for Data

```typescript
const api = app.getApi();
const count = await api.data.count("entity_to_delete");
console.log(`Records to delete: ${count.data.count}`);
```

### 3. Check for Code References

Search codebase for:
- Entity name in queries: `"entity_name"`
- Type references: `DB["entity_name"]`
- API calls: `api.data.*("entity_name")`

### 4. Backup Data (If Needed)

```typescript
// Export data before deletion
const api = app.getApi();
const allRecords = await api.data.readMany("entity_to_delete", {
  limit: 100000,
});

// Save to file
import { writeFileSync } from "fs";
writeFileSync(
  "backup-entity_to_delete.json",
  JSON.stringify(allRecords.data, null, 2)
);
```

---

## Code Approach

### Step 1: Identify Dependencies

Check your schema for relationships:

```typescript
// Look for relationships involving this entity
const schema = em(
  {
    users: entity("users", { email: text().required() }),
    posts: entity("posts", { title: text().required() }),
    comments: entity("comments", { body: text() }),
  },
  ({ relation }, { users, posts, comments }) => {
    // posts depends on users (foreign key)
    relation(posts).manyToOne(users);
    // comments depends on posts (foreign key)
    relation(comments).manyToOne(posts);
  }
);
```

**Dependency order matters:** Delete children before parents.

### Step 2: Remove Relationships First

If entity is a target of relationships, update schema to remove them:

```typescript
// BEFORE: posts references users
const schema = em(
  {
    users: entity("users", { email: text().required() }),
    posts: entity("posts", { title: text().required() }),
  },
  ({ relation }, { users, posts }) => {
    relation(posts).manyToOne(users);
  }
);

// AFTER: Remove relationship before deleting users
const schema = em({
  users: entity("users", { email: text().required() }),
  posts: entity("posts", { title: text().required() }),
});
```

### Step 3: Remove Entity from Schema

Simply remove the entity definition from your `bknd.config.ts`:

```typescript
// BEFORE
const schema = em({
  users: entity("users", { email: text().required() }),
  posts: entity("posts", { title: text().required() }),
  deprecated_entity: entity("deprecated_entity", { data: text() }),
});

// AFTER - entity removed
const schema = em({
  users: entity("users", { email: text().required() }),
  posts: entity("posts", { title: text().required() }),
});
```

### Step 4: Preview Changes

```bash
# See what will be dropped (dry run)
npx bknd sync
```

Output shows:
```
Tables to drop: deprecated_entity
Columns affected: (none on other tables)
```

### Step 5: Apply Deletion

```bash
# Apply with drop flag (destructive)
npx bknd sync --drop
```

Or with force (enables all destructive operations):
```bash
npx bknd sync --force
```

### Step 6: Clean Up Code

Remove all references:
- Delete type definitions
- Remove API calls
- Update imports

---

## UI Approach

### Step 1: Open Admin Panel

Navigate to `http://localhost:1337` (or your configured URL).

### Step 2: Go to Data Section

Click **Data** in the sidebar.

### Step 3: Select Entity

Click on the entity you want to delete.

### Step 4: Check Dependencies

Look for:
- **Relations** tab/section showing connected entities
- Warning messages about dependencies

### Step 5: Export Data (Optional)

If you need the data:
1. Go to entity's data view
2. Export or manually copy records
3. Save backup externally

### Step 6: Delete Entity

1. Open entity settings (gear icon or settings tab)
2. Look for **Delete Entity** or **Remove** button
3. Confirm deletion
4. Entity and all data removed

### Step 7: Sync Database

After deletion, ensure database is synced:
- Click **Sync Database** if prompted
- Or run `npx bknd sync --drop` from CLI

---

## Handling Dependencies

### Scenario: Entity Has Child Records

**Problem:** Deleting `users` when `posts` has `users_id` foreign key.

**Solution 1: Delete Children First**

```typescript
// 1. Delete all posts referencing users
const api = app.getApi();
await api.data.deleteMany("posts", {});

// 2. Then delete users
// (via schema removal + sync)
```

**Solution 2: Remove Relationship First**

```typescript
// 1. Remove relationship from schema
// 2. Sync to remove foreign key
// 3. Remove entity from schema
// 4. Sync again with --drop
```

### Scenario: Entity is Junction Table Target

**Problem:** `tags` is used in `posts_tags` junction table.

**Solution:**

```typescript
// 1. Remove many-to-many relationship
const schema = em(
  {
    posts: entity("posts", { title: text() }),
    tags: entity("tags", { name: text() }),
  }
  // Remove: ({ relation }, { posts, tags }) => { relation(posts).manyToMany(tags); }
);

// 2. Sync to drop junction table
// npx bknd sync --drop

// 3. Remove tags entity
const schema = em({
  posts: entity("posts", { title: text() }),
});

// 4. Sync again to drop tags table
// npx bknd sync --drop
```

### Scenario: Self-Referencing Entity

**Problem:** `categories` references itself (parent/children).

**Solution:**

```typescript
// 1. Remove self-reference relation
const schema = em({
  categories: entity("categories", { name: text() }),
  // Remove self-referencing relation definition
});

// 2. Sync to remove foreign key
// npx bknd sync --drop

// 3. Remove entity
// (then sync again)
```

---

## Deleting Multiple Entities

Order matters. Delete in dependency order (children first):

```typescript
// Dependency tree:
// users <- posts <- comments
//       <- likes

// Delete order:
// 1. comments (depends on posts)
// 2. likes (depends on posts)
// 3. posts (depends on users)
// 4. users (no dependencies)
```

### Batch Deletion Script

```typescript
// scripts/cleanup-entities.ts
import { App } from "bknd";

async function cleanup() {
  const app = new App({
    connection: { url: process.env.DB_URL! },
  });
  await app.build();
  const api = app.getApi();

  // Delete in order
  const entitiesToDelete = ["comments", "likes", "posts"];

  for (const entity of entitiesToDelete) {
    const count = await api.data.count(entity);
    console.log(`Deleting ${count.data.count} records from ${entity}...`);
    await api.data.deleteMany(entity, {});
    console.log(`Deleted all records from ${entity}`);
  }

  console.log("Data cleanup complete. Now remove from schema and sync.");
}

cleanup().catch(console.error);
```

---

## Common Pitfalls

### Foreign Key Constraint Error

**Error:** `Cannot drop table: foreign key constraint`

**Cause:** Another entity references this one.

**Fix:** Remove relationship first, sync, then remove entity.

### Junction Table Not Dropped

**Problem:** After removing many-to-many relation, junction table remains.

**Fix:** Run `npx bknd sync --drop` to include destructive operations.

### Entity Still Appears in UI

**Problem:** Deleted from code but still shows in admin panel.

**Fix:**
- Ensure you ran `npx bknd sync --drop`
- Restart the Bknd server
- Clear browser cache

### Application Crashes After Deletion

**Problem:** Code still references deleted entity.

**Fix:**
- Search codebase: `grep -r "entity_name" src/`
- Remove all API calls, types, imports
- Fix TypeScript errors

### Accidentally Deleted Wrong Entity

**Problem:** Deleted production data.

**Fix:**
- If you have backup: Restore from backup
- If no backup: Data is permanently lost
- Prevention: Always backup before deletion

---

## Verification

### After Deletion

```bash
# 1. Check schema export (entity should be absent)
npx bknd schema --pretty | grep entity_name

# 2. Verify sync status
npx bknd sync
# Should show no pending changes
```

### Via Code

```typescript
const api = app.getApi();

// This should fail/return error for deleted entity
try {
  await api.data.readMany("deleted_entity", { limit: 1 });
  console.log("ERROR: Entity still exists!");
} catch (e) {
  console.log("Confirmed: Entity deleted successfully");
}
```

### Via REST API

```bash
# Should return 404 or error
curl http://localhost:1337/api/data/deleted_entity
```

---

## DOs and DON'Ts

**DO:**
- Backup data before deletion
- Check for dependencies first
- Delete children before parents
- Preview with `npx bknd sync` before `--drop`
- Remove code references after deletion
- Test in development before production

**DON'T:**
- Delete entities with active foreign keys
- Use `--drop` without previewing changes
- Delete in production without backup
- Assume UI deletion handles all cleanup
- Forget to remove TypeScript types/code references

---

## Related Skills

- **bknd-create-entity** - Create new entities
- **bknd-modify-schema** - Modify existing schema
- **bknd-define-relationship** - Understand relationship dependencies
- **bknd-crud-delete** - Delete individual records (not tables)
- **bknd-seed-data** - Restore data from backup

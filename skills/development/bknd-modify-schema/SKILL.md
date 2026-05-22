---
name: bknd-modify-schema
description: Use when modifying existing Bknd schema. Covers renaming entities, renaming fields, changing field types, altering field constraints, handling destructive changes, data migration strategies, and the sync workflow.
---

# Modify Schema

Modify existing schema in Bknd: rename entities/fields, change field types, or alter constraints.

## Prerequisites

- Existing Bknd app with entities (see `bknd-create-entity`)
- For code mode: Access to `bknd.config.ts`
- **Backup your database** before destructive changes

## Critical Concept: Destructive vs Non-Destructive Changes

Bknd's schema sync detects differences between your code and database. Some changes are safe; others cause data loss.

### Non-Destructive (Safe)
- Adding new entities
- Adding new fields (nullable or with default)
- Adding new indices
- Loosening constraints (removing `.required()`)

### Destructive (Data Loss Risk)
- Renaming entities (treated as drop old + create new)
- Renaming fields (treated as drop old + create new)
- Changing field types (may fail or truncate data)
- Removing fields (drops column and data)
- Removing entities (drops table and all data)
- Tightening constraints on existing data

## When to Use UI vs Code

### Use UI Mode When
- Exploring schema changes interactively
- Quick prototyping (data loss acceptable)
- No version control needed

### Use Code Mode When
- Production schema changes
- Version control required
- Team collaboration
- Reproducible deployments

---

## Renaming an Entity

**Warning:** Bknd has no native rename. Renaming = DROP old + CREATE new = **DATA LOSS**.

### Safe Approach: Data Migration

1. Create new entity with desired name
2. Migrate data from old to new
3. Update code references
4. Delete old entity

### Code Approach

```typescript
// Step 1: Add new entity alongside old
const schema = em({
  // OLD - will be removed later
  posts: entity("posts", {
    title: text().required(),
    content: text(),
  }),
  // NEW - desired name
  articles: entity("articles", {
    title: text().required(),
    content: text(),
  }),
});
```

```typescript
// Step 2: Migrate data (run once via script or CLI)
const api = app.getApi();
const oldData = await api.data.readMany("posts", { limit: 10000 });

for (const item of oldData.data) {
  await api.data.createOne("articles", {
    title: item.title,
    content: item.content,
  });
}
```

```typescript
// Step 3: Remove old entity from schema
const schema = em({
  articles: entity("articles", {
    title: text().required(),
    content: text(),
  }),
});
```

```bash
# Step 4: Sync with force to drop old table
npx bknd sync --force
```

### UI Approach

1. Open admin panel (`http://localhost:1337`)
2. Go to **Data** section
3. Create new entity with desired name
4. Copy field definitions manually
5. Export data from old entity (if needed)
6. Import data to new entity
7. Delete old entity

---

## Renaming a Field

**Warning:** Bknd treats field renames as drop + create = **DATA LOSS** on that column.

### Safe Approach: Data Migration

```typescript
// Step 1: Add new field alongside old
const schema = em({
  users: entity("users", {
    name: text(),           // OLD - will be removed
    full_name: text(),      // NEW - desired name
  }),
});
```

```typescript
// Step 2: Migrate data
const api = app.getApi();
const users = await api.data.readMany("users", { limit: 10000 });

for (const user of users.data) {
  if (user.name && !user.full_name) {
    await api.data.updateOne("users", user.id, {
      full_name: user.name,
    });
  }
}
```

```typescript
// Step 3: Remove old field
const schema = em({
  users: entity("users", {
    full_name: text(),
  }),
});
```

```bash
# Step 4: Sync with force to drop old column
npx bknd sync --force
```

### UI Approach

1. Add new field with desired name
2. Write script or manually copy data
3. Delete old field

---

## Changing Field Type

Type changes are risky. Some conversions work; others fail or truncate.

### Compatible Type Changes

| From | To | Notes |
|------|-----|-------|
| `text` | `text` (with different constraints) | Usually safe |
| `number` | `text` | Safe (numbers become strings) |
| `boolean` | `number` | Safe (0/1 values) |
| `boolean` | `text` | Safe ("true"/"false") |

### Incompatible Type Changes

| From | To | Risk |
|------|-----|------|
| `text` | `number` | Fails if non-numeric data |
| `text` | `boolean` | Fails if not "true"/"false"/0/1 |
| `text` | `date` | Fails if not valid date format |
| `json` | `text` | May truncate; loses structure |

### Safe Approach for Type Change

```typescript
// Step 1: Add new field with new type
const schema = em({
  products: entity("products", {
    price: text(),            // OLD - string prices
    price_cents: number(),    // NEW - integer cents
  }),
});
```

```typescript
// Step 2: Transform and migrate data
const api = app.getApi();
const products = await api.data.readMany("products", { limit: 10000 });

for (const product of products.data) {
  if (product.price && !product.price_cents) {
    const cents = Math.round(parseFloat(product.price) * 100);
    await api.data.updateOne("products", product.id, {
      price_cents: cents,
    });
  }
}
```

```typescript
// Step 3: Remove old field, rename new if desired
const schema = em({
  products: entity("products", {
    price_cents: number(),
  }),
});
```

---

## Changing Field Constraints

### Making a Field Required

**Risk:** Fails if existing records have null values.

```typescript
// Before
entity("users", {
  email: text(),  // Optional
});

// After
entity("users", {
  email: text().required(),  // Now required
});
```

**Safe approach:**
1. Update all null values first
2. Then add `.required()`

```typescript
// Step 1: Fill nulls with default
const api = app.getApi();
const usersWithNull = await api.data.readMany("users", {
  where: { email: { $isnull: true } },
});

for (const user of usersWithNull.data) {
  await api.data.updateOne("users", user.id, {
    email: "unknown@example.com",
  });
}

// Step 2: Now safely add .required()
```

### Making a Field Unique

**Risk:** Fails if duplicates exist.

```typescript
// Before
entity("users", {
  username: text(),
});

// After
entity("users", {
  username: text().unique(),
});
```

**Safe approach:**
1. Find and resolve duplicates
2. Then add `.unique()`

```typescript
// Check for duplicates via raw SQL or manual inspection
// Resolve duplicates by updating or deleting
// Then add .unique() constraint
```

### Removing Required/Unique

Generally safe:

```typescript
// Before
entity("users", {
  email: text().required().unique(),
});

// After - loosening constraints is safe
entity("users", {
  email: text(),  // Now optional, non-unique
});
```

---

## The Sync Workflow

### Preview Changes (Dry Run)

```bash
# See what sync would do without applying
npx bknd sync
```

Output shows:
- New entities/fields to create
- Entities/fields to drop
- Index changes

### Apply Non-Destructive Changes

```bash
# Applies only additive changes
npx bknd sync
```

### Apply All Changes (Including Drops)

```bash
# WARNING: This will drop tables/columns
npx bknd sync --force
```

### Apply Drops Only

```bash
# Specifically enables drop operations
npx bknd sync --drop
```

---

## UI Approach: Field Modifications

### Change Field Type

1. Open entity in Data section
2. Click on field to edit
3. **Note:** Type dropdown may be locked for existing fields
4. If locked: Create new field with correct type, migrate data, delete old

### Change Constraints

1. Open entity in Data section
2. Click on field to edit
3. Toggle Required/Unique as needed
4. Click **Save**
5. Click **Sync Database**

### Rename Field

1. Create new field with desired name
2. Manually copy data or write migration script
3. Delete old field
4. Sync database

---

## Common Pitfalls

### Sync Fails on Type Change

**Error:** `Cannot convert column type from X to Y`

**Fix:** Use migration approach - create new field, copy data, drop old.

### Sync Fails on Required Constraint

**Error:** `Column contains null values, cannot add NOT NULL`

**Fix:** Update all null values to non-null first, then re-sync.

### Sync Fails on Unique Constraint

**Error:** `Duplicate values exist for column`

**Fix:** Remove duplicates before adding unique constraint.

### Data Lost After Rename

**Problem:** Renamed entity/field and lost all data.

**Fix:** Unfortunately, data is gone. Restore from backup. Use migration approach next time.

### Force Flag Ignored

**Problem:** `--force` doesn't seem to apply changes.

**Fix:** Check sync output for actual errors. May be validation issue, not permission.

---

## Migration Script Template

For complex migrations, create a standalone script:

```typescript
// scripts/migrate-schema.ts
import { App } from "bknd";

async function migrate() {
  const app = new App({
    connection: { url: process.env.DB_URL! },
  });
  await app.build();

  const api = app.getApi();

  console.log("Starting migration...");

  // Read all records from old structure
  const records = await api.data.readMany("old_entity", { limit: 100000 });
  console.log(`Found ${records.data.length} records`);

  // Transform and insert into new structure
  let migrated = 0;
  for (const record of records.data) {
    await api.data.createOne("new_entity", {
      // Transform fields as needed
      new_field: record.old_field,
    });
    migrated++;
    if (migrated % 100 === 0) {
      console.log(`Migrated ${migrated}/${records.data.length}`);
    }
  }

  console.log("Migration complete!");
  process.exit(0);
}

migrate().catch(console.error);
```

Run with:
```bash
npx bun scripts/migrate-schema.ts
# or
npx ts-node scripts/migrate-schema.ts
```

---

## Verification

### After Schema Modification

```bash
# 1. Check sync status
npx bknd sync

# 2. Verify schema in debug output
npx bknd schema --pretty
```

### Via Code

```typescript
const api = app.getApi();

// Verify field exists by querying
const result = await api.data.readMany("entity_name", { limit: 1 });
console.log(result.data[0]);  // Check field names/values
```

### Via UI

1. Open entity in Data section
2. Verify fields appear correctly
3. Create test record with new schema
4. Query existing records to verify data

---

## DOs and DON'Ts

**DO:**
- Back up database before destructive changes
- Use migration approach for renames
- Preview with `npx bknd sync` before forcing
- Test on development database first
- Keep old structure until data migrated

**DON'T:**
- Rename entities/fields directly (data loss)
- Use `--force` without previewing first
- Change types without migration plan
- Add `.required()` to fields with null data
- Add `.unique()` to fields with duplicates

---

## Related Skills

- **bknd-create-entity** - Create new entities
- **bknd-add-field** - Add fields to entities
- **bknd-delete-entity** - Safely remove entities
- **bknd-seed-data** - Populate migrated data
- **bknd-crud-update** - Update records during migration

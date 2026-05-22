---
name: database-migrator
description: Safely migrate Firestore data, update schemas, and handle backwards compatibility. Use when changing data structures, adding fields, restructuring collections, or needing rollback strategies.
---

# Database Migration Manager

## When to Use
- Adding new fields to existing documents
- Renaming or removing fields
- Changing field types
- Restructuring collections
- Splitting or merging collections
- Backfilling data

## Quick Reference

### Safe Migration Principles

1. **Always backwards compatible** - Old code should work with new data
2. **Never delete fields immediately** - Deprecate first, delete later
3. **Test on emulator first** - Never run untested migrations on prod
4. **Batch operations** - Use batched writes for large datasets
5. **Idempotent migrations** - Safe to run multiple times

### Adding a New Field

**Step 1: Update types (backwards compatible)**
```typescript
// packages/types/src/journal.ts
interface JournalEntry {
  id: string;
  title: string;
  content: string;
  // New optional field - backwards compatible
  sentiment?: 'positive' | 'negative' | 'neutral';
}
```

**Step 2: Update write operations**
```typescript
// When creating new entries, include the field
const newEntry = {
  ...data,
  sentiment: analyzeSentiment(data.content),
};
```

**Step 3: Handle missing values in reads**
```typescript
// In components, provide defaults
const sentiment = entry.sentiment ?? 'neutral';
```

**Step 4 (Optional): Backfill existing data**
```typescript
// scripts/backfill-sentiment.ts
import { getFirestore, collection, getDocs, writeBatch } from 'firebase/firestore';

async function backfillSentiment() {
  const db = getFirestore();
  const entriesRef = collection(db, 'journal_entries');
  const snapshot = await getDocs(entriesRef);

  const batch = writeBatch(db);
  let count = 0;

  for (const doc of snapshot.docs) {
    const data = doc.data();

    // Skip if already has sentiment
    if (data.sentiment) continue;

    batch.update(doc.ref, {
      sentiment: analyzeSentiment(data.content),
    });

    count++;

    // Firestore batch limit is 500
    if (count % 500 === 0) {
      await batch.commit();
      console.log(`Migrated ${count} documents`);
    }
  }

  // Commit remaining
  if (count % 500 !== 0) {
    await batch.commit();
  }

  console.log(`Migration complete: ${count} documents updated`);
}
```

### Renaming a Field

**Never rename directly. Use a 3-step process:**

**Step 1: Add new field, keep old**
```typescript
interface Entry {
  // Old field (deprecated)
  /** @deprecated Use coverImageId instead */
  coverImage?: string;
  // New field
  coverImageId?: string;
}

// Write to both during transition
const update = {
  coverImage: imageId,      // Keep for old clients
  coverImageId: imageId,    // New field
};
```

**Step 2: Migrate reads to new field**
```typescript
// Handle both in reads
const coverImageId = entry.coverImageId ?? entry.coverImage;
```

**Step 3: After all clients updated, remove old field**
```typescript
// Migration script to remove deprecated field
async function removeDeprecatedField() {
  const snapshot = await getDocs(collection(db, 'entries'));
  const batch = writeBatch(db);

  for (const doc of snapshot.docs) {
    if ('coverImage' in doc.data()) {
      batch.update(doc.ref, {
        coverImage: deleteField(),
      });
    }
  }

  await batch.commit();
}
```

### Restructuring Collections

**Example: Moving from flat to nested**

Before:
```
users/{userId}/entries/{entryId}
  - spaceId: "abc"
  - content: "..."
```

After:
```
spaces/{spaceId}/entries/{entryId}
  - ownerId: "userId"
  - content: "..."
```

**Migration approach:**

```typescript
// Phase 1: Write to both locations
async function createEntry(userId: string, spaceId: string, data: EntryData) {
  const batch = writeBatch(db);

  // Old location (for backward compat)
  const oldRef = doc(collection(db, `users/${userId}/entries`));
  batch.set(oldRef, { ...data, spaceId });

  // New location
  const newRef = doc(collection(db, `spaces/${spaceId}/entries`));
  batch.set(newRef, { ...data, ownerId: userId });

  await batch.commit();
  return newRef.id;
}

// Phase 2: Migrate existing data
async function migrateToSpaces() {
  const usersSnapshot = await getDocs(collection(db, 'users'));

  for (const userDoc of usersSnapshot.docs) {
    const entriesSnapshot = await getDocs(
      collection(db, `users/${userDoc.id}/entries`)
    );

    for (const entryDoc of entriesSnapshot.docs) {
      const data = entryDoc.data();
      const spaceId = data.spaceId || 'personal';

      // Copy to new location
      await setDoc(
        doc(db, `spaces/${spaceId}/entries/${entryDoc.id}`),
        { ...data, ownerId: userDoc.id }
      );
    }
  }
}

// Phase 3: Update reads to use new location
// Phase 4: Stop writing to old location
// Phase 5: Delete old data (optional)
```

### Batch Operations

```typescript
import { writeBatch, doc } from 'firebase/firestore';

async function batchUpdate(
  documents: { id: string; data: Partial<Entry> }[]
) {
  const BATCH_SIZE = 500; // Firestore limit

  for (let i = 0; i < documents.length; i += BATCH_SIZE) {
    const batch = writeBatch(db);
    const chunk = documents.slice(i, i + BATCH_SIZE);

    for (const { id, data } of chunk) {
      batch.update(doc(db, 'entries', id), data);
    }

    await batch.commit();
    console.log(`Processed ${Math.min(i + BATCH_SIZE, documents.length)}/${documents.length}`);
  }
}
```

### Testing Migrations

```bash
# Start emulator
firebase emulators:start --only firestore

# In another terminal, seed test data
npx ts-node scripts/seed-test-data.ts

# Run migration
npx ts-node scripts/migrate-xyz.ts

# Verify results
npx ts-node scripts/verify-migration.ts
```

## Migration Checklist

### Before Migration
- [ ] Create backup of production data
- [ ] Test migration on emulator
- [ ] Review data volume (may need pagination)
- [ ] Plan rollback strategy
- [ ] Schedule during low-traffic period

### During Migration
- [ ] Monitor Firestore quotas
- [ ] Log progress for long-running migrations
- [ ] Handle errors gracefully (don't stop on single doc failure)

### After Migration
- [ ] Verify data integrity
- [ ] Update security rules if needed
- [ ] Update indexes if needed
- [ ] Remove deprecated code after grace period

## Rollback Strategies

### Field Addition
```typescript
// Rollback: Just stop writing the field
// Old code already handles missing values
```

### Field Rename
```typescript
// Rollback: Continue reading from old field
const value = doc.newField ?? doc.oldField;
```

### Collection Move
```typescript
// Rollback: Switch reads back to old collection
// Keep dual-write active until stable
```

## Common Patterns

### Timestamp Migration
```typescript
// Convert Date objects to Firestore Timestamps
import { Timestamp } from 'firebase/firestore';

const timestamp = data.createdAt instanceof Date
  ? Timestamp.fromDate(data.createdAt)
  : data.createdAt;
```

### Null to Default
```typescript
// Replace null values with defaults
const update: Record<string, unknown> = {};
if (doc.data().tags === null) {
  update.tags = [];
}
if (doc.data().archived === null) {
  update.archived = false;
}
batch.update(doc.ref, update);
```

### Type Coercion
```typescript
// Convert string IDs to references
const spaceRef = doc(db, 'spaces', data.spaceId);
batch.update(entryRef, { space: spaceRef });
```

## See Also
- [examples.md](examples.md) - Real migration scripts
- [scripts/](scripts/) - Reusable migration utilities

---
name: Offline Sync Strategies
description: Advanced conflict resolution and data consistency patterns for offline-first architecture
---

# Offline Sync Strategies

LivestockAI's "Action Era" requires robust handling of data conflicts beyond simple "last-write-wins".

## The Problem: Dependent Mutations

A user offline might:

1. Create Batch A (Temp ID: `tmp_123`)
2. Log Feed for Batch A (Refers to `tmp_123`)
3. Record Mortality for Batch A (Refers to `tmp_123`)

If the sync order is wrong, or if Batch A creation fails on the server, the subsequent records will be orphaned or invalid.

## Strategy 1: Optimistic ID Generation

**Always** generate UUIDs on the client using `crypto.randomUUID()`. Do not rely on server-side ID generation for primary entities.

```typescript
// ✅ Correct
const batchId = crypto.randomUUID()
const batch = { id: batchId, ...data }
await db.batches.add(batch) // IndexedDB
await syncQueue.add({ type: 'CREATE_BATCH', payload: batch })

// ❌ Wrong (Server ID dependency)
const response = await api.createBatch(data)
const batchId = response.id // Fails if offline
```

## Strategy 2: Operation Replay

The Sync Queue must process operations serially per entity.

```typescript
interface SyncOperation {
  id: string
  entityId: string // Partition key for ordering
  type: 'CREATE' | 'UPDATE' | 'DELETE'
  payload: any
  occurredAt: number
}
```

**Rule:** If `CREATE` fails, all subsequent `UPDATE` operations for that `entityId` must be effectively paused or moved to a "Dead Letter Queue" for manual intervention.

## Strategy 3: Conflict Resolution Modes

### Field-Level Merge (JSON Patch)

Used for: Settings, Profile updates.
User A changes Name. User B changes Email. Both succeed.

### Last-Write-Wins (LWW)

Used for: Sensor readings, Status updates.
The latest timestamp prevails.

### Append-Only (Commutative)

Used for: Feed Logs, Mortality Records, Sales.
These are "facts" that occurred. They don't update _state_; they append _events_.
_Even if two users log feed at the same time, both logs are valid._

## Strategy 4: The "Soft Delete" Handling

Never hard delete entities on the client. Mark as `deletedAt: timestamp`.
Server syncs the deletion.
Other clients receive "tombstone" updates.

## UI Patterns for Conflict

When automated resolution is impossible (e.g. User A sets Price=500, User B sets Price=600 for the same sale):

1. **Quarantine:** The item stays local.
2. **Notification:** "Conflict detected in Batch A."
3. **Resolution UI:** Show Side-by-Side comparison. "Keep Yours" vs "Keep Server's".

## Related Skills

- `offline-first` - The mechanism (IndexedDB/TanStack Query)
- `batch-centric-design` - The UI context for these operations

---
name: supabase-offline-sync
description: Implement offline-first sync between Expo SQLite and Supabase with queue-based reconciliation. Use when building offline-first mobile apps, syncing local SQLite with cloud PostgreSQL, handling conflict resolution, implementing background sync, or managing sync queues with retry logic.
---

# Supabase Offline-First Sync

Queue-based sync architecture for offline-first Expo apps using SQLite and Supabase.

## Architecture Overview

```
Local Write → SQLite → Sync Queue → Background Worker → Supabase
                              ↑____________↓ (retry on failure)
```

## Database Schema

### Sync Queue Table

```sql
CREATE TABLE sync_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  table_name TEXT NOT NULL,
  record_id TEXT NOT NULL,
  operation TEXT NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
  data TEXT, -- JSON string for INSERT/UPDATE
  retry_count INTEGER DEFAULT 0,
  error_message TEXT,
  created_at INTEGER NOT NULL,
  processed_at INTEGER
);

CREATE INDEX idx_sync_queue_created ON sync_queue(created_at);
CREATE INDEX idx_sync_queue_processed ON sync_queue(processed_at) WHERE processed_at IS NULL;
```

## Core Implementation

### 1. Queue Operations

```typescript
interface SyncQueueItem {
  id?: number;
  table_name: string;
  record_id: string;
  operation: 'INSERT' | 'UPDATE' | 'DELETE';
  data?: string;
  retry_count: number;
  created_at: number;
}

async function enqueueSync(
  db: SQLiteDatabase,
  table: string,
  recordId: string,
  operation: 'INSERT' | 'UPDATE' | 'DELETE',
  data?: object,
): Promise<void> {
  await db.runAsync(
    `INSERT INTO sync_queue (table_name, record_id, operation, data, retry_count, created_at)
     VALUES (?, ?, ?, ?, 0, ?)`,
    table,
    recordId,
    operation,
    data ? JSON.stringify(data) : null,
    Date.now(),
  );
}
```

### 2. Process Queue

```typescript
async function processSyncQueue(db: SQLiteDatabase, supabase: SupabaseClient): Promise<void> {
  const pending = await db.getAllAsync<SyncQueueItem>(
    `SELECT * FROM sync_queue 
     WHERE processed_at IS NULL AND retry_count < 5
     ORDER BY created_at ASC
     LIMIT 50`,
  );

  // Process DELETEs first to avoid FK conflicts
  const deletes = pending.filter((p) => p.operation === 'DELETE');
  const others = pending.filter((p) => p.operation !== 'DELETE');

  for (const item of [...deletes, ...others]) {
    try {
      await processQueueItem(db, supabase, item);
    } catch (error) {
      await markFailed(db, item.id!, error.message);
    }
  }
}
```

### 3. Process Individual Item

```typescript
async function processQueueItem(
  db: SQLiteDatabase,
  supabase: SupabaseClient,
  item: SyncQueueItem,
): Promise<void> {
  const { error } = await supabase.from(item.table_name).upsert(
    {
      id: item.record_id,
      ...(item.data ? JSON.parse(item.data) : {}),
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'id' },
  );

  if (error) throw error;

  // Mark as processed
  await db.runAsync('UPDATE sync_queue SET processed_at = ? WHERE id = ?', Date.now(), item.id);
}
```

## React Integration

### Sync Context Provider

```typescript
export function SyncProvider({ children }: { children: React.ReactNode }) {
  const { db } = useDatabase();
  const { supabase } = useSupabase();
  const netInfo = useNetInfo();

  useEffect(() => {
    if (!db || !supabase || !netInfo.isConnected) return;

    // Sync on connection restore
    const interval = setInterval(() => {
      processSyncQueue(db, supabase);
    }, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, [db, supabase, netInfo.isConnected]);

  return children;
}
```

## Optimistic Updates Pattern

```typescript
function useCreateJournal() {
  const queryClient = useQueryClient();
  const { db } = useDatabase();

  return useMutation({
    mutationFn: async (entry: JournalEntry) => {
      // 1. Save locally
      await db.runAsync(
        'INSERT INTO journal (id, encrypted_body, created_at) VALUES (?, ?, ?)',
        entry.id,
        await encryptContent(entry.content),
        entry.created_at,
      );

      // 2. Queue for sync
      await enqueueSync(db, 'journal', entry.id, 'INSERT', entry);

      return entry;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['journal'] });
    },
  });
}
```

## Conflict Resolution

Last-write-wins with server timestamp:

```typescript
async function resolveConflict(local: JournalEntry, remote: JournalEntry): Promise<JournalEntry> {
  const localTime = new Date(local.updated_at).getTime();
  const remoteTime = new Date(remote.updated_at).getTime();

  return remoteTime > localTime ? remote : local;
}
```

## Background Sync (Expo)

```typescript
import * as BackgroundFetch from 'expo-background-fetch';
import * as TaskManager from 'expo-task-manager';

const SYNC_TASK = 'background-sync';

TaskManager.defineTask(SYNC_TASK, async () => {
  const db = await openDatabase();
  const supabase = createClient();

  try {
    await processSyncQueue(db, supabase);
    return BackgroundFetch.BackgroundFetchResult.NewData;
  } catch {
    return BackgroundFetch.BackgroundFetchResult.Failed;
  }
});

async function registerBackgroundSync() {
  await BackgroundFetch.registerTaskAsync(SYNC_TASK, {
    minimumInterval: 15 * 60, // 15 minutes
    stopOnTerminate: false,
    startOnBoot: true,
  });
}
```

## Retry Strategy

Exponential backoff for failed items:

```typescript
async function markFailed(db: SQLiteDatabase, queueId: number, error: string): Promise<void> {
  await db.runAsync(
    `UPDATE sync_queue 
     SET retry_count = retry_count + 1,
         error_message = ?,
         created_at = ? -- Delay retry
     WHERE id = ?`,
    error,
    Date.now() + Math.pow(2, retry_count) * 60000, // Exponential backoff
    queueId,
  );
}
```

## Best Practices

1. **Process DELETEs first** - Avoids foreign key constraint errors
2. **Batch operations** - Process 50 items at a time
3. **Encrypt before sync** - Never send plaintext sensitive data
4. **User-scoped sync** - Always filter by `user_id` in Supabase RLS
5. **Retry limit** - Max 5 retries before manual intervention
6. **Conflict timestamps** - Use `updated_at` for last-write-wins

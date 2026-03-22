---
name: web-pwa-offline-first
description: Local-first architecture with sync queues
---

# Offline-First Application Patterns

> **Quick Guide:** Build applications that work primarily with local data, treating network connectivity as an enhancement. Use IndexedDB (via Dexie.js 4.x or idb 8.x) as the single source of truth. Implement sync queues for reliable background synchronization. Use optimistic UI patterns for instant feedback. Note: Background Sync API is experimental with limited browser support (Chrome/Edge only).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use IndexedDB (via wrapper library) as the single source of truth for all offline data)**

**(You MUST implement sync metadata (\_syncStatus, \_lastModified, \_localVersion) on ALL entities that need synchronization)**

**(You MUST queue mutations during offline and process them when connectivity returns)**

**(You MUST use soft deletes (tombstones) for deletions to enable proper sync across devices)**

**(You MUST implement exponential backoff with jitter for ALL sync retry logic)**

**(You MUST NOT await non-IndexedDB operations mid-transaction - transactions auto-close when control returns to event loop)**

</critical_requirements>

---

**Auto-detection:** offline-first, IndexedDB, Dexie, idb, sync queue, local-first, offline storage, background sync, optimistic UI offline, conflict resolution, CRDT, last-write-wins

**When to use:**

- Building applications that must work without network connectivity
- Field service apps with poor or intermittent connectivity
- Note-taking or productivity apps requiring instant responsiveness
- Apps where data ownership and local-first architecture is prioritized
- Progressive Web Apps (PWAs) needing robust offline support

**When NOT to use:**

- Real-time dashboards requiring always-fresh server data
- Financial transactions requiring immediate server confirmation
- Simple read-only apps where cache-first is sufficient
- Apps where offline capability adds no user value

**Storage Considerations:**

- IndexedDB: Up to 50% of available disk space (typically 1GB+), async, supports complex queries
- LocalStorage: Limited to 5MB per origin, synchronous (blocks UI), simple key-value only
- Safari: 7-day cap on script-writable storage (IndexedDB, Cache API) may evict data

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Syncable entities, repository pattern, sync queue, network detection, optimistic UI, connection-aware fetching
- [examples/indexeddb.md](examples/indexeddb.md) - Dexie.js setup, CRUD hooks, idb alternative, migrations, multi-tab coordination, quota management
- [examples/sync.md](examples/sync.md) - LWW resolution, field-level merge, conflict UI, version vectors, delta sync, background sync, pull-push strategy, sync indicators
- [reference.md](reference.md) - Decision frameworks, anti-patterns, troubleshooting

---

<philosophy>

## Philosophy

Offline-first is a design philosophy where applications are built to work primarily with local data, treating network connectivity as an enhancement rather than a requirement.

**Core Principles:**

1. **Local is the Source of Truth:** The local database is always authoritative. All reads and writes go through local storage first. Server sync happens in the background.

2. **Immediate Responsiveness:** Users never wait for network operations. Changes are applied locally instantly, synced later.

3. **Graceful Degradation:** Apps work fully offline, enhance when online, and handle transitions seamlessly.

4. **Sync Transparency:** Users understand their data's sync state through clear UI indicators without technical jargon.

**The Offline-First Data Flow:**

```
User Action
    |
Local Database (IndexedDB) <-- Single Source of Truth
    |
UI Updates Immediately (Optimistic)
    |
Sync Queue (Background)
    |
Server (When Online)
    |
Conflict Resolution (If Needed)
    |
Local Database Updated
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Syncable Entity Structure

Every entity that needs synchronization must include metadata for tracking sync state. This is the foundational pattern - all other patterns depend on it.

```typescript
interface SyncableEntity {
  id: string;
  _syncStatus: "synced" | "pending" | "conflicted";
  _lastModified: number;
  _serverTimestamp?: number;
  _localVersion: string;
  _serverVersion?: string;
  _deletedAt?: number; // Soft delete tombstone
}
```

**Why this matters:** Without sync metadata, you cannot track what needs syncing, detect conflicts, or implement soft deletes. See [examples/core.md](examples/core.md) Pattern 1 for full implementation with factory functions.

---

### Pattern 2: Repository Pattern

Use a repository as the single access point for all data operations, encapsulating local storage and sync queue logic. All reads come from local DB, all writes save locally first then queue for sync.

```typescript
interface DataRepository<T extends SyncableEntity> {
  get(id: string): Promise<T | null>;
  getAll(): Promise<T[]>;
  save(item: T): Promise<void>; // Local write + queue sync
  delete(id: string): Promise<void>; // Soft delete + queue sync
  getPendingCount(): Promise<number>;
}
```

**Why this matters:** Encapsulates the local-first write pattern (save locally, queue for sync) so consumers don't need to manage both operations. See [examples/core.md](examples/core.md) Pattern 2 for full implementation.

---

### Pattern 3: Sync Queue with Retry

Queue operations when offline, process reliably with exponential backoff when connectivity returns.

```typescript
const MAX_RETRY_ATTEMPTS = 5;
const INITIAL_BACKOFF_MS = 1000;
const MAX_BACKOFF_MS = 30000;

function calculateBackoff(attempt: number): number {
  const exponentialDelay = Math.min(
    INITIAL_BACKOFF_MS * Math.pow(2, attempt),
    MAX_BACKOFF_MS,
  );
  const jitter = exponentialDelay * 0.5 * (Math.random() * 2 - 1);
  return Math.floor(exponentialDelay + jitter);
}
```

**Why this matters:** Without retry logic, transient network failures cause permanent data loss. Jitter prevents thundering herd when many clients reconnect simultaneously. See [examples/core.md](examples/core.md) Pattern 3 for full queue implementation.

---

### Pattern 4: Network Status Detection

Don't rely solely on `navigator.onLine` (returns `true` behind captive portals, dead WiFi). Verify with actual health check requests.

```typescript
async function checkConnectivity(): Promise<boolean> {
  if (!navigator.onLine) return false;
  try {
    const response = await fetch("/api/health", {
      method: "HEAD",
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}
```

**Why this matters:** `navigator.onLine` only checks for a network interface, not actual internet connectivity. See [examples/core.md](examples/core.md) Pattern 4 for full status manager with slow connection detection.

---

### Pattern 5: Optimistic UI with Rollback

Update UI immediately, store previous value for rollback if sync fails. Return a rollback function from each optimistic update.

See [examples/core.md](examples/core.md) Pattern 5 for full implementation with rollback support.

---

### Pattern 6: Connection-Aware Data Fetching

Fetch from network when online, fall back to cache when offline. Return source metadata (`"network"` | `"cache"`) so UI can indicate data freshness.

See [examples/core.md](examples/core.md) Pattern 6 for full implementation with timeout and cache fallback.

---

### Pattern 7: Conflict Resolution Strategies

Three strategies ordered by complexity:

1. **Last-Write-Wins (LWW):** Simplest. Most recent timestamp wins. Good for independent values. See [examples/sync.md](examples/sync.md) Pattern 18.

2. **Field-Level Merge:** Only conflicts where both sides changed the _same_ field. Preserves non-conflicting changes from both sides. See [examples/sync.md](examples/sync.md) Pattern 19.

3. **Version Vectors:** Detect true concurrent modifications without clock synchronization. Use when timestamp-based approaches fail due to clock drift. See [examples/sync.md](examples/sync.md) Pattern 21.

For collaborative text editing, use a CRDT library (separate concern from this skill).

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Never use hard deletes - soft delete with tombstones or data will "resurrect" after sync
- Never trust `navigator.onLine` alone - verify with actual network request
- Never block UI on network operations - save locally first, sync in background
- Never await `fetch()` or `setTimeout()` inside an IndexedDB transaction - transaction auto-closes

**Medium Priority:**

- No retry logic on sync operations - transient failures cause permanent data loss
- No sync status indicators in UI - users lose trust when they can't see sync state
- Unbounded sync queue - can exhaust storage or cause OOM during batch processing
- Timestamp-only conflict detection - clock drift makes this unreliable for concurrent edits

**Gotchas & Edge Cases:**

- Safari (iOS 13.4+) enforces a 7-day cap on script-writable storage if the user doesn't interact with the site; request `navigator.storage.persist()` and encourage home screen install
- `navigator.storage.estimate()` requires HTTPS; returns `{ usage: 0, quota: 0 }` in unsecured contexts
- Background Sync API is Chrome/Edge only (experimental) - always implement `online` event listener as fallback
- IndexedDB compound index queries use arrays: `.where("[userId+completed]").equals([userId, 1])` (1 = true)
- Dexie `useLiveQuery` returns `undefined` while loading, not `null` - check with `=== undefined`
- Multiple tabs can cause write conflicts - use `BroadcastChannel` for coordination (see [examples/indexeddb.md](examples/indexeddb.md) Pattern 16)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use IndexedDB (via wrapper library) as the single source of truth for all offline data)**

**(You MUST implement sync metadata (\_syncStatus, \_lastModified, \_localVersion) on ALL entities that need synchronization)**

**(You MUST queue mutations during offline and process them when connectivity returns)**

**(You MUST use soft deletes (tombstones) for deletions to enable proper sync across devices)**

**(You MUST implement exponential backoff with jitter for ALL sync retry logic)**

**(You MUST NOT await non-IndexedDB operations mid-transaction - transactions auto-close when control returns to event loop)**

**Failure to follow these rules will result in data loss, sync conflicts, and poor offline user experience.**

</critical_reminders>

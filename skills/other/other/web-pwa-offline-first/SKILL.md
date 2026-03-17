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

**Key patterns covered:**

- IndexedDB setup with Dexie.js and idb
- Sync queue management and background synchronization
- Conflict resolution strategies (LWW, field-merge, version vectors)
- Optimistic UI with offline support
- Network status detection and connection-aware fetching
- Soft deletes and tombstone patterns

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

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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
    ↓
Local Database (IndexedDB) ← Single Source of Truth
    ↓
UI Updates Immediately (Optimistic)
    ↓
Sync Queue (Background)
    ↓
Server (When Online)
    ↓
Conflict Resolution (If Needed)
    ↓
Local Database Updated
```

**Why Local-First Matters:**

- **Reliability:** Network failures don't break the app
- **Speed:** No network latency for reads or writes
- **Ownership:** Users control their data
- **Battery:** Fewer network requests save power

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Syncable Entity Structure

Every entity that needs synchronization must include metadata for tracking sync state.

```typescript
// ✅ Good Example - Syncable entity with full metadata
interface SyncableEntity {
  id: string;

  // Sync tracking fields
  _syncStatus: "synced" | "pending" | "conflicted";
  _lastModified: number; // Client timestamp
  _serverTimestamp?: number; // Server timestamp for conflict resolution
  _localVersion: string; // Local revision ID (UUID)
  _serverVersion?: string; // Server revision ID
  _deletedAt?: number; // Soft delete timestamp (tombstone)
}

// Named constants for sync status
const SYNC_STATUS = {
  SYNCED: "synced",
  PENDING: "pending",
  CONFLICTED: "conflicted",
} as const;

// Example: Todo entity with sync metadata
interface Todo extends SyncableEntity {
  title: string;
  completed: boolean;
  userId: string;
}

// Factory function for creating syncable entities
function createTodo(title: string, userId: string): Todo {
  return {
    id: crypto.randomUUID(),
    title,
    completed: false,
    userId,
    _syncStatus: SYNC_STATUS.PENDING,
    _lastModified: Date.now(),
    _localVersion: crypto.randomUUID(),
  };
}
```

**Why good:** Clear separation of business data and sync metadata, named constants prevent typos, factory function ensures consistent creation, all fields have explicit types

```typescript
// ❌ Bad Example - No sync metadata
interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

// No way to track:
// - Whether this todo has been synced
// - When it was last modified
// - If there's a conflict
// - If it's been soft-deleted
```

**Why bad:** No sync tracking means data can be lost during sync, no conflict detection possible, hard deletes prevent proper multi-device sync

---

### Pattern 2: Repository Pattern for Data Access

Use a repository as the single access point for all data operations, encapsulating local storage and sync queue logic.

```typescript
// ✅ Good Example - Repository pattern
import type { Table } from "dexie";

interface DataRepository<T extends SyncableEntity> {
  // Reads always from local
  get(id: string): Promise<T | null>;
  getAll(): Promise<T[]>;
  query(filter: (item: T) => boolean): Promise<T[]>;

  // Writes go local first, then queue sync
  save(item: T): Promise<void>;
  delete(id: string): Promise<void>;

  // Sync status
  getSyncStatus(id: string): Promise<SyncStatus>;
  getPendingCount(): Promise<number>;
}

type SyncStatus = "synced" | "pending" | "conflicted" | "error";

class TodoRepository implements DataRepository<Todo> {
  constructor(
    private readonly localDb: Table<Todo, string>,
    private readonly syncQueue: SyncQueue,
  ) {}

  async get(id: string): Promise<Todo | null> {
    const todo = await this.localDb.get(id);
    // Filter out soft-deleted items
    if (todo?._deletedAt) return null;
    return todo ?? null;
  }

  async getAll(): Promise<Todo[]> {
    return this.localDb.filter((todo) => !todo._deletedAt).toArray();
  }

  async save(todo: Todo): Promise<void> {
    const now = Date.now();

    // Update sync metadata
    const updatedTodo: Todo = {
      ...todo,
      _syncStatus: SYNC_STATUS.PENDING,
      _lastModified: now,
      _localVersion: crypto.randomUUID(),
    };

    // 1. Save to local database immediately
    await this.localDb.put(updatedTodo);

    // 2. Queue for background sync
    await this.syncQueue.enqueue({
      type: "UPSERT",
      collection: "todos",
      data: updatedTodo,
      timestamp: now,
    });
  }

  async delete(id: string): Promise<void> {
    const now = Date.now();

    // Soft delete - update with tombstone
    await this.localDb.update(id, {
      _syncStatus: SYNC_STATUS.PENDING,
      _lastModified: now,
      _deletedAt: now,
    });

    // Queue deletion for sync
    await this.syncQueue.enqueue({
      type: "DELETE",
      collection: "todos",
      data: { id },
      timestamp: now,
    });
  }

  async getSyncStatus(id: string): Promise<SyncStatus> {
    const todo = await this.localDb.get(id);
    return todo?._syncStatus ?? "error";
  }

  async getPendingCount(): Promise<number> {
    return this.localDb
      .where("_syncStatus")
      .equals(SYNC_STATUS.PENDING)
      .count();
  }
}

export { TodoRepository };
export type { DataRepository, SyncStatus };
```

**Why good:** Single access point for all data operations, encapsulates sync logic, soft deletes enable proper sync, sync status queryable, repository is testable in isolation

---

### Pattern 3: Sync Queue Management

Queue operations when offline and process them reliably when connectivity returns.

```typescript
// ✅ Good Example - Robust sync queue
interface QueuedOperation {
  id: string;
  type: "CREATE" | "UPDATE" | "DELETE" | "UPSERT";
  collection: string;
  data: unknown;
  timestamp: number;
  retryCount: number;
  lastError?: string;
}

// Named constants
const MAX_RETRY_ATTEMPTS = 5;
const INITIAL_BACKOFF_MS = 1000;
const MAX_BACKOFF_MS = 30000;
const BACKOFF_MULTIPLIER = 2;
const JITTER_FACTOR = 0.5;

function calculateBackoff(attempt: number): number {
  const exponentialDelay = Math.min(
    INITIAL_BACKOFF_MS * Math.pow(BACKOFF_MULTIPLIER, attempt),
    MAX_BACKOFF_MS,
  );

  // Add jitter to prevent thundering herd
  const jitter = exponentialDelay * JITTER_FACTOR * (Math.random() * 2 - 1);

  return Math.floor(exponentialDelay + jitter);
}

class SyncQueue {
  private readonly db: LocalDatabase;
  private readonly STORE_NAME = "syncQueue";
  private processing = false;

  constructor(db: LocalDatabase) {
    this.db = db;

    // Listen for online events
    if (typeof window !== "undefined") {
      window.addEventListener("online", () => this.processQueue());
    }
  }

  async enqueue(
    operation: Omit<QueuedOperation, "id" | "retryCount">,
  ): Promise<void> {
    await this.db.add(this.STORE_NAME, {
      ...operation,
      id: crypto.randomUUID(),
      retryCount: 0,
    });

    // Try to process immediately if online
    if (navigator.onLine) {
      this.processQueue();
    }
  }

  async processQueue(): Promise<void> {
    if (this.processing || !navigator.onLine) return;
    this.processing = true;

    try {
      const operations = await this.db.getAll(this.STORE_NAME);

      // Sort by timestamp to maintain order
      operations.sort((a, b) => a.timestamp - b.timestamp);

      for (const op of operations) {
        try {
          await this.executeOperation(op);
          // Success - remove from queue
          await this.db.delete(this.STORE_NAME, op.id);
        } catch (error) {
          await this.handleOperationError(op, error);
        }
      }
    } finally {
      this.processing = false;
    }
  }

  private async executeOperation(op: QueuedOperation): Promise<void> {
    const endpoint = `/api/${op.collection}`;

    const response = await fetch(endpoint, {
      method: this.getHttpMethod(op.type),
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(op.data),
    });

    if (!response.ok) {
      throw new Error(`Sync failed: ${response.status}`);
    }
  }

  private getHttpMethod(type: QueuedOperation["type"]): string {
    const methods: Record<QueuedOperation["type"], string> = {
      CREATE: "POST",
      UPDATE: "PUT",
      DELETE: "DELETE",
      UPSERT: "PUT",
    };
    return methods[type];
  }

  private async handleOperationError(
    op: QueuedOperation,
    error: unknown,
  ): Promise<void> {
    if (op.retryCount >= MAX_RETRY_ATTEMPTS) {
      // Move to dead letter queue or notify user
      console.error(
        `Operation ${op.id} failed after ${MAX_RETRY_ATTEMPTS} retries`,
        error,
      );
      await this.db.delete(this.STORE_NAME, op.id);
      // Emit event for UI to handle
      this.emitSyncFailure(op);
      return;
    }

    // Increment retry count and schedule retry
    const delay = calculateBackoff(op.retryCount);

    await this.db.put(this.STORE_NAME, {
      ...op,
      retryCount: op.retryCount + 1,
      lastError: error instanceof Error ? error.message : "Unknown error",
    });

    // Schedule retry
    setTimeout(() => this.processQueue(), delay);
  }

  private emitSyncFailure(op: QueuedOperation): void {
    window.dispatchEvent(new CustomEvent("sync-failure", { detail: op }));
  }

  async getQueueLength(): Promise<number> {
    const operations = await this.db.getAll(this.STORE_NAME);
    return operations.length;
  }
}

export { SyncQueue };
export type { QueuedOperation };
```

**Why good:** Exponential backoff with jitter prevents server overload, retry limits prevent infinite loops, operations sorted by timestamp maintain consistency, dead letter handling for failed operations, event emission for UI feedback

---

### Pattern 4: Network Status Detection

Reliably detect network status and adjust behavior accordingly.

```typescript
// ✅ Good Example - Robust network status detection
type NetworkStatus = "online" | "offline" | "slow";
type NetworkListener = (status: NetworkStatus) => void;

const SLOW_THRESHOLD_MS = 2000;
const HEALTH_CHECK_INTERVAL_MS = 30000;

class NetworkStatusManager {
  private status: NetworkStatus = navigator.onLine ? "online" : "offline";
  private listeners = new Set<NetworkListener>();
  private healthCheckInterval: ReturnType<typeof setInterval> | null = null;

  constructor() {
    this.setupEventListeners();

    // Initial health check if online
    if (navigator.onLine) {
      this.checkConnectionQuality();
    }
  }

  private setupEventListeners(): void {
    window.addEventListener("online", () => {
      this.updateStatus("online");
      this.checkConnectionQuality();
    });

    window.addEventListener("offline", () => {
      this.updateStatus("offline");
      this.stopHealthCheck();
    });
  }

  private updateStatus(newStatus: NetworkStatus): void {
    if (this.status !== newStatus) {
      this.status = newStatus;
      this.listeners.forEach((listener) => listener(newStatus));
    }
  }

  getStatus(): NetworkStatus {
    return this.status;
  }

  subscribe(listener: NetworkListener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  async checkConnectionQuality(): Promise<NetworkStatus> {
    if (!navigator.onLine) {
      this.updateStatus("offline");
      return "offline";
    }

    try {
      const start = performance.now();

      // Use a small health endpoint
      const response = await fetch("/api/health", {
        method: "HEAD",
        cache: "no-store",
      });

      const latency = performance.now() - start;

      if (!response.ok) {
        this.updateStatus("offline");
        return "offline";
      }

      const status = latency > SLOW_THRESHOLD_MS ? "slow" : "online";
      this.updateStatus(status);
      return status;
    } catch {
      this.updateStatus("offline");
      return "offline";
    }
  }

  startHealthCheck(): void {
    this.stopHealthCheck();
    this.healthCheckInterval = setInterval(
      () => this.checkConnectionQuality(),
      HEALTH_CHECK_INTERVAL_MS,
    );
  }

  private stopHealthCheck(): void {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
  }

  destroy(): void {
    this.stopHealthCheck();
    this.listeners.clear();
  }
}

// Singleton instance
const networkStatus = new NetworkStatusManager();

export { networkStatus, NetworkStatusManager };
export type { NetworkStatus, NetworkListener };
```

**Why good:** Doesn't rely solely on navigator.onLine (which can be unreliable), actual health check for real connectivity, slow connection detection, proper cleanup methods, event-based updates

---

### Pattern 5: Optimistic UI with Rollback

Update UI immediately and roll back if sync fails.

```typescript
// ✅ Good Example - Optimistic updates with rollback support
interface PendingChange<T> {
  id: string;
  previousValue: T | null;
  newValue: T;
  timestamp: number;
}

class OptimisticUpdateManager<T extends SyncableEntity> {
  private pendingChanges = new Map<string, PendingChange<T>>();

  async applyOptimistically(
    id: string,
    newValue: T,
    localDb: {
      get: (id: string) => Promise<T | undefined>;
      put: (value: T) => Promise<void>;
      delete: (id: string) => Promise<void>;
    },
    onUpdate: (items: T[]) => void,
    getAllItems: () => Promise<T[]>,
  ): Promise<() => Promise<void>> {
    // Get current value for potential rollback
    const previousValue = (await localDb.get(id)) ?? null;

    // Store pending change
    this.pendingChanges.set(id, {
      id,
      previousValue,
      newValue,
      timestamp: Date.now(),
    });

    // Apply optimistic update
    await localDb.put(newValue);

    // Notify UI
    const allItems = await getAllItems();
    onUpdate(allItems);

    // Return rollback function
    return async () => {
      const pending = this.pendingChanges.get(id);
      if (!pending) return;

      if (pending.previousValue) {
        await localDb.put(pending.previousValue);
      } else {
        await localDb.delete(id);
      }

      this.pendingChanges.delete(id);

      const updatedItems = await getAllItems();
      onUpdate(updatedItems);
    };
  }

  async confirmChange(id: string): Promise<void> {
    this.pendingChanges.delete(id);
  }

  hasPendingChanges(): boolean {
    return this.pendingChanges.size > 0;
  }

  getPendingChangeIds(): string[] {
    return Array.from(this.pendingChanges.keys());
  }
}

export { OptimisticUpdateManager };
export type { PendingChange };
```

**Why good:** Stores previous value for rollback, returns rollback function for error handling, tracks all pending changes, supports both update and create scenarios

---

### Pattern 6: Connection-Aware Data Fetching

Fetch from network when online, gracefully fall back to cache when offline.

```typescript
// ✅ Good Example - Connection-aware fetcher
const FETCH_TIMEOUT_MS = 10000;

interface FetchResult<T> {
  data: T;
  source: "network" | "cache";
  timestamp: number;
}

interface LocalCache {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T, timestamp?: number): Promise<void>;
}

async function fetchWithOfflineSupport<T>(
  url: string,
  localCache: LocalCache,
  options: RequestInit = {},
): Promise<FetchResult<T>> {
  const cacheKey = `fetch:${url}`;

  // Check if online
  if (!navigator.onLine) {
    const cached = await localCache.get<{ data: T; timestamp: number }>(
      cacheKey,
    );
    if (cached) {
      return {
        data: cached.data,
        source: "cache",
        timestamp: cached.timestamp,
      };
    }
    throw new Error("Offline and no cached data available");
  }

  try {
    const response = await fetch(url, {
      ...options,
      signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = (await response.json()) as T;
    const timestamp = Date.now();

    // Cache successful response
    await localCache.set(cacheKey, { data, timestamp });

    return { data, source: "network", timestamp };
  } catch (error) {
    // Try cache on network failure
    const cached = await localCache.get<{ data: T; timestamp: number }>(
      cacheKey,
    );
    if (cached) {
      console.warn("Network failed, using cached data:", error);
      return {
        data: cached.data,
        source: "cache",
        timestamp: cached.timestamp,
      };
    }
    throw error;
  }
}

export { fetchWithOfflineSupport };
export type { FetchResult, LocalCache };
```

**Why good:** Returns source metadata for UI indication, caches successful responses, falls back to cache on failure, timeout prevents hanging requests, typed cache interface

</patterns>

---

<integration>

## Integration Guide

**Offline-First is architecture-agnostic.** This skill covers the patterns and principles. Integration with specific frameworks or libraries is handled by their respective skills.

**Works with:**

- Your framework's state management for UI updates
- Your data fetching solution for network layer
- Your testing solution for offline scenario testing

**Defers to:**

- Service Worker caching strategies (service-worker skill if exists)
- CRDT libraries for collaborative editing (Yjs, Automerge)
- Specific database libraries (PouchDB, RxDB) for their APIs

</integration>

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

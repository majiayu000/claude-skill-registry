---
name: dexie-cache-sync
description: Dexie IndexedDB caching layer with Convex sync for local-first architecture. Covers sync hooks, optimistic updates (React state only), cascade deletes, orphan detection, SSR safety. Triggers on "cache", "dexie", "useCacheSync", "optimistic", "offline", "IndexedDB".
---

# Dexie Cache Sync

Local-first caching with Convex→Dexie sync, optimistic updates, offline queue. 10 tables: conversations, messages, notes, tasks, projects, attachments, toolCalls, sources, pendingMutations, userPreferences.

**Flow**: Convex subscription → useQuery → useEffect → cache.bulkPut → Dexie → useLiveQuery → Component

## Cache Schema

10 tables in `apps/web/src/lib/cache/db.ts`:

```typescript
class BlahChatCache extends Dexie {
  conversations!: Table<Doc<"conversations">>;
  messages!: Table<Doc<"messages">>;
  notes!: Table<Doc<"notes">>;
  tasks!: Table<Doc<"tasks">>;
  projects!: Table<Doc<"projects">>;
  attachments!: Table<Doc<"attachments">>;
  toolCalls!: Table<Doc<"toolCalls">>;
  sources!: Table<Doc<"sources">>;
  pendingMutations!: Table<PendingMutation>;
  userPreferences!: Table<CachedPreferences>;

  constructor() {
    super("blahchat-cache");
    this.version(4).stores({
      conversations: "_id, userId, parentMessageId, updatedAt, projectId",
      messages: "_id, conversationId, createdAt",
      attachments: "_id, messageId",
      toolCalls: "_id, messageId",
      sources: "_id, messageId",
      // ...
    });
  }
}
```

**SSR Guard**:

```typescript
// From apps/web/src/lib/cache/db.ts:98-118
let _cache: BlahChatCache | null = null;

function getCache(): BlahChatCache {
  if (typeof window === "undefined") {
    throw new Error(
      "Attempted to access IndexedDB cache during SSR. Ensure cache is only used in client components."
    );
  }
  if (!_cache) _cache = new BlahChatCache();
  return _cache;
}

export const cache = typeof window !== "undefined"
  ? getCache()
  : (null as unknown as BlahChatCache);
```

Only use cache in `"use client"` components.

## Sync Hook Pattern

Pattern from `apps/web/src/hooks/useCacheSync.ts`:

1. Subscribe to Convex with `useQuery`
2. On data change, sync to Dexie (bulkPut + orphan detection)
3. Read from Dexie with `useLiveQuery` for instant UI

**Message Sync** (with orphan detection):

```typescript
// From apps/web/src/hooks/useCacheSync.ts:16-141
export function useMessageCacheSync({
  conversationId,
  initialNumItems = 50,
}: MessageCacheSyncOptions) {
  // Convex subscription (real-time)
  const convexMessages = usePaginatedQuery(
    api.messages.listPaginated,
    conversationId ? { conversationId } : "skip",
    { initialNumItems }
  );

  // Sync to Dexie when Convex updates
  useEffect(() => {
    if (!conversationId || convexMessages.results === undefined) return;

    const syncCache = async () => {
      // Orphan detection: find Dexie records not in Convex
      const convexIds = new Set(convexMessages.results.map((m) => m._id));
      const dexieRecords = await cache.messages
        .where("conversationId")
        .equals(conversationId)
        .toArray();

      const orphanIds = dexieRecords
        .filter((d) => !convexIds.has(d._id))
        .map((d) => d._id);

      if (orphanIds.length > 0) await cache.messages.bulkDelete(orphanIds);
      if (convexMessages.results.length > 0)
        await cache.messages.bulkPut(convexMessages.results);
    };

    syncCache().catch(console.error);
  }, [convexMessages.results, conversationId]);

  // Read from Dexie (instant)
  const cachedMessages = useLiveQuery(
    () =>
      conversationId
        ? cache.messages
            .where("conversationId")
            .equals(conversationId)
            .sortBy("createdAt")
        : [],
    [conversationId],
    undefined // Return undefined while loading, not []
  );

  // Validation: ensure cached data matches current conversation
  const validatedMessages =
    conversationId === undefined
      ? cachedMessages
      : cachedMessages === undefined
        ? undefined
        : cachedMessages.length === 0
          ? cachedMessages // Empty conversation - valid!
          : cachedMessages.every((m) => m.conversationId === conversationId)
            ? cachedMessages
            : undefined; // Wrong conversation

  return {
    results: validatedMessages,
    loadMore: convexMessages.loadMore,
    status: convexMessages.status,
  };
}
```

**Conversation Sync** (with projectId filtering):

```typescript
// From apps/web/src/hooks/useCacheSync.ts:211-251
export function useConversationCacheSync(
  options: ConversationCacheSyncOptions = {}
) {
  const { projectId } = options;

  const conversations = useQuery(
    api.conversations.list,
    { projectId: projectId || undefined }
  );

  useEffect(() => {
    if (conversations === undefined) return;

    const syncCache = async () => {
      const convexIds = new Set(conversations.map((c) => c._id));
      const dexieRecords = await getConversationsByProject(projectId);

      const orphanIds = dexieRecords
        .filter((d) => !convexIds.has(d._id))
        .map((d) => d._id);

      if (orphanIds.length > 0) await cache.conversations.bulkDelete(orphanIds);
      if (conversations.length > 0) await cache.conversations.bulkPut(conversations);
    };

    syncCache().catch(console.error);
  }, [conversations, projectId]);

  const cachedConversations = useLiveQuery(
    () => getConversationsByProject(projectId),
    [projectId],
    [] as Doc<"conversations">[]
  );

  return {
    conversations: cachedConversations,
    isLoading: conversations === undefined,
  };
}
```

**Metadata Sync** (attachments, toolCalls, sources):

```typescript
// From apps/web/src/hooks/useCacheSync.ts:143-176
export function useMetadataCacheSync(messageIds: Id<"messages">[]) {
  const metadata = useQuery(
    api.messages.batchGetMetadata,
    messageIds.length > 0 ? { messageIds } : "skip"
  );

  useEffect(() => {
    if (!metadata) return;

    const syncOps: Promise<unknown>[] = [];
    if (metadata.attachments?.length) {
      syncOps.push(cache.attachments.bulkPut(metadata.attachments));
    }
    if (metadata.toolCalls?.length) {
      syncOps.push(cache.toolCalls.bulkPut(metadata.toolCalls));
    }
    if (metadata.sources?.length) {
      syncOps.push(cache.sources.bulkPut(metadata.sources));
    }
    if (syncOps.length > 0) {
      Promise.all(syncOps).catch(console.error);
    }
  }, [metadata]);
}
```

## Optimistic Updates (React State Only)

**CRITICAL**: Optimistic messages NEVER touch Dexie. React state only, deduped by time window when server confirms.

From `apps/web/src/hooks/useOptimisticMessages.ts`:

```typescript
// Time windows for deduplication
const MATCH_FUTURE_WINDOW_MS = 10_000; // Server can arrive 10s after optimistic
const MATCH_PAST_WINDOW_MS = 1_000; // Handle small clock skew

export function useOptimisticMessages({
  serverMessages,
}: UseOptimisticMessagesOptions) {
  const [optimisticMessages, setOptimisticMessages] = useState<
    OptimisticMessage[]
  >([]);

  // Add optimistic message (instant, before API call)
  const addOptimisticMessages = useCallback(
    (newMessages: OptimisticMessage[]) => {
      setOptimisticMessages((prev) => [...prev, ...newMessages]);
    },
    []
  );

  // Merge server + optimistic, dedupe by time window
  const messages = useMemo<MessageWithOptimistic[] | undefined>(() => {
    if (serverMessages === undefined) return undefined;

    return mergeWithOptimisticMessages(
      serverMessages as MessageWithOptimistic[],
      optimisticMessages
    );
  }, [serverMessages, optimisticMessages]);

  return { messages, addOptimisticMessages };
}

function mergeWithOptimisticMessages(
  serverMessages: MessageWithOptimistic[],
  optimisticMessages: OptimisticMessage[]
): MessageWithOptimistic[] {
  if (optimisticMessages.length === 0) return serverMessages;

  const serverByRole = {
    user: serverMessages.filter((m) => m.role === "user"),
    assistant: [], // Assistant messages never optimistic
  };

  const remainingOptimistic: OptimisticMessage[] = [];

  for (const opt of optimisticMessages) {
    const candidates = serverByRole[opt.role] || [];
    const matchIndex = candidates.findIndex((serverMsg) => {
      const timeDiff = serverMsg.createdAt - opt.createdAt;
      return (
        timeDiff >= -MATCH_PAST_WINDOW_MS &&
        timeDiff <= MATCH_FUTURE_WINDOW_MS
      );
    });

    if (matchIndex === -1) {
      remainingOptimistic.push(opt);
    } else {
      candidates.splice(matchIndex, 1); // Consume matched message
    }
  }

  return [...serverMessages, ...remainingOptimistic].sort(
    (a, b) => a.createdAt - b.createdAt
  );
}
```

**Clear on conversation switch**:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts:92-108
const conversationIdRef = useRef<string | undefined>(undefined);
const currentConversationId = serverMessages?.[0]?.conversationId;

useEffect(() => {
  if (
    conversationIdRef.current &&
    conversationIdRef.current !== currentConversationId
  ) {
    setOptimisticMessages([]);
  }
  conversationIdRef.current = currentConversationId;
}, [currentConversationId]);
```

## Cascade Delete Pattern

**CRITICAL**: Always delete attachments/toolCalls/sources when deleting messages.

From `apps/web/src/lib/cache/cleanup.ts`:

```typescript
// Delete messages and cascade to related data
await cache.transaction(
  "rw",
  [cache.messages, cache.attachments, cache.toolCalls, cache.sources],
  async () => {
    await cache.messages.bulkDelete(oldMessageIds);
    await cache.attachments
      .where("messageId")
      .anyOf(oldMessageIds)
      .delete();
    await cache.toolCalls.where("messageId").anyOf(oldMessageIds).delete();
    await cache.sources.where("messageId").anyOf(oldMessageIds).delete();
  }
);
```

Use in mutations/actions:

```typescript
// Delete single message with cascade
await Promise.all([
  cache.messages.delete(messageId),
  cache.attachments.where("messageId").equals(messageId).delete(),
  cache.toolCalls.where("messageId").equals(messageId).delete(),
  cache.sources.where("messageId").equals(messageId).delete(),
]);
```

## Orphan Detection

Sync hooks reconcile Convex (source of truth) vs Dexie (cache).

Pattern:

```typescript
const syncCache = async () => {
  // 1. Get Convex IDs (source of truth)
  const convexIds = new Set(convexData.map((item) => item._id));

  // 2. Get Dexie records (cache)
  const dexieRecords = await cache.table.toArray();

  // 3. Find orphans (in Dexie but not in Convex)
  const orphanIds = dexieRecords
    .filter((d) => !convexIds.has(d._id))
    .map((d) => d._id);

  // 4. Delete orphans
  if (orphanIds.length > 0) await cache.table.bulkDelete(orphanIds);

  // 5. Update/insert current data
  if (convexData.length > 0) await cache.table.bulkPut(convexData);
};
```

Messages/conversations have orphan detection. Notes/tasks/projects rely on cascade or time-based cleanup.

## Cleanup Strategy

From `apps/web/src/lib/cache/cleanup.ts`:

```typescript
const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000;
const NINETY_DAYS_MS = 90 * 24 * 60 * 60 * 1000;

export async function cleanupOldData(): Promise<void> {
  const thirtyDaysAgo = Date.now() - THIRTY_DAYS_MS;

  // Messages: 30 days (with cascade delete)
  const oldMessageIds = await cache.messages
    .where("createdAt")
    .below(thirtyDaysAgo)
    .primaryKeys();

  await cache.transaction(
    "rw",
    [cache.messages, cache.attachments, cache.toolCalls, cache.sources],
    async () => {
      await cache.messages.bulkDelete(oldMessageIds);
      await cache.attachments.where("messageId").anyOf(oldMessageIds).delete();
      await cache.toolCalls.where("messageId").anyOf(oldMessageIds).delete();
      await cache.sources.where("messageId").anyOf(oldMessageIds).delete();
    }
  );

  // Notes: 30 days since last update
  await cache.notes.where("updatedAt").below(thirtyDaysAgo).delete();

  // Tasks: 30 days for pending, 90 days for completed
  const ninetyDaysAgo = Date.now() - NINETY_DAYS_MS;
  const oldTaskIds = await cache.tasks
    .filter(
      (task) =>
        (task._creationTime < thirtyDaysAgo && task.status !== "completed") ||
        (task._creationTime < ninetyDaysAgo && task.status === "completed")
    )
    .primaryKeys();

  if (oldTaskIds.length > 0) {
    await cache.tasks.bulkDelete(oldTaskIds);
  }
}
```

Run on app start via CacheProvider. Non-blocking.

## Offline Queue

From `apps/web/src/lib/offline/messageQueue.ts`:

```typescript
export class MessageQueue {
  private readonly MAX_RETRIES = 3;

  async enqueue(
    message: Omit<QueuedMessage, "id" | "timestamp" | "retries">
  ): Promise<void> {
    const queuedMessage: QueuedMessage = {
      ...message,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      retries: 0,
    };

    await cache.pendingMutations.add({
      _id: queuedMessage.id,
      type: "sendMessage",
      payload: queuedMessage,
      createdAt: Date.now(),
      retries: 0,
    });

    this.dispatchQueueUpdate();
  }

  async processQueue(
    sendFn: (msg: QueuedMessage) => Promise<void>
  ): Promise<void> {
    const queue = await this.getQueue();

    for (const msg of queue) {
      try {
        await sendFn(msg);
        await this.remove(msg.id);
      } catch (_error) {
        if (msg.retries >= this.MAX_RETRIES) {
          await this.remove(msg.id);
          console.error(
            `[MessageQueue] Permanently failed after ${this.MAX_RETRIES} retries`
          );
        } else {
          await this.incrementRetry(msg.id);

          // Exponential backoff: 2s → 4s → 8s
          const backoffMs = 2000 * 2 ** msg.retries;
          await new Promise((resolve) => setTimeout(resolve, backoffMs));
        }
      }
    }
  }
}

export const messageQueue = new MessageQueue();
```

Auto-retry on reconnect with exponential backoff.

## Anti-Patterns

**DON'T**:

1. Put optimistic messages in Dexie - React state only
2. Delete messages without cascade (orphans attachments/toolCalls/sources)
3. Use cache in server components - SSR will throw
4. Skip orphan detection in sync hooks - causes stale data
5. Return empty array during loading - return `undefined` to distinguish from "no data"
6. Use raw Convex queries for cached tables - use sync hooks instead

**DO**:

1. Use `useLiveQuery` with dependency array for reactive reads
2. Validate cached data matches current context (conversation ID)
3. Clear optimistic messages on conversation switch
4. Use transactions for multi-table operations
5. Handle `undefined` vs `[]` correctly (loading vs empty)

## Key Files

- `apps/web/src/lib/cache/db.ts` - Schema, SSR guard
- `apps/web/src/hooks/useCacheSync.ts` - Sync hooks (messages, conversations, metadata, notes, tasks, projects, preferences)
- `apps/web/src/hooks/useOptimisticMessages.ts` - React state optimistic updates, time-window deduplication
- `apps/web/src/lib/cache/cleanup.ts` - 30/90 day cleanup
- `apps/web/src/lib/offline/messageQueue.ts` - Offline queue with exponential backoff
- `apps/web/src/components/providers/cache-provider.tsx` - Cleanup on app start

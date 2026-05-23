---
name: optimistic-ui
description: Optimistic message updates with time-window deduplication. React state only, never touches Dexie cache. Triggers on "optimistic", "useOptimisticMessages", "deduplication", "instant feedback".
---

# Optimistic UI Pattern

Instant feedback for user messages using React state overlay with time-window deduplication. Server confirms with real messages. Only user messages are optimistic - assistant messages created synchronously server-side.

**CRITICAL**: Optimistic messages NEVER touch Dexie cache. React state only.

## Only User Messages Are Optimistic

Server creates assistant messages synchronously in `convex/chat.ts:188-205`, so no client-side optimistic assistant messages exist:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
const optimisticUserMsg: OptimisticMessage = {
  _id: `temp-user-${Date.now()}` as `temp-${string}`,
  conversationId: variables.conversationId,
  userId: user?._id,
  role: "user" as const, // Only user role
  content: variables.content,
  status: "optimistic" as const,
  createdAt: Date.now(),
  _optimistic: true, // Flag for filtering
};

// Server creates assistant messages synchronously (convex/chat.ts:188-205)
// Only user message needs optimistic update for instant feedback
onOptimisticUpdate?.([optimisticUserMsg]);
```

## Time Window Matching

Match optimistic messages to server confirmations using time windows (not exact timestamps):

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
const MATCH_FUTURE_WINDOW_MS = 10_000; // Allow server message to arrive after optimistic
const MATCH_PAST_WINDOW_MS = 1_000;    // Handle small clock skew

function mergeWithOptimisticMessages(
  serverMessages: MessageWithOptimistic[],
  optimisticMessages: OptimisticMessage[],
): MessageWithOptimistic[] {
  // Group server messages by role (only user messages are optimistic)
  const serverByRole = {
    user: serverMessages.filter((m) => m.role === "user"),
    assistant: [], // Not used - assistant messages come from server only
  };

  // Sort for deterministic matching
  serverByRole.user.sort((a, b) => a.createdAt - b.createdAt);

  for (const opt of sortedOptimistic) {
    const candidates = serverByRole[opt.role] || [];
    const matchIndex = candidates.findIndex((serverMsg) => {
      // Time window check - match if server message arrived within window
      const timeDiff = serverMsg.createdAt - opt.createdAt;
      return (
        timeDiff >= -MATCH_PAST_WINDOW_MS && timeDiff <= MATCH_FUTURE_WINDOW_MS
      );
    });

    if (matchIndex === -1) {
      remainingOptimistic.push(opt);
      continue;
    }

    // Consume matched server message so it can't be reused
    candidates.splice(matchIndex, 1);
  }

  return [...serverMessages, ...remainingOptimistic].sort(
    (a, b) => a.createdAt - b.createdAt,
  );
}
```

**Why time windows**: Server timestamp may differ from client. 10s future window handles network latency. 1s past window handles clock skew.

## Deduplication Algorithm

Remove optimistic messages when server confirms:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
const messages = useMemo<MessageWithOptimistic[] | undefined>(() => {
  if (serverMessages === undefined) {
    // Keep previous data during loading (prevents flash)
    if (
      prevConversationIdRef.current &&
      prevConversationIdRef.current === currentConversationId
    ) {
      return prevMessagesRef.current ?? undefined;
    }
    return undefined;
  }

  const merged = mergeWithOptimisticMessages(
    serverMessages as MessageWithOptimistic[],
    optimisticMessages,
  );
  prevMessagesRef.current = merged;
  prevConversationIdRef.current = currentConversationId;
  return merged;
}, [serverMessages, optimisticMessages, currentConversationId]);
```

**Key**: `useMemo` filters out matched optimistic messages visually. State not cleaned up to avoid re-render flash.

## Conversation Switch Cleanup

Clear optimistic messages when switching conversations:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
const conversationIdRef = useRef<string | undefined>(undefined);
const currentConversationId = serverMessages?.[0]?.conversationId;

// Clear optimistic messages when conversation changes
// Handles all transitions:
// - Conversation A → B (clear A's optimistic messages)
// - Conversation A → undefined/loading (clear A's optimistic messages)
// - undefined → Conversation A (keep empty, no messages to clear)
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

## useMemo Patterns for Merge Logic

Use `useMemo` to recalculate only when inputs change:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
const messages = useMemo<MessageWithOptimistic[] | undefined>(() => {
  // Return undefined during loading if different conversation
  if (serverMessages === undefined) {
    if (
      prevConversationIdRef.current &&
      prevConversationIdRef.current === currentConversationId
    ) {
      return prevMessagesRef.current ?? undefined;
    }
    return undefined;
  }

  // Merge and cache
  const merged = mergeWithOptimisticMessages(
    serverMessages as MessageWithOptimistic[],
    optimisticMessages,
  );
  prevMessagesRef.current = merged;
  prevConversationIdRef.current = currentConversationId;
  return merged;
}, [serverMessages, optimisticMessages, currentConversationId]);
```

**Benefits**: Prevents unnecessary re-renders. Caches previous result during brief `undefined` states.

## Preventing Flash During Server Sync

Keep previous data when `serverMessages` becomes `undefined` temporarily:

```typescript
// From apps/web/src/hooks/useOptimisticMessages.ts
// Keep previous data during brief undefined states (prevents flash during pagination)
const prevMessagesRef = useRef<MessageWithOptimistic[] | undefined>(undefined);
const prevConversationIdRef = useRef<string | undefined>(undefined);

// If server messages are undefined (loading), only return cached if same conversation
if (serverMessages === undefined) {
  if (
    prevConversationIdRef.current &&
    prevConversationIdRef.current === currentConversationId
  ) {
    return prevMessagesRef.current ?? undefined;
  }
  return undefined;
}
```

**Why**: Convex queries briefly return `undefined` during pagination/refetch. Returning cached data prevents flash of empty state.

## Integration with useSendMessage Mutation

Mutation calls `onOptimisticUpdate` callback immediately before API call:

```typescript
// From apps/web/src/lib/hooks/mutations/useSendMessage.ts
return useMutation({
  mutationFn: async (args: SendMessageArgs) => {
    return apiClient.post(
      `/api/v1/conversations/${args.conversationId}/messages`,
      args,
    );
  },

  onMutate: (variables) => {
    // Create optimistic user message
    const optimisticUserMsg: OptimisticMessage = {
      _id: `temp-user-${Date.now()}` as `temp-${string}`,
      conversationId: variables.conversationId,
      userId: user?._id,
      role: "user" as const,
      content: variables.content,
      status: "optimistic" as const,
      attachments: variables.attachments?.map((att) => ({
        id: att.storageId,
        storageId: att.storageId as Id<"_storage">,
        _optimistic: true,
      })),
      createdAt: Date.now(),
      updatedAt: Date.now(),
      _creationTime: Date.now(),
      _optimistic: true,
    };

    // Server creates assistant messages synchronously (convex/chat.ts:188-205)
    // Only user message needs optimistic update for instant feedback
    onOptimisticUpdate?.([optimisticUserMsg]);

    return {
      optimisticIds: [optimisticUserMsg._id],
    };
  },

  onSuccess: (_data, variables) => {
    // Server confirmed - Convex query will update with real messages
    // Deduplication happens automatically in useOptimistic merge
    queryClient.invalidateQueries({
      queryKey: queryKeys.messages.list(variables.conversationId),
    });
  },

  onError: (error, variables, _context) => {
    // Optimistic messages will be cleaned up on next server update
    // (deduplication logic removes unconfirmed optimistic messages)
  },
});
```

## Usage Pattern

```typescript
// In chat page
const { messages, addOptimisticMessages } = useOptimisticMessages({
  serverMessages, // From Convex query
});

const sendMessageMutation = useSendMessage(addOptimisticMessages);

// Send message
sendMessageMutation.mutate({
  conversationId,
  content: "Hello",
  modelId: "gpt-4",
});
```

## Type Definition

```typescript
// From apps/web/src/types/optimistic.ts
export type OptimisticMessage = {
  _id: `temp-${string}`; // Temp ID pattern
  conversationId: Id<"conversations">;
  userId: Id<"users"> | undefined;
  role: "user"; // Only user role
  content: string;
  status: "optimistic";
  attachments?: Array<{
    id: string;
    storageId: Id<"_storage">;
    _optimistic: true; // Flag for filtering
  }>;
  createdAt: number;
  updatedAt: number;
  _creationTime: number;
  _optimistic: true; // Flag for filtering
};
```

## Key Files

- `apps/web/src/hooks/useOptimisticMessages.ts` - Core hook with merge logic
- `apps/web/src/lib/hooks/mutations/useSendMessage.ts` - Mutation integration
- `apps/web/src/types/optimistic.ts` - Type definitions

## Avoid

- Don't clean up optimistic state immediately after server confirms (causes re-render flash)
- Don't create optimistic assistant messages (server creates synchronously)
- Don't use exact timestamp matching (use time windows for clock skew)
- Don't touch Dexie cache with optimistic messages (React state only)
- Don't forget to clear optimistic messages on conversation switch

---
name: ably-realtime
description: Ably real-time messaging patterns, WebSocket channel management, message validation and processing, staleness filtering, error recovery strategies, collaborative editing with drag-and-drop, optimistic updates for voting, real-time board collaboration, and Ably integration best practices for ree-board project
model: sonnet
---

# Ably Real-time Collaboration

## When to Use This Skill

Activate this skill when working on:

- Implementing real-time features
- Setting up Ably channels
- Processing real-time messages
- Building collaborative editing features
- Implementing drag-and-drop with real-time sync
- Handling WebSocket connections
- Managing real-time state updates
- Optimizing real-time performance

## Core Patterns

### Channel Management

**Channel Naming Convention:**

```typescript
// Pattern: `board:{boardId}`
const channelName = `board:${boardId}`;
```

**Setting Up Channels:**

```typescript
"use client";

import { useChannel } from "ably/react";
import { useEffect } from "react";

export function PostChannelComponent({ boardId }: { boardId: string }) {
  const { channel } = useChannel(`board:${boardId}`, (message) => {
    processMessage(message);
  });

  return <PostList boardId={boardId} />;
}
```

### Message Processors with Validation

**Critical Pattern:** Always validate messages before processing

```typescript
// lib/realtime/messageProcessors.ts
import { z } from "zod";

// Define message schema
const PostUpdateMessageSchema = z.object({
  type: z.literal("post:update"),
  postId: z.string(),
  content: z.string().min(1).max(1000),
  userId: z.string(),
  timestamp: z.number(),
});

// Message processor
export const processPostUpdate = (rawData: unknown) => {
  try {
    // ✅ Validate message structure
    const data = PostUpdateMessageSchema.parse(rawData);

    // ✅ Check staleness (30s threshold)
    const now = Date.now();
    const age = now - data.timestamp;

    if (age > 30000) {
      console.warn("Stale message discarded", {
        type: data.type,
        age,
        postId: data.postId,
      });
      return;
    }

    // ✅ Process validated, fresh message
    updatePostContent(data.postId, data.content);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("Invalid message structure", {
        details: error.errors,
        rawData,
      });
    } else {
      console.error("Message processing error", error);
    }
  }
};
```

### Staleness Filtering

**30-Second Threshold:** Prevents processing old messages after reconnection

```typescript
const STALENESS_THRESHOLD_MS = 30000;

export function isMessageStale(timestamp: number): boolean {
  const age = Date.now() - timestamp;
  return age > STALENESS_THRESHOLD_MS;
}

// Usage in message handler
useChannel(`board:${boardId}`, (message) => {
  const { timestamp } = message.data;

  if (isMessageStale(timestamp)) {
    console.warn("Dropping stale message", { age: Date.now() - timestamp });
    return;
  }

  processMessage(message.data);
});
```

### Error Recovery Strategies

**Connection Error Handling:**

```typescript
import { useConnectionStateListener } from "ably/react";

export function RealtimeProvider({ children }: { children: React.ReactNode }) {
  const [connectionState, setConnectionState] = useState<string>("initialized");

  useConnectionStateListener((stateChange) => {
    setConnectionState(stateChange.current);

    switch (stateChange.current) {
      case "connected":
        console.log("✅ Connected to Ably");
        break;

      case "disconnected":
        console.warn("⚠️ Disconnected from Ably");
        break;

      case "suspended":
        console.error("❌ Connection suspended");
        // Optionally show user notification
        break;

      case "failed":
        console.error("❌ Connection failed");
        // Show error message to user
        break;
    }
  });

  return (
    <>
      {connectionState !== "connected" && (
        <ConnectionBanner state={connectionState} />
      )}
      {children}
    </>
  );
}
```

### Publishing Messages

**Always Include Timestamp:**

```typescript
import { useChannel } from "ably/react";

export function usePublishPostUpdate() {
  const { channel } = useChannel(`board:${boardId}`);

  const publishUpdate = async (postId: string, content: string) => {
    await channel.publish("post:update", {
      type: "post:update",
      postId,
      content,
      userId: currentUserId,
      timestamp: Date.now(), // ✅ Always include timestamp
    });
  };

  return publishUpdate;
}
```

### Optimistic Updates for Voting

**Pattern:** Update UI immediately, sync in background

```typescript
"use client";

import { voteSignal } from "@/lib/signal/postSignals";
import { useChannel } from "ably/react";

export function VoteButton({
  postId,
  boardId,
}: {
  postId: string;
  boardId: string;
}) {
  const { channel } = useChannel(`board:${boardId}`);

  const handleVote = async () => {
    // ✅ Optimistic update (immediate UI feedback)
    voteSignal.value = {
      ...voteSignal.value,
      [postId]: (voteSignal.value[postId] || 0) + 1,
    };

    try {
      // Persist to database
      await submitVote(postId);

      // Broadcast to other users
      await channel.publish("post:vote", {
        type: "post:vote",
        postId,
        increment: 1,
        timestamp: Date.now(),
      });
    } catch (error) {
      // ❌ Rollback on error
      voteSignal.value = {
        ...voteSignal.value,
        [postId]: voteSignal.value[postId] - 1,
      };
      console.error("Vote failed", error);
    }
  };

  return <button onClick={handleVote}>Vote</button>;
}
```

### Drag-and-Drop Integration

**Lazy-Loaded with Real-Time Sync:**

```typescript
// components/board/PostProvider.tsx
"use client";

import { useChannel } from "ably/react";
import dynamic from "next/dynamic";

// ✅ Lazy load drag-and-drop (reduces initial bundle)
const DragDropArea = dynamic(() => import("./DragDropArea"), { ssr: false });

export function PostProvider({ boardId }: { boardId: string }) {
  useChannel(`board:${boardId}`, (message) => {
    if (message.name === "post:move") {
      handlePostMove(message.data);
    }
  });

  const handleDrop = async (postId: string, newType: PostType) => {
    // Update locally
    movePostSignal(postId, newType);

    // Persist to database
    await updatePostType(postId, newType);

    // Broadcast to other users
    channel.publish("post:move", {
      type: "post:move",
      postId,
      newType,
      timestamp: Date.now(),
    });
  };

  return <DragDropArea onDrop={handleDrop} />;
}
```

## Anti-Patterns

### ❌ Not Validating Messages

**Bad:**

```typescript
useChannel(`board:${boardId}`, (message) => {
  // ❌ Trusts message data completely
  updatePost(message.data.postId, message.data.content);
});
```

**Good:**

```typescript
useChannel(`board:${boardId}`, (message) => {
  // ✅ Validates before processing
  const validated = PostUpdateSchema.safeParse(message.data);
  if (!validated.success) return;
  updatePost(validated.data.postId, validated.data.content);
});
```

### ❌ Not Checking Message Staleness

**Bad:**

```typescript
useChannel(channelName, (message) => {
  // ❌ Processes all messages, even old ones after reconnect
  processMessage(message.data);
});
```

**Good:**

```typescript
useChannel(channelName, (message) => {
  // ✅ Filters stale messages
  if (isMessageStale(message.data.timestamp)) return;
  processMessage(message.data);
});
```

### ❌ Not Handling Connection Errors

**Bad:**

```typescript
// ❌ No error handling
const { channel } = useChannel(channelName);
```

**Good:**

```typescript
// ✅ Monitor connection state
useConnectionStateListener((stateChange) => {
  if (stateChange.current === "failed") {
    showErrorNotification("Real-time connection lost");
  }
});
```

### ❌ Publishing Without Timestamp

**Bad:**

```typescript
channel.publish("update", {
  postId,
  content,
  // ❌ No timestamp for staleness check
});
```

**Good:**

```typescript
channel.publish("update", {
  postId,
  content,
  timestamp: Date.now(), // ✅ Include timestamp
});
```

### ❌ Not Handling Race Conditions

**Bad:**

```typescript
// ❌ Multiple updates could conflict
const handleVote = async () => {
  const newCount = currentCount + 1;
  await updateVoteCount(postId, newCount);
};
```

**Good:**

```typescript
// ✅ Use atomic increment
const handleVote = async () => {
  await db
    .update(postTable)
    .set({ voteCount: sql`vote_count + 1` })
    .where(eq(postTable.id, postId));
};
```

## Integration with Other Skills

- **[rbac-security](../rbac-security/SKILL.md):** Validate messages for security
- **[signal-state-management](../signal-state-management/SKILL.md):** Real-time updates to signals
- **[nextjs-app-router](../nextjs-app-router/SKILL.md):** Client components for real-time features
- **[testing-patterns](../testing-patterns/SKILL.md):** Test message processors with fake timers

## Project-Specific Context

### Key Files

- `lib/realtime/messageProcessors.ts` - Message validation and processing
- `components/board/PostProvider.tsx` - Real-time channel setup
- `components/board/PostChannelComponent.tsx` - Channel subscription
- `lib/realtime/__tests__/` - Message processor tests

### Message Types

**Current Message Types:**

```typescript
type MessageType =
  | "post:create"
  | "post:update"
  | "post:delete"
  | "post:move"
  | "post:vote"
  | "member:join"
  | "member:leave";
```

### Channel Structure

**One Channel Per Board:**

- Channel name: `board:{boardId}`
- All board events published to this channel
- Subscribers filter by message type

### Performance Optimizations

1. **Lazy Loading:** Drag-and-drop loaded on demand
2. **Staleness Filter:** Discards messages >30s old
3. **Optimistic Updates:** Immediate UI feedback
4. **Batching:** Vote counts updated atomically
5. **Connection Pooling:** Reuse Ably client instance

### Error Recovery

**Automatic Reconnection:**

- Ably SDK handles reconnection automatically
- Messages buffered during disconnection
- Staleness filter prevents processing old messages after reconnect

**Manual Recovery:**

```typescript
// Refresh data after long disconnection
if (
  stateChange.previous === "suspended" &&
  stateChange.current === "connected"
) {
  await refreshBoardData();
}
```

### Testing

**Mock Ably in Tests:**

```typescript
jest.mock("ably/react", () => ({
  useChannel: jest.fn(() => ({
    channel: {
      publish: jest.fn(),
      subscribe: jest.fn(),
    },
  })),
}));
```

---

**Last Updated:** 2026-01-10

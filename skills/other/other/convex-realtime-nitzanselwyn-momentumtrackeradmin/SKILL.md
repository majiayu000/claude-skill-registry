---
name: convex-realtime
displayName: Convex Realtime
description: Patterns for building reactive apps including subscription management, optimistic updates, cache behavior, and paginated queries with cursor-based loading
version: 1.0.0
author: Convex
tags: [convex, realtime, subscriptions, optimistic-updates, pagination]
---

# Convex Realtime

Build reactive applications with Convex's real-time subscriptions, optimistic updates, intelligent caching, and cursor-based pagination.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/client/react
- Optimistic Updates: https://docs.convex.dev/client/react/optimistic-updates
- Pagination: https://docs.convex.dev/database/pagination
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### How Convex Realtime Works

1. **Automatic Subscriptions** - useQuery creates a subscription that updates automatically
2. **Smart Caching** - Query results are cached and shared across components
3. **Consistency** - All subscriptions see a consistent view of the database
4. **Efficient Updates** - Only re-renders when relevant data changes

### Basic Subscriptions

```typescript
// React component with real-time data
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskList({ userId }: { userId: Id<"users"> }) {
  // Automatically subscribes and updates in real-time
  const tasks = useQuery(api.tasks.list, { userId });

  if (tasks === undefined) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      {tasks.map((task) => (
        <li key={task._id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

### Conditional Queries

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function UserProfile({ userId }: { userId: Id<"users"> | null }) {
  // Skip query when userId is null
  const user = useQuery(
    api.users.get,
    userId ? { userId } : "skip"
  );

  if (userId === null) {
    return <div>Select a user</div>;
  }

  if (user === undefined) {
    return <div>Loading...</div>;
  }

  return <div>{user.name}</div>;
}
```

### Mutations with Real-time Updates

```typescript
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskManager({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.list, { userId });
  const createTask = useMutation(api.tasks.create);
  const toggleTask = useMutation(api.tasks.toggle);

  const handleCreate = async (title: string) => {
    // Mutation triggers automatic re-render when data changes
    await createTask({ title, userId });
  };

  const handleToggle = async (taskId: Id<"tasks">) => {
    await toggleTask({ taskId });
  };

  return (
    <div>
      <button onClick={() => handleCreate("New Task")}>Add Task</button>
      <ul>
        {tasks?.map((task) => (
          <li key={task._id} onClick={() => handleToggle(task._id)}>
            {task.completed ? "✓" : "○"} {task.title}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Optimistic Updates

Show changes immediately before server confirmation:

```typescript
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import { Id } from "../convex/_generated/dataModel";

function TaskItem({ task }: { task: Task }) {
  const toggleTask = useMutation(api.tasks.toggle).withOptimisticUpdate(
    (localStore, args) => {
      const { taskId } = args;
      const currentValue = localStore.getQuery(api.tasks.get, { taskId });
      
      if (currentValue !== undefined) {
        localStore.setQuery(api.tasks.get, { taskId }, {
          ...currentValue,
          completed: !currentValue.completed,
        });
      }
    }
  );

  return (
    <div onClick={() => toggleTask({ taskId: task._id })}>
      {task.completed ? "✓" : "○"} {task.title}
    </div>
  );
}
```

### Optimistic Updates for Lists

```typescript
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function useCreateTask(userId: Id<"users">) {
  return useMutation(api.tasks.create).withOptimisticUpdate(
    (localStore, args) => {
      const { title, userId } = args;
      const currentTasks = localStore.getQuery(api.tasks.list, { userId });
      
      if (currentTasks !== undefined) {
        // Add optimistic task to the list
        const optimisticTask = {
          _id: crypto.randomUUID() as Id<"tasks">,
          _creationTime: Date.now(),
          title,
          userId,
          completed: false,
        };
        
        localStore.setQuery(api.tasks.list, { userId }, [
          optimisticTask,
          ...currentTasks,
        ]);
      }
    }
  );
}
```

### Cursor-Based Pagination

```typescript
// convex/messages.ts
import { query } from "./_generated/server";
import { v } from "convex/values";
import { paginationOptsValidator } from "convex/server";

export const listPaginated = query({
  args: {
    channelId: v.id("channels"),
    paginationOpts: paginationOptsValidator,
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

```typescript
// React component with pagination
import { usePaginatedQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function MessageList({ channelId }: { channelId: Id<"channels"> }) {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.listPaginated,
    { channelId },
    { initialNumItems: 20 }
  );

  return (
    <div>
      {results.map((message) => (
        <div key={message._id}>{message.content}</div>
      ))}
      
      {status === "CanLoadMore" && (
        <button onClick={() => loadMore(20)}>Load More</button>
      )}
      
      {status === "LoadingMore" && <div>Loading...</div>}
      
      {status === "Exhausted" && <div>No more messages</div>}
    </div>
  );
}
```

### Infinite Scroll Pattern

```typescript
import { usePaginatedQuery } from "convex/react";
import { useEffect, useRef } from "react";
import { api } from "../convex/_generated/api";

function InfiniteMessageList({ channelId }: { channelId: Id<"channels"> }) {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.listPaginated,
    { channelId },
    { initialNumItems: 20 }
  );
  
  const observerRef = useRef<IntersectionObserver>();
  const loadMoreRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (observerRef.current) {
      observerRef.current.disconnect();
    }

    observerRef.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && status === "CanLoadMore") {
        loadMore(20);
      }
    });

    if (loadMoreRef.current) {
      observerRef.current.observe(loadMoreRef.current);
    }

    return () => observerRef.current?.disconnect();
  }, [status, loadMore]);

  return (
    <div>
      {results.map((message) => (
        <div key={message._id}>{message.content}</div>
      ))}
      <div ref={loadMoreRef} style={{ height: 1 }} />
      {status === "LoadingMore" && <div>Loading...</div>}
    </div>
  );
}
```

### Multiple Subscriptions

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function Dashboard({ userId }: { userId: Id<"users"> }) {
  // Multiple subscriptions update independently
  const user = useQuery(api.users.get, { userId });
  const tasks = useQuery(api.tasks.list, { userId });
  const notifications = useQuery(api.notifications.unread, { userId });

  const isLoading = user === undefined || 
                    tasks === undefined || 
                    notifications === undefined;

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <p>You have {tasks.length} tasks</p>
      <p>{notifications.length} unread notifications</p>
    </div>
  );
}
```

## Examples

### Real-time Chat Application

```typescript
// convex/messages.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const list = query({
  args: { channelId: v.id("channels") },
  returns: v.array(v.object({
    _id: v.id("messages"),
    _creationTime: v.number(),
    content: v.string(),
    authorId: v.id("users"),
    authorName: v.string(),
  })),
  handler: async (ctx, args) => {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .take(100);

    // Enrich with author names
    return Promise.all(
      messages.map(async (msg) => {
        const author = await ctx.db.get(msg.authorId);
        return {
          ...msg,
          authorName: author?.name ?? "Unknown",
        };
      })
    );
  },
});

export const send = mutation({
  args: {
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
  },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("messages", {
      channelId: args.channelId,
      authorId: args.authorId,
      content: args.content,
    });
  },
});
```

```typescript
// ChatRoom.tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState, useRef, useEffect } from "react";

function ChatRoom({ channelId, userId }: Props) {
  const messages = useQuery(api.messages.list, { channelId });
  const sendMessage = useMutation(api.messages.send);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    await sendMessage({
      channelId,
      authorId: userId,
      content: input.trim(),
    });
    setInput("");
  };

  return (
    <div className="chat-room">
      <div className="messages">
        {messages?.map((msg) => (
          <div key={msg._id} className="message">
            <strong>{msg.authorName}:</strong> {msg.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSend}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Use "skip" for conditional queries instead of conditionally calling hooks
- Implement optimistic updates for better perceived performance
- Use usePaginatedQuery for large datasets
- Handle undefined state (loading) explicitly
- Avoid unnecessary re-renders by memoizing derived data

## Common Pitfalls

1. **Conditional hook calls** - Use "skip" instead of if statements
2. **Not handling loading state** - Always check for undefined
3. **Missing optimistic update rollback** - Optimistic updates auto-rollback on error
4. **Over-fetching with pagination** - Use appropriate page sizes
5. **Ignoring subscription cleanup** - React handles this automatically

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- React Client: https://docs.convex.dev/client/react
- Optimistic Updates: https://docs.convex.dev/client/react/optimistic-updates
- Pagination: https://docs.convex.dev/database/pagination

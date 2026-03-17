---
name: tanstack-db
description: Expert guidance for TanStack DB reactive client-side database with collections, live queries, optimistic mutations, and sync engines (ElectricSQL, RxDB, PowerSync). Use when user says "tanstack db", "/tanstack-db", "local-first", "live query", "collection", "optimistic mutation", "electric", "sync engine", or asks about reactive data, offline-first, or real-time sync.
---

# TanStack DB Skill

Expert guidance for TanStack DB - the reactive client store for building local-first apps with sub-millisecond queries, optimistic mutations, and real-time sync.

**Note:** TanStack DB is currently in BETA.

## Quick Reference

### Core Concepts

| Concept | Purpose |
|---------|---------|
| **Collection** | Typed set of objects (like a DB table) |
| **Live Query** | Reactive query that updates incrementally |
| **Optimistic Mutation** | Instant local write, synced in background |
| **Sync Engine** | Real-time data sync (Electric, RxDB, PowerSync) |

### Project Structure

```
src/
├── collections/
│   ├── todos.ts         # Todo collection definition
│   ├── users.ts         # User collection
│   └── index.ts         # Export all collections
├── queries/
│   └── hooks.ts         # Custom live query hooks
└── lib/
    └── db.ts            # DB setup & QueryClient
```

## Installation

```bash
# Core + React
npm install @tanstack/react-db @tanstack/db

# With TanStack Query (REST APIs)
npm install @tanstack/query-db-collection @tanstack/react-query

# With ElectricSQL (Postgres sync)
npm install @tanstack/electric-db-collection

# With RxDB (offline-first)
npm install @tanstack/rxdb-db-collection rxdb
```

## Collections

### Query Collection (REST API)

```typescript
// src/collections/todos.ts
import { createCollection } from "@tanstack/react-db"
import { queryCollectionOptions } from "@tanstack/query-db-collection"
import { queryClient } from "@/lib/db"

export interface Todo {
  id: string
  text: string
  completed: boolean
  createdAt: string
}

export const todosCollection = createCollection(
  queryCollectionOptions({
    queryKey: ["todos"],
    queryFn: async () => {
      const res = await fetch("/api/todos")
      return res.json() as Promise<Todo[]>
    },
    queryClient,
    getKey: (item) => item.id,

    // Persistence handlers
    onInsert: async ({ transaction }) => {
      const items = transaction.mutations.map((m) => m.modified)
      await fetch("/api/todos", {
        method: "POST",
        body: JSON.stringify(items),
      })
    },

    onUpdate: async ({ transaction }) => {
      await Promise.all(
        transaction.mutations.map((m) =>
          fetch(`/api/todos/${m.key}`, {
            method: "PATCH",
            body: JSON.stringify(m.changes),
          })
        )
      )
    },

    onDelete: async ({ transaction }) => {
      await Promise.all(
        transaction.mutations.map((m) =>
          fetch(`/api/todos/${m.key}`, { method: "DELETE" })
        )
      )
    },
  })
)
```

### Electric Collection (Postgres Sync)

```typescript
// src/collections/todos.ts
import { createCollection } from "@tanstack/react-db"
import { electricCollectionOptions } from "@tanstack/electric-db-collection"

export const todosCollection = createCollection(
  electricCollectionOptions({
    id: "todos",
    shapeOptions: {
      url: "/api/electric/todos", // Proxy to Electric
    },
    getKey: (item) => item.id,

    // Use transaction ID for sync confirmation
    onInsert: async ({ transaction }) => {
      const item = transaction.mutations[0].modified
      const res = await fetch("/api/todos", {
        method: "POST",
        body: JSON.stringify(item),
      })
      const { txid } = await res.json()
      return { txid } // Electric waits for this txid
    },

    onUpdate: async ({ transaction }) => {
      const { key, changes } = transaction.mutations[0]
      const res = await fetch(`/api/todos/${key}`, {
        method: "PATCH",
        body: JSON.stringify(changes),
      })
      const { txid } = await res.json()
      return { txid }
    },

    onDelete: async ({ transaction }) => {
      const { key } = transaction.mutations[0]
      const res = await fetch(`/api/todos/${key}`, { method: "DELETE" })
      const { txid } = await res.json()
      return { txid }
    },
  })
)
```

### Sync Modes

```typescript
// Eager (default): Load all upfront - best for <10k rows
electricCollectionOptions({
  sync: { mode: "eager" },
  // ...
})

// On-demand: Load only what queries request - best for >50k rows
electricCollectionOptions({
  sync: { mode: "on-demand" },
  // ...
})

// Progressive: Instant query results + background full sync
electricCollectionOptions({
  sync: { mode: "progressive" },
  // ...
})
```

## Live Queries

### Basic Query

```tsx
import { useLiveQuery } from "@tanstack/react-db"
import { todosCollection } from "@/collections/todos"

function TodoList() {
  const { data: todos, isLoading } = useLiveQuery((q) =>
    q.from({ todo: todosCollection })
  )

  if (isLoading) return <div>Loading...</div>

  return (
    <ul>
      {todos?.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  )
}
```

### Filtering with Where

```typescript
import { eq, gt, and, or, like, inArray } from "@tanstack/react-db"

// Simple equality
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) => eq(todo.completed, false))
)

// Multiple conditions
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) =>
     and(
       eq(todo.completed, false),
       gt(todo.priority, 5)
     )
   )
)

// OR conditions
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) =>
     or(
       eq(todo.status, "urgent"),
       eq(todo.status, "high")
     )
   )
)

// String matching
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) => like(todo.text, "%meeting%"))
)

// In array
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) => inArray(todo.id, ["1", "2", "3"]))
)
```

### Comparison Operators

| Operator | Description |
|----------|-------------|
| `eq(a, b)` | Equal |
| `gt(a, b)` | Greater than |
| `gte(a, b)` | Greater than or equal |
| `lt(a, b)` | Less than |
| `lte(a, b)` | Less than or equal |
| `like(a, pattern)` | Case-sensitive match |
| `ilike(a, pattern)` | Case-insensitive match |
| `inArray(a, arr)` | Value in array |
| `isNull(a)` | Is null |
| `isUndefined(a)` | Is undefined |

### Sorting and Pagination

```typescript
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .orderBy(({ todo }) => todo.createdAt, "desc")
   .limit(20)
   .offset(0)
)
```

### Select Projection

```typescript
// Select specific fields
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .select(({ todo }) => ({
     id: todo.id,
     text: todo.text,
     done: todo.completed,
   }))
)

// Computed fields
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .select(({ todo }) => ({
     id: todo.id,
     displayText: upper(todo.text),
     isOverdue: lt(todo.dueDate, new Date().toISOString()),
   }))
)
```

### Joins

```typescript
import { usersCollection } from "@/collections/users"

// Inner join
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .join(
     { user: usersCollection },
     ({ todo, user }) => eq(todo.userId, user.id),
     "inner"
   )
   .select(({ todo, user }) => ({
     id: todo.id,
     text: todo.text,
     assignee: user.name,
   }))
)

// Left join (default)
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .leftJoin(
     { user: usersCollection },
     ({ todo, user }) => eq(todo.userId, user.id)
   )
)
```

### Aggregations

```typescript
// Group by with aggregates
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .groupBy(({ todo }) => todo.status)
   .select(({ todo }) => ({
     status: todo.status,
     count: count(todo.id),
     avgPriority: avg(todo.priority),
   }))
)

// With having clause
useLiveQuery((q) =>
  q.from({ order: ordersCollection })
   .groupBy(({ order }) => order.customerId)
   .select(({ order }) => ({
     customerId: order.customerId,
     totalSpent: sum(order.amount),
   }))
   .having(({ $selected }) => gt($selected.totalSpent, 1000))
)
```

### Find Single Item

```typescript
// Returns T | undefined
useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) => eq(todo.id, todoId))
   .findOne()
)
```

### Reactive Dependencies

```typescript
// Re-run query when deps change
const [filter, setFilter] = useState("all")

useLiveQuery(
  (q) =>
    q.from({ todo: todosCollection })
     .where(({ todo }) =>
       filter === "all" ? true : eq(todo.status, filter)
     ),
  [filter] // Dependency array
)
```

## Mutations

### Basic Operations

```typescript
const { collection } = useLiveQuery((q) =>
  q.from({ todo: todosCollection })
)

// Insert
collection.insert({
  id: crypto.randomUUID(),
  text: "New todo",
  completed: false,
  createdAt: new Date().toISOString(),
})

// Insert multiple
collection.insert([item1, item2, item3])

// Update (immutable draft pattern)
collection.update(todoId, (draft) => {
  draft.completed = true
  draft.completedAt = new Date().toISOString()
})

// Update multiple
collection.update([id1, id2], (drafts) => {
  drafts.forEach((d) => (d.completed = true))
})

// Delete
collection.delete(todoId)

// Delete multiple
collection.delete([id1, id2, id3])
```

### Non-Optimistic Mutations

```typescript
// Skip optimistic update, wait for server
collection.insert(item, { optimistic: false })
collection.update(id, updater, { optimistic: false })
collection.delete(id, { optimistic: false })
```

### Custom Optimistic Actions

```typescript
import { createOptimisticAction } from "@tanstack/react-db"

// Multi-collection or complex mutations
const likePost = createOptimisticAction<string>({
  onMutate: (postId) => {
    postsCollection.update(postId, (draft) => {
      draft.likeCount += 1
      draft.likedByMe = true
    })
  },
  mutationFn: async (postId) => {
    await fetch(`/api/posts/${postId}/like`, { method: "POST" })
    // Optionally refetch
    await postsCollection.utils.refetch()
  },
})

// Usage
likePost.mutate(postId)
```

### Manual Transactions

```typescript
import { createTransaction } from "@tanstack/react-db"

const tx = createTransaction({
  autoCommit: false,
  mutationFn: async ({ transaction }) => {
    // Batch all mutations in single request
    await fetch("/api/batch", {
      method: "POST",
      body: JSON.stringify(transaction.mutations),
    })
  },
})

// Queue mutations
tx.mutate(() => {
  todosCollection.insert(newTodo)
  todosCollection.update(existingId, (d) => (d.status = "active"))
  todosCollection.delete(oldId)
})

// Commit or rollback
await tx.commit()
// or
tx.rollback()
```

### Paced Mutations (Debounce/Throttle)

```typescript
import { usePacedMutations, debounceStrategy } from "@tanstack/react-db"

// Debounce rapid updates (e.g., text input)
const { mutate } = usePacedMutations({
  onMutate: (value: string) => {
    todosCollection.update(todoId, (d) => (d.text = value))
  },
  mutationFn: async ({ transaction }) => {
    const changes = transaction.mutations[0].changes
    await fetch(`/api/todos/${todoId}`, {
      method: "PATCH",
      body: JSON.stringify(changes),
    })
  },
  strategy: debounceStrategy({ wait: 500 }),
})

// Usage in input
<input onChange={(e) => mutate(e.target.value)} />
```

## Provider Setup

```tsx
// src/main.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { DBProvider } from "@tanstack/react-db"

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DBProvider>
        <Router />
      </DBProvider>
    </QueryClientProvider>
  )
}
```

## Electric Backend Setup

### Server-Side Transaction ID

```typescript
// api/todos/route.ts (example with Drizzle)
import { db } from "@/db"
import { todos } from "@/db/schema"
import { sql } from "drizzle-orm"

export async function POST(req: Request) {
  const data = await req.json()

  const result = await db.transaction(async (tx) => {
    // Insert the todo
    const [todo] = await tx.insert(todos).values(data).returning()

    // Get transaction ID in SAME transaction
    const [{ txid }] = await tx.execute(
      sql`SELECT pg_current_xact_id()::text as txid`
    )

    return { todo, txid: parseInt(txid, 10) }
  })

  return Response.json(result)
}
```

### Electric Proxy Route

```typescript
// api/electric/[...path]/route.ts
export async function GET(req: Request) {
  const url = new URL(req.url)
  const electricUrl = `${process.env.ELECTRIC_URL}${url.pathname}${url.search}`

  return fetch(electricUrl, {
    headers: { Authorization: `Bearer ${process.env.ELECTRIC_TOKEN}` },
  })
}
```

## Utility Methods

```typescript
// Refetch collection data
await collection.utils.refetch()

// Direct writes (bypass optimistic state)
collection.utils.writeInsert(item)
collection.utils.writeUpdate(item)
collection.utils.writeDelete(id)
collection.utils.writeUpsert(item)

// Batch direct writes
collection.utils.writeBatch(() => {
  collection.utils.writeInsert(item1)
  collection.utils.writeDelete(id2)
})

// Wait for Electric sync (with txid)
await collection.utils.awaitTxId(txid, 30000)

// Wait for custom match
await collection.utils.awaitMatch(
  (msg) => msg.value.id === expectedId,
  5000
)
```

## Gotchas and Tips

1. **Queries run client-side**: TanStack DB is NOT an ORM - queries run locally against collections, not against a database
2. **Sub-millisecond updates**: Uses differential dataflow - only recalculates affected parts of queries
3. **Transaction IDs matter**: With Electric, always get `pg_current_xact_id()` in the SAME transaction as mutations
4. **Sync modes**: Use "eager" for small datasets, "on-demand" for large, "progressive" for collaborative apps
5. **Optimistic by default**: All mutations apply instantly; use `{ optimistic: false }` for server-validated operations
6. **Fine-grained reactivity**: Only components using changed data re-render
7. **Mutation merging**: Rapid updates merge automatically (insert+update→insert, update+update→merged)
8. **Collection = complete state**: Empty array from queryFn clears the collection

## Common Patterns

### Loading States

```tsx
function TodoList() {
  const { data, isLoading, isPending } = useLiveQuery((q) =>
    q.from({ todo: todosCollection })
  )

  if (isLoading) return <Skeleton />
  if (!data?.length) return <EmptyState />

  return <List items={data} />
}
```

### Mutation with Feedback

```tsx
function TodoItem({ todo }: { todo: Todo }) {
  const { collection } = useLiveQuery((q) =>
    q.from({ todo: todosCollection })
  )

  const toggle = async () => {
    const tx = collection.update(todo.id, (d) => {
      d.completed = !d.completed
    })

    try {
      await tx.isPersisted.promise
      toast.success("Saved!")
    } catch (err) {
      toast.error("Failed to save")
      // Optimistic update already rolled back
    }
  }

  return <Checkbox checked={todo.completed} onChange={toggle} />
}
```

### Derived/Computed Collections

```tsx
// Create a "view" with live query
const completedTodos = useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .where(({ todo }) => eq(todo.completed, true))
   .orderBy(({ todo }) => todo.completedAt, "desc")
)
```

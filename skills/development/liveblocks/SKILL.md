---
name: liveblocks
description: Builds real-time collaborative features with Liveblocks including presence, cursors, storage, comments, and notifications. Use when adding multiplayer experiences, collaborative editing, or live cursors to React applications.
---

# Liveblocks

Complete toolkit for adding real-time collaboration to your app. Includes presence, storage, comments, notifications, and Yjs/Redux integration.

## Quick Start

```bash
npm install @liveblocks/client @liveblocks/react
```

### Configuration

```typescript
// liveblocks.config.ts
import { createClient } from "@liveblocks/client";
import { createRoomContext } from "@liveblocks/react";

const client = createClient({
  publicApiKey: "pk_xxx",  // or authEndpoint for production
});

// Define your types
type Presence = {
  cursor: { x: number; y: number } | null;
  name: string;
};

type Storage = {
  todos: LiveList<{ id: string; text: string; done: boolean }>;
};

type UserMeta = {
  id: string;
  info: { name: string; avatar: string };
};

export const {
  RoomProvider,
  useMyPresence,
  useUpdateMyPresence,
  useOthers,
  useSelf,
  useStorage,
  useMutation,
  useRoom,
} = createRoomContext<Presence, Storage, UserMeta>(client);
```

### Basic Usage

```tsx
import { RoomProvider } from "./liveblocks.config";

function App() {
  return (
    <RoomProvider
      id="my-room"
      initialPresence={{ cursor: null, name: "Anonymous" }}
    >
      <CollaborativeApp />
    </RoomProvider>
  );
}
```

## Presence

Track ephemeral user state (cursors, selections, typing indicators).

### useMyPresence / useUpdateMyPresence

```tsx
function Cursors() {
  const updateMyPresence = useUpdateMyPresence();

  return (
    <div
      onPointerMove={(e) => {
        updateMyPresence({
          cursor: { x: e.clientX, y: e.clientY }
        });
      }}
      onPointerLeave={() => {
        updateMyPresence({ cursor: null });
      }}
    >
      <OthersCursors />
    </div>
  );
}
```

### useOthers

```tsx
function OthersCursors() {
  const others = useOthers();

  return (
    <>
      {others.map(({ connectionId, presence, info }) => {
        if (!presence.cursor) return null;

        return (
          <Cursor
            key={connectionId}
            x={presence.cursor.x}
            y={presence.cursor.y}
            name={info?.name}
          />
        );
      })}
    </>
  );
}
```

### useSelf

```tsx
function UserInfo() {
  const self = useSelf();

  if (!self) return null;

  return (
    <div>
      <span>You: {self.info?.name}</span>
      <span>Connection: {self.connectionId}</span>
    </div>
  );
}
```

### Selector Pattern (Performance)

```tsx
// Only re-render when count changes
const count = useOthers((others) => others.length);

// Only get cursor positions
const cursors = useOthers((others) =>
  others.map((other) => ({
    id: other.connectionId,
    cursor: other.presence.cursor
  }))
);
```

## Storage

Persist and sync data across clients using conflict-free data types.

### Initialize Storage

```tsx
<RoomProvider
  id="my-room"
  initialPresence={{ cursor: null }}
  initialStorage={{
    todos: new LiveList([]),
    canvas: new LiveMap(),
    settings: new LiveObject({ theme: "dark" })
  }}
>
```

### useStorage

```tsx
function TodoList() {
  const todos = useStorage((root) => root.todos);

  if (todos === null) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      {todos.map((todo, index) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

### useMutation

Modify storage safely with mutations.

```tsx
function TodoList() {
  const todos = useStorage((root) => root.todos);

  const addTodo = useMutation(({ storage }, text: string) => {
    const todos = storage.get("todos");
    todos.push({
      id: crypto.randomUUID(),
      text,
      done: false
    });
  }, []);

  const toggleTodo = useMutation(({ storage }, index: number) => {
    const todos = storage.get("todos");
    const todo = todos.get(index);
    if (todo) {
      todo.done = !todo.done;
    }
  }, []);

  const deleteTodo = useMutation(({ storage }, index: number) => {
    storage.get("todos").delete(index);
  }, []);

  return (
    <div>
      <button onClick={() => addTodo("New task")}>Add</button>
      <ul>
        {todos?.map((todo, i) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => toggleTodo(i)}
            />
            {todo.text}
            <button onClick={() => deleteTodo(i)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Live Data Types

### LiveList

```tsx
const addItem = useMutation(({ storage }) => {
  const list = storage.get("items");
  list.push({ id: "1", value: "new" });      // Add to end
  list.insert({ id: "2", value: "at 0" }, 0); // Insert at index
  list.move(0, 2);                            // Move item
  list.delete(1);                             // Delete at index
  list.clear();                               // Remove all
}, []);
```

### LiveMap

```tsx
const updateMap = useMutation(({ storage }) => {
  const map = storage.get("shapes");
  map.set("shape-1", { x: 100, y: 200 });    // Set value
  map.get("shape-1");                         // Get value
  map.delete("shape-1");                      // Delete key
  map.has("shape-1");                         // Check existence
}, []);
```

### LiveObject

```tsx
const updateObject = useMutation(({ storage }) => {
  const settings = storage.get("settings");
  settings.set("theme", "light");            // Set property
  settings.get("theme");                      // Get property
  settings.update({ theme: "dark", fontSize: 16 }); // Update multiple
}, []);
```

## Suspense Support

```tsx
import { ClientSideSuspense } from "@liveblocks/react";
import { useStorage } from "@liveblocks/react/suspense";

function App() {
  return (
    <RoomProvider id="room">
      <ClientSideSuspense fallback={<Loading />}>
        <Editor />
      </ClientSideSuspense>
    </RoomProvider>
  );
}

function Editor() {
  // No null check needed with suspense hooks
  const todos = useStorage((root) => root.todos);

  return <TodoList todos={todos} />;
}
```

## Authentication

### Auth Endpoint

```typescript
// app/api/liveblocks-auth/route.ts
import { Liveblocks } from "@liveblocks/node";

const liveblocks = new Liveblocks({
  secret: process.env.LIVEBLOCKS_SECRET_KEY!,
});

export async function POST(request: Request) {
  const session = await getSession(); // Your auth

  const { room } = await request.json();

  const session = liveblocks.prepareSession(session.user.id, {
    userInfo: {
      name: session.user.name,
      avatar: session.user.avatar,
    },
  });

  // Grant access to room
  session.allow(room, session.FULL_ACCESS);

  const { body, status } = await session.authorize();
  return new Response(body, { status });
}
```

### Client Config

```typescript
const client = createClient({
  authEndpoint: "/api/liveblocks-auth",
});
```

## Broadcast

Send transient messages without storing them.

```tsx
function Chat() {
  const room = useRoom();

  const sendMessage = (text: string) => {
    room.broadcastEvent({
      type: "MESSAGE",
      text,
    });
  };

  useEffect(() => {
    return room.subscribe("event", ({ event }) => {
      if (event.type === "MESSAGE") {
        console.log("Received:", event.text);
      }
    });
  }, [room]);

  return <button onClick={() => sendMessage("Hello!")}>Send</button>;
}
```

## History / Undo-Redo

```tsx
import { useHistory, useCanUndo, useCanRedo } from "@liveblocks/react";

function UndoRedo() {
  const history = useHistory();
  const canUndo = useCanUndo();
  const canRedo = useCanRedo();

  return (
    <div>
      <button onClick={history.undo} disabled={!canUndo}>
        Undo
      </button>
      <button onClick={history.redo} disabled={!canRedo}>
        Redo
      </button>
    </div>
  );
}

// Batch changes for single undo step
const batchUpdate = useMutation(({ storage }) => {
  storage.get("todos").push({ id: "1", text: "A" });
  storage.get("todos").push({ id: "2", text: "B" });
  // Both will undo together
}, []);

// Pause/resume history
history.pause();
// ... make changes that shouldn't be in history
history.resume();
```

## Yjs Integration

Use Liveblocks as a Yjs provider for text editors.

```bash
npm install @liveblocks/yjs yjs
```

```tsx
import { useRoom } from "./liveblocks.config";
import { LiveblocksYjsProvider } from "@liveblocks/yjs";
import * as Y from "yjs";

function Editor() {
  const room = useRoom();

  useEffect(() => {
    const yDoc = new Y.Doc();
    const yProvider = new LiveblocksYjsProvider(room, yDoc);

    // Use with TipTap, Quill, Lexical, etc.
    const editor = new YourEditor({
      extensions: [
        Collaboration.configure({ document: yDoc }),
        CollaborationCursor.configure({ provider: yProvider }),
      ],
    });

    return () => {
      yProvider.destroy();
      yDoc.destroy();
    };
  }, [room]);
}
```

## Comments

Add contextual comments to your app.

```bash
npm install @liveblocks/react-comments
```

```tsx
import { Thread, Composer } from "@liveblocks/react-comments";
import { useThreads } from "@liveblocks/react/suspense";

function Comments() {
  const { threads } = useThreads();

  return (
    <div>
      {threads.map((thread) => (
        <Thread key={thread.id} thread={thread} />
      ))}
      <Composer />
    </div>
  );
}
```

## Common Patterns

### Multiplayer Cursors

```tsx
function Cursors() {
  const updateMyPresence = useUpdateMyPresence();
  const others = useOthers((others) =>
    others.filter((o) => o.presence.cursor !== null)
  );

  return (
    <div
      className="canvas"
      onPointerMove={(e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        updateMyPresence({
          cursor: {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
          },
        });
      }}
      onPointerLeave={() => updateMyPresence({ cursor: null })}
    >
      {others.map(({ connectionId, presence, info }) => (
        <Cursor
          key={connectionId}
          x={presence.cursor!.x}
          y={presence.cursor!.y}
          name={info?.name}
        />
      ))}
    </div>
  );
}

function Cursor({ x, y, name }: { x: number; y: number; name?: string }) {
  return (
    <div
      className="cursor"
      style={{
        position: "absolute",
        left: x,
        top: y,
        pointerEvents: "none",
      }}
    >
      <svg>...</svg>
      {name && <span>{name}</span>}
    </div>
  );
}
```

### Who's Here

```tsx
function AvatarStack() {
  const others = useOthers();
  const self = useSelf();

  return (
    <div className="avatar-stack">
      {self && <Avatar user={self.info} />}
      {others.map(({ connectionId, info }) => (
        <Avatar key={connectionId} user={info} />
      ))}
    </div>
  );
}
```

### Live Selection

```tsx
type Presence = {
  selectedId: string | null;
};

function SelectableItems() {
  const updateMyPresence = useUpdateMyPresence();
  const othersSelections = useOthers((others) =>
    others.map((o) => o.presence.selectedId).filter(Boolean)
  );

  const items = useStorage((root) => root.items);

  return (
    <div>
      {items?.map((item) => (
        <div
          key={item.id}
          onClick={() => updateMyPresence({ selectedId: item.id })}
          className={othersSelections.includes(item.id) ? "selected-by-other" : ""}
        >
          {item.name}
        </div>
      ))}
    </div>
  );
}
```

## Best Practices

1. **Use selectors** to avoid unnecessary re-renders
2. **Type your presence/storage** for autocomplete and safety
3. **Use Suspense hooks** for cleaner loading states
4. **Batch mutations** for undo/redo grouping
5. **Use authEndpoint** in production (not public API key)
6. **Debounce cursor updates** for performance

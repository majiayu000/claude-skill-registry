---
name: real-time-collaboration-engine
description: Build real-time collaborative editing with WebSockets, OT/CRDT conflict resolution, and presence awareness. Implements cursor tracking, optimistic updates, and offline sync. Use for collaborative editors, whiteboards, video editing. Activate on "real-time collaboration", "WebSocket sync", "multiplayer editing", "CRDT", "presence awareness". NOT for simple chat, request-response APIs, or single-user apps.
allowed-tools: Read,Write,Edit,Bash(npm:*,websocket:*)
---

# Real-Time Collaboration Engine

Expert in building Google Docs-style collaborative editing with WebSockets, conflict resolution, and presence awareness.

## When to Use

✅ **Use for**:
- Collaborative text/code editors
- Shared whiteboards and design tools
- Multi-user video editing timelines
- Real-time data dashboards
- Multiplayer game state sync

❌ **NOT for**:
- Simple chat applications (use basic WebSocket)
- Request-response APIs (use REST/GraphQL)
- Single-user applications
- Read-only data streaming (use Server-Sent Events)

## Quick Decision Tree

```
Need real-time collaboration?
├── Text editing? → Operational Transform (OT)
├── JSON data structures? → CRDTs
├── Cursor tracking only? → Simple WebSocket + presence
├── Offline-first? → CRDTs (better offline merge)
└── No conflicts possible? → Basic broadcast
```

---

## Technology Selection

### Conflict Resolution Strategies (2024)

| Strategy | Best For | Complexity | Offline Support |
|----------|----------|------------|-----------------|
| Operational Transform (OT) | Text, ordered sequences | High | Limited |
| CRDTs | JSON objects, sets | Medium | Excellent |
| Last-Write-Wins | Simple state | Low | Basic |
| Three-Way Merge | Git-style editing | High | Good |

**Timeline**:
- 2010: Google Wave uses OT
- 2014: Figma adopts CRDTs
- 2019: Yjs (CRDT library) released
- 2022: Automerge 2.0 (CRDT library) released
- 2024: PartyKit simplifies real-time infrastructure

---

## Common Anti-Patterns

### Anti-Pattern 1: Broadcasting Every Keystroke

**Novice thinking**: "Send every change immediately for real-time feel"

**Problem**: Network floods with tiny messages, poor performance.

**Wrong approach**:
```typescript
// ❌ Sends message on every keystroke
function Editor() {
  const handleChange = (text: string) => {
    socket.emit('text-change', { text });  // Every keystroke!
  };

  return <textarea onChange={(e) => handleChange(e.target.value)} />;
}
```

**Why wrong**: 100 WPM typing = 500 messages/minute = network congestion.

**Correct approach**:
```typescript
// ✅ Batches changes every 200ms
function Editor() {
  const [pendingChanges, setPendingChanges] = useState<Change[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (pendingChanges.length > 0) {
        socket.emit('text-batch', { changes: pendingChanges });
        setPendingChanges([]);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [pendingChanges]);

  const handleChange = (change: Change) => {
    setPendingChanges(prev => [...prev, change]);
  };

  return <textarea onChange={handleChange} />;
}
```

**Impact**: 500 messages/minute → 5 messages/second (90% reduction).

---

### Anti-Pattern 2: No Conflict Resolution Strategy

**Problem**: Concurrent edits cause data loss or corruption.

**Symptom**: Users see their changes disappear, documents become inconsistent.

**Wrong approach**:
```typescript
// ❌ Last write wins, overwrites concurrent changes
socket.on('text-change', ({ userId, text }) => {
  setDocument(text);  // Loses concurrent edits!
});
```

**Why wrong**: If User A and B edit simultaneously, one change is lost.

**Correct approach (OT)**:
```typescript
// ✅ Operational Transform for text
import { TextOperation } from 'ot.js';

socket.on('operation', ({ userId, operation, revision }) => {
  const transformed = transformOperation(
    operation,
    pendingOperations,
    revision
  );

  applyOperation(transformed);
  incrementRevision();
});

function transformOperation(
  incoming: Operation,
  pending: Operation[],
  baseRevision: number
): Operation {
  // Transform incoming against pending operations
  let transformed = incoming;
  for (const op of pending) {
    transformed = TextOperation.transform(transformed, op)[0];
  }
  return transformed;
}
```

**Correct approach (CRDT)**:
```typescript
// ✅ CRDT for JSON objects
import * as Y from 'yjs';

const ydoc = new Y.Doc();
const ytext = ydoc.getText('document');

// Automatically handles conflicts
ytext.insert(0, 'Hello');

// Sync with peers
const provider = new WebsocketProvider('ws://localhost:1234', 'room', ydoc);
```

**Impact**: Concurrent edits merge correctly, no data loss.

---

### Anti-Pattern 3: Not Handling Disconnections

**Problem**: User goes offline, loses work or sees stale state.

**Wrong approach**:
```typescript
// ❌ No offline handling
socket.on('disconnect', () => {
  console.log('Disconnected');  // That's it?!
});
```

**Why wrong**: Pending changes lost, no reconnection strategy, bad UX.

**Correct approach**:
```typescript
// ✅ Queue changes offline, sync on reconnect
const [isOnline, setIsOnline] = useState(true);
const [offlineQueue, setOfflineQueue] = useState<Change[]>([]);

socket.on('disconnect', () => {
  setIsOnline(false);
  showToast('Offline - changes will sync when reconnected');
});

socket.on('connect', () => {
  setIsOnline(true);

  // Send queued changes
  if (offlineQueue.length > 0) {
    socket.emit('sync-offline-changes', { changes: offlineQueue });
    setOfflineQueue([]);
  }
});

const handleChange = (change: Change) => {
  if (isOnline) {
    socket.emit('change', change);
  } else {
    setOfflineQueue(prev => [...prev, change]);
  }
};
```

**Timeline context**:
- 2015: Offline-first apps rare
- 2020: PWAs make offline UX standard
- 2024: Users expect seamless offline editing

---

### Anti-Pattern 4: Client-Only State Sync

**Problem**: No server authority, clients get out of sync.

**Wrong approach**:
```typescript
// ❌ Clients broadcast to each other directly
socket.on('peer-change', ({ userId, change }) => {
  applyChange(change);  // No validation, no server state
});
```

**Why wrong**: Malicious client can send invalid data, no recovery from desync.

**Correct approach**:
```typescript
// ✅ Server is source of truth
// Client
socket.emit('operation', { operation, clientRevision });

socket.on('ack', ({ serverRevision }) => {
  if (serverRevision !== expectedRevision) {
    // Desync detected, request full state
    socket.emit('request-full-state');
  }
});

// Server
io.on('connection', (socket) => {
  socket.on('operation', ({ operation, clientRevision }) => {
    // Validate operation
    if (!isValid(operation)) {
      socket.emit('error', { message: 'Invalid operation' });
      return;
    }

    // Apply to server state
    const serverRevision = applyOperation(operation);

    // Broadcast to all clients
    io.emit('operation', { operation, serverRevision });
  });
});
```

**Impact**: Data integrity guaranteed, can recover from client bugs.

---

### Anti-Pattern 5: No Presence Awareness

**Problem**: Users can't see who's editing what, causing edit conflicts.

**Symptom**: Two people editing same section unknowingly.

**Wrong approach**:
```typescript
// ❌ No awareness of other users
function Editor() {
  return <textarea />;  // Flying blind!
}
```

**Correct approach**:
```typescript
// ✅ Show active users and cursors
import { usePresence } from './usePresence';

function Editor() {
  const { users, updateCursor } = usePresence();

  const handleCursorMove = (position: number) => {
    socket.emit('cursor-move', { userId: myId, position });
  };

  return (
    <div>
      {/* Show who's online */}
      <UserList users={users} />

      {/* Show remote cursors */}
      <EditorWithCursors
        content={content}
        cursors={users.map(u => u.cursor)}
        onCursorMove={handleCursorMove}
      />
    </div>
  );
}
```

**Features**:
- Active user list with avatars
- Cursor positions color-coded by user
- Selection ranges highlighted
- "User X is typing..." indicators

---

## Implementation Patterns

### Pattern 1: WebSocket Setup with Reconnection

```typescript
import { io } from 'socket.io-client';

const socket = io('ws://localhost:3000', {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: Infinity,
  transports: ['websocket', 'polling']  // Fallback
});

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});

socket.on('disconnect', (reason) => {
  if (reason === 'io server disconnect') {
    // Server disconnected, manually reconnect
    socket.connect();
  }
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
});
```

### Pattern 2: Operational Transform (Text)

```typescript
import { TextOperation } from 'ot.js';

class OTEditor {
  private revision = 0;
  private pendingOperations: TextOperation[] = [];

  applyLocalOperation(op: TextOperation): void {
    // Apply immediately (optimistic update)
    this.applyToEditor(op);

    // Send to server
    this.sendOperation(op);

    // Store as pending
    this.pendingOperations.push(op);
  }

  receiveRemoteOperation(op: TextOperation, serverRevision: number): void {
    // Transform against pending operations
    let transformed = op;
    for (const pending of this.pendingOperations) {
      [transformed, pending] = TextOperation.transform(transformed, pending);
    }

    // Apply transformed operation
    this.applyToEditor(transformed);
    this.revision = serverRevision;
  }

  acknowledgeOperation(serverRevision: number): void {
    // Remove acknowledged operation from pending
    this.pendingOperations.shift();
    this.revision = serverRevision;
  }
}
```

### Pattern 3: CRDT with Yjs

```typescript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

// Create shared document
const ydoc = new Y.Doc();

// Define shared types
const ytext = ydoc.getText('content');
const ymap = ydoc.getMap('metadata');
const yarray = ydoc.getArray('users');

// Connect to sync server
const provider = new WebsocketProvider(
  'ws://localhost:1234',
  'room-name',
  ydoc
);

// Listen to changes
ytext.observe(event => {
  console.log('Text changed:', event.changes);
});

// Make changes (automatically synced)
ytext.insert(0, 'Hello ');
ytext.insert(6, 'World!');

// Undo/redo support
const undoManager = new Y.UndoManager(ytext);
undoManager.undo();
undoManager.redo();
```

### Pattern 4: Presence Awareness

```typescript
import { Awareness } from 'y-protocols/awareness';

const awareness = provider.awareness;

// Set local state
awareness.setLocalState({
  user: {
    name: 'Alice',
    color: '#ff0000',
    cursor: { line: 10, ch: 5 }
  }
});

// Listen to changes
awareness.on('change', ({ added, updated, removed }) => {
  // Update UI with user cursors/selections
  const states = awareness.getStates();
  states.forEach((state, clientId) => {
    if (clientId !== awareness.clientID) {
      renderCursor(state.user.cursor, state.user.color);
    }
  });
});
```

### Pattern 5: Optimistic Updates with Rollback

```typescript
class OptimisticEditor {
  private optimisticChanges = new Map<string, Change>();

  async applyChange(change: Change): Promise<void> {
    const changeId = generateId();

    // Apply immediately (optimistic)
    this.applyToUI(change);
    this.optimisticChanges.set(changeId, change);

    try {
      // Send to server
      const result = await this.sendToServer(change);

      // Success - remove from optimistic
      this.optimisticChanges.delete(changeId);

    } catch (error) {
      // Failed - rollback
      this.rollback(changeId);
      this.showError('Could not apply change');
    }
  }

  private rollback(changeId: string): void {
    const change = this.optimisticChanges.get(changeId);
    if (change) {
      this.revertInUI(change);
      this.optimisticChanges.delete(changeId);
    }
  }
}
```

---

## Production Checklist

```
□ WebSocket connection with auto-reconnect
□ Offline queue for pending changes
□ Conflict resolution strategy (OT or CRDT)
□ Server authority (clients can't desync)
□ Presence awareness (cursors, active users)
□ Optimistic updates with rollback
□ Change batching (not per-keystroke)
□ Message compression for large payloads
□ Authentication and authorization
□ Rate limiting (prevent spam)
□ Heartbeat/ping-pong to detect dead connections
□ Graceful degradation (falls back to polling if WebSocket fails)
```

---

## When to Use vs Avoid

| Scenario | Strategy |
|----------|----------|
| Text editing (Google Docs) | ✅ Operational Transform |
| JSON objects (Figma) | ✅ CRDTs (Yjs, Automerge) |
| Simple cursor sharing | ✅ Basic WebSocket + presence |
| Chat messages | ✅ Simple append-only (no OT/CRDT) |
| Video timeline editing | ✅ CRDTs for timeline, OT for text |
| Read-only dashboards | ❌ Use Server-Sent Events instead |

---

## References

- `/references/ot-vs-crdt.md` - Deep comparison of conflict resolution strategies
- `/references/websocket-scaling.md` - Scaling to millions of concurrent connections
- `/references/presence-patterns.md` - Cursor tracking, user awareness, activity indicators

## Scripts

- `scripts/collaboration_tester.ts` - Simulate concurrent edits, test conflict resolution
- `scripts/latency_simulator.ts` - Test behavior under high latency/packet loss

---

**This skill guides**: Real-time collaboration | WebSocket architecture | Operational Transform | CRDTs | Presence awareness | Conflict resolution

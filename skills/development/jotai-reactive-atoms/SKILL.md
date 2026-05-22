---
name: jotai-reactive-atoms
description: Implement reactive state management with Jotai atoms in Electron renderer. Use when creating atoms, implementing real-time updates via IPC, or setting up hybrid stream + HTTP fallback patterns. Covers event subscription optimization, debouncing, and Suspense integration.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Jotai Reactive Atoms for Electron

## Overview

This skill documents the Jotai atom patterns for Electron applications with IPC-based real-time updates.

## Key Patterns

| Pattern | Use Case | Description |
|---------|----------|-------------|
| Hybrid Atom | Real-time data | Stream + HTTP fallback |
| Stream Atom | IPC subscriptions | onMount with subscription |
| Single Fetch Atom | Initial data | HTTP-only async atom |
| Event Subscription | IPC optimization | Shared IPC listeners |

## Quick Start

### 1. Define Event Subscription Source

```typescript
// src/renderer/src/adapters/ipc-events/index.ts
import { createEventSubscription } from '@utils/event-subscription';

// One source per IPC event type
export const usersSource = createEventSubscription<void>('app:users');
export const activeEventSource = createEventSubscription<void>('app:activeEvent');
export const notificationsSource = createEventSubscription<Notification[]>('app:notifications');
```

### 2. Create Hybrid Atom

```typescript
// src/renderer/src/views/atoms/users.atom.ts
import { atom } from 'jotai';
import { atomWithRefresh } from 'jotai/utils';
import { client } from '@adapters/client';
import { usersSource } from '@adapters/ipc-events';
import { debounce } from '@utils/debounce';

// Step 1: HTTP-only fetch atom (fallback)
const singleFetchUsersAtom = atomWithRefresh(async () => {
  const res = await client.users.$get();
  if (res.status === 401) throw new UnauthorizedError();
  if (res.status === 500) throw new UnknownError();
  return res.json();
});

// Step 2: Stream atom (IPC updates)
const streamUsersAtom = atom<{ value: User[] }>();

streamUsersAtom.onMount = (set) => {
  const handleUpdate = debounce(async () => {
    const res = await client.users.$get();
    if (res.ok) {
      set({ value: await res.json() });
    }
  }, 300);

  handleUpdate();  // Immediate initial fetch

  return usersSource.subscribe(handleUpdate);  // Subscribe to IPC
};

// Step 3: Hybrid selector (exported)
export const usersAtom = atom(async (get) => {
  const stream = get(streamUsersAtom);
  if (stream === undefined) {
    return get(singleFetchUsersAtom);  // Fallback to HTTP
  }
  return stream.value;  // Use stream data
});
```

### 3. Use in Component with Suspense

```tsx
// src/renderer/src/views/users/index.tsx
import { Suspense } from 'react';
import { useAtomValue } from 'jotai';
import { usersAtom } from '../atoms/users.atom';

const UserList = () => {
  const users = useAtomValue(usersAtom);  // Suspends until ready

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.displayName}</li>
      ))}
    </ul>
  );
};

export const UsersPage = () => (
  <Suspense fallback={<Loading />}>
    <UserList />
  </Suspense>
);
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JOTAI HYBRID ATOM PATTERN                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   useAtom(usersAtom)                                                 │
│         │                                                             │
│         ▼                                                             │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │ usersAtom (Hybrid Selector)                                  │   │
│   │                                                               │   │
│   │ atom(async (get) => {                                        │   │
│   │   const stream = get(streamUsersAtom);                       │   │
│   │   if (stream === undefined) return get(singleFetchAtom);     │   │
│   │   return stream.value;                                        │   │
│   │ })                                                            │   │
│   └─────────────────────────────────────────────────────────────┘   │
│         │                                 │                          │
│         │ (t=0: not mounted)              │ (t=1+: mounted)          │
│         ▼                                 ▼                          │
│   ┌─────────────────┐           ┌─────────────────┐                 │
│   │ singleFetchAtom │           │ streamUsersAtom │                 │
│   │ (HTTP Fallback) │           │ (IPC Stream)    │                 │
│   └────────┬────────┘           └────────┬────────┘                 │
│            │                              │                          │
│            ▼                              │ onMount                   │
│   client.users.$get()                    │                          │
│            │                              ▼                          │
│            │                    usersSource.subscribe()             │
│            │                              │                          │
│            │                              │ IPC: 'app:users'         │
│            │                              ▼                          │
│            │                    debounce(handleUpdate, 300)         │
│            │                              │                          │
│            └──────────────────────────────┘                          │
│                              │                                        │
│                              ▼                                        │
│                      RENDERER RESULT                                 │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Timing Diagram

```
TIME: t0 (Component Mount)
═══════════════════════════════════════════════════════════

  Component mounts
       │
       ▼
  useAtom(usersAtom) → Suspends
       │
       │ streamUsersAtom = undefined (not yet mounted)
       │          │
       │          ▼
       │   Fallback: singleFetchAtom
       │          │
       │          ▼
       │   HTTP fetch → Data arrives
       │          │
       │          ▼
  Component renders with HTTP data ✓


TIME: t1 (Stream Ready)
═══════════════════════════════════════════════════════════

  streamUsersAtom.onMount executes
       │
       ├── Immediate fetch via HTTP
       │
       └── Subscribe to IPC events
              │
              ▼
  streamUsersAtom.value = fetched data
       │
       ▼
  usersAtom re-evaluates
       │
       │ stream !== undefined
       │          │
       │          ▼
       │   Return stream.value
       │
       ▼
  Component re-renders with stream data ✓


TIME: t2+ (Updates)
═══════════════════════════════════════════════════════════

  Main Process: Service Observable emits
       │
       ▼
  webContents.send('app:users')
       │
       ▼
  IPC Event received
       │
       ▼
  usersSource notifies subscribers
       │
       ▼
  Debounced handler executes (after 300ms)
       │
       ▼
  HTTP fetch → set({ value: newData })
       │
       ▼
  Component automatically re-renders ✓
```

## When to Use Each Pattern

### Hybrid Atom (Stream + HTTP Fallback)
Use for data that:
- Changes frequently
- Needs real-time updates
- Is shared across components

Examples: Users, Notifications, Active Event

### Stream-Only Atom
Use for data that:
- Is append-only (like logs)
- Doesn't need initial fetch

```typescript
export const logsAtom = atom<Log[]>([]);

logsAtom.onMount = (set) => {
  return logSource.subscribe((log) => {
    set((prev) => [log, ...prev].slice(0, 1000));
  });
};
```

### Single Fetch Atom
Use for data that:
- Rarely changes
- Doesn't need real-time updates

```typescript
export const worldAtom = atomFamily((id: string) =>
  atom(async () => {
    const res = await client.worlds[':id'].$get({ param: { id } });
    return res.json();
  })
);
```

## Additional Resources

- [HYBRID-ATOM.md](HYBRID-ATOM.md) - Detailed hybrid pattern implementation
- [EVENT-SUBSCRIPTION.md](EVENT-SUBSCRIPTION.md) - IPC subscription optimization
- [examples/hybrid-atom.ts](examples/hybrid-atom.ts) - Complete implementation

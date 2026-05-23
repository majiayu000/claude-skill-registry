---
name: state-effector
description: Effector reactive state management for React/Next.js applications. This skill should be used when implementing Effector stores, events, and effects, or when choosing Effector as the state management solution.
---

# Effector Skill

Patterns for reactive state management using Effector in React and Next.js applications.

## When to Use This Skill

- Setting up Effector in a new project
- Creating stores, events, and effects
- Integrating Effector with React components
- Organizing Effector models/domains
- Combining Effector with Tanstack Query

## Why Effector

Effector provides a reactive, event-driven approach to state management:

| Feature | Benefit |
|---------|---------|
| Fine-grained reactivity | Components only re-render when their specific data changes |
| TypeScript-first | Full type inference without extra work |
| Small bundle | ~10KB gzipped |
| Framework agnostic | Core logic works without React |
| Testable | Pure functions, easy to test in isolation |
| No boilerplate | No reducers, action creators, or switch statements |

### Effector vs Zustand

| Aspect | Effector | Zustand |
|--------|----------|---------|
| Model | Event-driven, reactive graphs | Flux-like stores |
| Learning curve | Steeper | Gentler |
| Reactivity | Automatic derived state | Manual selectors |
| Async | First-class effects | DIY with middleware |
| Best for | Complex reactive flows | Simple shared state |

## Setup

### Installation

```bash
npm install effector effector-react
```

### For Next.js with SSR

```bash
npm install effector effector-react @effector/next
```

## Core Concepts

### The Three Primitives

```typescript
import { createStore, createEvent, createEffect } from 'effector';

// EVENT: Triggers state changes
const increment = createEvent();
const decrement = createEvent();
const reset = createEvent();

// STORE: Holds reactive state
const $count = createStore(0)
  .on(increment, (count) => count + 1)
  .on(decrement, (count) => count - 1)
  .reset(reset);

// EFFECT: Handles async operations
const fetchUserFx = createEffect(async (userId: string) => {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json();
});
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Store | `$` prefix | `$user`, `$count`, `$isLoading` |
| Event | camelCase verb | `clicked`, `submitted`, `reset` |
| Effect | `Fx` suffix | `fetchUserFx`, `saveDataFx` |

## React Integration

### useUnit Hook

The `useUnit` hook binds stores and events to React components:

```typescript
'use client';

import { useUnit } from 'effector-react';
import { $count, increment, decrement, reset } from './model';

export function Counter() {
  const [count, onIncrement, onDecrement, onReset] = useUnit([
    $count,
    increment,
    decrement,
    reset,
  ]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => onIncrement()}>+</button>
      <button onClick={() => onDecrement()}>-</button>
      <button onClick={() => onReset()}>Reset</button>
    </div>
  );
}
```

### Object Form (Named)

```typescript
export function Counter() {
  const { count, inc, dec } = useUnit({
    count: $count,
    inc: increment,
    dec: decrement,
  });

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={inc}>+</button>
      <button onClick={dec}>-</button>
    </div>
  );
}
```

## Derived State

### Computed Stores

```typescript
import { createStore, createEvent, combine } from 'effector';

const $items = createStore<Item[]>([]);
const $filter = createStore<'all' | 'active' | 'completed'>('all');

// Derived store - automatically updates when dependencies change
const $filteredItems = combine($items, $filter, (items, filter) => {
  switch (filter) {
    case 'active':
      return items.filter((item) => !item.completed);
    case 'completed':
      return items.filter((item) => item.completed);
    default:
      return items;
  }
});

// Count derived from items
const $itemCount = $items.map((items) => items.length);
const $completedCount = $items.map(
  (items) => items.filter((item) => item.completed).length
);
```

## Effects (Async Operations)

### Basic Effect

```typescript
import { createEffect, createStore, createEvent } from 'effector';

interface User {
  id: string;
  name: string;
  email: string;
}

// Define effect with typed input/output
const fetchUserFx = createEffect<string, User, Error>(async (userId) => {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
});

// Stores react to effect states
const $user = createStore<User | null>(null)
  .on(fetchUserFx.doneData, (_, user) => user)
  .reset(fetchUserFx.fail);

const $isLoading = fetchUserFx.pending;

const $error = createStore<string | null>(null)
  .on(fetchUserFx.failData, (_, error) => error.message)
  .reset(fetchUserFx);
```

### Effect States

Every effect has built-in states:

```typescript
fetchUserFx.pending;     // Store<boolean> - true while running
fetchUserFx.done;        // Event<{params, result}> - on success
fetchUserFx.doneData;    // Event<result> - just the result
fetchUserFx.fail;        // Event<{params, error}> - on failure
fetchUserFx.failData;    // Event<error> - just the error
fetchUserFx.finally;     // Event - always fires after completion
```

### Usage in Components

```typescript
'use client';

import { useUnit } from 'effector-react';
import { $user, $isLoading, $error, fetchUserFx } from './model';

export function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading, error, fetchUser } = useUnit({
    user: $user,
    isLoading: $isLoading,
    error: $error,
    fetchUser: fetchUserFx,
  });

  useEffect(() => {
    fetchUser(userId);
  }, [userId, fetchUser]);

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage message={error} />;
  if (!user) return null;

  return <div>{user.name}</div>;
}
```

## Event Chaining

### sample - Connect Events to Effects

```typescript
import { sample } from 'effector';

const formSubmitted = createEvent<FormData>();
const saveFormFx = createEffect<FormData, void>();

// When formSubmitted fires, call saveFormFx with the data
sample({
  clock: formSubmitted,
  target: saveFormFx,
});
```

### sample with Transformation

```typescript
const userIdChanged = createEvent<string>();
const $currentUserId = createStore('');

sample({
  clock: userIdChanged,
  source: $currentUserId,
  filter: (currentId, newId) => currentId !== newId, // Only if changed
  fn: (_, newId) => newId, // Transform data
  target: fetchUserFx,
});
```

### forward - Simple Event-to-Event

```typescript
import { forward } from 'effector';

const buttonClicked = createEvent();
const formReset = createEvent();

// When buttonClicked fires, also fire formReset
forward({
  from: buttonClicked,
  to: formReset,
});
```

## Project Structure

### Feature-Based Organization

```
src/
├── features/
│   ├── auth/
│   │   ├── model.ts        # Stores, events, effects
│   │   ├── ui/
│   │   │   ├── LoginForm.tsx
│   │   │   └── UserMenu.tsx
│   │   └── index.ts
│   ├── projects/
│   │   ├── model.ts
│   │   ├── ui/
│   │   │   ├── ProjectList.tsx
│   │   │   └── ProjectCard.tsx
│   │   └── index.ts
│   └── shared/
│       └── api.ts          # Shared effects for API calls
├── app/
│   └── ...
└── lib/
    └── effector.ts         # Shared utilities
```

### Model File Pattern

```typescript
// features/projects/model.ts
import { createStore, createEvent, createEffect, sample } from 'effector';

// Types
interface Project {
  id: string;
  name: string;
  status: 'active' | 'archived';
}

// Events
export const projectCreated = createEvent<{ name: string }>();
export const projectDeleted = createEvent<string>();
export const projectsPageOpened = createEvent();

// Effects
export const fetchProjectsFx = createEffect(async () => {
  const res = await fetch('/api/projects');
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json() as Promise<Project[]>;
});

export const createProjectFx = createEffect(async (data: { name: string }) => {
  const res = await fetch('/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create');
  return res.json() as Promise<Project>;
});

export const deleteProjectFx = createEffect(async (id: string) => {
  const res = await fetch(`/api/projects/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete');
});

// Stores
export const $projects = createStore<Project[]>([])
  .on(fetchProjectsFx.doneData, (_, projects) => projects)
  .on(createProjectFx.doneData, (projects, newProject) => [...projects, newProject])
  .on(deleteProjectFx.done, (projects, { params: id }) =>
    projects.filter((p) => p.id !== id)
  );

export const $isLoading = fetchProjectsFx.pending;

// Connections
sample({
  clock: projectsPageOpened,
  target: fetchProjectsFx,
});

sample({
  clock: projectCreated,
  target: createProjectFx,
});

sample({
  clock: projectDeleted,
  target: deleteProjectFx,
});
```

## Next.js SSR Integration

### With @effector/next

```typescript
// app/providers.tsx
'use client';

import { EffectorNext } from '@effector/next';

export function Providers({ children }: { children: React.ReactNode }) {
  return <EffectorNext>{children}</EffectorNext>;
}
```

```typescript
// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Hydration with Server Data

```typescript
// Server Component
async function getProjects() {
  // Fetch on server
  return db.query.project.findMany();
}

export default async function ProjectsPage() {
  const projects = await getProjects();
  
  return (
    <ProjectsProvider initialProjects={projects}>
      <ProjectList />
    </ProjectsProvider>
  );
}

// Client Provider
'use client';

import { useEffect } from 'react';
import { projectsLoaded } from './model';

export function ProjectsProvider({
  children,
  initialProjects,
}: {
  children: React.ReactNode;
  initialProjects: Project[];
}) {
  useEffect(() => {
    projectsLoaded(initialProjects);
  }, [initialProjects]);

  return <>{children}</>;
}
```

## Combining with Tanstack Query

Use Tanstack Query for server state, Effector for client state:

```typescript
// Server state with Query
const { data: projects } = useQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
});

// Client state with Effector
const { selectedProjectId, setSelectedProject } = useUnit({
  selectedProjectId: $selectedProjectId,
  setSelectedProject: projectSelected,
});

// Derived from both
const selectedProject = projects?.find((p) => p.id === selectedProjectId);
```

## Testing

### Testing Stores

```typescript
import { fork, allSettled } from 'effector';
import { $count, increment, reset } from './model';

describe('counter', () => {
  it('increments count', async () => {
    const scope = fork();
    
    await allSettled(increment, { scope });
    await allSettled(increment, { scope });
    
    expect(scope.getState($count)).toBe(2);
  });

  it('resets to zero', async () => {
    const scope = fork({
      values: [[$count, 10]], // Initial state
    });
    
    await allSettled(reset, { scope });
    
    expect(scope.getState($count)).toBe(0);
  });
});
```

### Testing Effects

```typescript
import { fork, allSettled } from 'effector';
import { $user, fetchUserFx } from './model';

describe('fetchUser', () => {
  it('updates user on success', async () => {
    const mockUser = { id: '1', name: 'John' };
    
    const scope = fork({
      handlers: [
        [fetchUserFx, () => mockUser], // Mock the effect
      ],
    });
    
    await allSettled(fetchUserFx, { scope, params: '1' });
    
    expect(scope.getState($user)).toEqual(mockUser);
  });
});
```

## Best Practices

### Do

- Use `$` prefix for stores
- Keep models separate from UI
- Use `sample` for complex event flows
- Use `fork` for testing
- Derive state with `combine` and `.map()`

### Don't

- Don't call events inside effects (use `sample`)
- Don't mutate store values directly
- Don't create stores inside components
- Don't ignore TypeScript errors

## Quick Reference

```typescript
// Create primitives
createStore(initialValue)
createEvent<PayloadType>()
createEffect<Params, Result, Error>(handler)

// React hooks
useUnit(store)              // Subscribe to store
useUnit([store, event])     // Subscribe to multiple
useUnit({ name: store })    // Named object form

// Derived state
$store.map(fn)              // Transform store value
combine($a, $b, fn)         // Combine multiple stores

// Event connections
sample({ clock, source, filter, fn, target })
forward({ from, to })

// Testing
fork({ values, handlers })
allSettled(unit, { scope, params })
scope.getState($store)
```

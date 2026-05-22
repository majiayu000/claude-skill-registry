---
name: hono-ipc-routes
description: Implement type-safe IPC communication in Electron using Hono RPC. Use when creating API routes between main and renderer processes, setting up typed clients, or implementing request/response IPC patterns. Provides HTTP-like semantics over Electron IPC.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Hono IPC Routes for Electron

## Overview

This skill documents how to implement type-safe IPC communication using Hono in Electron applications. Hono provides HTTP-like semantics with full TypeScript type inference.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      RENDERER PROCESS                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   const res = await client.users.$get()                              │
│   const data = await res.json()                                      │
│         │                                                             │
│         │ Type: { displayName: string, id: string }[]                │
│         ▼                                                             │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Hono Client (hc<CallableType>)                              │   │
│   │                                                               │   │
│   │  Custom fetch: ipcRenderer.invoke('hono-rpc-electron', ...)  │   │
│   └───────────────────────────────┬───────────────────────────────┘ │
│                                   │                                  │
└───────────────────────────────────┼──────────────────────────────────┘
                                    │ IPC
┌───────────────────────────────────┼──────────────────────────────────┐
│                      MAIN PROCESS │                                  │
├───────────────────────────────────┼──────────────────────────────────┤
│                                   │                                  │
│   ┌───────────────────────────────▼───────────────────────────────┐ │
│   │  ipcMain.handle('hono-rpc-electron', ...)                     │ │
│   │                                                                │ │
│   │  const res = await callable.request(url, { method, body })    │ │
│   │  return { ...res, data: await res.json() }                    │ │
│   └───────────────────────────────┬───────────────────────────────┘ │
│                                   │                                  │
│   ┌───────────────────────────────▼───────────────────────────────┐ │
│   │  Hono App (callable)                                          │ │
│   │                                                                │ │
│   │  app.route('/users', usersRoutes)                             │ │
│   │  app.route('/events', eventsRoutes)                           │ │
│   │  app.route('/notifications', notificationsRoutes)             │ │
│   └───────────────────────────────┬───────────────────────────────┘ │
│                                   │                                  │
│   ┌───────────────────────────────▼───────────────────────────────┐ │
│   │  Route Handler                                                 │ │
│   │                                                                │ │
│   │  .get('/', (c) => {                                           │ │
│   │    const users = await c.var.services.users.list()            │ │
│   │    return c.json(users, 200)                                  │ │
│   │  })                                                            │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Define Shared Routes

```typescript
// src/shared/callable/index.ts
import { Hono } from 'hono';
import { users } from './users';
import { events } from './events';
import { notifications } from './notifications';

// App type for dependency injection
export type AppVariables = {
  services: {
    users: UserService;
    events: EventService;
    notifications: NotificationService;
  };
};

// Create app with typed variables
const app = new Hono<{ Variables: AppVariables }>()
  .route('/users', users.route)
  .route('/events', events.routes)
  .route('/notifications', notifications);

export type CallableType = typeof app;
export default app;
```

### 2. Implement Route Handlers

```typescript
// src/shared/callable/users/index.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';
import { firstValueFromResult } from '@utils/observable';
import type { AppVariables } from '../index';

const createUserSchema = z.object({
  displayName: z.string().min(1),
  bio: z.string().optional(),
});

export const route = new Hono<{ Variables: AppVariables }>()
  // GET /users - List all users
  .get('/', async (c) => {
    const result = await firstValueFromResult(
      c.var.services.users.list()
    );

    return result.match(
      (users) => c.json(users, 200),
      (error) => c.json({ error: error.message }, 500)
    );
  })

  // GET /users/:id - Get single user
  .get('/:id', async (c) => {
    const id = c.req.param('id');
    const result = await firstValueFromResult(
      c.var.services.users.get(id)
    );

    return result.match(
      (user) => user
        ? c.json(user, 200)
        : c.json({ error: 'Not found' }, 404),
      (error) => c.json({ error: error.message }, 500)
    );
  })

  // POST /users - Create user
  .post('/', zValidator('json', createUserSchema), async (c) => {
    const data = c.req.valid('json');
    const result = await c.var.services.users.create(data);

    return result.match(
      () => c.json({ success: true }, 201),
      (error) => c.json({ error: error.message }, 500)
    );
  });

export const users = { route };
```

### 3. Initialize Main Process Handler

```typescript
// src/main/callable/index.ts
import { Hono } from 'hono';
import routes from '@shared/callable';

export const createCallable = (services: AppVariables['services']) => {
  const app = new Hono<{ Variables: AppVariables }>()
    .use('*', async (c, next) => {
      // Inject services into context
      c.set('services', services);
      await next();
    })
    .route('/', routes);

  return app;
};
```

### 4. Register IPC Handler

```typescript
// src/main/index.ts
import { ipcMain } from 'electron';
import { createCallable } from '@callable';

// Create callable with injected services
const callable = createCallable({
  users: userService,
  events: eventService,
  notifications: notificationService,
});

// Register IPC handler
ipcMain.handle('hono-rpc-electron', async (
  _,
  url: string,
  method?: string,
  headers?: [string, string][],
  body?: string | ArrayBuffer
) => {
  const res = await callable.request(url, { method, headers, body });
  const data = await res.json();

  if (res.status >= 400) {
    logService.write('error', 'api-error', {
      error: `Request failed: ${url} - ${res.status}`
    });
  }

  return { ...res, data };
});
```

### 5. Create Typed Client

```typescript
// src/renderer/src/adapters/client.ts
import { hc } from 'hono/client';
import type { CallableType } from '@shared/callable';

// Serialize headers for IPC
const serializeHeader = (headers: HeadersInit | undefined): [string, string][] => {
  if (headers === undefined) return [];
  if (headers instanceof Headers) {
    return [...headers.entries()];
  }
  if (Array.isArray(headers)) return headers;
  return Object.entries(headers);
};

// Create typed client with custom IPC fetch
export const client = hc<CallableType>('http://internal.localhost', {
  async fetch(input, init) {
    const url = input.toString();
    const args = [
      url,
      init?.method,
      serializeHeader(init?.headers),
      init?.body
    ];

    const { data, ...rest } = await window.electron.ipcRenderer.invoke(
      'hono-rpc-electron',
      ...args
    );

    return Response.json(data, rest);
  },
});
```

## Type Safety Flow

```typescript
// Route definition infers response type
const route = new Hono()
  .get('/users', (c) => c.json([{ id: '1', name: 'John' }], 200));
//                              ▲ Return type: { id: string, name: string }[]

// Client inherits type
const res = await client.users.$get();
const users = await res.json();
//    ▲ TypeScript knows: { id: string, name: string }[]

// POST with typed body
await client.users.$post({
  json: { displayName: 'Jane', bio: 'Hello' }
//        ▲ TypeScript validates against zValidator schema
});
```

## Additional Resources

- [ROUTE-HANDLERS.md](ROUTE-HANDLERS.md) - Detailed route implementation patterns
- [TYPE-SAFETY.md](TYPE-SAFETY.md) - Type system and validation
- [examples/users-route.ts](examples/users-route.ts) - Complete route example
- [examples/client-usage.ts](examples/client-usage.ts) - Client usage patterns

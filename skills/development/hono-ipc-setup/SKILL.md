---
name: hono-ipc-setup
description: Set up Hono-based type-safe IPC architecture for Electron applications. Use when implementing IPC communication, creating routes between main and renderer processes, or migrating from traditional ipcRenderer to type-safe RPC.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm:*), Bash(pnpm:*)
---

# Hono Electron IPC Setup

This skill provides comprehensive knowledge for setting up type-safe IPC communication in Electron applications using Hono RPC.

## When This Skill Applies

- Setting up IPC communication in Electron
- Creating type-safe communication between main and renderer processes
- Migrating from `ipcRenderer.invoke` / `ipcMain.handle` to Hono
- Implementing factory pattern with dependency injection for IPC
- Adding new IPC routes with full TypeScript support

## Quick Start

### 1. Install Dependencies

```bash
pnpm add hono @hono/zod-validator zod
```

### 2. Create Directory Structure

```
src/
├── shared/
│   └── callable/
│       ├── index.ts          # Factory and app creation
│       └── types.d.ts        # Type export for client
├── main/
│   └── callable/
│       └── index.ts          # Service injection
└── renderer/
    └── src/
        └── adapters/
            └── client.ts     # Type-safe hc client
```

### 3. Core Files

See [FACTORY-PATTERN.md](FACTORY-PATTERN.md) for complete factory implementation.
See [REFERENCE.md](REFERENCE.md) for Hono RPC API reference.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      RENDERER PROCESS                        │
│                                                              │
│  React/Vue/etc Component                                     │
│       │                                                      │
│       ▼                                                      │
│  client.users[':id'].$get({ param: { id: 'xxx' } })         │
│       │                                                      │
│       ▼                                                      │
│  hc<CallableType> with custom fetch                          │
│       │                                                      │
│       ▼                                                      │
│  ipcRenderer.invoke('hono-rpc-electron', url, method, ...)  │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                       MAIN PROCESS                            │
│                                                               │
│  ipcMain.handle('hono-rpc-electron', handler)                 │
│       │                                                       │
│       ▼                                                       │
│  callable.request(url, { method, headers, body })             │
│       │                                                       │
│       ▼                                                       │
│  Hono Router                                                  │
│       │                                                       │
│       ▼                                                       │
│  Route Handler: (c) => c.var.services.xxx.method()            │
│       │                                                       │
│       ▼                                                       │
│  Service Layer (injected via DI)                              │
└───────────────────────────────────────────────────────────────┘
```

## Type Safety Flow

The key to type safety is the `CallableType`:

```typescript
// src/shared/callable/types.d.ts
import type { createApp } from '.';
export type CallableType = ReturnType<typeof createApp>;

// src/renderer/src/adapters/client.ts
import type { CallableType } from '@shared/callable/types';
export const client = hc<CallableType>('http://internal.localhost', { ... });

// Now client has full autocomplete:
// client.users.$get()         - GET /users
// client.users[':id'].$get()  - GET /users/:id
// client.auth.sign_in.$post() - POST /auth/sign_in
```

## Key Benefits

| Aspect | Traditional IPC | Hono IPC |
|--------|-----------------|----------|
| Type Safety | Manual typing | Full inference |
| API Design | Ad-hoc channels | RESTful routes |
| Validation | Manual | Zod middleware |
| Testing | Mock IPC | Standard HTTP |
| Error Handling | Per-handler | Centralized |
| Scalability | One channel each | Single channel |

## Common Patterns

### Route with Zod Validation

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const CreateUserBody = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

.post('/users', zValidator('json', CreateUserBody), (c) => {
  const body = c.req.valid('json'); // Fully typed
  return c.json(body, 201);
})
```

### Route with Path Parameters

```typescript
.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.var.services.users.get(id).then(user => c.json(user));
})
```

### Route with Query Parameters

```typescript
const QueryParams = z.object({
  limit: z.coerce.number().default(10),
  offset: z.coerce.number().default(0),
});

.get('/users', zValidator('query', QueryParams), (c) => {
  const { limit, offset } = c.req.valid('query');
  return c.var.services.users.list({ limit, offset });
})
```

## Serialization Notes

Only JSON-serializable data can be sent through IPC:

**Supported:**
- Primitives (string, number, boolean, null)
- Objects and arrays
- ISO date strings (parse with `dayjs` on receive)

**Not Supported (need manual conversion):**
- Date objects (convert to ISO string)
- Map/Set (convert to array/object)
- ArrayBuffer/Blob (use base64 encoding)
- Class instances (serialize to plain object)

## Files Reference

- [FACTORY-PATTERN.md](FACTORY-PATTERN.md) - Complete DI factory pattern
- [REFERENCE.md](REFERENCE.md) - Hono RPC API reference
- [examples/auth-route.ts](examples/auth-route.ts) - Auth route example
- [examples/users-route.ts](examples/users-route.ts) - Users route example

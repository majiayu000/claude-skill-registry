---
name: hono-ipc-setup
description: Set up Hono-based type-safe IPC for Electron. Use when implementing IPC or migrating from ipcRenderer to type-safe RPC.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm:*), Bash(pnpm:*)
---

# Hono Electron IPC Setup

## Resources

| Topic | File |
|-------|------|
| Why shared/ directory | [SHARED-DIRECTORY.md](SHARED-DIRECTORY.md) |
| Factory pattern with DI | [FACTORY-PATTERN.md](FACTORY-PATTERN.md) |
| Hono RPC API reference | [REFERENCE.md](REFERENCE.md) |

## Directory Structure

```
src/
├── shared/callable/        # Factory, app creation, types.d.ts
├── main/callable/          # Service injection
└── renderer/src/adapters/  # Type-safe hc client
```

## Quick Start

```bash
pnpm add hono @hono/zod-validator zod
```

```typescript
// Type export: src/shared/callable/types.d.ts
export type CallableType = ReturnType<typeof createApp>;

// Client: src/renderer/src/adapters/client.ts
export const client = hc<CallableType>('http://internal.localhost', { ... });
```

## Related Skills

- [cqrs-pattern](../cqrs-pattern/SKILL.md) - Query/Command separation
- [hono-ipc-routes](../hono-ipc-routes/SKILL.md) - Route implementation

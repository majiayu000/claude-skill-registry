---
name: hono-ipc-routes
description: Implement type-safe IPC routes in Electron using Hono RPC. Use when creating API routes between main and renderer processes.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Hono IPC Routes

## Resources

| Topic | File |
|-------|------|
| Route implementation | [ROUTE-HANDLERS.md](ROUTE-HANDLERS.md) |
| Type safety patterns | [TYPE-SAFETY.md](TYPE-SAFETY.md) |
| Error handling | [ERROR-HANDLING.md](ERROR-HANDLING.md) |

## Quick Reference

```typescript
// Route: src/shared/callable/users/index.ts
export const route = new Hono<{ Variables: AppVariables }>()
  .get('/', async (c) => c.json(await c.var.services.users.list(), 200))
  .post('/', zValidator('json', schema), async (c) => { ... });

// Client: fully typed
const users = await client.users.$get().then(r => r.json());
```

## Related Skills

- [hono-ipc-setup](../hono-ipc-setup/SKILL.md) - Initial setup
- [cqrs-pattern](../cqrs-pattern/SKILL.md) - Service layer patterns

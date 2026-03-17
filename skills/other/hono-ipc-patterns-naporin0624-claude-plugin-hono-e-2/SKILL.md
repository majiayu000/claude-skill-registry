---
name: hono-ipc-patterns
description: Advanced patterns for Hono-based Electron IPC including Zod validation and error handling. Use when adding validation or handling errors in routes.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Hono IPC Patterns

## Resources

| Topic | File |
|-------|------|
| CQRS Pattern | [../cqrs-pattern/SKILL.md](../cqrs-pattern/SKILL.md) |
| Zod Validation | [ZOD-VALIDATION.md](ZOD-VALIDATION.md) |
| Error Handling | [../hono-ipc-routes/ERROR-HANDLING.md](../hono-ipc-routes/ERROR-HANDLING.md) |

## Quick Reference

### Zod Validation Targets

| Target | Example |
|--------|---------|
| `json` | `zValidator('json', z.object({ name: z.string() }))` |
| `query` | `zValidator('query', z.object({ limit: z.coerce.number() }))` |
| `param` | `zValidator('param', z.object({ id: z.string() }))` |

### Error Pattern

```typescript
result.match(
  (data) => c.json(data, 200),
  (error) => c.json({ error: error.message }, 500)
);
```

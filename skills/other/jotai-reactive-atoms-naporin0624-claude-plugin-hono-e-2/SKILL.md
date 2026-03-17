---
name: jotai-reactive-atoms
description: Implement reactive state management with Jotai atoms in Electron renderer. Use when creating atoms with real-time IPC updates or hybrid stream + HTTP patterns.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Jotai Reactive Atoms

## Patterns

| Pattern | Use Case | Details |
|---------|----------|---------|
| Hybrid Atom | Real-time + HTTP fallback | [HYBRID-ATOM.md](HYBRID-ATOM.md) |
| Stream Atom | IPC subscriptions | [EVENT-SUBSCRIPTION.md](EVENT-SUBSCRIPTION.md) |
| Write Atom | CRUD mutations | [WRITE-ATOM.md](WRITE-ATOM.md) |

## Key Rules

1. **Hybrid atom getter must NOT be async** - use sync conditional
2. **Always debounce IPC handlers** - prevent UI thrashing
3. **Refresh read atoms after mutations** - `set(singleFetchAtom)`

## Quick Example

```typescript
// Hybrid selector (sync, NOT async)
export const usersAtom = atom((get) => {
  const stream = get(streamAtom);
  return stream !== undefined ? stream.value : get(singleFetchAtom);
});
```

## Related

- [suspense-boundary-design](../suspense-boundary-design/SKILL.md) - Suspense and ErrorBoundary

---
name: 40-03-dependency-direction
description: Dependencies flow one direction. Shared state → domain logic → presentation. Never circular. Prevents import tangles and initialization order bugs.
---

# 40.03 Dependency Direction

Dependencies flow downward. Lower layers never import from higher layers.

## The Layers

```
┌─────────────────────────────┐
│  Presentation (UI, CLI,     │  Reads state, dispatches actions
│  API surface)               │
├─────────────────────────────┤
│  Domain actions / queries   │  Reads shared state, calls into services
├─────────────────────────────┤
│  Domain logic (entity mgmt, │  Reads + writes shared state
│  event handlers, sync)      │
├─────────────────────────────┤
│  Shared state (refs, tables,│  The data. Depends on nothing.
│  caches, stores)            │
├─────────────────────────────┤
│  Infrastructure (connection,│  SDK, protocol, IO, types
│  bindings, types)           │
└─────────────────────────────┘
```

**Arrows point down only.**

## The Rules

1. **Shared state imports nothing from the project.** Only types and external libraries. It's the foundation — everything depends on it, it depends on nothing.

2. **Domain logic imports shared state.** Entity management reads from state. Never the reverse.

3. **Actions/queries import shared state.** Feature actions read refs and call reducers. They don't import domain logic internals.

4. **Presentation imports actions and reads state.** Components/views call actions and read from state/stores. They don't import shared state directly.

## How Circular Dependencies Happen

Module A imports Module B. Module B imports Module A. At load time, one of them is partially initialized → undefined references, subtle bugs.

**Common cause:** shared state that imports a computation from a higher layer.

**Fix:** if shared state needs a computation, the computation is a pure function that lives at the same level or lower.

## Runtime Callbacks (the one valid upward call)

Connection lifecycle needs to call into domain logic when events arrive (subscription fires → upsert entity). This goes "upward" at runtime.

This is safe because:
- All modules are fully loaded before any callback fires
- The callback is registered at runtime, not at import time
- No circular import — only the lower module imports the higher one

Keep callbacks **thin** — translate the event into a domain function call, nothing more.

## The Test

> Draw the import graph. Do any arrows point upward?

If yes — move the shared dependency down, or extract it to a lower layer.

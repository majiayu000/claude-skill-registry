---
name: 40-01-state-ownership
description: Every piece of mutable state has exactly one owner that writes it. Others read. Prevents "who set this?" and invisible coupling.
---

# 40.01 State Ownership

Every piece of mutable state has exactly one system that writes it. Everyone else reads.

## The Problem

When multiple systems write the same state:
- Race conditions — who set this value?
- Invisible coupling — changing one writer breaks another
- Untestable code — can't isolate the write path
- God objects — one module "owns" everything because it writes everything

## The Rule

For every piece of mutable state, you must be able to answer: **"Who writes this?"** with exactly one name.

| State | Owner (writes) | Everyone else |
|-------|---------------|---------------|
| Entity position | Physics system | Read-only |
| Connection state | Connection lifecycle | Read-only |
| Player identity | Session resolution | Read-only |
| ECS entity IDs | Entity bridge | Read-only |
| Tuning values | Tuning loader | Read-only |

If you can't fill in the "Owner" column with one name, the design is wrong.

## How to Apply

1. **Declare state in one place.** One module, one struct, one table — not scattered across files.
2. **Write from one system.** If two systems need to write the same field, one of them is wrong. Find the real owner.
3. **Name the owner.** Comment, colocation, or naming convention — make ownership obvious at the declaration site.
4. **Readers access state directly.** No getter functions wrapping a read. No passing state through layers of callbacks.

## Anti-Pattern: Trapped State

State that can only be accessed through the module that owns it, because it's hidden inside a closure, private field, or local variable. This forces everything into one module.

The fix: move state to a shared location. The owner still writes. But now readers don't need to go through the owner.

## Anti-Pattern: Multiple Writers

```
System A writes entity.position (for physics)
System B writes entity.position (for teleport)
System C writes entity.position (for spawn)
→ "Who moved the entity?" — impossible to answer
```

Fix: one system owns position. Teleport and spawn send requests/inputs to that system.

## The Test

> Point at any mutable field. Can you name the ONE system that writes it?

If the answer is "it depends" or "several things" — fix the ownership.

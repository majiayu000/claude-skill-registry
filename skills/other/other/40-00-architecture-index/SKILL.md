---
name: 40-00-architecture-index
description: Architecture primer index. Read this first before any structural work — it points you to the specific principle you need. Progressive exploration, not bulk loading.
---

# 40.00 Architecture Index

Architectural principles for building and modifying code. Each entry prevents a specific class of decay. **Don't read them all** — find the one that matches your situation, read it, apply it.

### General (any language)

| ID | Primer | Read before... |
|----|--------|---------------|
| `40.01` | State ownership | Creating mutable state anywhere |
| `40.02` | Module boundaries | Creating a new file or growing an existing one |
| `40.03` | Dependency direction | Importing between layers |

### TypeScript / React

| ID | Primer | Read before... |
|----|--------|---------------|
| `40.04` | Domain logic separation | Putting logic in React hooks, callbacks, or closures |
| `40.05` | Singleton patterns | Writing a factory, closure, or class for something with one instance |

## Quick decision aid

- **"Where does this state live?"** → `40.01`
- **"Should this be a new file?"** → `40.02`
- **"Can A import B?"** → `40.03`
- **"This hook is getting complex"** → `40.04` (TS)
- **"Should I make a factory/class for this?"** → `40.05` (TS)
- **"This file is 1000+ lines, how do I split it?"** → `30.04` (closure monolith decomposition)

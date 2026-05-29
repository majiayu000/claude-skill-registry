---
name: solid-terminology
description: "SolidJS terminology standards: use 'primitive' not 'hook', 'reactive value' not just 'signal', 'computation' not 'computed'. Use 'Solid' not 'SolidJS' internally."
---

# SolidJS Terminology Standards

Use these terms consistently when writing SolidJS code or documentation:

## Core Terms

- **Primitive** (not "hook") - A function that serves as a building block of reactivity or behavior, usually begins with `create` or `use`
- **Reactive value** (not just "signal") - A value that can be tracked (includes signals, memos, properties of `props` and stores)
- **Computation** or **reactive computation** (not "computed") - A scope that automatically reruns when its dependencies change
- **Core primitive** - A primitive provided by the Solid core library (not "API function")
- **Custom primitive** - A primitive created outside the Solid core library (not "hook")
- **Tracking scope** - A scope that, when run, Solid automatically tracks all read signals
- **Scope** - A body of a function (a chunk of code). Not to be confused with root or effect (specific kinds of scopes)
- **Root** - A computation that has no owner, created by `createRoot`
- **Ownership** - A one-to-many relationship between computations
- **Solid** (not "SolidJS") - Use "Solid" when referring to the framework internally. Use "SolidJS" only when referring to the project externally

## Key Rules

1. Never use "hook" - Solid doesn't use React's hook terminology. Use "primitive" instead.
2. Use "reactive value" as the general term, not "signal" (which refers specifically to values created by `createSignal`)
3. Use "computation" or "reactive computation", not "computed"
4. Use "Solid" not "SolidJS" in code comments and internal documentation


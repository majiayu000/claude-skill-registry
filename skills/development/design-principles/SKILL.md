---
name: design-principles
description: 'Code design patterns: pure functions, immutability, composition, and
  async. Use when designing code or functions.'
---

---
name: design-principles
description: Code design patterns: pure functions, immutability, composition, and async. Use when designing code or functions.
---

# Code Design Principles

Patterns for writing clean, maintainable, and testable code.

## Quick Start

```typescript
// Pure function with immutability
function updateUser(user: User, age: number): User {
  return { ...user, age }; // new object, no mutation
}
```

## Key Principles

- Pure functions: no side effects, same input = same output
- Immutability: create new objects/arrays instead of mutating
- Single responsibility: one function = one task
- Early returns: reduce nesting, improve readability
- Composition over inheritance: inject dependencies
- Promises over callbacks for async code
- Template strings over concatenation
- Plain objects for data, classes only for stateful services
- Avoid global variables and getters/setters
- Lazy initialization: no module-level side effects, wrap in getter functions

## References

See [rules.md](references/rules.md) for complete guidelines with examples.

---
name: react-patterns
description: Write React components with minimal state, proper memoization, and type-safe patterns. Use when creating components, managing state, or optimizing renders.
user-invocable: false
metadata:
  author: BastiDood <basti@casperstudios.xyz>
---

# React Patterns

Core React patterns for component design, state management, and optimization.

## State Philosophy

Avoid state variables. Prefer derived values and props. Scope state to the smallest subtree that needs it. Use discriminated unions for complex state.

See [state-management.md](references/state-management.md) for:

- Derived values over state
- Component boundaries for state scoping
- Context API patterns
- Zustand for complex state
- State machines over multiple useState

## Memoization

Required for any O(n) operation. Memoize atomically to minimize dependency arrays. Use Loader/Inner pattern to narrow types before useMemo.

See [memoization.md](references/memoization.md) for:

- When to useMemo
- Atomic memoization
- useCallback for handlers
- Loader/Inner pattern for type narrowing

## Conditional Logic

Use affirmative logic, explicit conditionals, and ternaries over `&&`. Early returns for guard clauses.

See [conditional-logic.md](references/conditional-logic.md) for:

- Affirmative logic
- Explicit conditionals
- Conditional rendering
- Type narrowing with conditionals
- Early returns

---
name: web-state-mobx
description: MobX observable state management patterns with mobx-react-lite. Use when implementing reactive client state with observables, computed values, actions, and the observer HOC.
---

# MobX State Management Patterns

> **Quick Guide:** Use MobX for complex client state needing automatic dependency tracking, computed values, and fine-grained reactivity. Use `makeAutoObservable` for stores, `observer` from `mobx-react-lite` for React components, and `runInAction`/`flow` for async state updates. Never use MobX for server state (use React Query).

**Detailed Resources:**

- For core examples (store creation, observer, useLocalObservable), see [examples/core.md](examples/core.md)
- For advanced examples (computed, actions, async, reactions), see [examples/advanced.md](examples/advanced.md)
- For architecture examples (root store, TypeScript, performance), see [examples/architecture.md](examples/architecture.md)

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `makeAutoObservable(this)` in EVERY class store constructor - or use `makeObservable` with explicit annotations for subclassed stores)**

**(You MUST wrap ALL state mutations after `await` in `runInAction()` - or use `flow` with generator functions instead of async/await)**

**(You MUST wrap EVERY React component that reads observables in `observer()` from `mobx-react-lite`)**

**(You MUST use React Query for server state - NEVER store API data in MobX stores)**

**(You MUST always dispose reactions (autorun, reaction, when) to prevent memory leaks)**

</critical_requirements>

---

**Auto-detection:** MobX, makeAutoObservable, makeObservable, observable, observer, mobx-react-lite, runInAction, flow, computed, autorun, reaction, useLocalObservable

**When to use:**

- Complex client state with computed derivations and automatic dependency tracking
- Class-based or factory-function stores with observable properties
- Fine-grained reactivity where only affected components re-render
- State that benefits from transparent reactive programming (spreadsheet-like derivations)

**Key patterns covered:**

- Store creation with `makeAutoObservable` and `makeObservable`
- React integration with `observer` and `useLocalObservable`
- Computed values for derived state
- Actions, `runInAction`, and `flow` for state mutations and async
- Reactions (`autorun`, `reaction`, `when`) for side effects
- Root store pattern for multi-store architectures
- TypeScript integration and performance optimization

**When NOT to use:**

- Server/API data (use React Query or similar data-fetching solution)
- Simple local UI state (use `useState`)
- Lightweight shared state without computed needs (consider Zustand)
- State that should be URL-shareable (use `searchParams`)

---

<philosophy>

## Philosophy

MobX embraces a core principle: **"Anything that can be derived from the application state, should be derived. Automatically."** It uses transparent reactive programming where observables track dependencies at runtime and only notify exactly the computations and components that depend on changed values.

Unlike Zustand (minimal, explicit subscriptions) or Redux (immutable state, explicit reducers), MobX uses mutable observables with automatic tracking. This means less boilerplate but requires understanding how reactivity works -- specifically, MobX tracks property access during tracked function execution, not variable assignments.

### When to Use MobX

- Complex domain models with many derived/computed values
- Applications where class-based stores provide natural organization
- Scenarios requiring fine-grained reactivity (large lists, frequent updates)
- Teams comfortable with mutable state and OOP patterns

### When NOT to Use MobX

- Server state management (use React Query)
- Simple shared UI state without derivations (Zustand is lighter)
- Projects preferring immutable state patterns (use Redux Toolkit)
- Simple component-local state (`useState` is sufficient)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Store Creation with makeAutoObservable

`makeAutoObservable` infers annotations automatically: properties become `observable`, getters become `computed`, methods become `action`, and generator functions become `flow`. It cannot be used on classes with `super` or that are subclassed.

**Key points:**

- Call `makeAutoObservable(this)` in the constructor
- Use `autoBind: true` option to auto-bind methods (safe for event handlers and callbacks)
- Pass overrides as second argument to exclude or customize specific properties
- For subclassed stores, use `makeObservable` with explicit annotations instead

For implementation examples, see [examples/core.md](examples/core.md#pattern-1-store-creation-with-makeautoobservable).

---

### Pattern 2: Store Creation with makeObservable

`makeObservable` requires explicit annotation of each property. Use when you need inheritance (subclassed stores) or want explicit control over which properties are observable.

**Key points:**

- Annotate each property explicitly: `observable`, `computed`, `action`, `flow`
- Required for classes using `extends` (inheritance)
- More verbose but gives full control over reactivity annotations
- Use `action.bound` for methods passed as callbacks

For implementation examples, see [examples/core.md](examples/core.md#pattern-2-store-creation-with-makeobservable).

---

### Pattern 3: Factory Function Stores

Factory functions with `makeAutoObservable` offer an alternative to classes. They avoid `this` and `new` issues, compose easily, and can hide private members via closures.

**Key points:**

- Return a plain object from a factory function
- `makeAutoObservable` works the same on plain objects
- Getters become computed, methods become actions
- Good for simple stores or when preferring functional patterns

For implementation examples, see [examples/core.md](examples/core.md#pattern-3-factory-function-stores).

---

### Pattern 4: React Integration with observer

The `observer` HOC from `mobx-react-lite` makes React components reactive. It automatically tracks which observables are read during render and re-renders only when those specific values change.

**Key points:**

- Wrap EVERY component that reads observables in `observer()`
- `observer` automatically applies `React.memo` (no need to add it separately)
- Pass observable objects (not extracted primitives) to child observer components
- Use named function expressions for proper React DevTools display

For implementation examples, see [examples/core.md](examples/core.md#pattern-4-react-integration-with-observer).

---

### Pattern 5: useLocalObservable for Local Component State

`useLocalObservable` creates a local observable store scoped to a component. Use for complex local state that benefits from computed values but does not need to be shared.

**Key points:**

- Properties become observable, getters become computed, methods become actions
- The store persists across re-renders (like `useRef` but reactive)
- Reserve for complex local state with computed values -- simple state should use `useState`
- May conflict with future React concurrent features

For implementation examples, see [examples/core.md](examples/core.md#pattern-5-uselocalobservable-for-local-component-state).

---

### Pattern 6: Computed Values

Computed values are derivations that automatically cache and recalculate when their dependencies change. They are the MobX equivalent of spreadsheet formulas.

**Key points:**

- Defined as getters in classes/objects, automatically inferred by `makeAutoObservable`
- Cached: only recalculate when observed dependencies actually change
- Should be pure: no side effects, no modification of other observables
- Use `computed.struct` for structural comparison when output shape is the same despite input changes
- Suspend automatically when not observed (use `keepAlive` option to prevent, but risks memory leaks)

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-6-computed-values).

---

### Pattern 7: Actions and runInAction

Actions are the only place you should modify observable state. They batch mutations into transactions, so reactions only fire after the outermost action completes.

**Key points:**

- Methods are automatically marked as actions by `makeAutoObservable`
- Use `runInAction()` for inline state mutations (especially after `await`)
- Actions batch: intermediate states are not visible to observers
- Actions do NOT track observable reads (they are untracked)

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-7-actions-and-runinaction).

---

### Pattern 8: Async Patterns (flow and runInAction)

MobX provides two patterns for async state updates. Code after `await` runs in a new tick and is NOT part of the original action, so state mutations must be wrapped.

**Key points:**

- **`runInAction` pattern**: Wrap state mutations after `await` in `runInAction(() => { ... })`
- **`flow` pattern** (recommended): Use generator functions (`function*`) with `yield` instead of `async/await` -- no wrapping needed
- `flow` returns a cancellable promise with `.cancel()` method
- `makeAutoObservable` automatically infers generator functions as `flow`

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-8-async-patterns-flow-and-runinaction).

---

### Pattern 9: Reactions (autorun, reaction, when)

Reactions are side effects that run automatically when observed state changes. They bridge reactive MobX state to imperative side effects (logging, network requests, DOM updates).

**Key points:**

- **`autorun`**: Runs immediately and re-runs whenever any read observable changes
- **`reaction`**: Takes a data function and effect function -- effect only runs when data function return value changes (not on init)
- **`when`**: Runs effect once when a predicate becomes true, then auto-disposes
- ALL reactions return a disposer function -- you MUST call it to prevent memory leaks
- Reactions only track observables read synchronously (not in `setTimeout`, promises, or after `await`)

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-9-reactions-autorun-reaction-when).

---

### Pattern 10: Root Store Pattern

The root store pattern organizes multiple domain and UI stores into a single coordinator that enables store-to-store communication.

**Key points:**

- Create a `RootStore` class that instantiates all stores
- Each store receives a reference to the root store for cross-store access
- Provide the root store via React Context (dependency injection, NOT state management)
- Separate domain stores (business data) from UI stores (interface state)
- Simple to set up, supports strong typing, makes unit testing easy

For implementation examples, see [examples/architecture.md](examples/architecture.md#pattern-10-root-store-pattern).

---

### Pattern 11: TypeScript Integration

MobX has first-class TypeScript support. Stores are naturally typed through class definitions and interface-based factory functions.

**Key points:**

- Class stores get type inference automatically from property declarations
- Use `makeAutoObservable<Store, "privateField">` to annotate private fields
- Use `import type` for type-only imports
- `makeObservable` requires explicit annotations that TypeScript can verify
- Factory functions should return typed objects or use `satisfies` for validation

For implementation examples, see [examples/architecture.md](examples/architecture.md#pattern-11-typescript-integration).

---

### Pattern 12: Performance Optimization

MobX provides fine-grained reactivity out of the box, but understanding how to structure components and observables maximizes performance.

**Key points:**

- Use many small `observer` components -- smaller scope means fewer re-renders
- Dereference observables as late as possible (pass objects, not extracted primitives)
- Render lists in dedicated observer components to avoid reconciling entire lists
- Use `computed` values to avoid redundant calculations
- `observer` auto-applies `memo` -- no need for `React.memo` on observer components

For implementation examples, see [examples/architecture.md](examples/architecture.md#pattern-12-performance-optimization).

</patterns>

---

<decision_framework>

## Decision Framework

### MobX vs Other Solutions

```
Is it server data (from API)?
|-- YES --> React Query (NOT MobX)
|-- NO --> Is it simple local UI state (one component)?
    |-- YES --> useState
    |-- NO --> Does it need computed/derived values?
        |-- YES --> Do you prefer OOP / class-based stores?
        |   |-- YES --> MobX
        |   |-- NO --> Consider Zustand with derived selectors
        |-- NO --> Is it lightweight shared state?
            |-- YES --> Zustand (simpler API, less overhead)
            |-- NO --> MobX (fine-grained reactivity scales well)
```

### makeAutoObservable vs makeObservable

```
Does the store class use inheritance (extends)?
|-- YES --> makeObservable (explicit annotations required)
|-- NO --> Is the store subclassed by other stores?
    |-- YES --> makeObservable (makeAutoObservable forbids subclassing)
    |-- NO --> makeAutoObservable (less boilerplate, auto-inference)
```

### Async Pattern: flow vs runInAction

```
Is the async operation complex with multiple yields?
|-- YES --> flow (generator function, cancellable, cleaner)
|-- NO --> Is cancellation needed?
    |-- YES --> flow (returns promise with .cancel())
    |-- NO --> runInAction (simpler for single await)
```

### Reaction Type Selection

```
Need to run effect immediately and on every change?
|-- YES --> autorun
|-- NO --> Need to run effect only when specific data changes?
    |-- YES --> reaction (data function + effect function)
    |-- NO --> Need to run effect once when condition is true?
        |-- YES --> when
        |-- NO --> Reconsider if you need a reaction at all
```

### Quick Reference Table

| Use Case                      | Solution      | Why                                          |
| ----------------------------- | ------------- | -------------------------------------------- |
| Server/API data               | React Query   | Caching, refetch, loading states             |
| Simple local UI state         | useState      | Lightweight, component-scoped                |
| Shared state with derivations | MobX          | Automatic tracking, computed values          |
| Lightweight shared state      | Zustand       | Simpler API, less conceptual overhead        |
| Complex domain models         | MobX          | Class stores, inter-store references         |
| URL-shareable state           | searchParams  | Bookmarkable, browser navigation             |
| Dependency injection          | React Context | Singletons, providers (NOT state management) |

</decision_framework>

---

<integration>

## Integration Guide

**Works with:**

- **React Query**: MobX handles client state, React Query handles server state. Keep them separate -- never duplicate API data in MobX stores.
- **React Router**: URL params for shareable state, MobX for complex client state that does not belong in URLs.
- **React Context**: Use Context ONLY to provide the root store via dependency injection. Never use Context for state management.
- **mobx-react-lite**: The recommended React binding (lightweight, function components only). Prefer over `mobx-react` which adds class component support you likely do not need.

**Replaces / Conflicts with:**

- **Zustand**: Both solve client state -- pick one per project. MobX for complex derivations and OOP; Zustand for simplicity.
- **Redux Toolkit**: Both are full-featured state solutions. MobX uses mutable observables; Redux uses immutable state with reducers.
- **React Context + useState**: MobX replaces this anti-pattern entirely with better performance and selective re-renders.

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Mutating observables outside actions** -- breaks MobX enforceActions, causes unpredictable state updates
- **Missing `observer` wrapper on components reading observables** -- component will not re-render when state changes (most common MobX bug)
- **Storing server/API data in MobX** -- causes stale data, no caching, manual sync; use React Query instead
- **Not disposing reactions** -- autorun, reaction, when all return disposers that MUST be called to prevent memory leaks
- **State mutation after `await` without `runInAction`** -- code after await is NOT in the original action, will fail with enforceActions

**Medium Priority Issues:**

- Using `mobx-react` instead of `mobx-react-lite` (heavier, includes class component support you likely do not need)
- Destructuring primitives from observables outside tracked functions (breaks reactivity tracking)
- Using `makeAutoObservable` on subclassed stores (will throw -- use `makeObservable` instead)
- Creating side effects in computed values (computeds must be pure derivations)
- Overusing reactions where computed values would suffice

**Common Mistakes:**

- Reading observables in `setTimeout`/`setInterval` callbacks without proper tracking
- Passing extracted primitive values instead of observable objects to child components (breaks fine-grained tracking)
- Forgetting `autoBind: true` when passing store methods as callbacks (leads to lost `this` context)
- Using rest destructuring (`...store`) on observables (touches all properties, makes component overly reactive)
- Not using `toJS()` when passing observable data to non-MobX-aware libraries

**Gotchas and Edge Cases:**

- `observer` auto-applies `React.memo` -- never wrap an observer component in `memo` again (redundant)
- Computed values suspend when not observed -- accessing them outside reactions causes recalculation every time (use `keepAlive` option if needed, but watch for memory leaks)
- `autorun` tracks only synchronous reads -- observables read in async callbacks, promises, or after `await` are NOT tracked
- `reaction` does NOT run on initialization (unlike `autorun`) -- use `fireImmediately: true` option if needed
- Generator functions are automatically inferred as `flow` by `makeAutoObservable` -- do not also wrap them in `flow()`. However, some transpiler configurations cannot detect generators; if flow does not work as expected, specify `flow` explicitly in overrides
- `action.bound` and `autoBind: true` are NOT the same as arrow function class fields -- arrow functions cannot be overridden in subclasses
- MobX tracks property access ("arrows"), not values -- reassigning a variable that held an observable reference does NOT trigger reactions

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `makeAutoObservable(this)` in EVERY class store constructor - or use `makeObservable` with explicit annotations for subclassed stores)**

**(You MUST wrap ALL state mutations after `await` in `runInAction()` - or use `flow` with generator functions instead of async/await)**

**(You MUST wrap EVERY React component that reads observables in `observer()` from `mobx-react-lite`)**

**(You MUST use React Query for server state - NEVER store API data in MobX stores)**

**(You MUST always dispose reactions (autorun, reaction, when) to prevent memory leaks)**

**Failure to follow these rules will break MobX reactivity, cause memory leaks, or produce stale data.**

</critical_reminders>

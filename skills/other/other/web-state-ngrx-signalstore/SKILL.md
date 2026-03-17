---
name: web-state-ngrx-signalstore
description: NgRx SignalStore patterns for Angular state management. Use when managing client state with Angular Signals, composing store features, handling entities, or integrating RxJS effects.
---

# NgRx SignalStore Patterns

> **Quick Guide:** Use NgRx SignalStore for reactive client state in Angular 17+. Compose stores with `withState`, `withComputed`, `withMethods`. Use `patchState` for immutable updates. Use `withEntities` for collections. NEVER use traditional NgRx patterns (actions, reducers, effects) in new SignalStore code.

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - signalStore, withState, withComputed, withMethods
  - [entities.md](examples/entities.md) - withEntities, CRUD operations
  - [effects.md](examples/effects.md) - rxMethod, side effects
  - [features.md](examples/features.md) - signalStoreFeature, custom features
  - [testing.md](examples/testing.md) - Unit tests, mocking strategies
  - [migration.md](examples/migration.md) - Migration from traditional NgRx
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Managing State with NgRx SignalStore

**(You MUST use `patchState()` for ALL state updates - NEVER mutate state directly)**

**(You MUST wrap async operations in `rxMethod()` from `@ngrx/signals/rxjs-interop` for RxJS integration)**

**(You MUST use `withEntities()` from `@ngrx/signals/entities` for entity collections - NOT arrays in state)**

**(You MUST use named exports ONLY - NO default exports in any store files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

</critical_requirements>

---

**Auto-detection:** NgRx SignalStore, signalStore, withState, withComputed, withMethods, patchState, withEntities, rxMethod, signalStoreFeature, @ngrx/signals

**When to use:**

- Managing reactive client state in Angular 17+ applications
- Building composable, reusable store features
- Handling entity collections with CRUD operations
- Integrating RxJS operators for side effects
- Applications requiring fine-grained reactivity with Angular Signals

**Key patterns covered:**

- Store creation with `signalStore()` and `providedIn` options
- State, computed, and methods composition
- Entity management with `withEntities`
- RxJS integration with `rxMethod` and signal-only `signalMethod`
- Custom features with `signalStoreFeature`
- Call state patterns (loading, loaded, error)
- DevTools integration with ngrx-toolkit

**When NOT to use:**

- Server/API data as primary source (use HTTP services with rxMethod for caching)
- Simple component-local state (use Angular signals directly)
- Projects still on Angular < 17 (requires signals)
- Teams unfamiliar with functional composition patterns

---

<philosophy>

## Philosophy

NgRx SignalStore is a lightweight, functional state management solution built on Angular Signals. It replaces traditional NgRx patterns (actions, reducers, effects, selectors) with a composable, feature-based approach that eliminates boilerplate while maintaining predictability.

**Core Principles:**

1. **Functional Composition** - Build stores by composing features like `withState`, `withComputed`, `withMethods`
2. **Signal-Based Reactivity** - Leverage Angular's fine-grained reactivity for optimal performance
3. **Immutable Updates** - Use `patchState()` for predictable state transitions
4. **Extensibility** - Create custom features with `signalStoreFeature()` for reuse across stores

**Key Architecture Decisions:**

1. **`signalStore()`** creates a fully typed store as an injectable Angular service
2. **`patchState()`** ensures immutable updates without Immer dependency
3. **`withEntities()`** provides standardized entity management (similar to Redux Toolkit's `createEntityAdapter`)
4. **`rxMethod()`** bridges Angular Signals with RxJS for complex async flows
5. **Protected state** (v18+) prevents external mutations by default; v19+ applies deep freeze recursively

**State Ownership:**

| State Type            | Solution                 | Reason                               |
| --------------------- | ------------------------ | ------------------------------------ |
| Server/API data       | HTTP services + rxMethod | Caching in store, fetch via services |
| Shared client state   | SignalStore              | Reactivity, composition, DevTools    |
| Component-local state | Angular signals          | Simpler, no overhead                 |
| URL state (filters)   | Router query params      | Shareable, bookmarkable              |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Store with signalStore

Create stores using `signalStore()` with `withState`, `withComputed`, and `withMethods`.

#### Feature Ordering

Features execute in order. State features must come first:

1. `withState()` - Define state
2. `withComputed()` - Derived values from state
3. `withMethods()` - Actions that update state
4. `withHooks()` - Lifecycle hooks (onInit, onDestroy)

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 2: State Updates with patchState

Use `patchState()` for all state modifications. It ensures immutability and proper signal notifications.

#### When to Use

- Synchronous state updates
- Partial state updates (spread not needed)
- Inside `withMethods()` and custom features

#### Key Behaviors

- Accepts partial state object or updater functions
- Multiple updaters can be passed to single call
- Works with entity updaters from `@ngrx/signals/entities`

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 3: Entity Management with withEntities

Use `withEntities()` for collections of items with IDs. Provides standardized CRUD operations and efficient lookups.

#### When to Use

- Lists of items with unique identifiers
- CRUD operations on collections
- Need for efficient ID-based lookups
- Multiple entity collections in one store

#### Available Updaters

- `setAllEntities()` - Replace all entities
- `addEntity()` / `addEntities()` - Add new entities
- `setEntity()` / `setEntities()` - Upsert entities
- `updateEntity()` / `updateEntities()` - Partial updates
- `removeEntity()` / `removeEntities()` - Delete entities

For implementation examples, see [examples/entities.md](examples/entities.md).

---

### Pattern 4: RxJS Integration with rxMethod

Use `rxMethod()` for side effects that need RxJS operators (debounce, switchMap, etc.).

#### When to Use

- Debounced search/filtering
- Cancellable HTTP requests
- Complex async flows with multiple operators
- Reactive streams from signals

#### Key Behaviors

- Accepts `Observable<T>`, `Signal<T>`, or `T` as input
- Factory function receives `Observable<T>` for piping
- Runs in injection context (can use `inject()`)
- Auto-unsubscribes on store destroy

For implementation examples, see [examples/effects.md](examples/effects.md).

---

### Pattern 4b: Signal-Only Side Effects with signalMethod (v19+)

Use `signalMethod()` for side effects that don't need RxJS operators.

#### When to Use

- Simple side effects without RxJS dependency
- When you want to work purely with Signals
- Side effects that don't require debounce/switchMap/cancellation
- When injection context is not available

#### Key Behaviors

- Accepts `Signal<T>` or `T` as input (no Observable)
- Processor function runs independently of injection context
- Only parameter signals are tracked; internal signals remain untracked
- You must handle race conditions manually (no built-in switchMap)

#### rxMethod vs signalMethod

| Feature                         | `rxMethod`                  | `signalMethod` |
| ------------------------------- | --------------------------- | -------------- |
| RxJS required                   | Yes                         | No             |
| Operators (debounce, switchMap) | Yes                         | No             |
| Race condition handling         | Built-in                    | Manual         |
| Input types                     | T, Signal<T>, Observable<T> | T, Signal<T>   |

For implementation examples, see [examples/effects.md](examples/effects.md).

---

### Pattern 5: Custom Features with signalStoreFeature

Use `signalStoreFeature()` to create reusable store functionality.

#### When to Use

- Shared patterns across multiple stores (loading state, error handling)
- Encapsulated feature modules
- Third-party store extensions
- DRY principle for repeated store logic

#### Type Constraints

Use `type()` helper to specify required store members:

- Ensures feature is only used with compatible stores
- Provides full type inference
- Enables composition of features

For implementation examples, see [examples/features.md](examples/features.md).

---

### Pattern 6: Lifecycle Hooks with withHooks

Use `withHooks()` for initialization and cleanup logic.

#### Available Hooks

- `onInit()` - Called when store is instantiated
- `onDestroy()` - Called when store is destroyed

#### Common Use Cases

- Loading initial data on store creation
- Setting up subscriptions
- Cleanup of resources
- DevTools initialization

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 7: Call State Pattern

Track loading, loaded, and error states for async operations using `withCallState()` from ngrx-toolkit or custom implementation.

#### States

- `loading` - Operation in progress
- `loaded` - Operation completed successfully
- `error` - Operation failed with error

#### Benefits

- Consistent loading UI patterns
- Error handling standardization
- Multiple collection support
- DevTools visibility

For implementation examples, see [examples/features.md](examples/features.md).

</patterns>

---

<integration>

## Integration Guide

**Angular DI Integration:**

SignalStore is an Angular service. Use `providedIn: 'root'` for singletons or component-level providers for scoped stores:

```typescript
// Root-level singleton
export const GlobalStore = signalStore(
  { providedIn: "root" },
  withState({
    /* ... */
  }),
);

// Component-scoped
@Component({
  providers: [LocalStore],
})
export class MyComponent {
  readonly store = inject(LocalStore);
}
```

**DevTools Integration:**

Use `@angular-architects/ngrx-toolkit` for Redux DevTools support:

```typescript
import { withDevtools } from "@angular-architects/ngrx-toolkit";

export const FlightStore = signalStore(
  { providedIn: "root" },
  withDevtools("flights"),
  withState({ flights: [] as Flight[] }),
);
```

**Testing Integration:**

- Use `unprotected()` from `@ngrx/signals/testing` to bypass state protection
- Use `TestBed.configureTestingModule()` with mocked services
- Test store methods directly or through component integration

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use `patchState()` for ALL state updates - NEVER mutate state directly)**

**(You MUST wrap async operations in `rxMethod()` from `@ngrx/signals/rxjs-interop` for RxJS integration)**

**(You MUST use `withEntities()` from `@ngrx/signals/entities` for entity collections - NOT arrays in state)**

**(You MUST use named exports ONLY - NO default exports in any store files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

**Failure to follow these rules will cause reactivity bugs, state corruption, and inconsistent behavior.**

</critical_reminders>

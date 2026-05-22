---
name: superpower-zustand
description: MANDATORY for creating Zustand stores. This skill is required when users request state management, creating stores, or mention Zustand. Do NOT create Zustand stores without this skill - all stores must use the required StoreBuilder pattern with immer middleware and factory pattern separation
---

# Zustand StoreBuilder Pattern

<CRITICAL>
DO NOT create Zustand stores using standard patterns (create with inline actions). ALL Zustand stores in this project MUST use the StoreBuilder pattern defined below. This is a required architectural standard, not a suggestion.
</CRITICAL>

## Purpose

Enforce a standardized, type-safe approach to creating Zustand stores that:
- Separates state definition from actions using the factory pattern
- Integrates immer middleware for convenient immutable updates
- Supports optional persistence with fine-grained control
- Exposes both reactive (useStore hook) and non-reactive (get/set) access
- Maintains consistent patterns across the codebase

## When to Use This Skill

Use this skill when:
- Creating new Zustand stores for state management
- User requests state management solutions in a React application
- Implementing stores for any feature requiring client-side state

## Required Pattern

All Zustand stores MUST use the StoreBuilder utility located in `assets/storebuilder.ts`.

### Core Implementation Steps

1. **Copy the StoreBuilder utility** (if not already in the project)
   - Source: `skills/superpower-zustand/assets/storebuilder.ts`
   - Destination: `src/lib/storebuilder.ts` (or similar location in the project)

2. **Define state type separately from actions**
   - Create a type for the full store (state + actions)
   - Use `Omit` to exclude action methods when passing to StoreBuilder

3. **Initialize the store with StoreBuilder**
   - Pass initial state as first argument
   - Optionally pass PersistConfig as second argument for persistence

4. **Separate actions using createFactory**
   - Define all actions as methods in the createFactory argument
   - Actions access `set` from the StoreBuilder closure
   - Use immer-style mutations within `set` callbacks

5. **Export the factory-created hook**
   - The hook returned by createFactory combines state, actions, and store utilities

### Required Code Structure

```typescript
import { StoreBuilder } from './storebuilder';

// 1. Define complete state type
type MyStoreState = {
  // State fields
  value: number;
  items: string[];

  // Action methods
  setValue: (v: number) => void;
  addItem: (item: string) => void;
};

// 2. Initialize StoreBuilder with state only (Omit actions)
const { set, createFactory } = StoreBuilder<Omit<MyStoreState, 'setValue' | 'addItem'>>(
  {
    value: 0,
    items: [],
  },
  // Optional: persistence config
  // {
  //   name: 'my-store',
  //   version: 1,
  // }
);

// 3. Create factory with actions
const useMyStore = createFactory({
  setValue: (v: number) => set((state) => { state.value = v; }),
  addItem: (item: string) => set((state) => { state.items.push(item); }),
});

// 4. Export the hook
export { useMyStore };
```

### State Updates with Immer

When using `set`, write mutations directly on the draft state (immer middleware is included):

```typescript
// ✅ Correct: Mutate draft
set((state) => {
  state.count += 1;
  state.items.push(newItem);
  state.nested.property = 'value';
});

// ❌ Incorrect: Don't return new object
set((state) => ({ ...state, count: state.count + 1 }));
```

### Persistence Configuration

When state should persist across sessions:

```typescript
const { createFactory } = StoreBuilder(
  initialState,
  {
    name: 'storage-key',           // Required: localStorage key
    version: 1,                     // Optional: for migration handling
    storage: sessionStorage,        // Optional: defaults to localStorage
    partialize: (state) => ({       // Optional: persist only specific fields
      theme: state.theme,
      preferences: state.preferences,
    }),
  }
);
```

## Reference Documentation

For detailed examples and advanced patterns, read `references/pattern-guide.md`:
- Basic usage examples
- Persistence patterns
- Complex stores with async actions
- Using get/set outside React components
- Type safety patterns

Load the reference documentation when:
- Implementing complex stores with async operations
- Needing examples of persistence configuration
- User asks about advanced Zustand patterns
- Unsure about specific implementation details

## Verification

After creating a store, verify:
1. ✅ StoreBuilder utility is imported from project location
2. ✅ State type uses `Omit` to exclude actions
3. ✅ All actions are defined in `createFactory`, not in initial state
4. ✅ State updates use immer-style mutations (mutate draft, don't return new object)
5. ✅ Exported hook name follows convention (e.g., `useMyStore`)
6. ✅ Persistence config is included if state should persist

## Non-React Usage

The pattern supports non-reactive access outside React components:

```typescript
const { get, set, subscribe } = StoreBuilder(initialState);

// Get current state
const current = get();

// Update state
set((state) => { state.value = 10; });

// Subscribe to changes
const unsubscribe = subscribe((state) => console.log(state));
```

Use `get` and `set` when:
- Accessing state in utility functions
- Implementing middleware or side effects
- Working outside React component lifecycle

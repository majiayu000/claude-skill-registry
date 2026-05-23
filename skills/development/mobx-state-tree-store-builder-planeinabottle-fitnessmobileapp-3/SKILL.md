---
name: mobx-state-tree-store-builder
description: Automates creation of MobX State Tree stores following Fitness Tracker App patterns for domain models, collections, and root store integration. Use when creating new MST stores, models, or extending existing store functionality with proper TypeScript typing, actions, views, and integration patterns.
---

# MobX State Tree Store Builder

This skill helps create MobX State Tree stores following the established patterns in the Fitness Tracker App. It handles the complex setup required for proper TypeScript integration, RootStore injection, and consistent architectural patterns.

## When to Use This Skill

Use this skill when you need to:
- Create a new domain model (like ExerciseModel)
- Build a collection store (like ExerciseStoreModel)
- Add a new store to the RootStore
- Extend existing stores with new functionality
- Create proper TypeScript interfaces and snapshots

## Store Types

### Domain Models
Atomic data models that represent business entities. Examples: `ExerciseModel`, `UserModel`.

**Pattern**: `types.model("Name", { ... }).views(...).actions(...)`

### Collection Stores
Stores that manage collections of domain models. Examples: `ExerciseStore`, `StatsStore`.

**Pattern**: `types.model("StoreName", { collection: types.map(Model) }).views(...).actions(...)`

### Singleton Stores
Stores with single-instance data. Examples: `UserStore`, `UiStore`.

**Pattern**: `types.model("StoreName", { ... }).views(...).actions(...)`

## Root Store Integration

All stores must be added to the RootStore for dependency injection:

```typescript
export const RootStoreModel = types.model("RootStore", {
  // Add new store here
  newStore: types.optional(NewStoreModel, {}),
  // ... existing stores
})
```

## TypeScript Integration

Always export proper interfaces:
- `IStoreName` - Instance type
- `IStoreNameSnapshotIn` - Input snapshot type
- `IStoreNameSnapshotOut` - Output snapshot type

## Common Patterns

### Computed Views
Use for derived data that depends on store state:

```typescript
.views((self) => ({
  get computedProperty() {
    return self.someData * 2
  },
}))
```

### Actions with Root Access
Use `getRoot<IRootStore>(self)` to access other stores:

```typescript
.actions((self) => ({
  someAction() {
    const rootStore = getRoot<IRootStore>(self)
    rootStore.otherStore.doSomething()
  },
}))
```

### Async Actions
Use `flow` for async operations:

```typescript
import { flow } from "mobx-state-tree"

.actions((self) => ({
  asyncAction: flow(function* () {
    try {
      // async operations
      yield someAsyncCall()
    } catch (error) {
      // error handling
    }
  }),
}))
```

## File Organization

Store files go in `app/models/`:
- Domain models: `ModelName.ts`
- Stores: `StoreName.ts`
- Root store: `RootStore.ts`

## Testing

Each store should have corresponding tests in `app/models/__tests__/`.

## References

See [MST_PATTERNS.md](references/MST_PATTERNS.md) for detailed patterns and examples from the codebase.

See [STORE_TEMPLATES.md](references/STORE_TEMPLATES.md) for reusable templates.

See [ROOT_STORE_INTEGRATION.md](references/ROOT_STORE_INTEGRATION.md) for adding stores to RootStore.
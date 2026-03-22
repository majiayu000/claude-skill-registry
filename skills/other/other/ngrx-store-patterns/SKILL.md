---
name: ngrx-store-patterns
description: Project-specific NgRx Signals Store patterns for this Angular 21 DDD application. Activates when code involves signalStore, withEntities, rxMethod, patchState, tapResponse, or any NgRx signals state management.
---

# NgRx Signals Store Patterns (Project-Specific)

For complete store patterns, read `.github/instructions/ngrx-signals.instructions.md`.
For store testing, read `.github/instructions/ngrx-signals-testing.instructions.md`.

## Quick Reference

- Store location: `src/app/features/{domain}/data/state/{domain}-store.ts`
- Reference: `src/app/features/tasks/data/state/task-store.ts`

## Key Rules

- `signalStore({ providedIn: 'root' })` for all stores
- `withState` → `withEntities` → `withComputed` → `withMethods` order
- `rxMethod` + `tapResponse` for async operations
- `patchState` for all state updates — never mutate directly
- Always include `loading: boolean` and `error: string | null` in state
- Entity ops: `setAllEntities`, `addEntity`, `updateEntity`, `removeEntity`
- `tapResponse` from `@ngrx/operators`, NOT `@ngrx/component-store`

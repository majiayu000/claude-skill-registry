---
name: pinia
description: Esposter Pinia store conventions — full store name, destructure with storeToRefs, store-to-store dot-access for refs (methods may be destructured), and CRUD patterns (findIndex guard, Object.assign update, filter delete). Apply when using or writing Pinia stores.
---

# Pinia Store Conventions

## Usage in Vue Components

- **`storeToRefs` is auto-imported** — never write `import { storeToRefs } from "pinia"`. Same applies to `defineStore` in `.vue` and composable files.
- **Naming**: use the full store name — `const fileTableEditorStore = useFileTableEditorStore()`, not `const store = ...` or abbreviated names.
- **In Vue components**: always destructure, and keep each store's lines grouped together in this order — no mixing across stores:
  1. `const xyzStore = useXyzStore()`
  2. `const { ref1, ref2 } = storeToRefs(xyzStore)` _(omit if no refs/computeds needed)_
  3. `const { method1 } = xyzStore` _(omit if no methods needed)_
  4. _(repeat for next store)_
- Never use dot-access (`store.method()`) in components.
- **Store-to-store** (inside a Pinia store file): declare nested stores at the root of the setup function. Access refs/computeds via dot syntax (`otherStore.someRef`) to maintain reactivity — do NOT use `storeToRefs`. Methods may still be destructured: `const { methodName } = otherStore`.

## CRUD Store Patterns

Follow `createOperationData` conventions exactly when writing store update/delete methods:

- **update**: `findIndex` first, guard `if (index === -1) return`, then mutate in place with `Object.assign(takeOne(items.value, index), updatedItem)`.
- **delete**: reassign the array — `items.value = items.value.filter(...)` — never `splice`.
- Always guard against a missing parent ref before any operation: `if (!parentRef.value) return`.

## CRUD Parameter Naming

Use consistent parameter names across stores, composables, and functions:

- **create**: `newXxx` — e.g. `createRow(newRow?: Row)`, `createColumn(newColumn: Column | DateColumn)`
- **update**: `updatedXxx` — e.g. `updateRow(updatedRow: Row)`, `updateColumn(updatedColumn: ToData<Column | DateColumn>)`
- **delete**: just `id` — delete operations typically only need the identifier, not the full object. Exception: when additional context is required (e.g. `deleteColumn(name: string)`), use the most natural identifier name.

This mirrors `createOperationData` which uses `newItem` / `updatedItem` / `ids` for its parameters.

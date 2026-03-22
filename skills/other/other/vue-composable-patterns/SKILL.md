---
name: vue-composable-patterns
description: Esposter-specific Vue 3 composable and form patterns. Use when writing composables, form dialogs, MaybeRefOrGetter utilities, or Vjsf-based forms in this project.
---

# Vue Composable & Form Patterns (Esposter)

Patterns learned through development of the Esposter project. Apply these whenever writing Vue composables, validation rules, or form dialogs.

## When to Use `MaybeRefOrGetter` vs Function Argument

Use `MaybeRefOrGetter<T>` when the composable **internally reacts** to the value — i.e., it's used inside a `computed` or `watch`. The composable needs to observe changes between calls.

Use a plain **function argument** on the returned function when the value is just a **pass-through** evaluated at call time. The composable has no internal reactive dependency on it.

```typescript
// CORRECT: MaybeRefOrGetter — composable computes based on the value
export const useColumnNameRule = (columns: MaybeRefOrGetter<DataSource['columns']>) =>
  computed(() => {
    const columnsValue = toValue(columns) // reactive, re-evaluates on change
    return (value: string) => columnsValue.some(...) ? 'exists' : true
  })

// CORRECT: plain argument — value is just passed through at call time
export const useCopyToClipboard = () => {
  return async (rowIds?: string[]) => { // rowIds evaluated at click time
    await copyToClipboard(dataSource, item, rowIds)
  }
}
```

## MaybeRefOrGetter Composables

When a composable argument should work with a plain value, a `ref`, or a getter function, type it as `MaybeRefOrGetter<T>` and unwrap with `toValue()`.

**Naming convention:** `const {name}Value = toValue({name})` — always suffix with `Value`.

```typescript
// composables/tableEditor/file/useColumnNameRule.ts
import type { DataSource } from "#shared/models/tableEditor/file/DataSource";

export const useColumnNameRule = (columns: MaybeRefOrGetter<DataSource["columns"]>, currentName?: string) =>
  computed(() => {
    const columnsValue = toValue(columns);
    return (value: string): string | true => {
      if (value !== currentName && columnsValue.some(({ name }) => name === value)) return "Column already exists";
      return true;
    };
  });
```

**Callers pass a getter to stay reactive to prop changes:**

```typescript
const uniqueNameRule = useColumnNameRule(() => dataSource.columns, column.name); // edit
const uniqueNameRule = useColumnNameRule(() => dataSource.columns); // create
```

**Rules:**

- Don't explicitly annotate composable return types — let TypeScript infer. Only annotate if inference fails or a specific contract must be enforced.
- Vue auto-unwraps computed refs in templates, so `:rules="[uniqueNameRule]"` correctly passes the function value.

## Extract Duplicate Validation Rules

When the same validation rule appears in 2+ components, extract it to a shared composable immediately. Don't copy-paste. The `currentName` optional param handles the "allow own name" case for edit vs create:

```typescript
// WRONG: Duplicate inline rules in EditDialogButton and CreateDialogButton
const uniqueNameRule = (v: string) => v === column.name || !columns.some(...) || 'Column already exists'

// RIGHT: Single composable, optional exclude param covers both edit and create
const uniqueNameRule = useColumnNameRule(() => dataSource.columns, column.name) // edit
const uniqueNameRule = useColumnNameRule(() => dataSource.columns)               // create (no exclude)
```

## Schema-Controlling Selectors in `#prepend-form`

When a dialog has a selector (e.g., column type, chart type) that controls **which Vjsf schema** is rendered, put it in the `#prepend-form` slot — not in the default slot alongside the schema content.

This matches the established pattern in `Dashboard/Visual/Preview/EditFormDialog.vue`:

```vue
<!-- WRONG: type selector mixed into default slot with Vjsf -->
<TableEditorFileEditDialogButton ...>
  <v-select v-model="columnType" label="Type" ... />
  <Vjsf v-model="editedColumn" :schema="jsonSchema" />
</TableEditorFileEditDialogButton>

<!-- RIGHT: type selector in #prepend-form, schema content in default -->
<TableEditorFileEditDialogButton ...>
  <template #prepend-form>
    <v-select v-model="columnType" label="Type" ... />
  </template>
  <v-text-field v-model="editedColumn.name" label="Column" ... />
  <Vjsf v-model="editedColumn" :schema="jsonSchema" />
</TableEditorFileEditDialogButton>
```

The `TableEditorFileEditDialogButton` component exposes a `#prepend-form` slot rendered inside `v-form` before the default slot content.

## Reactive Type-Switching with `watch`

When switching a form object's type (e.g., column type change), preserve unchanged fields (like `name`) and reset type-specific fields to defaults by constructing a new class instance:

```typescript
const columnType = ref(ColumnType.String);
const editedColumn = ref<Column | DateColumn>(new Column());

watch(columnType, (newType) => {
  const name = editedColumn.value.name; // preserve name
  editedColumn.value = newType === ColumnType.Date ? new DateColumn({ name }) : new Column({ name, type: newType });
});
```

Note use of `name` (not `currentName`) to enable object shorthand `{ name }`.

## No `structuredClone` / `toRawDeep` on Freshly Newed Instances

Only call `structuredClone(toRawDeep(...))` on data pulled from Vue reactive stores or refs. Freshly constructed class instances are already plain, non-reactive objects.

```typescript
// WRONG: Unnecessary wrapping
const newRow = new Row({ data: { ... } })
executeAndRecord(new CreateRowCommand(index, structuredClone(toRawDeep(newRow))))

// RIGHT: Just pass the instance directly
const newRow = new Row({ data: { ... } })
executeAndRecord(new CreateRowCommand(index, newRow))

// CORRECT: Clone IS needed for data from reactive stores
const originalRow = structuredClone(toRawDeep(takeOne(editedItem.value.dataSource.rows, index)))
```

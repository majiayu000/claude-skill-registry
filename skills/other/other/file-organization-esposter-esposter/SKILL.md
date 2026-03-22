---
name: file-organization
description: Esposter file and folder organisation — one export per file, no export{} syntax, models vs services vs constants, command pattern field ordering, constant maps with as-const-satisfies, generic Vue components, MIME types, and LF line endings.
---

# File & Folder Organisation

## Imports

- **Always use `@/` alias imports** — never use relative imports (`./`, `../`), even for files in the same folder. Example: `import { ... } from "@/composables/tableEditor/file/useEditedItemDataSourceOperations/testUtils"` not `"./testUtils"`.

## Files and Exports

- **One export per file** — each exported function, class, or interface lives in its own file. Exception: Zod schemas may be co-located with their interface/type since they are tightly coupled.
- **One class per file** — classes belong in a `models/` folder (e.g., `app/models/`, `shared/models/`).
- **Never use `export { }` syntax** — always use `export const`, `export class`, `export interface`, `export type`, or `export function` at the declaration site. The only valid exceptions are empty `export {}` in `.d.ts` files (to mark them as a module) and `ctix`-generated barrel files (pinned package). If you see `export { ... }` in a hand-written `.ts` file, it is wrong — inline the `export` keyword at each declaration instead.
- **Constants go in `constants.ts`** — all module-level constants in a `constants.ts` file under `services/` alongside the files that use them. Never put `constants.ts` inside `composables/`.
- **Functions go in `services/`** — factory functions, command creators, and other exported functions belong in `services/`, not `models/`. `models/` is strictly for classes and interfaces/types.
- **Generic browser utilities** go in `app/utils/` (e.g., `readFileAsText.ts`).
- **Feature folders**: related models/services/components are grouped under a feature subfolder (e.g., `tableEditor/file/`).
- **No magic strings** — always use enums instead of string literals for discriminants, command types, and other categorical values.

## Constant Maps

- **Constant maps and arrays use PascalCase** matching the filename with `as const satisfies` — e.g. `export const DataSourceConfigurationMap = { ... } as const satisfies Record<...>` and `export const ColumnStatDefinitions = [ ... ] as const satisfies readonly ColumnStatDefinition[]`.
  - **Exception**: for generic definition arrays where the `format` (or similar) callback is contravariant over the union of entry types, `satisfies` will fail with a type error. In that case, use `as const` alone and cast at the call site with `as never`. See `.claude/skills/typescript/SKILL.md` — "Generic Definition Arrays".
- **Destructure in `v-for` unless passing the base item as component props** — `v-for="{ key, format } of ColumnStatDefinitions"` is preferred over `v-for="def of ColumnStatDefinitions"` when you only need specific fields. Exception: if the item itself must be passed as a prop to a child component (e.g. `<SomeCard :item="def" />`), keep the variable name undestructured.
- **One constant map per file, named after the constant** — `ColumnTypeFormSchemaMap.ts` exports only `ColumnTypeFormSchemaMap`. Never co-locate multiple maps in one file. When a map is a transformation of another (e.g. omitting a key), derive it directly rather than repeating the source values: `[ColumnType.Boolean]: ColumnTypeFormSchemaMap[ColumnType.Boolean].omit({ name: true })`.
- **Generic type maps for polymorphic dispatch** — when a constant map needs to associate a discriminant key (e.g. `DataSourceType`) with a type-parameterised generic (e.g. `DataSourceConfiguration<TItem>`), define an explicit type map first, then use a mapped type in `satisfies` to get per-entry type safety without any `as` casts:
  ```typescript
  // 1. Explicit type map (one file, in models/)
  type DataSourceItemTypeMap = { [DataSourceType.Csv]: CsvDataSourceItem };
  // 2. Satisfies mapped type — each entry is checked against its specific type param
  export const DataSourceConfigurationMap: Record<
    DataSourceType,
    DataSourceConfiguration<DataSourceItemTypeMap[keyof DataSourceItemTypeMap]>
  > = { ... };
  ```
- **Generic map lookup composables** — when a component needs to look up a typed configuration from a generic map using a discriminant key on a generic item, extract the lookup into a composable. Use `MaybeRefOrGetter<TItem>` with `toValue()` so callers can pass refs or plain values. Hide the single internal `as` cast and expose a fully typed API:
  ```typescript
  export const useDataSourceConfiguration = <
    TDataSourceItem extends DataSourceItemTypeMap[keyof DataSourceItemTypeMap],
  >(
    item: MaybeRefOrGetter<TDataSourceItem>,
  ): ComputedRef<DataSourceConfiguration<TDataSourceItem>> =>
    computed(() => DataSourceConfigurationMap[toValue(item).type] as DataSourceConfiguration<TDataSourceItem>);
  // Caller (no cast needed):
  const dataSourceConfiguration = useDataSourceConfiguration(modelValue);
  ```

## Generic Vue Components

Use `<script setup lang="ts" generic="T extends SomeBase">` to make components type-safe over a specific subtype. Pass the typed value AND its associated generic config/interface as props so the parent resolves the concrete types and the child stays fully typed without lookups or casts:

```vue
<!-- Parent (knows concrete type): -->
<FilePicker :item="modelValue" :configuration="DataSourceConfigurationMap[DataSourceType.Csv]" />
<!-- Child: -->
<script setup lang="ts" generic="TDataSourceItem extends DataSourceItemTypeMap[keyof DataSourceItemTypeMap]">
interface FilePickerProps {
  configuration: DataSourceConfiguration<TDataSourceItem>;
  item: TDataSourceItem;
}
</script>
```

## Command Pattern

Commands are classes extending `ADataSourceCommand<T extends CommandType>`. Each command declares `readonly type = CommandType.X` (no `name` — the base class provides `get name() { return this.type; }`). `CommandType` enum lives in `models/tableEditor/file/commands/CommandType.ts`. Class field ordering within a command: `readonly type` → blank line → `get description()` → blank line → all `private readonly` fields grouped together (no blank lines between same-level fields) → blank line → constructor → blank line between each method.

## MIME Types

Store MIME type strings in the relevant configuration map (e.g. `DataSourceConfigurationMap`) rather than calling `mime-types` `lookup` at runtime — `mime-types` uses Node.js `path.extname` which is not available in the browser. Access `mimeType` through the configuration map at the call site.

## Line Endings

- All files must use **LF** line endings (`\n`), not CRLF.
- The `Write` tool on Windows always produces CRLF. **Immediately after every `Write` call**, convert with:
  ```bash
  sed -i 's/\r//' "path/to/file"
  ```
  For multiple files at once:
  ```bash
  find "path/to/dir" -name "*.md" | xargs -I{} sed -i 's/\r//' "{}"
  ```

## File Length

- **Target 50–100 lines per `.ts` file** — a file over 100 lines is a yellow flag that a helper, sub-service, or model extraction is overdue.
- Each file should have a single clear responsibility. If a file grows because it handles multiple concerns, split it.
- Exceptions: generated files, large constant maps with many entries, and files where co-location of tightly coupled logic (e.g. a Zod schema next to its interface) is intentional.

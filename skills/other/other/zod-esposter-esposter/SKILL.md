---
name: zod
description: Esposter Zod schema conventions — z namespace imports, no optional+default combos, generic schemas with create* functions, vjsf form schemas, and satisfies with ToData for class types. Apply when writing Zod schemas.
---

# Zod Conventions

## Imports

Always use the `z` namespace export: `z.ZodType`, `z.ZodError`, etc. Never use named imports like `import type { ZodType }`.

## Schema Rules

- **`.default()`** — do not combine `.optional().default(value)`; `.default()` already handles `undefined` input, so `.optional()` is redundant.
- **Generic schemas** — when an abstract class has a generic type parameter (e.g. `ADataSourceItem<TType, TConfig>`), its schema must also be generic. Export a `create*Schema` function that takes typed zod schemas as parameters and returns the composed schema. Never hardcode type-specific values in a base schema. Use `T` for a single type parameter, descriptive `T*` names (e.g. `TType`, `TConfiguration`) for multiple:
  ```typescript
  // WRONG — hardcodes type, missing configuration
  export const aDataSourceItemSchema = z.object({ ...base.shape, type: dataSourceTypeSchema });
  // CORRECT — generic function, concrete schemas passed by callers
  export const createDataSourceItemSchema = <
    TType extends z.ZodType<keyof DataSourceConfigurationTypeMap>,
    TConfiguration extends z.ZodType<object>,
  >(
    typeSchema: TType,
    configurationSchema: TConfiguration,
  ) => z.object({ ...aTableEditorItemEntitySchema.shape, configuration: configurationSchema, type: typeSchema });
  // Caller:
  export const csvDataSourceItemSchema = createDataSourceItemSchema(
    z.literal(DataSourceType.Csv),
    csvDataSourceConfigurationSchema,
  ) satisfies z.ZodType<ToData<CsvDataSourceItem>>;
  ```
  For the union schema used by parent models, create a separate `*ItemSchema.ts` file using `z.discriminatedUnion`:
  ```typescript
  export const dataSourceItemSchema = z.discriminatedUnion("type", [csvDataSourceItemSchema]);
  ```
  Adding a new type = add its schema to the discriminated union array.
- **vjsf form schemas** — never pass a full entity schema to `zodToJsonSchema()` if it contains `z.date()` fields — vjsf will throw. Create a separate `*FormSchema` co-located in the same file using `.pick().extend()` to add `.meta()` titles. The form schema picks only user-editable fields (no entity metadata like `id`, `createdAt`, `updatedAt`).
- **`satisfies z.ZodType<T>` with class types** — when a schema output has plain objects but the interface uses class instances (with `toJSON`), use `Except` + `ToData` in the satisfies to strip `toJSON` from nested classes:
  ```typescript
  export const dataSourceSchema = z.object({...})
    satisfies z.ZodType<Except<DataSource, "columns"> & { columns: ToData<Column>[] }>;
  ```

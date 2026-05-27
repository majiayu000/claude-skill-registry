---
name: dbc-schema
description: Generate Effect Schema definitions for WoW DBC tables. Use when adding new game data tables or updating existing schemas.
---

# DBC Schema Generator

Generate Effect Schema definitions for WoW database tables.

## Schema Location

`packages/wowlab-core/src/internal/schemas/dbc/`

## Schema Template

```ts
// {TableName}Schema.ts
import * as Schema from "effect/Schema";

export class {TableName} extends Schema.Class<{TableName}>("{TableName}")({
  ID: Schema.Number,
  // Other fields - preserve CSV column order!
  Name: Schema.String,
  Description: Schema.String,
  Flags: Schema.Number,
  // ...
}) {}

export const {TableName}Schema = Schema.Array({TableName});
```

## Important Rules

1. **Preserve CSV column order** - perfectionist sorting is disabled for DBC schemas
2. **Use Schema primitives** - `Schema.Number`, `Schema.String`, `Schema.Boolean`
3. **Nullable fields** - Use `Schema.NullOr(Schema.Number)` for optional numeric fields
4. **Arrays** - Use `Schema.Array(Schema.Number)` for array columns

## Column Type Mapping

| CSV Type         | Effect Schema                                   |
| ---------------- | ----------------------------------------------- |
| int              | `Schema.Number`                                 |
| float            | `Schema.Number`                                 |
| string           | `Schema.String`                                 |
| localized string | `Schema.String`                                 |
| bool             | `Schema.Boolean`                                |
| foreign key      | `Schema.Number` (reference to another table ID) |

## Registration

After creating schema, register in `DbcTableRegistry.ts`:

```ts
import { {TableName} } from "./internal/schemas/dbc/{TableName}Schema.js";

// Add to registry type
export type DbcTableName =
  | "Spell"
  | "{TableName}"  // Add here
  | ...;

// Add to row type mapping
export type DbcRow<T extends DbcTableName> =
  T extends "{TableName}" ? {TableName} :
  ...;
```

## Instructions

1. Get CSV headers from DBC table
2. Map columns to Schema types
3. Generate schema class (preserve column order!)
4. Register in DbcTableRegistry
5. Re-export from Schemas.ts if public API

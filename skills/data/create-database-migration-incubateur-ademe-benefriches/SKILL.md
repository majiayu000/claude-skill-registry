---
name: create-database-migration
description: Create Knex database migrations for the Benefriches API. Use when adding, modifying, or removing database columns/tables. Handles schema changes (create table, add/drop/rename columns), data migrations, and updates to tableTypes.d.ts.
---

# Create Database Migration

Generate timestamped Knex migrations following project conventions.

## Quick Start

1. Create migration: `pnpm --filter api knex:new-migration {description}`
   - Example: `pnpm --filter api knex:new-migration add-column-email-to-users-table`
   - Creates timestamped file in `apps/api/src/shared-kernel/adapters/sql-knex/migrations/`
2. Implement `up()` and `down()` functions in the generated file
3. Update `apps/api/src/shared-kernel/adapters/sql-knex/tableTypes.d.ts` if schema changes
4. Run: `pnpm --filter api knex:migrate-latest`

## File Naming

Format: `{YYYYMMDDHHmmss}_{verb}-{description}.ts`

| Operation | Pattern | Example |
|-----------|---------|---------|
| Create table | `create-table-{name}` | `20250211105813_create-table-users-features-alerts.ts` |
| Add column | `add-column-{name}-to-{table}` or `add-{name}-to-{table}` | `20250915091313_add_newsletter_subscription_to_users_table.ts` |
| Drop column | `drop-{column}-from-{table}` | `20250613111514_drop-is_friche-column-from-sites-table.ts` |
| Rename column | `rename-{old}-to-{new}-in-{table}` | `20250729160857_rename-insee-to-city_code-in-cities-table.ts` |
| Update data | `update-{description}` | `20250225095318_update-friche-activity-values-in-sites-table.ts` |

Use kebab-case OR snake_case consistently within a single filename.

## Migration Templates

### Create Table

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  await knex.schema.createTable("table_name", (table) => {
    table.uuid("id").primary();
    table.string("name").notNullable();
    table.uuid("related_id").references("id").inTable("other_table");
    table.timestamp("created_at").notNullable();
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.dropTableIfExists("table_name");
}
```

### Add Column

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.string("column_name");  // nullable by default
    // OR: table.boolean("flag").defaultTo(false);
    // OR: table.string("required_col").notNullable();
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.dropColumn("column_name");
  });
}
```

### Drop Column

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.dropColumn("column_name");
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.string("column_name").nullable();
  });
  // Optionally restore data if recoverable
}
```

### Rename Column

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.renameColumn("old_name", "new_name");
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.table("table_name", (table) => {
    table.renameColumn("new_name", "old_name");
  });
}
```

### Data Migration

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  await knex("table_name")
    .whereIn("column", ["old_value1", "old_value2"])
    .update({ column: "new_value" });
}

export async function down(knex: Knex): Promise<void> {
  await knex("table_name")
    .where("column", "new_value")
    .update({ column: "old_value1" });  // Best effort
}
```

### Complex Data Migration (JSON columns)

```typescript
import type { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  const rows = await knex("table_name")
    .select("id", "json_column")
    .whereRaw(`json_column::json->>'field' IS NOT NULL`);

  for (const row of rows) {
    const data = row.json_column as Record<string, unknown>;
    const updated = { ...data, newField: transformValue(data.oldField) };
    delete (updated as Record<string, unknown>).oldField;

    await knex("table_name").update({ json_column: updated }).where({ id: row.id });
  }
}

export async function down(): void {
  return;  // Data migration not reversible
}
```

## Column Types Reference

| Knex Method | PostgreSQL | TypeScript |
|-------------|------------|------------|
| `table.uuid("id")` | UUID | `string` |
| `table.string("name")` | VARCHAR(255) | `string` |
| `table.text("desc")` | TEXT | `string` |
| `table.boolean("flag")` | BOOLEAN | `boolean` |
| `table.integer("count")` | INTEGER | `number` |
| `table.float("amount")` | REAL | `number` |
| `table.timestamp("at")` | TIMESTAMP | `Date` |
| `table.json("data")` | JSON | `Record<string, unknown>` |

## tableTypes.d.ts Updates

After schema changes, update `apps/api/src/shared-kernel/adapters/sql-knex/tableTypes.d.ts`:

```typescript
// Add new type for new table
type SqlNewTable = {
  id: string;
  name: string;
  created_at: Date;
  optional_col: string | null;  // nullable columns use | null
};

// Register in Tables interface
declare module "knex/types/tables" {
  interface Tables {
    new_table: SqlNewTable;  // table_name: SqlType
  }
}
```

**Rules:**
- Use `snake_case` for column names (matches DB)
- Use `| null` for nullable columns (not `?:`)
- Use `Date` for timestamps (Knex converts)
- Register table in `Tables` interface

## Checklist

1. [ ] Migration created with `pnpm --filter api knex:new-migration {description}`
2. [ ] `up()` implements forward migration
3. [ ] `down()` reverses migration (or returns void if not possible)
4. [ ] `tableTypes.d.ts` updated for schema changes
5. [ ] Migration tested: `pnpm --filter api knex:migrate-latest`
6. [ ] Rollback tested: `pnpm --filter api knex:migrate-rollback`

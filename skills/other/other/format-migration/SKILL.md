---
name: format-migration
description: Format TypeORM migrations with beautifully formatted SQL code. Use this skill after generating migrations to ensure consistent SQL formatting.
---

# TypeORM Migration Formatter

You are an expert in TypeORM and PostgreSQL 18. You will format TypeORM migrations to be beautifully formatted SQL code.

## Formatting Rules

### 1. Always Provide Full Migration Code

Present the entire `MigrationInterface` class, not just snippets. This helps maintain context and prevents errors.

### 2. Explicitly State Changes

Clearly mention any new columns, constraints, indexes, or other SQL features you're adding or modifying.

### 3. SQL Formatting Style

All SQL within `queryRunner.query()` must be multi-line, wrapped in `/* sql */\` \`` blocks, with `/* sql */` on the same line as `await queryRunner.query`:

```typescript
await queryRunner.query(/* sql */ `
  CREATE TABLE "example" (
    "id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    "name" text NOT NULL
  )
`);
```

### 4. ALTER TABLE Formatting

Use consistent indentation for `ALTER TABLE` clauses:

```typescript
await queryRunner.query(/* sql */ `
  ALTER TABLE "table_name"
    ALTER COLUMN "column_name" SET DEFAULT 'value'
`);
```

### 5. Foreign Key Constraints in CREATE TABLE

Split across multiple lines:

```typescript
await queryRunner.query(/* sql */ `
  CREATE TABLE "example" (
    "id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    "otherId" uuid NOT NULL,
    CONSTRAINT "FK_example_other"
      FOREIGN KEY ("otherId")
      REFERENCES "other_table"("id")
      ON DELETE CASCADE
      ON UPDATE NO ACTION
  )
`);
```

### 6. Index Handling

- `CREATE INDEX` in `up` should always include `IF NOT EXISTS`
- `DROP INDEX` in `down` should always include `IF EXISTS`

```typescript
// up
await queryRunner.query(/* sql */ `
  CREATE INDEX IF NOT EXISTS "IDX_example_column"
    ON "example" ("column")
`);

// down
await queryRunner.query(/* sql */ `
  DROP INDEX IF EXISTS "IDX_example_column"
`);
```

### 7. Atomic CREATE TABLE

Define all possible constraints (Primary Key, Unique, Foreign Key) directly within the `CREATE TABLE` statement itself. Do not use `ALTER TABLE ADD CONSTRAINT` for foreign keys that can be defined inline during `CREATE TABLE`.

### 8. Concise down Migrations

- When constraints (PK, FK) are defined within `CREATE TABLE`, they will be implicitly dropped with the table. Do not include explicit `DROP CONSTRAINT` for them in `down`.
- Indexes created on the same table are also implicitly dropped when the table is dropped. Do not include explicit `DROP INDEX` in `down` for table-bound indexes.
- If an index is created on a column that is subsequently dropped, that index is implicitly dropped with the column.
- The `down` migration for a `CREATE TABLE` should typically just be `DROP TABLE`.
- If you're dropping and re-adding columns, ensure corresponding `COMMENT ON COLUMN ... IS NULL` is in `down` if a comment was added in `up`.

### 9. Single Query Per Statement

Each `queryRunner.query()` call should only execute a single SQL query.

### 10. No Comments

You will not add any comments to the code. Any existing comments will be left there.

## Example Migration

```typescript
import type { MigrationInterface, QueryRunner } from 'typeorm';

export class CreateUserProfile1234567890123 implements MigrationInterface {
  name = 'CreateUserProfile1234567890123';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(/* sql */ `
      CREATE TABLE "user_profile" (
        "id" uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
        "userId" text NOT NULL,
        "bio" text,
        "avatarUrl" text,
        "createdAt" timestamp NOT NULL DEFAULT now(),
        "updatedAt" timestamp NOT NULL DEFAULT now(),
        CONSTRAINT "FK_user_profile_user"
          FOREIGN KEY ("userId")
          REFERENCES "user"("id")
          ON DELETE CASCADE
          ON UPDATE NO ACTION
      )
    `);

    await queryRunner.query(/* sql */ `
      CREATE INDEX IF NOT EXISTS "IDX_user_profile_userId"
        ON "user_profile" ("userId")
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(/* sql */ `
      DROP TABLE "user_profile"
    `);
  }
}
```

## Best Practice Suggestions

When reviewing migrations, point out opportunities to improve:
- Generic PK names (e.g., `PK_tablename` instead of auto-generated names)
- Nullable foreign keys where appropriate
- Missing indexes on frequently queried columns
- Proper use of `ON DELETE` behavior

## Instructions

When the user asks you to format a migration:

1. Read the migration file
2. Apply all formatting rules above
3. Present the complete formatted migration
4. If there are best practice improvements, mention them as suggestions
5. Keep replies short unless explanations are needed

When migrations are generated via `pnpm run db:migrate:make`:

1. The auto-lint hook will run ESLint
2. Use this skill to format the SQL for readability
3. Review for schema drift (unrelated changes from local DB differences)

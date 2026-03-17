---
name: add-database-table
description: Create database migrations, define table schemas, and manage constant tables (enums). Use when: (1) creating a new database table, (2) running 'make migrate.create', (3) adding enum/status values, (4) modifying table structure. REQUIRED first step before add-domain-entity.
---

# Add Database Table

Create database migrations and constant tables for new entities.

## Quick Start

```bash
# 1. Create migration file
make migrate.create

# 2. Edit the generated SQL file in db/{database}/migrations/

# 3. Run migration and generate SQLBoiler models
make migrate.up
```

## Overview

```
add-database-table ──> add-domain-entity ──> add-api-endpoint
       ^
   YOU ARE HERE
```

This skill is **Step 1** of the CRUD implementation workflow.

## Workflow

### Step 1: Create Migration File

Run the migration creation command:

```bash
make migrate.create
```

Enter a descriptive name when prompted (e.g., `create_examples_table`).

A new file is created at: `db/postgresql/migrations/{timestamp}_{name}.sql`

### Step 2: Define Constant Tables (if needed)

If the entity has status/enum fields, create the constant table **first**.

**Migration SQL:**

```sql
-- +goose Up
CREATE TABLE "example_statuses" (
    "id" VARCHAR(64) PRIMARY KEY
);

-- +goose Down
DROP TABLE IF EXISTS "example_statuses";
```

**YAML Definition** in `db/postgresql/constants/constants.yaml`:

```yaml
- table: example_statuses
  values:
    - draft
    - published
    - archived
```

### Step 3: Write Main Table Migration

Use the template below, adapting field names and types:

```sql
-- +goose Up
CREATE TABLE "examples" (
    "id"            VARCHAR(64)     PRIMARY KEY,
    "tenant_id"     VARCHAR(64)     NOT NULL,
    "name"          VARCHAR(256)    NOT NULL,
    "description"   TEXT            NOT NULL,
    "status"        VARCHAR(64)     NOT NULL,
    "created_at"    TIMESTAMPTZ     NOT NULL,
    "updated_at"    TIMESTAMPTZ     NOT NULL,

    CONSTRAINT "examples_fkey_tenant_id"
        FOREIGN KEY ("tenant_id") REFERENCES "tenants" ("id"),
    CONSTRAINT "examples_fkey_status"
        FOREIGN KEY ("status") REFERENCES "example_statuses" ("id")
);

CREATE INDEX "examples_idx_tenant_id" ON "examples" ("tenant_id");
CREATE INDEX "examples_idx_status" ON "examples" ("status");
CREATE INDEX "examples_idx_created_at" ON "examples" ("created_at" DESC);

-- +goose Down
DROP TABLE IF EXISTS "examples";
```

See [references/sql-patterns.md](references/sql-patterns.md) for advanced patterns.

### Step 4: Run Migration

```bash
make migrate.up
```

This command:
- Executes pending migrations
- Syncs constant table values from YAML
- Generates SQLBoiler models in `internal/infrastructure/{database}/internal/dbmodel/`

### Step 5: Verify

Confirm the SQLBoiler model was generated:

```
internal/infrastructure/postgresql/internal/dbmodel/examples.go
```

## Quick Reference

### Column Types

| Go Type | PostgreSQL | Notes |
|---------|------------|-------|
| `string` (ID) | `VARCHAR(64)` | Primary/foreign keys |
| `string` (short) | `VARCHAR(256)` | Names, titles |
| `string` (long) | `TEXT` | Descriptions |
| `int` | `INTEGER` | Counts, order |
| `bool` | `BOOLEAN` | Flags |
| `time.Time` | `TIMESTAMPTZ` | Always with timezone |
| `null.Time` | `TIMESTAMPTZ` | Nullable timestamps |
| `map/struct` | `JSONB` | Flexible data |

See [references/type-mappings.md](references/type-mappings.md) for complete mappings.

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Foreign Key | `{table}_fkey_{column}` | `examples_fkey_tenant_id` |
| Index | `{table}_idx_{column}` | `examples_idx_tenant_id` |
| Unique | `{table}_uq_{columns}` | `examples_uq_tenant_id_name` |
| Unique Index | `{table}_uidx_{column}` | `examples_uidx_email` |

## Checklist

- [ ] Migration file created with Up and Down sections
- [ ] Constant table created (if entity has status/enum)
- [ ] YAML constants defined in `db/postgresql/constants/constants.yaml`
- [ ] Foreign key constraints added
- [ ] Indexes created for foreign keys and common queries
- [ ] `make migrate.up` executed successfully
- [ ] SQLBoiler model generated in `dbmodel/`

## Next Step

Proceed to **add-domain-entity** skill to create:
- Domain model (`internal/domain/model/`)
- Repository interface (`internal/domain/repository/`)
- Repository implementation
- Marshaller

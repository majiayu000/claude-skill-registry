---
name: migrating-sql-to-dbt
description: |
  Converts legacy SQL to modular dbt models. Use when migrating SQL to dbt for:
  (1) Converting stored procedures, views, or raw SQL files to dbt models
  (2) Task mentions "migrate", "convert", "legacy SQL", "transform to dbt", or "modernize"
  (3) Breaking monolithic queries into modular layers (discovers project conventions first)
  (4) Porting existing data pipelines or ETL to dbt patterns
  Checks for existing models/sources, builds and validates layer by layer.
---

# dbt Migration

**Don't convert everything at once. Build and validate layer by layer.**

## Workflow

### 1. Analyze Legacy SQL

```bash
cat <legacy_sql_file>
```

Identify all tables referenced in the query.

### 2. Check What Already Exists

```bash
# Search for existing models/sources that reference the table
grep -r "<table_name>" models/ --include="*.sql" --include="*.yml"
find models/ -name "*.sql" | xargs grep -l "<table_name>"
```

For each table referenced in the legacy SQL:
1. Check if an existing model already references this table
2. Check if a source definition exists
3. If neither exists, ask user: "Table X not found - should I create it as a source?"

Only proceed to intermediate/mart layers after all dependencies exist.

### 3. Create Missing Sources

```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw_database
    schema: raw_schema
    tables:
      - name: orders
        description: Raw orders from source system
      - name: customers
        description: Raw customer records
```

### 4. Build Staging Layer

One staging model per source table. Follow existing project naming conventions.

**Build before proceeding:**
```bash
dbt build --select <staging_model>
```

### 5. Build Intermediate Layer (if needed)

Extract complex joins/logic into intermediate models.

**Build incrementally:**
```bash
dbt build --select <intermediate_model>
```

### 6. Build Mart Layer

Final business-facing model with aggregations.

### 7. Validate Migration

```bash
# Build entire lineage
dbt build --select +<final_model>
dbt show --select <final_model>
```

## Migration Checklist

- [ ] All source tables identified and documented
- [ ] Sources.yml created with descriptions
- [ ] Staging models: 1:1 with sources, renamed columns
- [ ] Intermediate models: business logic extracted
- [ ] Mart models: final aggregations
- [ ] Each layer compiles successfully
- [ ] Each layer builds successfully
- [ ] Row counts match original (manual validation)
- [ ] Tests added for key constraints

## Common Migration Patterns

- Nested subqueries → Separate models (staging → intermediate → mart)
- Temp tables → Ephemeral materialization `{{ config(materialized='ephemeral') }}`
- Hardcoded values → Variables `{{ var("name") }}`

## Anti-Patterns

- Converting entire legacy query to single dbt model
- Skipping the staging layer
- Not validating each layer before proceeding
- Keeping hardcoded values instead of using variables
- Not documenting business logic during migration


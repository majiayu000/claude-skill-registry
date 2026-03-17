---
name: dbt-migration-postgres
description:
  Convert PostgreSQL/Greenplum/Netezza DDL to dbt models compatible with Snowflake. This skill
  should be used when converting views, tables, or stored procedures from PostgreSQL, Greenplum, or
  Netezza to dbt code, generating schema.yml files with tests and documentation, or migrating
  PostgreSQL SQL to follow dbt best practices.
---

# PostgreSQL/Greenplum/Netezza to dbt Model Conversion

## Purpose

Transform PostgreSQL/Greenplum/Netezza DDL (views, tables, stored procedures) into
production-quality dbt models compatible with Snowflake, maintaining the same business logic and
data transformation steps while following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting PostgreSQL/Greenplum/Netezza views or tables to dbt models
- Migrating PostgreSQL stored procedures to dbt
- Translating PostgreSQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling PostgreSQL-specific syntax conversions (array expressions, CHAR padding, psql commands)

---

## Task Description

You are a database engineer working for a hospital system. You need to convert
PostgreSQL/Greenplum/Netezza DDL to equivalent dbt code compatible with Snowflake, maintaining the
same business logic and data transformation steps while following dbt best practices.

## Input Requirements

I will provide you the PostgreSQL DDL to convert.

## Audience

The code will be executed by data engineers who are learning Snowflake and dbt.

## Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions
5. Inline comments highlighting any syntax that was converted

## Conversion Guidelines

### General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests
- Use Snowflake SQL functions rather than macros whenever possible

### Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original Object: [database].[schema].[object_name]
   Source Platform: PostgreSQL/Greenplum/Netezza
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        -- SERIAL converted to INTEGER (use IDENTITY in table)
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        account_balance::NUMBER(18,2) AS account_balance,
        -- TIMESTAMPTZ converted to TIMESTAMP_TZ
        created_date::TIMESTAMP_TZ AS created_date
    FROM {{ ref('upstream_model') }}
),

transformed_data AS (
    SELECT
        customer_id,
        UPPER(customer_name)::VARCHAR(100) AS customer_name_upper,
        account_balance,
        created_date,
        CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS loaded_at
    FROM source_data
)

SELECT
    customer_id,
    customer_name_upper,
    account_balance,
    created_date,
    loaded_at
FROM transformed_data
```

```yaml
## models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from PostgreSQL [Original object name]"
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier"
        tests:
          - unique
          - not_null
      - name: customer_name_upper
        description: "Customer name in uppercase"
      - name: account_balance
        description: "Current account balance; Foreign key to OTHER_TABLE"
        tests:
          - relationships:
              to: ref('OTHER_TABLE')
              field: OTHER_TABLE_KEY
      - name: created_date
        description: "Date the customer record was created"
      - name: loaded_at
        description: "Timestamp when the record was loaded by dbt"
```

```yaml
## dbt_project.yml (excerpt)
models:
  my_project:
    +materialized: view
    domain_name:
      +schema: target_schema_name
```

### Specific Translation Rules

#### dbt Specific Requirements

- If the source is a view, use a view materialization in dbt
- Include appropriate dbt model configuration (materialization type)
- Add documentation blocks for a schema.yml
- Add descriptions for tables and columns
- Include relevant tests
- Define primary keys and relationships
- Assume that upstream objects are models
- Comprehensively provide all the columns in the output
- Break complex procedures into multiple models if needed
- Implement appropriate incremental strategies for large tables
- Use Snowflake SQL functions rather than macros whenever possible
- **Always cast columns with explicit precision/scale** using `::TYPE` syntax (e.g.,
  `column_name::VARCHAR(100)`, `amount::NUMBER(18,2)`) to ensure output matches expected data types
- **Always provide explicit column aliases** for clarity and documentation

#### Performance Optimization

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

#### PostgreSQL to Snowflake Syntax Conversion

- Convert array expressions (<> ALL, = ANY) to Snowflake equivalents
- Handle CHAR padding differences
- Replace psql commands with SnowSQL equivalents
- Convert distribution keys (Greenplum) to clustering keys
- Handle string comparison behavior differences
- Convert PL/pgSQL to Snowflake Scripting
- Replace PostgreSQL-specific operators
- Handle SERIAL/BIGSERIAL with IDENTITY

#### Key Data Type Mappings

| PostgreSQL              | Snowflake              | Notes                   |
| ----------------------- | ---------------------- | ----------------------- |
| INTEGER/INT/INT4        | INTEGER                |                         |
| BIGINT/INT8             | BIGINT                 |                         |
| SMALLINT/INT2           | SMALLINT               |                         |
| SERIAL/BIGSERIAL        | IDENTITY               | Use AUTOINCREMENT       |
| NUMERIC/DECIMAL         | NUMERIC                |                         |
| REAL/FLOAT4             | FLOAT                  |                         |
| DOUBLE PRECISION/FLOAT8 | FLOAT                  |                         |
| BOOLEAN/BOOL            | BOOLEAN                |                         |
| CHAR/VARCHAR/TEXT       | Same                   |                         |
| BYTEA                   | BINARY                 |                         |
| DATE                    | DATE                   |                         |
| TIME/TIMETZ             | TIME                   | Time zone not supported |
| TIMESTAMP/TIMESTAMPTZ   | TIMESTAMP/TIMESTAMP_TZ |                         |
| INTERVAL                | VARCHAR                |                         |
| JSON/JSONB              | VARIANT                |                         |
| ARRAY                   | ARRAY                  |                         |
| UUID                    | VARCHAR                |                         |

#### Key Syntax Conversions

```sql
-- SERIAL -> AUTOINCREMENT
id SERIAL PRIMARY KEY -> id INT AUTOINCREMENT PRIMARY KEY

-- Array expressions
col <> ALL(ARRAY[1,2,3]) -> NOT ARRAY_CONTAINS(col, ARRAY_CONSTRUCT(1,2,3))
col = ANY(ARRAY[1,2,3]) -> ARRAY_CONTAINS(col, ARRAY_CONSTRUCT(1,2,3))

-- psql commands -> SnowSQL
\d table -> DESCRIBE TABLE table
\dt -> SHOW TABLES

-- generate_series -> TABLE(GENERATOR())
generate_series(1, 10) -> TABLE(GENERATOR(ROWCOUNT => 10))

-- NOW() -> CURRENT_TIMESTAMP
NOW() -> CURRENT_TIMESTAMP()
```

#### Common Function Mappings

| PostgreSQL                 | Snowflake                             | Notes           |
| -------------------------- | ------------------------------------- | --------------- |
| `COALESCE(...)`            | `COALESCE(...)`                       | Same            |
| `NULLIF(a, b)`             | `NULLIF(a, b)`                        | Same            |
| `NOW()`                    | `CURRENT_TIMESTAMP()`                 |                 |
| `CURRENT_DATE`             | `CURRENT_DATE()`                      | Add parentheses |
| `CURRENT_TIMESTAMP`        | `CURRENT_TIMESTAMP()`                 | Add parentheses |
| `DATE_TRUNC(unit, d)`      | `DATE_TRUNC(unit, d)`                 | Same            |
| `EXTRACT(part FROM d)`     | `EXTRACT(part FROM d)`                | Same            |
| `TO_CHAR(d, fmt)`          | `TO_CHAR(d, fmt)`                     | Same            |
| `TO_DATE(s, fmt)`          | `TO_DATE(s, fmt)`                     | Same            |
| `TO_NUMBER(s, fmt)`        | `TO_NUMBER(s, fmt)`                   | Same            |
| `generate_series(a, b)`    | `TABLE(GENERATOR(ROWCOUNT => b-a+1))` |                 |
| `array_agg(col)`           | `ARRAY_AGG(col)`                      | Same            |
| `string_agg(col, delim)`   | `LISTAGG(col, delim)`                 |                 |
| `SUBSTR(s, pos, len)`      | `SUBSTR(s, pos, len)`                 | Same            |
| `POSITION(s IN str)`       | `POSITION(s IN str)`                  | Same            |
| `REGEXP_REPLACE(...)`      | `REGEXP_REPLACE(...)`                 | Same            |
| `json_extract_path_text()` | `JSON_EXTRACT_PATH_TEXT()`            | Same            |
| `::type` cast              | `::type` cast                         | Same            |

#### Dependencies

- List any upstream dependencies
- Suggest model organization in dbt project

---

## Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] PostgreSQL-specific syntax converted (array expressions, CHAR padding, distribution keys)
- [] All business logic preserved
- [] All columns included in output
- [] Data types correctly mapped
- [] Functions translated to Snowflake equivalents
- [] Materialization strategy selected
- [] Tests added
- [] SQL logic description complete
- [] Table descriptions added
- [] Column descriptions added
- [] Dependencies correctly mapped
- [] Incremental logic (if applicable) verified
- [] Inline comments added for converted syntax

---

## Related Skills

- $dbt-migration - For the complete migration workflow (discovery, planning, placeholder models,
  testing, deployment)
- $dbt-modeling - For CTE patterns and SQL structure guidance
- $dbt-testing - For implementing comprehensive dbt tests
- $dbt-architecture - For project organization and folder structure
- $dbt-materializations - For choosing materialization strategies (view, table, incremental,
  snapshots)
- $dbt-performance - For clustering keys, warehouse sizing, and query optimization
- $dbt-commands - For running dbt commands and model selection syntax
- $dbt-core - For dbt installation, configuration, and package management
- $snowflake-cli - For executing SQL and managing Snowflake objects

---

## Supported Source Database

| Database                             | Key Considerations                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------------------------- |
| **PostgreSQL / Greenplum / Netezza** | Array expressions (<> ALL, = ANY), CHAR padding differences, psql commands, distribution keys |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

- [Data Types Netezza Data Types](translation-references/postgres-data-types-netezza-data-types.md)
- [Data Types Postgresql Data Types](translation-references/postgres-data-types-postgresql-data-types.md)
- [Ddls Create Materialized View Greenplum Create Materialized View](translation-references/postgres-ddls-create-materialized-view-greenplum-create-materialized-view.md)
- [Ddls Create Materialized View Postgresql Create Materialized View](translation-references/postgres-ddls-create-materialized-view-postgresql-create-materialized-view.md)
- [Ddls Create Table Greenplum Create Table](translation-references/postgres-ddls-create-table-greenplum-create-table.md)
- [Ddls Create Table Netezza Create Table](translation-references/postgres-ddls-create-table-netezza-create-table.md)
- [Ddls Create Table Postgresql Create Table](translation-references/postgres-ddls-create-table-postgresql-create-table.md)
- [Ddls Postgresql Create View](translation-references/postgres-ddls-postgresql-create-view.md)
- [ETL BI Repointing Power BI Postgres Repointing](translation-references/postgres-etl-bi-repointing-power-bi-postgres-repointing.md)
- [Overview (README)](translation-references/postgres-readme.md)
- [Subqueries](translation-references/postgres-subqueries.md)
- [Built In Functions](translation-references/postgresql-built-in-functions.md)
- [Expressions](translation-references/postgresql-expressions.md)
- [Interactive Terminal](translation-references/postgresql-interactive-terminal.md)
- [String Comparison](translation-references/postgresql-string-comparison.md)

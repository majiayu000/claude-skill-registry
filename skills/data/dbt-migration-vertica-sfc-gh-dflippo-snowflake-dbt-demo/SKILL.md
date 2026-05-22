---
name: dbt-migration-vertica
description:
  Convert Vertica DDL to dbt models compatible with Snowflake. This skill should be used when
  converting views, tables, or stored procedures from Vertica to dbt code, generating schema.yml
  files with tests and documentation, or migrating Vertica SQL to follow dbt best practices.
---

# Vertica to dbt Model Conversion

## Purpose

Transform Vertica DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Vertica views or tables to dbt models
- Migrating Vertica stored procedures to dbt
- Translating Vertica SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Vertica-specific syntax (projections, flex tables, ANY/ALL predicates)

---

# Task Description

You are a database engineer working for a hospital system. You need to convert Vertica DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

# Input Requirements

I will provide you the Vertica DDL to convert.

# Audience

The code will be executed by data engineers who are learning Snowflake and dbt.

# Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions
5. Inline comments highlighting any syntax that was converted

# Conversion Guidelines

## General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests
- Use Snowflake SQL functions rather than macros whenever possible

## Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original Object: [schema].[object_name]
   Source Platform: Vertica
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
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
# models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from Vertica [Original object name]"
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
# dbt_project.yml (excerpt)
models:
  my_project:
    +materialized: view
    domain_name:
      +schema: target_schema_name
```

## Specific Translation Rules

### dbt Specific Requirements:

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

### Performance Optimization:

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

### Vertica to Snowflake Syntax Conversion:

- Remove projection specifications
- Handle flex table conversions
- Convert case sensitivity with quoted identifiers
- Replace ANY/ALL array predicates with Snowflake equivalents
- Convert Vertica-specific functions
- Handle COPY syntax differences
- Remove SEGMENTED BY clauses

### Key Data Type Mappings

| Vertica                             | Snowflake              | Notes |
| ----------------------------------- | ---------------------- | ----- |
| INT/INTEGER/BIGINT/SMALLINT/TINYINT | Same                   |       |
| NUMERIC/DECIMAL                     | Same                   |       |
| FLOAT/REAL/DOUBLE PRECISION         | FLOAT                  |       |
| CHAR/VARCHAR                        | Same                   |       |
| LONG VARCHAR                        | VARCHAR                |       |
| BINARY/VARBINARY/LONG VARBINARY     | BINARY                 |       |
| BOOLEAN                             | BOOLEAN                |       |
| DATE                                | DATE                   |       |
| TIME/TIMETZ                         | TIME                   |       |
| TIMESTAMP/TIMESTAMPTZ               | TIMESTAMP/TIMESTAMP_TZ |       |
| INTERVAL                            | VARCHAR                |       |
| UUID                                | VARCHAR                |       |

### Key Syntax Conversions

```sql
-- Projections -> Remove (Snowflake auto-manages)
CREATE PROJECTION proj AS SELECT ... -> (remove entirely)

-- SEGMENTED BY -> CLUSTER BY
CREATE TABLE t (...) SEGMENTED BY HASH(id) ->
CREATE TABLE t (...) CLUSTER BY (id)

-- Flex tables -> VARIANT columns
CREATE FLEX TABLE t() -> CREATE TABLE t (data VARIANT)

-- Case sensitivity (Vertica folds to lowercase)
SELECT Col -> SELECT "Col"  -- if case matters

-- ANY/ALL array predicates
col = ANY(ARRAY[1,2,3]) -> col IN (1,2,3)
col <> ALL(ARRAY[1,2,3]) -> col NOT IN (1,2,3)
```

### Common Function Mappings

| Vertica                  | Snowflake                  | Notes |
| ------------------------ | -------------------------- | ----- |
| `NVL(a, b)`              | `NVL(a, b)`                | Same  |
| `NVL2(a, b, c)`          | `IFF(a IS NOT NULL, b, c)` |       |
| `COALESCE(...)`          | `COALESCE(...)`            | Same  |
| `NULLIF(a, b)`           | `NULLIF(a, b)`             | Same  |
| `DECODE(expr, ...)`      | `CASE expr WHEN ... END`   |       |
| `GETDATE()`              | `CURRENT_TIMESTAMP()`      |       |
| `SYSDATE`                | `CURRENT_TIMESTAMP()`      |       |
| `ADD_MONTHS(d, n)`       | `DATEADD('month', n, d)`   |       |
| `DATEDIFF(unit, d1, d2)` | `DATEDIFF(unit, d1, d2)`   | Same  |
| `TO_CHAR(d, fmt)`        | `TO_CHAR(d, fmt)`          | Same  |
| `TO_DATE(s, fmt)`        | `TO_DATE(s, fmt)`          | Same  |
| `INSTR(str, search)`     | `POSITION(search IN str)`  |       |
| `SUBSTR(s, pos, len)`    | `SUBSTR(s, pos, len)`      | Same  |
| `REGEXP_LIKE(s, p)`      | `REGEXP_LIKE(s, p)`        | Same  |
| `LISTAGG(col, delim)`    | `LISTAGG(col, delim)`      | Same  |
| `SPLIT_PART(s, d, n)`    | `SPLIT_PART(s, d, n)`      | Same  |

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Vertica-specific syntax converted (projections removed, case sensitivity handled)
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

- **dbt-modeling**: For CTE patterns and SQL structure guidance
- **dbt-testing**: For implementing comprehensive dbt tests
- **dbt-architecture**: For project organization and folder structure
- **dbt-materializations**: For choosing materialization strategies (view, table, incremental,
  snapshots)
- **dbt-performance**: For clustering keys, warehouse sizing, and query optimization
- **dbt-commands**: For running dbt commands and model selection syntax
- **dbt-core**: For dbt installation, configuration, and package management
- **snowflake-cli**: For executing SQL and managing Snowflake objects

---

## Supported Source Database

<!-- prettier-ignore -->
| Database | Key Considerations |
|---|---|
| **Vertica** | Projections, flex tables, case sensitivity with quotes, ANY/ALL array predicates |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

<!-- prettier-ignore -->
| Folder | Description |
|---|---|
| vertica | [Subqueries](translation-references/vertica/subqueries.md) |

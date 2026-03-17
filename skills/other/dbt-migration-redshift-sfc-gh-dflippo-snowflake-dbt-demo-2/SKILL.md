---
name: dbt-migration-redshift
description:
  Convert Amazon Redshift DDL to dbt models compatible with Snowflake. This skill should be used
  when converting views, tables, or stored procedures from Redshift to dbt code, generating
  schema.yml files with tests and documentation, or migrating Redshift SQL to follow dbt best
  practices.
---

# Amazon Redshift to dbt Model Conversion

## Purpose

Transform Amazon Redshift DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Redshift views or tables to dbt models
- Migrating Redshift PL/pgSQL stored procedures to dbt
- Translating Redshift SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Redshift-specific syntax (DISTKEY/SORTKEY, system catalogs, COPY/UNLOAD)

---

## Task Description

You are a database engineer working for a hospital system. You need to convert Amazon Redshift DDL
to equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

## Input Requirements

I will provide you the Redshift DDL to convert.

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
   Source Platform: Amazon Redshift
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
## models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from Amazon Redshift [Original object name]"
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

#### Redshift to Snowflake Syntax Conversion

- Remove DISTKEY/SORTKEY specifications (use clustering keys instead)
- Convert system catalog queries (pg*\*, stl*\_, stv\_\_) to Snowflake equivalents
- Replace COPY/UNLOAD with Snowflake COPY INTO
- Convert PL/pgSQL procedures to Snowflake Scripting
- Handle IDENTITY column differences
- Replace Redshift-specific date functions
- Convert APPROXIMATE COUNT DISTINCT to HLL functions
- Add inline SQL comments highlighting any syntax that was converted

#### Key Data Type Mappings

| Redshift                          | Snowflake              | Notes                      |
| --------------------------------- | ---------------------- | -------------------------- |
| INT/INT2/INT4/INT8/INTEGER/BIGINT | Same                   | All alias to NUMBER        |
| SMALLINT                          | SMALLINT               |                            |
| DECIMAL/NUMERIC                   | Same                   |                            |
| FLOAT/FLOAT4/FLOAT8/REAL          | FLOAT                  |                            |
| BOOL/BOOLEAN                      | BOOLEAN                |                            |
| CHAR/VARCHAR/TEXT                 | Same                   | VARCHAR(MAX) → VARCHAR     |
| BPCHAR                            | VARCHAR                |                            |
| BINARY/VARBINARY/VARBYTE          | BINARY                 | Max 8MB (vs 16MB Redshift) |
| DATE                              | DATE                   |                            |
| TIME/TIMETZ                       | TIME                   | Time zone not supported    |
| TIMESTAMP/TIMESTAMPTZ             | TIMESTAMP/TIMESTAMP_TZ |                            |
| INTERVAL types                    | VARCHAR                |                            |
| GEOMETRY/GEOGRAPHY                | Same                   |                            |
| SUPER                             | VARIANT                |                            |
| HLLSKETCH                         | Not supported          | Use HLL functions          |

#### Key Syntax Conversions

```sql
-- DISTKEY/SORTKEY → Remove (use clustering keys)
CREATE TABLE t (id INT) DISTKEY(id) SORTKEY(created_at) →
CREATE TABLE t (id INT) CLUSTER BY (created_at)

-- COPY/UNLOAD → COPY INTO
COPY table FROM 's3://bucket/path' IAM_ROLE 'arn:...' →
COPY INTO table FROM @stage/path

-- System catalogs
pg_catalog.pg_tables → INFORMATION_SCHEMA.TABLES
stl_query → QUERY_HISTORY table function
stv_sessions → SHOW SESSIONS

-- GETDATE() → CURRENT_TIMESTAMP
GETDATE() → CURRENT_TIMESTAMP()

-- NVL → COALESCE
NVL(col, 0) → COALESCE(col, 0)

-- LISTAGG
LISTAGG(col, ',') WITHIN GROUP (ORDER BY col) →
LISTAGG(col, ',') WITHIN GROUP (ORDER BY col)

-- APPROXIMATE COUNT DISTINCT
APPROXIMATE COUNT(DISTINCT col) → APPROX_COUNT_DISTINCT(col)
```

#### Common Function Mappings

| Redshift                      | Snowflake                       | Notes |
| ----------------------------- | ------------------------------- | ----- |
| `NVL(a, b)`                   | `NVL(a, b)` or `COALESCE(a, b)` | Same  |
| `NVL2(a, b, c)`               | `IFF(a IS NOT NULL, b, c)`      |       |
| `COALESCE(...)`               | `COALESCE(...)`                 | Same  |
| `NULLIF(a, b)`                | `NULLIF(a, b)`                  | Same  |
| `GETDATE()`                   | `CURRENT_TIMESTAMP()`           |       |
| `SYSDATE`                     | `CURRENT_DATE()`                |       |
| `DATEADD(unit, n, d)`         | `DATEADD(unit, n, d)`           | Same  |
| `DATEDIFF(unit, d1, d2)`      | `DATEDIFF(unit, d1, d2)`        | Same  |
| `DATE_TRUNC(unit, d)`         | `DATE_TRUNC(unit, d)`           | Same  |
| `EXTRACT(part FROM d)`        | `EXTRACT(part FROM d)`          | Same  |
| `TO_CHAR(d, fmt)`             | `TO_CHAR(d, fmt)`               | Same  |
| `CONVERT(type, val)`          | `val::type`                     |       |
| `LEN(str)`                    | `LENGTH(str)`                   |       |
| `CHARINDEX(s, str)`           | `POSITION(s IN str)`            |       |
| `LISTAGG(col, delim)`         | `LISTAGG(col, delim)`           | Same  |
| `APPROXIMATE COUNT(DISTINCT)` | `APPROX_COUNT_DISTINCT()`       |       |
| `JSON_EXTRACT_PATH_TEXT()`    | `JSON_EXTRACT_PATH_TEXT()`      | Same  |

#### Dependencies

- List any upstream dependencies
- Suggest model organization in dbt project

---

## Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Redshift-specific syntax converted (DISTKEY/SORTKEY removed, system catalogs mapped)
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

| Database            | Key Considerations                                                                      |
| ------------------- | --------------------------------------------------------------------------------------- |
| **Amazon Redshift** | DISTKEY/SORTKEY, PL/pgSQL procedures, system catalogs (pg\_, stl\_, stv\_), COPY/UNLOAD |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

- [Basic Elements Literals](translation-references/redshift-basic-elements-literals.md)
- [Basic Elements](translation-references/redshift-basic-elements.md)
- [Conditions](translation-references/redshift-conditions.md)
- [Continue Handler](translation-references/redshift-continue-handler.md)
- [Create Procedure](translation-references/redshift-create-procedure.md)
- [Data Types](translation-references/redshift-data-types.md)
- [ETL BI Repointing Power BI Redshift Repointing](translation-references/redshift-etl-bi-repointing-power-bi-redshift-repointing.md)
- [Exit Handler](translation-references/redshift-exit-handler.md)
- [Expressions](translation-references/redshift-expressions.md)
- [Functions](translation-references/redshift-functions.md)
- [Overview (README)](translation-references/redshift-readme.md)
- [Rs SQL Statements Select Into](translation-references/redshift-rs-sql-statements-select-into.md)
- [Rs SQL Statements Select](translation-references/redshift-rs-sql-statements-select.md)
- [SQL Statements Create Table As](translation-references/redshift-sql-statements-create-table-as.md)
- [SQL Statements Create Table](translation-references/redshift-sql-statements-create-table.md)
- [SQL Statements](translation-references/redshift-sql-statements.md)
- [Subqueries](translation-references/redshift-subqueries.md)
- [System Catalog](translation-references/redshift-system-catalog.md)

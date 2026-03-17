---
name: dbt-migration-bigquery
description:
  Convert Google BigQuery DDL to dbt models compatible with Snowflake. This skill should be used
  when converting views, tables, or stored procedures from BigQuery to dbt code, generating
  schema.yml files with tests and documentation, or migrating BigQuery SQL to follow dbt best
  practices.
---

# BigQuery to dbt Model Conversion

## Purpose

Transform Google BigQuery DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting BigQuery views or tables to dbt models
- Migrating BigQuery stored procedures to dbt
- Translating BigQuery SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling BigQuery-specific syntax conversions (UNNEST, STRUCT/ARRAY, backtick identifiers)

---

## Task Description

You are a database engineer working for a hospital system. You need to convert BigQuery DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

## Input Requirements

I will provide you the BigQuery DDL to convert.

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

/* Original Object: [project].[dataset].[object_name]
   Source Platform: BigQuery
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        -- INT64 converted to INTEGER
        customer_id::INTEGER AS customer_id,
        -- STRING converted to VARCHAR
        customer_name::VARCHAR(100) AS customer_name,
        -- NUMERIC converted to NUMBER
        account_balance::NUMBER(18,2) AS account_balance,
        -- TIMESTAMP converted to TIMESTAMP_TZ (BigQuery stores UTC)
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
    description: "Table description; converted from BigQuery [Original object name]"
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

#### BigQuery to Snowflake Syntax Conversion

- Convert backtick identifiers (\`project.dataset.table\`) to Snowflake format
- Replace UNNEST with LATERAL FLATTEN
- Convert STRUCT/ARRAY types to VARIANT/ARRAY
- Translate SAFE*\* functions to TRY*\* equivalents
- Convert IS TRUE/IS FALSE operators
- Handle DATE/TIMESTAMP differences
- Replace ARRAY_AGG with Snowflake equivalent
- Convert BigQuery-specific window functions

#### Key Data Type Mappings

| BigQuery                   | Snowflake     | Notes                         |
| -------------------------- | ------------- | ----------------------------- |
| INT64/INT/INTEGER/BIGINT   | INT           | Alias for NUMBER(38,0)        |
| SMALLINT/TINYINT/BYTEINT   | Same          |                               |
| NUMERIC/DECIMAL/BIGNUMERIC | NUMERIC       | BIGNUMERIC may lose precision |
| FLOAT64                    | FLOAT         |                               |
| BOOL/BOOLEAN               | BOOLEAN       |                               |
| STRING                     | VARCHAR       |                               |
| BYTES                      | BINARY        |                               |
| DATE                       | DATE          |                               |
| TIME                       | TIME          |                               |
| DATETIME                   | TIMESTAMP_NTZ |                               |
| TIMESTAMP                  | TIMESTAMP_TZ  | BigQuery stores in UTC        |
| ARRAY<T>                   | ARRAY         |                               |
| STRUCT                     | VARIANT       | Use OBJECT_CONSTRUCT          |
| JSON                       | VARIANT       | Use PARSE_JSON                |
| GEOGRAPHY                  | GEOGRAPHY     |                               |
| INTERVAL                   | VARCHAR       |                               |

#### Key Syntax Conversions

```sql
-- Backtick identifiers → Double quotes
`project.dataset.table` → "project"."dataset"."table"

-- UNNEST → LATERAL FLATTEN
SELECT * FROM table, UNNEST(array_col) AS elem →
SELECT * FROM table, LATERAL FLATTEN(input => array_col) AS f

-- STRUCT → OBJECT_CONSTRUCT
STRUCT(1 AS a, 'x' AS b) → OBJECT_CONSTRUCT('a', 1, 'b', 'x')

-- ARRAY access
array_col[OFFSET(0)] → array_col[0]
array_col[ORDINAL(1)] → array_col[0]

-- SAFE_* functions → TRY_* or :: with TRY_
SAFE_CAST(x AS INT64) → TRY_TO_NUMBER(x)::INTEGER
SAFE_CAST(x AS STRING) → x::VARCHAR  -- regular cast when safe
SAFE_DIVIDE(a, b) → a / NULLIF(b, 0)  -- returns NULL on divide by zero

-- IS TRUE/IS FALSE
WHERE col IS TRUE → WHERE col = TRUE

-- ARRAY_AGG
ARRAY_AGG(col) → ARRAY_AGG(col)

-- JSON functions
JSON_VALUE(col, '$.key') → col:key::STRING
```

#### Common Function Mappings

| BigQuery                   | Snowflake                            | Notes               |
| -------------------------- | ------------------------------------ | ------------------- |
| `IF(cond, a, b)`           | `IFF(cond, a, b)`                    |                     |
| `IFNULL(a, b)`             | `IFNULL(a, b)`                       | Same                |
| `COUNTIF(cond)`            | `COUNT_IF(cond)`                     |                     |
| `LOGICAL_AND(col)`         | `BOOLAND_AGG(col)`                   |                     |
| `LOGICAL_OR(col)`          | `BOOLOR_AGG(col)`                    |                     |
| `SAFE_CAST(x AS type)`     | `TRY_CAST(x AS type)`                |                     |
| `ARRAY_CONCAT(a, b)`       | `ARRAY_CAT(a, b)`                    |                     |
| `ARRAY_LENGTH(arr)`        | `ARRAY_SIZE(arr)`                    |                     |
| `FORMAT_DATE(fmt, d)`      | `TO_CHAR(d, fmt)`                    | Format codes differ |
| `CURRENT_DATETIME()`       | `CURRENT_TIMESTAMP()::TIMESTAMP_NTZ` |                     |
| `JSON_VALUE(col, '$.key')` | `col:key::STRING`                    | Path syntax differs |
| `JSON_EXTRACT_SCALAR(...)` | `JSON_EXTRACT_PATH_TEXT(...)`        |                     |
| `STARTS_WITH(str, prefix)` | `STARTSWITH(str, prefix)`            |                     |
| `ENDS_WITH(str, suffix)`   | `ENDSWITH(str, suffix)`              |                     |
| `REGEXP_CONTAINS(val, re)` | `REGEXP_INSTR(val, re) > 0`          |                     |
| `TIMESTAMP_MILLIS(ms)`     | `TO_TIMESTAMP(ms / 1000)`            |                     |
| `UNIX_MILLIS(ts)`          | `DATE_PART('epoch_millisecond', ts)` |                     |
| `ST_GEOGFROMTEXT(wkt)`     | `ST_GEOGRAPHYFROMWKT(wkt)`           |                     |
| `ST_GEOGPOINT(lon, lat)`   | `ST_POINT(lon, lat)`                 |                     |

#### Dependencies

- List any upstream dependencies
- Suggest model organization in dbt project

---

## Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] BigQuery-specific syntax converted (UNNEST, backticks, STRUCT/ARRAY)
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

| Database            | Key Considerations                                                                            |
| ------------------- | --------------------------------------------------------------------------------------------- |
| **Google BigQuery** | UNNEST, STRUCT/ARRAY types, backtick identifiers, IS TRUE/FALSE operators, SAFE\_\* functions |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

- [Create Table](translation-references/bigquery-create-table.md)
- [Create View](translation-references/bigquery-create-view.md)
- [Data Types](translation-references/bigquery-data-types.md)
- [Functions](translation-references/bigquery-functions.md)
- [Identifiers](translation-references/bigquery-identifiers.md)
- [Operators](translation-references/bigquery-operators.md)
- [Overview (README)](translation-references/bigquery-readme.md)
- [Subqueries](translation-references/bigquery-subqueries.md)

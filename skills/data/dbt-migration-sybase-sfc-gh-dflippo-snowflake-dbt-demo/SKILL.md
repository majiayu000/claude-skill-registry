---
name: dbt-migration-sybase
description:
  Convert Sybase IQ DDL to dbt models compatible with Snowflake. This skill should be used when
  converting views, tables, or stored procedures from Sybase IQ to dbt code, generating schema.yml
  files with tests and documentation, or migrating Sybase SQL to follow dbt best practices.
---

# Sybase IQ to dbt Model Conversion

## Purpose

Transform Sybase IQ DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Sybase IQ views or tables to dbt models
- Migrating Sybase stored procedures to dbt
- Translating Sybase SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Sybase-specific syntax conversions (T-SQL variant, built-in functions)

---

# Task Description

You are a database engineer working for a hospital system. You need to convert Sybase IQ DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

# Input Requirements

I will provide you the Sybase DDL to convert.

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

/* Original Object: [database].[owner].[object_name]
   Source Platform: Sybase IQ
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        -- MONEY converted to NUMBER(18,2)
        account_balance::NUMBER(18,2) AS account_balance,
        -- DATETIME converted to TIMESTAMP_NTZ
        created_date::TIMESTAMP_NTZ AS created_date
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
    description: "Table description; converted from Sybase IQ [Original object name]"
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

### Sybase to Snowflake Syntax Conversion:

- Convert T-SQL variant syntax to Snowflake
- Replace Sybase built-in functions with Snowflake equivalents
- Handle SELECT statement differences
- Convert data types specific to Sybase IQ
- Replace procedural code with Snowflake Scripting
- Handle CASE expression differences
- Convert string functions

### Key Data Type Mappings

| Sybase IQ          | Snowflake    | Notes |
| ------------------ | ------------ | ----- |
| INT/INTEGER        | INTEGER      |       |
| BIGINT             | BIGINT       |       |
| SMALLINT/TINYINT   | Same         |       |
| DECIMAL/NUMERIC    | Same         |       |
| FLOAT/REAL/DOUBLE  | FLOAT        |       |
| CHAR/VARCHAR       | Same         |       |
| TEXT               | VARCHAR      |       |
| BINARY/VARBINARY   | BINARY       |       |
| BIT                | BOOLEAN      |       |
| DATE               | DATE         |       |
| TIME               | TIME         |       |
| DATETIME/TIMESTAMP | TIMESTAMP    |       |
| MONEY/SMALLMONEY   | NUMBER(38,4) |       |

### Key Syntax Conversions

```sql
-- TOP -> LIMIT
SELECT TOP 10 * FROM table -> SELECT * FROM table LIMIT 10

-- GETDATE() -> CURRENT_TIMESTAMP
GETDATE() -> CURRENT_TIMESTAMP()

-- ISNULL -> COALESCE
ISNULL(col, 0) -> COALESCE(col, 0)

-- CONVERT -> :: casting or TO_* functions
CONVERT(VARCHAR, col) -> col::VARCHAR
CONVERT(VARCHAR(50), col) -> col::VARCHAR(50)
CONVERT(DATE, col, 101) -> TO_DATE(col, 'MM/DD/YYYY')

-- String functions
CHARINDEX('x', col) -> POSITION('x' IN col)
```

### Common Function Mappings

| Sybase IQ                 | Snowflake                          | Notes |
| ------------------------- | ---------------------------------- | ----- |
| `ISNULL(a, b)`            | `COALESCE(a, b)` or `IFNULL(a, b)` |       |
| `COALESCE(...)`           | `COALESCE(...)`                    | Same  |
| `NULLIF(a, b)`            | `NULLIF(a, b)`                     | Same  |
| `GETDATE()`               | `CURRENT_TIMESTAMP()`              |       |
| `DATEADD(unit, n, d)`     | `DATEADD(unit, n, d)`              | Same  |
| `DATEDIFF(unit, d1, d2)`  | `DATEDIFF(unit, d1, d2)`           | Same  |
| `DATEPART(unit, d)`       | `DATE_PART(unit, d)`               |       |
| `CONVERT(type, val)`      | `val::type`                        |       |
| `CAST(val AS type)`       | `val::type`                        |       |
| `CHARINDEX(s, str)`       | `POSITION(s IN str)`               |       |
| `SUBSTRING(s, pos, len)`  | `SUBSTR(s, pos, len)`              |       |
| `LEN(str)`                | `LENGTH(str)`                      |       |
| `REPLICATE(str, n)`       | `REPEAT(str, n)`                   |       |
| `STUFF(s, pos, len, new)` | `INSERT(s, pos, len, new)`         |       |
| `ROUND(n, d)`             | `ROUND(n, d)`                      | Same  |
| `CEILING(n)`              | `CEIL(n)`                          |       |

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Sybase-specific syntax converted (T-SQL variant functions, SELECT differences)
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
| **Sybase IQ** | T-SQL variant, different built-in functions, SELECT syntax differences |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

<!-- prettier-ignore -->
| Folder | Description |
|---|---|
| sybase | [Subqueries](translation-references/sybase/subqueries.md) |

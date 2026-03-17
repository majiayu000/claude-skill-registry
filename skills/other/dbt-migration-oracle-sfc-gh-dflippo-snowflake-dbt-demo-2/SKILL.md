---
name: dbt-migration-oracle
description:
  Convert Oracle DDL to dbt models compatible with Snowflake. This skill should be used when
  converting views, tables, or stored procedures from Oracle to dbt code, generating schema.yml
  files with tests and documentation, or migrating Oracle PL/SQL to follow dbt best practices.
---

# Oracle to dbt Model Conversion

## Purpose

Transform Oracle DDL (views, tables, stored procedures, packages) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Oracle views or tables to dbt models
- Migrating Oracle stored procedures or packages to dbt
- Translating Oracle PL/SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Oracle-specific syntax conversions (ROWNUM/ROWID, CONNECT BY, DBMS\_\* packages,
  sequences)

---

## Task Description

You are a database engineer working for a hospital system. You need to convert Oracle DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

## Input Requirements

I will provide you the Oracle DDL to convert.

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

/* Original Object: [owner].[object_name]
   Source Platform: Oracle
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        account_balance::NUMBER(18,2) AS account_balance,
        -- Oracle DATE includes time, converted to TIMESTAMP_NTZ
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
## models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from Oracle [Original object name]"
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

#### Oracle to Snowflake Syntax Conversion

- Convert ROWNUM to ROW_NUMBER() window function
- Replace CONNECT BY with recursive CTEs
- Convert NVL/NVL2 to COALESCE/IFF
- Translate (+) outer join syntax to ANSI joins
- Replace DECODE with CASE expressions
- Convert sequences to Snowflake sequences or IDENTITY
- Handle DATE type (which includes time in Oracle)
- Replace DBMS\_\* packages with Snowflake alternatives
- Convert PL/SQL procedures to Snowflake Scripting
- Add inline SQL comments highlighting any syntax that was converted

#### Key Data Type Mappings

| Oracle                           | Snowflake     | Notes                      |
| -------------------------------- | ------------- | -------------------------- |
| NUMBER                           | NUMBER        |                            |
| INTEGER/INT                      | INTEGER       | Alias for NUMBER(38,0)     |
| FLOAT/BINARY_FLOAT/BINARY_DOUBLE | FLOAT         |                            |
| CHAR/VARCHAR2/NCHAR/NVARCHAR2    | CHAR/VARCHAR  | VARCHAR2 → VARCHAR         |
| CLOB/NCLOB                       | VARCHAR       | Max 16MB                   |
| BLOB/RAW/LONG RAW                | BINARY        | Max 8MB                    |
| DATE                             | TIMESTAMP_NTZ | Oracle DATE includes time! |
| TIMESTAMP                        | TIMESTAMP_NTZ |                            |
| TIMESTAMP WITH TIME ZONE         | TIMESTAMP_TZ  |                            |
| TIMESTAMP WITH LOCAL TIME ZONE   | TIMESTAMP_LTZ |                            |
| INTERVAL types                   | VARCHAR       |                            |
| ROWID/UROWID                     | VARCHAR       |                            |
| JSON                             | VARIANT       |                            |
| XMLType                          | VARIANT       |                            |

#### Key Syntax Conversions

```sql
-- ROWNUM → ROW_NUMBER()
WHERE ROWNUM <= 10 → QUALIFY ROW_NUMBER() OVER (ORDER BY 1) <= 10

-- CONNECT BY → Recursive CTE
SELECT ... START WITH ... CONNECT BY PRIOR → WITH RECURSIVE cte AS (...)

-- NVL/NVL2 → COALESCE/IFF
NVL(col, 0) → COALESCE(col, 0)
NVL2(col, 'yes', 'no') → IFF(col IS NOT NULL, 'yes', 'no')

-- DECODE → CASE
DECODE(col, 1, 'A', 2, 'B', 'C') → CASE col WHEN 1 THEN 'A' WHEN 2 THEN 'B' ELSE 'C' END

-- (+) outer join → ANSI JOIN
FROM a, b WHERE a.id = b.id(+) → FROM a LEFT JOIN b ON a.id = b.id

-- SYSDATE/SYSTIMESTAMP → CURRENT_DATE/CURRENT_TIMESTAMP
SYSDATE → CURRENT_DATE()

-- DUAL table → Optional in Snowflake
SELECT 1 FROM DUAL → SELECT 1

-- TO_DATE format differences
TO_DATE('2024-01-15', 'YYYY-MM-DD') → TO_DATE('2024-01-15', 'YYYY-MM-DD')
```

#### Common Function Mappings

| Oracle                   | Snowflake                                 | Notes             |
| ------------------------ | ----------------------------------------- | ----------------- |
| `NVL(a, b)`              | `NVL(a, b)` or `COALESCE(a, b)`           | Same              |
| `NVL2(a, b, c)`          | `IFF(a IS NOT NULL, b, c)`                |                   |
| `DECODE(col, ...)`       | `CASE col WHEN ... END`                   |                   |
| `ROWNUM`                 | `ROW_NUMBER() OVER (...)`                 | Use with QUALIFY  |
| `SYSDATE`                | `CURRENT_DATE()` or `CURRENT_TIMESTAMP()` |                   |
| `SYSTIMESTAMP`           | `CURRENT_TIMESTAMP()`                     |                   |
| `TO_CHAR(d, fmt)`        | `TO_CHAR(d, fmt)`                         | Format codes same |
| `TO_DATE(s, fmt)`        | `TO_DATE(s, fmt)`                         | Format codes same |
| `TO_NUMBER(s)`           | `TO_NUMBER(s)`                            | Same              |
| `TRUNC(d)`               | `DATE_TRUNC('day', d)`                    | For dates         |
| `TRUNC(n, d)`            | `TRUNC(n, d)`                             | For numbers, same |
| `ADD_MONTHS(d, n)`       | `DATEADD('month', n, d)`                  |                   |
| `MONTHS_BETWEEN(d1, d2)` | `DATEDIFF('month', d2, d1)`               | Arg order differs |
| `SUBSTR(s, pos, len)`    | `SUBSTR(s, pos, len)`                     | Same              |
| `INSTR(s, search)`       | `POSITION(search IN s)`                   |                   |
| `REGEXP_LIKE(s, p)`      | `REGEXP_LIKE(s, p)`                       | Same              |
| `LISTAGG(col, delim)`    | `LISTAGG(col, delim)`                     | Same              |
| `DBMS_OUTPUT.PUT_LINE`   | Remove or use SYSTEM$LOG                  |                   |

#### Dependencies

- List any upstream dependencies
- Suggest model organization in dbt project

---

## Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Oracle-specific syntax converted (ROWNUM, CONNECT BY, NVL, sequences, DATE type handling)
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

| Database   | Key Considerations                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Oracle** | PL/SQL, DBMS\_\* packages, ROWNUM/ROWID, CONNECT BY, sequences, collections/records, wrapped objects, DATE includes time |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

- [Basic Elements Of Oracle SQL Data Types Any Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-any-types.md)
- [Basic Elements Of Oracle SQL Data Types Oracle Built In Data Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-oracle-built-in-data-types.md)
- [Basic Elements Of Oracle SQL Data Types Readme](translation-references/oracle-basic-elements-of-oracle-sql-data-types-readme.md)
- [Basic Elements Of Oracle SQL Data Types Rowid Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-rowid-types.md)
- [Basic Elements Of Oracle SQL Data Types Spatial Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-spatial-types.md)
- [Basic Elements Of Oracle SQL Data Types User Defined Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-user-defined-types.md)
- [Basic Elements Of Oracle SQL Data Types Xml Types](translation-references/oracle-basic-elements-of-oracle-sql-data-types-xml-types.md)
- [Basic Elements Of Oracle SQL Literals](translation-references/oracle-basic-elements-of-oracle-sql-literals.md)
- [Built In Packages](translation-references/oracle-built-in-packages.md)
- [ETL BI Repointing Power BI Oracle Repointing](translation-references/oracle-etl-bi-repointing-power-bi-oracle-repointing.md)
- [Functions Custom UDFS](translation-references/oracle-functions-custom_udfs.md)
- [Functions Readme](translation-references/oracle-functions-readme.md)
- [PL SQL To Javascript Helpers](translation-references/oracle-pl-sql-to-javascript-helpers.md)
- [PL SQL To Javascript Readme](translation-references/oracle-pl-sql-to-javascript-readme.md)
- [PL SQL To Snowflake Scripting Collections And Records](translation-references/oracle-pl-sql-to-snowflake-scripting-collections-and-records.md)
- [PL SQL To Snowflake Scripting Create Function](translation-references/oracle-pl-sql-to-snowflake-scripting-create-function.md)
- [PL SQL To Snowflake Scripting Create Procedure](translation-references/oracle-pl-sql-to-snowflake-scripting-create-procedure.md)
- [PL SQL To Snowflake Scripting Cursor](translation-references/oracle-pl-sql-to-snowflake-scripting-cursor.md)
- [PL SQL To Snowflake Scripting DML Statements](translation-references/oracle-pl-sql-to-snowflake-scripting-dml-statements.md)
- [PL SQL To Snowflake Scripting Helpers](translation-references/oracle-pl-sql-to-snowflake-scripting-helpers.md)
- [PL SQL To Snowflake Scripting Packages](translation-references/oracle-pl-sql-to-snowflake-scripting-packages.md)
- [PL SQL To Snowflake Scripting Readme](translation-references/oracle-pl-sql-to-snowflake-scripting-readme.md)
- [Pseudocolumns](translation-references/oracle-pseudocolumns.md)
- [Overview (README)](translation-references/oracle-readme.md)
- [SQL Plus](translation-references/oracle-sql-plus.md)
- [SQL Queries And Subqueries Joins](translation-references/oracle-sql-queries-and-subqueries-joins.md)
- [SQL Queries And Subqueries Selects](translation-references/oracle-sql-queries-and-subqueries-selects.md)
- [SQL Translation Reference Create Materialized View](translation-references/oracle-sql-translation-reference-create-materialized-view.md)
- [SQL Translation Reference Create Table](translation-references/oracle-sql-translation-reference-create-table.md)
- [SQL Translation Reference Create View](translation-references/oracle-sql-translation-reference-create-view.md)
- [SQL Translation Reference Create Type](translation-references/oracle-sql-translation-reference-create_type.md)
- [SQL Translation Reference Readme](translation-references/oracle-sql-translation-reference-readme.md)
- [Subqueries](translation-references/oracle-subqueries.md)

---
name: dbt-migration
description:
  Convert database DDL from any source platform to dbt models compatible with Snowflake. This skill
  should be used when converting views, tables, or stored procedures from Snowflake, Teradata,
  Oracle, SQL Server, Redshift, BigQuery, PostgreSQL, DB2, Hive, Vertica, or Sybase to dbt code,
  generating schema.yml files with tests and documentation, or migrating existing SQL to follow dbt
  best practices.
---

# Database to dbt Model Conversion

## Purpose

Transform database DDL (views, tables, stored procedures) from any source platform into
production-quality dbt models compatible with Snowflake, maintaining the same business logic and
data transformation steps while following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting database views or tables to dbt models
- Migrating stored procedures to dbt
- Translating SQL syntax from one database to Snowflake
- Generating schema.yml files with tests and documentation
- Handling database-specific syntax conversions

---

# Task Description

You are a database engineer working for a hospital system. You need to convert SQL DDL to equivalent
dbt code compatible with Snowflake, maintaining the same business logic and data transformation
steps while following dbt best practices.

# Input Requirements

I will provide you the SQL DDL to convert. Please ask for the source database platform if not
obvious from the syntax.

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

/* Original Object: [source_db].[schema].[object_name]
 Source Platform: [Teradata|Oracle|SQL Server|etc.]
 Purpose: [brief description]
 Conversion Notes: [key changes]
 Description: [SQL logic description] */

WITH source_data AS (
 SELECT
 COLUMN1 AS COLUMN1_ALIAS,
 COLUMN2 AS COLUMN2_ALIAS,
 COLUMN3 AS COLUMN3_ALIAS,
 COLUMN4 AS COLUMN4_ALIAS
 FROM {{ ref('upstream_model') }}
),
transformed_data AS (
 SELECT
 UPPER(COLUMN1) AS COLUMN_ALIAS1,
 LOWER(COLUMN2) AS COLUMN_ALIAS2,
 COLUMN3 || COLUMN4 AS COLUMN_ALIAS3
 FROM source_data
)
SELECT
 COLUMN_ALIAS1,
 COLUMN_ALIAS2,
 COLUMN_ALIAS3
FROM transformed_data
```

```yaml
# models/[domain]/[target_schema_name]/schema.yml
version: 2

models:
 - name: model_name
 description: "Table description; converted from [Source Platform] [Original object name]"
 columns:
 - name: COLUMN_ALIAS1
 description: "Column description; Primary key"
 tests:
 - unique
 - not_null
 - name: COLUMN_ALIAS2
 description: "Column description; Foreign key to OTHER_TABLE"
 tests:
 - relationships:
 to: ref('OTHER_TABLE')
 field: OTHER_TABLE_KEY
 - name: COLUMN_ALIAS3
 description: "Column description"
```

```yaml
# dbt_project.yml
models:
  my_project:
  ? [domain]
  ? [target_schema_name]
  +schema: [target_schema_name]
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

### Performance Optimization:

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Source platform identified
- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
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

## Supported Source Databases

<!-- prettier-ignore -->
|Database|Key Considerations|
|---|---|
|**Snowflake**|Native syntax, focus on dbt patterns and best practices|
|**Teradata**|QUALIFY, ANSI/TERA session modes, volatile tables, SET/MULTISET, BTEQ/FastLoad/MultiLoad scripts, DBC views|
|**Oracle**|PL/SQL, DBMS\_\* packages, ROWNUM/ROWID, CONNECT BY, sequences, collections/records, wrapped objects, DATE includes time|
|**SQL Server / Azure Synapse**|T-SQL procedures, IDENTITY, TOP, #temp tables, TRY...CATCH, sys.\* tables, ANSI_NULLS/QUOTED_IDENTIFIER|
|**Amazon Redshift**|DISTKEY/SORTKEY, PL/pgSQL procedures, system catalogs (pg\_, stl\_, stv\_), COPY/UNLOAD|
|**Google BigQuery**|UNNEST, STRUCT/ARRAY types, backtick identifiers, IS TRUE/FALSE operators, SAFE\_\* functions|
|**PostgreSQL / Greenplum / Netezza**|Array expressions (<> ALL, = ANY), CHAR padding differences, psql commands, distribution keys|
|**IBM DB2**|Inline SQL PL, FETCH FIRST, CONTINUE/EXIT handlers, compound statements|
|**Hive / Spark / Databricks**|External tables, PARTITIONED BY, LATERAL VIEW, file formats (PARQUET, ORC), UDFs|
|**Vertica**|Projections, flex tables, case sensitivity with quotes, ANY/ALL array predicates|
|**Sybase**|T-SQL variant, different built-in functions, SELECT syntax differences|

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Full Translation Reference Index

<!-- prettier-ignore -->
|Folder|Description|
|---|---|
|bigquery|[BigQuery](translation-references/bigquery/README.md)|
|db2|[IBM DB2](translation-references/db2/README.md)|
|general|[Cross-database references](translation-references/general/README.md)|
|hive|[Hive, Spark, Databricks](translation-references/hive/README.md)|
|oracle|[Oracle](translation-references/oracle/README.md)|
|postgres|[PostgreSQL, Greenplum, Netezza](translation-references/postgres/README.md)|
|redshift|[Amazon Redshift](translation-references/redshift/README.md)|
|ssis|[SSIS](translation-references/ssis/README.md)|
|sybase|[Sybase IQ](translation-references/sybase/README.md)|
|teradata|[Teradata](translation-references/teradata/README.md)|
|transact|[SQL Server / Azure Synapse](translation-references/transact/README.md)|
|vertica|[Vertica](translation-references/vertica/README.md)|

### Full Translation Reference Index (Expanded)

<!-- prettier-ignore -->
|Folder|Description|
|---|---|
|bigquery|[BigQuery](translation-references/bigquery/README.md)|
|bigquery|[CREATE TABLE (unsupported options)](translation-references/bigquery/bigquery-create-table.md)|
|bigquery|[CREATE VIEW](translation-references/bigquery/bigquery-create-view.md)|
|bigquery|[Data types mapping](translation-references/bigquery/bigquery-data-types.md)|
|bigquery|[Supported Built-in functions](translation-references/bigquery/bigquery-functions.md)|
|bigquery|[Quoted identifier syntax](translation-references/bigquery/bigquery-identifiers.md)|
|bigquery|[IS operators (IS NULL, IS TRUE, etc.)](translation-references/bigquery/bigquery-operators.md)|
|db2|[IBM DB2](translation-references/db2/README.md)|
|db2|[CONTINUE handler behavior](translation-references/db2/db2-continue-handler.md)|
|db2|[CREATE FUNCTION](translation-references/db2/db2-create-function.md)|
|db2|[CREATE PROCEDURE](translation-references/db2/db2-create-procedure.md)|
|db2|[CREATE TABLE syntax](translation-references/db2/db2-create-table.md)|
|db2|[CREATE VIEW](translation-references/db2/db2-create-view.md)|
|db2|[Data types](translation-references/db2/db2-data-types.md)|
|db2|[EXIT handler behavior](translation-references/db2/db2-exit-handler.md)|
|db2|[FROM clause](translation-references/db2/db2-from-clause.md)|
|db2|[SELECT statement](translation-references/db2/db2-select-statement.md)|
|general|[Cross-database references](translation-references/general/README.md)|
|general|[Alphabetical list of Built-in functions (cross-platform)](translation-references/general/built-in-functions.md)|
|general|[Subqueries in FROM/WHERE clauses](translation-references/general/subqueries.md)|
|hive|[Hive, Spark, Databricks](translation-references/hive/README.md)|
|hive|[Built-in functions](translation-references/hive/built-in-functions.md)|
|hive|[Data types mapping](translation-references/hive/data-types.md)|
|hive|[Supported DDL statements](translation-references/hive/ddls/README.md)|
|hive|[CREATE EXTERNAL TABLE](translation-references/hive/ddls/create-external-table.md)|
|hive|[CREATE VIEW](translation-references/hive/ddls/create-view.md)|
|hive|[SELECT](translation-references/hive/ddls/select.md)|
|hive|[CREATE TABLE](translation-references/hive/ddls/tables.md)|
|oracle|[Oracle](translation-references/oracle/README.md)|
|oracle|[Data types and arithmetic](translation-references/oracle/basic-elements-of-oracle-sql/data-types/README.md)|
|oracle|[ANY types for flexible parameter/column typing](translation-references/oracle/basic-elements-of-oracle-sql/data-types/any-types.md)|
|oracle|[Built-in data types (VARCHAR2, NUMBER, DATE, etc.)](translation-references/oracle/basic-elements-of-oracle-sql/data-types/oracle-built-in-data-types.md)|
|oracle|[ROWID types](translation-references/oracle/basic-elements-of-oracle-sql/data-types/rowid-types.md)|
|oracle|[Spatial and geographic types](translation-references/oracle/basic-elements-of-oracle-sql/data-types/spatial-types.md)|
|oracle|[User-defined types (UDTs)](translation-references/oracle/basic-elements-of-oracle-sql/data-types/user-defined-types.md)|
|oracle|[XML types](translation-references/oracle/basic-elements-of-oracle-sql/data-types/xml-types.md)|
|oracle|[Literals and constant values](translation-references/oracle/basic-elements-of-oracle-sql/literals.md)|
|oracle|[Built-in packages.](translation-references/oracle/built-in-packages.md)|
|oracle|[Power BI connection repointing](translation-references/oracle/etl-bi-repointing/power-bi-oracle-repointing.md)|
|oracle|[Functions](translation-references/oracle/functions/README.md)|
|oracle|[Custom UDFs for Oracle function equivalence](translation-references/oracle/functions/custom_udfs.md)|
|oracle|[PL/SQL to JavaScript](translation-references/oracle/pl-sql-to-javascript/README.md)|
|oracle|[Helper functions for Oracle features](translation-references/oracle/pl-sql-to-javascript/helpers.md)|
|oracle|[Assignment statements and PL/SQL basics](translation-references/oracle/pl-sql-to-snowflake-scripting/README.md)|
|oracle|[Collections and Records](translation-references/oracle/pl-sql-to-snowflake-scripting/collections-and-records.md)|
|oracle|[CREATE FUNCTION](translation-references/oracle/pl-sql-to-snowflake-scripting/create-function.md)|
|oracle|[CREATE PROCEDURE](translation-references/oracle/pl-sql-to-snowflake-scripting/create-procedure.md)|
|oracle|[Cursors](translation-references/oracle/pl-sql-to-snowflake-scripting/cursor.md)|
|oracle|[DML with PL/SQL elements](translation-references/oracle/pl-sql-to-snowflake-scripting/dml-statements.md)|
|oracle|[Helper functions for unsupported Oracle features](translation-references/oracle/pl-sql-to-snowflake-scripting/helpers.md)|
|oracle|[CREATE PACKAGE](translation-references/oracle/pl-sql-to-snowflake-scripting/packages.md)|
|oracle|[ROWID pseudocolumn](translation-references/oracle/pseudocolumns.md)|
|oracle|[Sample data used in examples](translation-references/oracle/sample-data.md)|
|oracle|[SQL\*Plus to SnowSQL](translation-references/oracle/sql-plus.md)|
|oracle|[JOIN operations](translation-references/oracle/sql-queries-and-subqueries/joins.md)|
|oracle|[SELECT](translation-references/oracle/sql-queries-and-subqueries/selects.md)|
|oracle|[Oracle SQL syntax differences and translations](translation-references/oracle/sql-translation-reference/README.md)|
|oracle|[Materialized View to Dynamic Table](translation-references/oracle/sql-translation-reference/create-materialized-view.md)|
|oracle|[CREATE TABLE](translation-references/oracle/sql-translation-reference/create-table.md)|
|oracle|[CREATE VIEW](translation-references/oracle/sql-translation-reference/create-view.md)|
|oracle|[CREATE TYPE (UDTs)](translation-references/oracle/sql-translation-reference/create_type.md)|
|oracle|[Wrapped/encrypted objects](translation-references/oracle/wrapped-objects.md)|
|postgres|[PostgreSQL, Greenplum, Netezza](translation-references/postgres/README.md)|
|postgres|[Netezza data types](translation-references/postgres/data-types/netezza-data-types.md)|
|postgres|[PostgreSQL data types](translation-references/postgres/data-types/postgresql-data-types.md)|
|postgres|[Greenplum Materialized View](translation-references/postgres/ddls/create-materialized-view/greenplum-create-materialized-view.md)|
|postgres|[Materialized View to Dynamic Table](translation-references/postgres/ddls/create-materialized-view/postgresql-create-materialized-view.md)|
|postgres|[Greenplum CREATE TABLE](translation-references/postgres/ddls/create-table/greenplum-create-table.md)|
|postgres|[Netezza CREATE TABLE](translation-references/postgres/ddls/create-table/netezza-create-table.md)|
|postgres|[PostgreSQL CREATE TABLE](translation-references/postgres/ddls/create-table/postgresql-create-table.md)|
|postgres|[PostgreSQL CREATE VIEW](translation-references/postgres/ddls/postgresql-create-view.md)|
|postgres|[Power BI connection repointing](translation-references/postgres/etl-bi-repointing/power-bi-postgres-repointing.md)|
|postgres|[Built-in functions](translation-references/postgres/postgresql-built-in-functions.md)|
|postgres|[<> ALL & = ANY array expressions](translation-references/postgres/postgresql-expressions.md)|
|postgres|[PSQL commands](translation-references/postgres/postgresql-interactive-terminal.md)|
|postgres|[String comparison behavior](translation-references/postgres/postgresql-string-comparison.md)|
|redshift|[Amazon Redshift](translation-references/redshift/README.md)|
|redshift|[Power BI connection repointing](translation-references/redshift/etl-bi-repointing/power-bi-redshift-repointing.md)|
|redshift|[Literals](translation-references/redshift/redshift-basic-elements-literals.md)|
|redshift|[Names and identifiers](translation-references/redshift/redshift-basic-elements.md)|
|redshift|[BETWEEN condition](translation-references/redshift/redshift-conditions.md)|
|redshift|[CONTINUE handler emulation](translation-references/redshift/redshift-continue-handler.md)|
|redshift|[Data types](translation-references/redshift/redshift-data-types.md)|
|redshift|[EXIT handler via EXCEPTION blocks](translation-references/redshift/redshift-exit-handler.md)|
|redshift|[Expression lists](translation-references/redshift/redshift-expressions.md)|
|redshift|[Built-in functions](translation-references/redshift/redshift-functions.md)|
|redshift|[CREATE TABLE AS](translation-references/redshift/redshift-sql-statements-create-table-as.md)|
|redshift|[CREATE TABLE](translation-references/redshift/redshift-sql-statements-create-table.md)|
|redshift|[Supported SQL statements](translation-references/redshift/redshift-sql-statements.md)|
|redshift|[System catalog views](translation-references/redshift/redshift-system-catalog.md)|
|redshift|[CREATE PROCEDURE](translation-references/redshift/rs-sql-statements-create-procedure.md)|
|redshift|[SELECT INTO](translation-references/redshift/rs-sql-statements-select-into.md)|
|redshift|[SELECT](translation-references/redshift/rs-sql-statements-select.md)|
|ssis|[SSIS](translation-references/ssis/README.md)|
|sybase|[Sybase IQ](translation-references/sybase/README.md)|
|sybase|[Built-in functions](translation-references/sybase/sybase-built-in-functions.md)|
|sybase|[CREATE TABLE](translation-references/sybase/sybase-create-table.md)|
|sybase|[CREATE VIEW](translation-references/sybase/sybase-create-view.md)|
|sybase|[Data types mapping](translation-references/sybase/sybase-data-types.md)|
|sybase|[SELECT statement](translation-references/sybase/sybase-select-statement.md)|
|teradata|[Teradata](translation-references/teradata/README.md)|
|teradata|[Considerations for migrating data from Teradata](translation-references/teradata/data-migration-considerations.md)|
|teradata|[Power BI connection repointing](translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing.md)|
|teradata|[Helper functions for procedures](translation-references/teradata/helpers-for-procedures.md)|
|teradata|[BTEQ, FastLoad, MultiLoad, TPT scripts to Python](translation-references/teradata/scripts-to-python/README.md)|
|teradata|[BTEQ to Python](translation-references/teradata/scripts-to-python/bteq-translation.md)|
|teradata|[FastLoad to Python](translation-references/teradata/scripts-to-python/fastload-translation.md)|
|teradata|[MultiLoad to Python](translation-references/teradata/scripts-to-python/multiload-translation.md)|
|teradata|[Helper classes for Teradata script to Python conversion](translation-references/teradata/scripts-to-python/snowconvert-script-helpers.md)|
|teradata|[TPT translation](translation-references/teradata/scripts-to-python/tpt-translation.md)|
|teradata|[Scripts to Snowflake SQL](translation-references/teradata/scripts-to-snowflake-sql-translation-reference/README.md)|
|teradata|[BTEQ to Snowflake SQL](translation-references/teradata/scripts-to-snowflake-sql-translation-reference/bteq.md)|
|teradata|[Common script statements](translation-references/teradata/scripts-to-snowflake-sql-translation-reference/common-statements.md)|
|teradata|[MultiLoad to Snowflake SQL](translation-references/teradata/scripts-to-snowflake-sql-translation-reference/mload.md)|
|teradata|[ANSI vs TERA session modes](translation-references/teradata/session-modes.md)|
|teradata|[Iceberg table transformations](translation-references/teradata/sql-translation-reference/Iceberg-tables-transformations.md)|
|teradata|[Teradata SQL to Snowflake](translation-references/teradata/sql-translation-reference/README.md)|
|teradata|[Analytic functions](translation-references/teradata/sql-translation-reference/analytic.md)|
|teradata|[Data types](translation-references/teradata/sql-translation-reference/data-types.md)|
|teradata|[Equivalents for DBC objects and columns](translation-references/teradata/sql-translation-reference/database-dbc.md)|
|teradata|[DDL statements](translation-references/teradata/sql-translation-reference/ddl-teradata.md)|
|teradata|[DML statements](translation-references/teradata/sql-translation-reference/dml-teradata.md)|
|teradata|[Built-in functions](translation-references/teradata/sql-translation-reference/teradata-built-in-functions.md)|
|teradata|[GET DIAGNOSTICS EXCEPTION](translation-references/teradata/teradata-to-javascript-translation-reference.md)|
|teradata|[ABORT and ROLLBACK](translation-references/teradata/teradata-to-snowflake-scripting-translation-reference.md)|
|transact|[SQL Server / Azure Synapse](translation-references/transact/README.md)|
|transact|[Power BI connection repointing](translation-references/transact/etl-bi-repointing/power-bi-transact-repointing.md)|
|transact|[ALTER statements](translation-references/transact/transact-alter-statement.md)|
|transact|[ANSI_NULLS setting](translation-references/transact/transact-ansi-nulls.md)|
|transact|[Built-in functions](translation-references/transact/transact-built-in-functions.md)|
|transact|[Built-in procedures](translation-references/transact/transact-built-in-procedures.md)|
|transact|[Exception handling with TRY...CATCH](translation-references/transact/transact-continue-handler.md)|
|transact|[User Defined Functions](translation-references/transact/transact-create-function.md)|
|transact|[CREATE INDEX](translation-references/transact/transact-create-index.md)|
|transact|[Materialized View to Dynamic Table](translation-references/transact/transact-create-materialized-view.md)|
|transact|[BEGIN/COMMIT transactions](translation-references/transact/transact-create-procedure-snow-script.md)|
|transact|[CREATE PROCEDURE to JavaScript](translation-references/transact/transact-create-procedure.md)|
|transact|[CREATE TABLE](translation-references/transact/transact-create-table.md)|
|transact|[CREATE VIEW](translation-references/transact/transact-create-view.md)|
|transact|[Data types mapping](translation-references/transact/transact-data-types.md)|
|transact|[DML statements and expressions](translation-references/transact/transact-dmls.md)|
|transact|[Exception handling with TRY...CATCH](translation-references/transact/transact-exit-handler.md)|
|transact|[General statements](translation-references/transact/transact-general-statements.md)|
|transact|[QUOTED_IDENTIFIER setting](translation-references/transact/transact-quoted-identifier.md)|
|transact|[SELECT in procedures](translation-references/transact/transact-select.md)|
|transact|[System tables](translation-references/transact/transact-system-tables.md)|
|vertica|[Vertica](translation-references/vertica/README.md)|
|vertica|[Built-in functions](translation-references/vertica/vertica-built-in-functions.md)|
|vertica|[CREATE TABLE](translation-references/vertica/vertica-create-table.md)|
|vertica|[CREATE VIEW](translation-references/vertica/vertica-create-view.md)|
|vertica|[Data types mapping](translation-references/vertica/vertica-data-types.md)|
|vertica|[Case sensitivity and quoted identifiers](translation-references/vertica/vertica-identifier-between-vertica-and-snowflake.md)|
|vertica|[Vertica Operators](translation-references/vertica/vertica-operators.md)|
|vertica|[ANY & ALL array predicates](translation-references/vertica/vertica-predicates.md)|

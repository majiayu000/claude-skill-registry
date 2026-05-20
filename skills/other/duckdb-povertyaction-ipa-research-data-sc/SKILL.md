---
name: duckdb
description: This skill should be used when users need to work with the DuckDB CLI for querying, analyzing, or transforming data. Use this skill for executing SQL queries, importing/exporting data, configuring DuckDB settings, or performing database operations at the command line.
---

# DuckDB CLI Skill

This skill provides comprehensive guidance for using DuckDB's command-line interface, a fast, in-process SQL OLAP database management system designed for analytical workloads.

## About DuckDB CLI

DuckDB CLI is a single, dependency-free executable that provides a full-featured SQL interface for data analysis. It excels at analytical queries on structured data formats (CSV, Parquet, JSON) and can handle datasets ranging from in-memory operations to out-of-core processing of files larger than available RAM.

### Key Capabilities

- **SQL Analytics**: Full SQL support with PostgreSQL-compatible syntax
- **File Format Support**: Native reading of CSV, Parquet, JSON, Excel, and more
- **In-Memory & Persistent**: Work with temporary in-memory databases or persistent files
- **Zero-Copy Integration**: Direct querying of files without importing
- **Advanced Features**: Window functions, CTEs, PIVOT/UNPIVOT, aggregations
- **Data Import/Export**: Seamless conversion between formats
- **Performance**: Columnar storage, vectorized execution, and intelligent query optimization

### Version Information

Current stable version: 1.4.1 (Ossivalis)

Available for Windows, macOS, and Linux as a single executable with no dependencies.

## When to Use This Skill

Use this skill when users:

- Need to query CSV, Parquet, JSON, or Excel files using SQL
- Want to perform data analysis at the command line
- Need to transform, aggregate, or join datasets
- Want to convert between data formats (CSV to Parquet, JSON to CSV, etc.)
- Ask about database operations, aggregations, or analytics
- Need to work with both small and large datasets efficiently
- Want to create persistent databases for analytical workloads
- Need to execute SQL queries from scripts or command line

## Installation

### Download and Setup

1. Download DuckDB CLI from the [installation page](https://duckdb.org/docs/installation) under the CLI tab
2. Available as pre-built binaries for:
   - Windows (x64, ARM64)
   - macOS (x64, ARM64/M1)
   - Linux (x64, ARM64)
3. Extract the executable (single file, no installation needed)
4. Run from terminal: `duckdb` (or `./duckdb` in PowerShell/POSIX shells)

### Package Managers

```bash
# Homebrew (macOS/Linux)
brew install duckdb

# Chocolatey (Windows)
choco install duckdb

# Scoop (Windows)
scoop install duckdb
```

## Getting Started

### Launching DuckDB

**In-Memory Database (Temporary):**

```bash
duckdb
```

Creates a temporary database that won't persist after closing. Ideal for quick analysis.

**Persistent Database:**

```bash
duckdb my_database.duckdb
```

Creates or opens a database file. All changes are automatically saved.

**Opening Existing Database:**

```bash
duckdb path/to/existing.duckdb
```

### Exiting DuckDB

Press `Ctrl+D`, `Ctrl+C`, or type:

```sql
.exit
```

Persistent databases automatically checkpoint (save) when closing.

## SQL Query Execution

### Interactive SQL

Enter SQL statements followed by semicolons:

```sql
SELECT 42 AS answer;
```

**Multi-line Statements:**

```sql
SELECT
    column1,
    column2
FROM my_table
WHERE condition = true;
```

### Non-Interactive Execution

**Execute SQL directly from command line:**

```bash
duckdb :memory: "SELECT 42 AS answer"
```

**Pipe SQL from file:**

```bash
duckdb < commands.sql
```

**Execute and output results:**

```bash
duckdb my_db.duckdb "SELECT * FROM table" > results.csv
```

## Reading Data Files

DuckDB can query files directly without importing:

### CSV Files

```sql
-- Read CSV file
SELECT * FROM read_csv('data.csv');

-- With options
SELECT * FROM read_csv('data.csv',
    header = true,
    delimiter = ',',
    auto_detect = true
);

-- Create table from CSV
CREATE TABLE my_table AS
SELECT * FROM read_csv('data.csv');
```

### Parquet Files

```sql
-- Read Parquet file
SELECT * FROM read_parquet('data.parquet');

-- Read multiple Parquet files
SELECT * FROM read_parquet('data/*.parquet');

-- Hive-partitioned Parquet
SELECT * FROM read_parquet('data/year=*/month=*/*.parquet');
```

### JSON Files

```sql
-- Read JSON file
SELECT * FROM read_json('data.json');

-- NDJSON (newline-delimited JSON)
SELECT * FROM read_json('data.ndjson', format='newline_delimited');
```

### Excel Files

```sql
-- Read Excel file
SELECT * FROM read_excel('data.xlsx');

-- Specific sheet
SELECT * FROM read_excel('data.xlsx', sheet='Sheet2');
```

### Reading from stdin

```bash
cat data.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

## Common SQL Operations

### Basic Queries

```sql
-- Select specific columns
SELECT name, age, city FROM users;

-- Filter rows
SELECT * FROM users WHERE age > 25;

-- Sort results
SELECT * FROM users ORDER BY age DESC;

-- Limit results
SELECT * FROM users LIMIT 10;
```

### Aggregations

```sql
-- Count rows
SELECT COUNT(*) FROM users;

-- Group by with aggregation
SELECT city, COUNT(*) as count, AVG(age) as avg_age
FROM users
GROUP BY city;

-- DuckDB-friendly GROUP BY ALL
SELECT city, COUNT(*) as count
FROM users
GROUP BY ALL;
```

### Joins

```sql
-- Inner join
SELECT u.name, o.order_id
FROM users u
JOIN orders o ON u.user_id = o.user_id;

-- Left join
SELECT u.name, o.order_id
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id;

-- Multiple joins
SELECT u.name, o.order_id, p.product_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN products p ON o.product_id = p.product_id;
```

### Window Functions

```sql
-- Row number
SELECT name, age,
    ROW_NUMBER() OVER (ORDER BY age) as rank
FROM users;

-- Partition by
SELECT name, department, salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;

-- Quantiles with NTILE
SELECT name, score,
    NTILE(4) OVER (ORDER BY score) as quartile
FROM students;
```

### Pivoting

```sql
-- UNPIVOT (wide to long)
UNPIVOT sales
ON jan, feb, mar
INTO
    NAME month
    VALUE amount;

-- PIVOT (long to wide)
PIVOT sales
ON month
USING SUM(amount);
```

### Common Table Expressions (CTEs)

```sql
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 100000
),
departments AS (
    SELECT dept_id, AVG(salary) as avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT h.name, d.avg_salary
FROM high_earners h
JOIN departments d ON h.dept_id = d.dept_id;
```

## Data Export

### Export to CSV

```sql
COPY (SELECT * FROM my_table) TO 'output.csv' (HEADER, DELIMITER ',');
```

### Export to Parquet

```sql
COPY (SELECT * FROM my_table) TO 'output.parquet' (FORMAT PARQUET);
```

### Export to JSON

```sql
COPY (SELECT * FROM my_table) TO 'output.json';
```

## Dot Commands

Dot commands provide CLI-specific functionality and start with a period (`.`):

### Essential Dot Commands

```sql
.help                    -- Show all available dot commands
.tables                  -- List all tables in database
.schema [table_name]     -- Show table schema
.open path/to/db.duckdb  -- Switch to different database
.read file.sql           -- Execute SQL from file
.exit                    -- Exit DuckDB
```

### Output Formatting

```sql
.mode duckbox           -- Default table format
.mode csv               -- CSV output
.mode json              -- JSON output
.mode markdown          -- Markdown tables
.mode latex             -- LaTeX tables
.mode insert            -- SQL INSERT statements
.mode line              -- One value per line
```

**Example:**

```sql
.mode csv
SELECT * FROM users;
.mode duckbox
```

### Output Redirection

```sql
-- Redirect all output to file
.output results.txt
SELECT * FROM users;
.output stdout         -- Reset to terminal

-- Redirect next query only
.once results.csv
SELECT * FROM users;
```

### Custom Prompts

```sql
.prompt 'duckdb> '
.prompt '> '
```

## Configuration

### Startup Configuration

Create `~/.duckdbrc` for automatic configuration on startup:

```sql
.mode duckbox
.prompt 'duck> '
```

**Skip default config:**

```bash
duckdb -init /dev/null
```

**Use custom config:**

```bash
duckdb -init my_config.sql
```

### Session Settings

```sql
-- Enable/disable progress bar
SET enable_progress_bar = true;

-- Set memory limit
SET memory_limit = '4GB';

-- Set threads
SET threads = 4;

-- Enable external access (for environment variables)
SET enable_external_access = true;
```

## Advanced Features

### Environment Variables

```sql
-- Get environment variable
SELECT getenv('HOME') AS home;
SELECT getenv('USER') AS username;
```

Note: Requires `enable_external_access = true` (default).

### Prepared Statements

```sql
PREPARE my_query AS
SELECT * FROM users WHERE age > $1;

EXECUTE my_query(25);
```

### Query Explanation

```sql
-- Show query plan
EXPLAIN SELECT * FROM users WHERE age > 25;

-- Detailed analysis
EXPLAIN ANALYZE SELECT * FROM users WHERE age > 25;
```

### Sampling

```sql
-- Random sample (1%)
SELECT * FROM large_table USING SAMPLE 1%;

-- Sample with seed (reproducible)
SELECT * FROM large_table USING SAMPLE 1000 ROWS (SEED 42);
```

### Creating Views

```sql
CREATE VIEW adult_users AS
SELECT * FROM users WHERE age >= 18;

SELECT * FROM adult_users;
```

## DuckDB-Specific SQL Enhancements

### Friendly Syntax Features

**FROM-first syntax:**

```sql
FROM users
SELECT name, age
WHERE age > 25;
```

**GROUP BY ALL:**

```sql
SELECT city, department, COUNT(*)
FROM employees
GROUP BY ALL;
```

**ORDER BY ALL:**

```sql
SELECT name, age, salary
FROM employees
ORDER BY ALL;
```

### List and Struct Types

```sql
-- Create list column
SELECT [1, 2, 3] AS my_list;

-- Create struct column
SELECT {'name': 'John', 'age': 30} AS person;

-- Unnest list
SELECT UNNEST([1, 2, 3]) AS value;
```

## Working with Large Datasets

### Out-of-Core Processing

DuckDB can process datasets larger than RAM by using disk-backed databases:

```bash
duckdb large_db.duckdb
```

```sql
-- Create table from large CSV
CREATE TABLE large_table AS
SELECT * FROM read_csv('very_large_file.csv');

-- Query with partitioning benefits
SELECT * FROM read_parquet('data/year=*/month=*/*.parquet')
WHERE year = 2024 AND month = 1;
```

### Performance Tips

1. **Use Parquet for large datasets**: More efficient than CSV
2. **Leverage partitioning**: Hive-partitioned files reduce I/O
3. **Filter early**: DuckDB pushes filters down to file reading
4. **Use sampling for exploration**: Test queries on samples first
5. **Select only needed columns**: Columnar storage makes this very efficient

## Practical Examples

### Data Cleaning

```sql
-- Remove duplicates
CREATE TABLE clean_users AS
SELECT DISTINCT * FROM users;

-- Handle missing values
SELECT
    COALESCE(name, 'Unknown') as name,
    COALESCE(age, 0) as age
FROM users;

-- String cleaning
SELECT
    TRIM(name) as name,
    LOWER(email) as email,
    REGEXP_REPLACE(phone, '[^0-9]', '') as phone
FROM contacts;
```

### Data Transformation

```sql
-- Create derived columns
SELECT
    name,
    age,
    CASE
        WHEN age < 18 THEN 'Minor'
        WHEN age < 65 THEN 'Adult'
        ELSE 'Senior'
    END as age_group
FROM users;

-- Date operations
SELECT
    order_date,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    DATE_TRUNC('month', order_date) as month_start
FROM orders;
```

### Multi-File Analysis

```sql
-- Combine multiple CSV files
SELECT * FROM read_csv('sales_*.csv');

-- Join files from different formats
SELECT
    u.name,
    o.order_id,
    o.amount
FROM read_csv('users.csv') u
JOIN read_parquet('orders.parquet') o
    ON u.user_id = o.user_id;
```

### Data Quality Checks

```sql
-- Check for duplicates
SELECT user_id, COUNT(*)
FROM users
GROUP BY user_id
HAVING COUNT(*) > 1;

-- Find missing values
SELECT
    COUNT(*) as total_rows,
    COUNT(name) as name_count,
    COUNT(*) - COUNT(name) as name_missing,
    COUNT(email) as email_count,
    COUNT(*) - COUNT(email) as email_missing
FROM users;

-- Value distribution
SELECT age, COUNT(*) as frequency
FROM users
GROUP BY age
ORDER BY frequency DESC;
```

## Integration with Python and R

While this skill focuses on the CLI, DuckDB integrates seamlessly with programming languages:

**Python:**

```python
import duckdb
con = duckdb.connect('my_db.duckdb')
result = con.execute("SELECT * FROM users").df()  # Returns pandas DataFrame
```

**R:**

```r
library(DBI)
con <- dbConnect(duckdb::duckdb(), "my_db.duckdb")
result <- dbGetQuery(con, "SELECT * FROM users")
```

## Troubleshooting

### Common Issues

**"Table does not exist" errors:**

- Verify file path is correct
- Use absolute paths or ensure working directory is correct
- Check file format matches read function (read_csv vs read_parquet)

**Memory errors:**

- Use persistent database instead of :memory:
- Reduce dataset size with WHERE clauses or sampling
- Set memory limit: `SET memory_limit = '2GB';`

**Performance issues:**

- Use EXPLAIN to check query plan
- Ensure proper indexes on join columns
- Use appropriate file formats (Parquet > CSV for large data)
- Consider partitioning large files

**Character encoding issues:**

- Specify encoding in read_csv: `encoding='UTF-8'`
- Use `normalize_names=true` for column name cleanup

## Best Practices

1. **Start with exploration**: Use `LIMIT` and sampling for initial analysis
2. **Use appropriate formats**: Parquet for large datasets, CSV for small/human-readable
3. **Leverage partitioning**: Organize large datasets by date, category, etc.
4. **Test queries incrementally**: Build complex queries step-by-step
5. **Save intermediate results**: Create tables/views for multi-step analysis
6. **Use CTEs for readability**: Break complex queries into named steps
7. **Configure .duckdbrc**: Set preferred defaults for consistent experience
8. **Check query plans**: Use EXPLAIN for performance-critical queries
9. **Version control SQL**: Save reusable queries in .sql files
10. **Document complex queries**: Add comments with `--` or `/* */`

## Resources and References

### Official Documentation

- [DuckDB Documentation](https://duckdb.org/docs/)
- [CLI Reference](https://duckdb.org/docs/clients/cli/overview)
- [SQL Introduction](https://duckdb.org/docs/sql/introduction)
- [Data Import](https://duckdb.org/docs/data/overview)

### Additional Learning

- [Grant McDermott's DuckDB Guide](https://grantmcdermott.com/duckdb-polars/duckdb-sql.html)
- DuckDB Blog for latest features and use cases
- Community examples on GitHub

## Quick Reference Card

```sql
-- Launch CLI
duckdb                           # In-memory
duckdb mydb.duckdb              # Persistent

-- Read files
SELECT * FROM read_csv('file.csv');
SELECT * FROM read_parquet('file.parquet');
SELECT * FROM read_json('file.json');

-- Export data
COPY (...) TO 'output.csv' (HEADER);
COPY (...) TO 'output.parquet' (FORMAT PARQUET);

-- Dot commands
.help                           # Show help
.tables                         # List tables
.schema table_name              # Show schema
.mode csv                       # CSV output
.output file.txt                # Redirect output
.read script.sql                # Run SQL file
.exit                           # Quit

-- Useful settings
SET threads = 4;
SET memory_limit = '4GB';
SET enable_progress_bar = true;

-- Query optimization
EXPLAIN query;                  # Show plan
USING SAMPLE 1%;               # Sample data
GROUP BY ALL;                   # Auto-group
```

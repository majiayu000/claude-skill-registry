---
name: duckdb-data-explorer
description: This skill should be used when performing local data exploration, profiling, quality analysis, or transformation tasks using DuckDB. It handles CSV, Parquet, and JSON files, provides automated data quality reports, supports complex JSON transformations, and generates interactive HTML reports for data analysis.
---

# DuckDB Data Explorer

## Overview

This skill enables comprehensive local data exploration using DuckDB, supporting automated data profiling, quality analysis, and transformation workflows for CSV, Parquet, and JSON files. It provides reusable scripts for common data tasks, reference patterns for complex queries, and HTML report generation for interactive data visualization.

## Quick Start

### Basic Data Profiling
To quickly analyze a data file and generate a quality report:

1. Use `scripts/data_profiler.py` to profile the file:
   ```bash
   python scripts/data_profiler.py data.csv --output profile.json
   ```

2. Generate an HTML report:
   ```bash
   python scripts/html_report_generator.py profile.json report.html
   ```

3. Open the HTML report to view data quality metrics, null analysis, and sample data.

### JSON Data Transformation
For complex JSON handling and transformation:

1. Analyze JSON structure:
   ```bash
   python scripts/json_transformer.py structure data.json
   ```

2. Transform JSON data:
   ```bash
   python scripts/json_transformer.py transform "*.json" "SELECT json_extract(data, '$.user.name') as name FROM json_data" --output transformed.parquet
   ```

## Core Capabilities

### 1. Data Profiling and Quality Analysis

Use `scripts/data_profiler.py` for automated data quality assessment:

- **Null analysis**: Percentage of null values per column
- **Data type detection**: Automatic type inference and validation
- **Uniqueness analysis**: Distinct value counts and percentages
- **Sample data**: First 10 rows for quick inspection
- **Summary statistics**: Row counts, column counts, file type detection

**When to use**: Initial data exploration, data quality assessment, before data cleaning or transformation.

### 2. Complex JSON Handling

Use `scripts/json_transformer.py` for advanced JSON operations:

- **Structure analysis**: Understand nested JSON schemas
- **Pattern matching**: Extract specific fields from complex JSON
- **Array operations**: Flatten and transform JSON arrays
- **Multi-file processing**: Handle glob patterns like `*.json`
- **Export options**: Output to Parquet or JSON formats

**When to use**: Working with nested JSON data, API responses, log files, or document databases.

### 3. Interactive HTML Reports

Use `scripts/html_report_generator.py` to create visual data exploration reports:

- **Summary dashboards**: Key metrics at a glance
- **Column analysis**: Detailed null percentage bars with color coding
- **Sample data viewer**: Scrollable data tables with copy functionality
- **Quality indicators**: Visual quality scores for each column
- **Responsive design**: Works on desktop and mobile devices

**When to use**: Sharing data insights, creating documentation, or interactive data exploration.

### 4. DuckDB Query Patterns

Reference `references/duckdb_patterns.md` for common query patterns:

- **File reading**: CSV, Parquet, JSON ingestion patterns
- **Data quality**: Null analysis, type validation, duplicate detection
- **Transformation**: String operations, date handling, JSON extraction
- **Performance**: Optimization tips and best practices

**When to use**: Writing custom DuckDB queries, optimizing performance, learning DuckDB syntax.

### 5. JSON Function Reference

Reference `references/json_functions.md` for comprehensive JSON function documentation:

- **Extraction functions**: `json_extract`, `json_extract_string`, etc.
- **Array operations**: `json_array_length`, `json_contains`, etc.
- **Structure analysis**: `json_structure`, `json_type`, etc.
- **Advanced patterns**: Nested object handling, conditional operations

**When to use**: Complex JSON transformations, API data processing, nested data extraction.

### 6. Data Quality Framework

Reference `references/data_quality_checks.md` for comprehensive quality assessment:

- **Null analysis**: Multi-dimensional null value reporting
- **Type validation**: Consistency checking and conflict detection
- **Outlier detection**: Statistical methods for anomaly identification
- **Duplicate analysis**: Record and column-level duplication detection
- **Quality scoring**: Automated quality assessment metrics

**When to use**: Data quality audits, data cleaning workflows, data validation pipelines.

## Workflow Examples

### Example 1: Initial Data Exploration
```bash
# Profile a new dataset
python scripts/data_profiler.py sales_data.csv --output sales_profile.json

# Generate interactive report
python scripts/html_report_generator.py sales_profile.json sales_report.html

# Open report for exploration
open sales_report.html
```

### Example 2: JSON Data Transformation
```bash
# Analyze JSON structure
python scripts/json_transformer.py structure api_responses.json

# Transform and flatten JSON data
python scripts/json_transformer.py transform "logs/*.json" \
  "SELECT 
    json_extract(data, '$.timestamp') as timestamp,
    json_extract(data, '$.user.id') as user_id,
    json_extract(data, '$.event.type') as event_type
   FROM json_data" \
  --output cleaned_logs.parquet
```

### Example 3: Data Quality Assessment
```bash
# Profile data for quality issues
python scripts/data_profiler.py customer_data.parquet --output quality_profile.json

# Generate detailed quality report
python scripts/html_report_generator.py quality_profile.json quality_report.html

# Use reference queries for deeper analysis
duckdb :memory: "SELECT * FROM read_parquet('customer_data.parquet') LIMIT 10"
```

## File Type Support

### CSV Files
- Auto-detection of delimiters, headers, and data types
- Custom configuration support for non-standard formats
- Multiple file ingestion with glob patterns

### Parquet Files
- Columnar format optimization
- Schema preservation and type inference
- Efficient handling of large datasets

### JSON Files
- Auto-detection of JSON structure
- Support for nested objects and arrays
- Multi-file processing with glob patterns
- Complex JSON function support

## Integration Patterns

### With PostgreSQL Export
When exporting to PostgreSQL for analysis:

1. **Profile before export**: Use data profiler to understand data quality
2. **Transform to Parquet**: Clean and transform data locally first
3. **Export to PostgreSQL**: Use DuckDB's PostgreSQL extension or export Parquet
4. **Validate export**: Compare profiles before and after export

### Batch Processing
For processing multiple files:

```bash
# Process all CSV files in directory
for file in data/*.csv; do
  python scripts/data_profiler.py "$file" --output "profiles/$(basename "$file" .csv).json"
  python scripts/html_report_generator.py "profiles/$(basename "$file" .csv).json" "reports/$(basename "$file" .csv).html"
done
```

## Resources

### scripts/
Executable Python scripts for data operations:

- **`data_profiler.py`**: Automated data quality analysis and profiling
- **`json_transformer.py`**: Complex JSON handling and transformation utilities  
- **`html_report_generator.py`**: Interactive HTML report generation

### references/
Comprehensive documentation for DuckDB operations:

- **`duckdb_patterns.md`**: Common query patterns and best practices
- **`json_functions.md`**: Complete JSON function reference with examples
- **`data_quality_checks.md`**: Data quality assessment frameworks and queries

### assets/
Templates and resources for output generation:

- **`report_template.html`**: Interactive HTML template for data exploration reports

## Best Practices

1. **Start with profiling**: Always profile data before transformation
2. **Use HTML reports**: Generate interactive reports for better insights
3. **Leverage patterns**: Use reference patterns for common operations
4. **Validate transformations**: Profile data before and after transformations
5. **Handle nulls explicitly**: Use DuckDB's null handling functions
6. **Optimize queries**: Use column pruning and early filtering
7. **Document processes**: Keep track of transformations for reproducibility
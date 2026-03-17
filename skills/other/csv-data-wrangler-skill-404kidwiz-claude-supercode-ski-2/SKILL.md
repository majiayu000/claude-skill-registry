---
name: csv-data-wrangler
description: Expert in high-performance CSV processing, parsing, and data cleaning using Python, DuckDB, and command-line tools. Use when working with CSV files, cleaning data, transforming datasets, or processing large tabular data files.
---

# CSV Data Wrangler

## Purpose
Provides expertise in efficient CSV file processing, data cleaning, and transformation. Handles large files, encoding issues, malformed data, and performance optimization for tabular data workflows.

## When to Use
- Processing large CSV files efficiently
- Cleaning and validating CSV data
- Transforming and reshaping datasets
- Handling encoding and delimiter issues
- Merging or splitting CSV files
- Converting between tabular formats
- Querying CSV with SQL (DuckDB)

## Quick Start
**Invoke this skill when:**
- Processing large CSV files efficiently
- Cleaning and validating CSV data
- Transforming and reshaping datasets
- Handling encoding and delimiter issues
- Querying CSV with SQL

**Do NOT invoke when:**
- Building Excel files with formatting (use xlsx-skill)
- Statistical analysis of data (use data-analyst)
- Building data pipelines (use data-engineer)
- Database operations (use sql-pro)

## Decision Framework
```
Tool Selection by File Size:
├── < 100MB → pandas
├── 100MB - 1GB → pandas with chunking or polars
├── 1GB - 10GB → DuckDB or polars
├── > 10GB → DuckDB, Spark, or streaming
└── Quick exploration → csvkit or xsv CLI

Processing Type:
├── SQL-like queries → DuckDB
├── Complex transforms → pandas/polars
├── Simple filtering → csvkit/xsv
└── Streaming → Python csv module
```

## Core Workflows

### 1. Large CSV Processing
1. Profile file (size, encoding, delimiter)
2. Choose appropriate tool for scale
3. Process in chunks if memory-constrained
4. Handle encoding issues (UTF-8, Latin-1)
5. Validate data types per column
6. Write output with proper quoting

### 2. Data Cleaning Pipeline
1. Load sample to understand structure
2. Identify missing and malformed values
3. Define cleaning rules per column
4. Apply transformations
5. Validate output quality
6. Log cleaning statistics

### 3. CSV Query with DuckDB
1. Point DuckDB at CSV file(s)
2. Let DuckDB infer schema
3. Write SQL queries directly
4. Export results to new CSV
5. Optionally persist as Parquet

## Best Practices
- Always specify encoding explicitly
- Use chunked reading for large files
- Profile before choosing tools
- Preserve original files, write to new
- Validate row counts before/after
- Handle quoted fields and escapes properly

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Loading all to memory | OOM on large files | Use chunking or streaming |
| Guessing encoding | Corrupted characters | Detect with chardet first |
| Ignoring quoting | Broken field parsing | Use proper CSV parser |
| No validation | Silent data corruption | Validate row/column counts |
| Manual string splitting | Breaks on edge cases | Use csv module or pandas |

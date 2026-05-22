---
name: csv-parser
description: Parse and analyze CSV files with data validation
---

# CSV Parser Skill

You are a CSV file analysis assistant from the example-plugin.

## Capabilities

- Parse CSV files with various delimiters
- Validate data types and constraints
- Generate summary statistics
- Detect encoding issues
- Handle malformed data gracefully

## Usage

To analyze a CSV file, provide the file path as an argument:

```
Arguments: $ARGUMENTS
```

## Output Format

The analysis will include:
- Row count and column count
- Column names and inferred data types
- Missing value report
- Basic statistics for numeric columns
- Encoding and delimiter detection results

## Example

Input: data.csv
Output: Analysis report with statistics and validation results

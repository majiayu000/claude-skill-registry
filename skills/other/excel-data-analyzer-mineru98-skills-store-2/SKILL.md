---
name: excel-data-analyzer
description: Analyze messy and unstructured Excel files to identify data quality issues, detect format inconsistencies, find missing values, and generate comprehensive analysis reports. Use when Claude needs to work with Excel files (.xlsx, .xls) for data quality assessment, structure analysis, or when users request data auditing, cleaning recommendations, or statistical summaries of spreadsheet data.
---

# Excel Data Analyzer

## Overview

Analyze Excel files to identify data structure, quality issues, format inconsistencies, and statistical patterns. Generate comprehensive markdown reports with actionable insights for data cleaning and improvement.

## Quick Start

Analyze any Excel file with a single command:

```bash
cd /path/to/skill/scripts
bun install  # First time only
bun run analyze_excel.ts /path/to/data.xlsx
```

Output: Markdown report (`data_analysis.md`) with complete analysis.

## Core Capabilities

### 1. Data Structure Detection

Automatically identifies:
- Column names and data types (integer, float, string, date, email, boolean, mixed)
- Row and column counts per sheet
- Distinct value counts
- Sample values for quick inspection

### 2. Data Quality Analysis

Detects quality issues:
- **Missing values:** Percentage and count of nulls per column
- **High null columns:** Flags columns with >50% missing data
- **Mixed data types:** Identifies columns with inconsistent types
- **Format issues:** Detects leading/trailing whitespace, inconsistent casing, numeric strings

### 3. Statistical Summaries

Generates statistics for numeric columns:
- Min, max, mean, median, standard deviation
- **Outlier detection:** Values beyond 3 standard deviations
- **Value distribution:** Top 10 most frequent values with counts

For text columns:
- Min/max/average length
- Value frequency distribution

### 4. Quality Scoring

Assigns quality scores (0-100) based on:
- Missing headers: -10 points
- High null percentage columns: -15 points
- Format inconsistencies: -10 points
- Duplicate column names: -15 points

### 5. Multi-Sheet Support

Analyzes all sheets in workbook:
- Per-sheet quality scores
- Sheet-by-sheet column analysis
- Overall workbook quality score

## Usage

### Basic Analysis

```bash
bun run analyze_excel.ts data.xlsx
```

Generates: `data_analysis.md`

### Custom Output Path

```bash
bun run analyze_excel.ts data.xlsx --output reports/audit.md
```

### First-Time Setup

Before running analysis scripts:

```bash
cd /path/to/excel-data-analyzer/scripts
bun install
```

This installs required dependencies (xlsx library).

## Workflow

When a user provides an Excel file for analysis:

1. **Run the analysis script** on the provided file
2. **Read the generated report** to understand findings
3. **Summarize key issues** for the user:
   - Overall quality score
   - Most critical issues (missing values, format problems)
   - Columns requiring attention
4. **Provide recommendations** based on analysis:
   - Which columns to investigate
   - Suggested cleaning strategies
   - Priority of fixes (high/medium/low)

## Report Structure

Generated markdown reports include:

### Executive Summary
- File metadata (name, size, sheets)
- Overall quality score
- High-level findings

### Per-Sheet Analysis
- Dimensions (rows × columns)
- Quality score
- Detected issues list
- Column analysis table (type, distinct values, missing %, issues)

### Detailed Column Information
For each column:
- Data type classification
- Missing value statistics
- Sample values
- Format issues (if any)
- Statistical summaries (numeric columns)
- Value distributions

## Common Data Issues

### High Priority Issues

**Mixed data types:**
- Column contains numbers, strings, and dates
- Prevents proper analysis
- Example: `123`, `"abc"`, `2023-01-15`

**High missing percentage (>50%):**
- Column has insufficient data
- Consider dropping or imputing

**Duplicate column names:**
- Creates ambiguity in analysis
- Requires renaming

### Medium Priority Issues

**Numeric strings:**
- Numbers stored as text: `"123"` instead of `123`
- Prevents calculations

**Format inconsistencies:**
- Leading/trailing whitespace: `" value "`
- Inconsistent casing: `"john"`, `"JOHN"`, `"John"`
- Mixed date formats: `"2023-01-15"`, `"01/15/2023"`

**Outliers:**
- Values beyond 3 standard deviations
- May indicate errors or special cases
- Requires investigation

### Low Priority Issues

**Missing headers:**
- Empty column names
- Generates systematic names (Column_1, Column_2)

**Text length variations:**
- Wide range in string lengths
- May indicate data entry inconsistencies

## Advanced Patterns

For detailed information on data quality patterns and detection methods, see:

**references/analysis-patterns.md** - Comprehensive guide covering:
- Data type issues (mixed types, numeric strings, date formats)
- Missing data patterns (high missing %, sparse data, placeholders)
- Format inconsistencies (whitespace, casing, delimiters)
- Statistical anomalies (outliers, skewed distributions)
- Structural issues (duplicate names, empty rows/columns)
- Domain-specific patterns (emails, phone numbers, dates)
- Encoding issues (character encoding, Unicode)

Consult this reference when encountering unusual patterns or needing deeper analysis strategies.

## Output Interpretation

### Quality Score Ranges

- **90-100:** Excellent - minimal issues
- **70-89:** Good - minor format issues
- **50-69:** Fair - significant quality concerns
- **Below 50:** Poor - major data problems

### Prioritizing Fixes

1. **First:** Address structural issues (duplicate columns, missing headers)
2. **Second:** Fix high missing value columns (>50%)
3. **Third:** Resolve mixed data types
4. **Fourth:** Clean format inconsistencies
5. **Fifth:** Investigate outliers

## Performance

Optimized for large files:
- **Bun runtime:** Fast JavaScript execution
- **Streaming support:** Memory-efficient for large datasets
- **xlsx library:** Industry-standard Excel parsing

Typical performance:
- Small files (<1MB): <1 second
- Medium files (1-100MB): 1-10 seconds
- Large files (>100MB): 10-60 seconds

## Limitations

- Only generates analysis reports (does not perform data cleaning)
- Text-based analysis (does not interpret business context)
- Statistical methods assume numeric data for quantitative analysis
- Outlier detection uses simple 3-sigma rule (not robust methods)

## Resources

### scripts/

**analyze_excel.ts** - Main analysis script (Bun/TypeScript)
- Parses Excel files using xlsx library
- Detects data types and quality issues
- Generates statistical summaries
- Produces markdown reports

**package.json** - Bun dependencies
- xlsx: Excel file parsing

### references/

**analysis-patterns.md** - Comprehensive guide to data quality patterns
- Detailed detection methods
- Impact assessments
- Recommendations for each issue type

### assets/

**report-template.md** - Markdown report template structure
- Shows expected output format
- Reference for understanding report sections

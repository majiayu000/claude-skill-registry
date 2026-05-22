---
name: xsv
description: Use xsv for fast CSV data processing with selection, filtering, statistics, joining, sorting, and indexing for high-performance data manipulation.
---
# xsv - CSV Command Line Toolkit Skill

You are a CSV data manipulation specialist using `xsv`, a fast command-line CSV toolkit written in Rust. This skill provides comprehensive guidance for processing, analyzing, and transforming CSV data efficiently.

## Why xsv?

`xsv` is designed for high-performance CSV operations:
- **Extremely fast**: Rust-based, optimized for speed
- **Low memory**: Streaming operations when possible
- **Rich features**: 20+ commands for CSV manipulation
- **Indexing**: Create indexes for faster random access
- **Composable**: Unix philosophy - pipe commands together

## Core Capabilities

1. **Selection**: select, headers, slice, sample
2. **Searching**: search, frequency
3. **Analysis**: stats, frequency, count
4. **Transformation**: fmt, fixlengths, flatten
5. **Combination**: join, cat
6. **Sorting**: sort
7. **Display**: table
8. **Splitting**: split
9. **Performance**: index

## Quick Start

### View CSV Data as Table

```bash
xsv table data.csv
xsv table data.csv | less -S

# Limit field width for readability
xsv table -c 20 data.csv
```

### Count Rows

```bash
xsv count data.csv
```

### View Headers

```bash
xsv headers data.csv
```

### Select Columns

```bash
xsv select 1,3,5 data.csv
xsv select Name,Email,Age data.csv
```

## Essential Commands

### headers - View Column Names

```bash
# Show all column names with indices
xsv headers data.csv

# Output format:
# 1   Name
# 2   Email
# 3   Age
```

**Use case**: Understand CSV structure before operations

### count - Count Records

```bash
# Count records (excluding header)
xsv count data.csv

# Count with index (much faster)
xsv count data.csv.idx
```

**Performance**: O(1) with index, O(n) without

### select - Select Columns

```bash
# By index (1-based)
xsv select 1,3,5 data.csv

# By name
xsv select Name,Email,Age data.csv

# Column ranges
xsv select 1-4 data.csv
xsv select Name-Age data.csv

# From column to end
xsv select 3- data.csv

# Exclude columns
xsv select '!1-2' data.csv

# Reorder and duplicate
xsv select 3,1,2,1 data.csv

# Disambiguate duplicate column names
xsv select 'Name[0],Name[1],Name[2]' data.csv

# Quote names with special characters
xsv select '"Date - Opening","Date - Closing"' data.csv
```

**Common options**:
- `-o, --output <file>`: Write to file
- `-n, --no-headers`: Treat first row as data
- `-d, --delimiter <char>`: Input delimiter (default: ,)

### search - Filter Rows by Regex

```bash
# Basic search
xsv search "pattern" data.csv

# Case insensitive
xsv search -i "pattern" data.csv

# Search specific columns
xsv search -s Email "gmail.com" data.csv
xsv search -s 1,3,5 "pattern" data.csv

# Invert match (exclude matching rows)
xsv search -v "pattern" data.csv

# Save results
xsv search "active" data.csv -o active_users.csv
```

**Use case**: Filter CSV rows like grep

### slice - Extract Row Ranges

```bash
# First 10 rows
xsv slice -l 10 data.csv

# Rows 100-200
xsv slice -s 100 -e 200 data.csv

# Start at row 50, take 20 rows
xsv slice -s 50 -l 20 data.csv

# Last 10 rows (requires index)
xsv count data.csv  # Get total
xsv slice -s -10 data.csv

# Single row
xsv slice -i 42 data.csv
```

**Performance**: Much faster with index

### stats - Compute Statistics

```bash
# Basic stats (mean, min, max, stddev)
xsv stats data.csv

# All statistics (includes median, mode, cardinality)
xsv stats --everything data.csv

# Specific columns
xsv stats -s Age,Salary data.csv

# Include median (requires memory)
xsv stats --median data.csv

# Include mode
xsv stats --mode data.csv

# Include cardinality (unique count)
xsv stats --cardinality data.csv

# Parallel processing
xsv stats -j 4 data.csv

# Output as table
xsv stats data.csv | xsv table
```

**Output fields**: field, type, sum, min, max, mean, stddev, median, mode, cardinality

### frequency - Frequency Tables

```bash
# Top 10 values per column
xsv frequency data.csv

# Specific columns
xsv frequency -s Status,Category data.csv

# Top 20 values
xsv frequency -l 20 data.csv

# All values (no limit)
xsv frequency -l 0 data.csv

# Ascending order
xsv frequency --asc data.csv

# Exclude nulls
xsv frequency --no-nulls data.csv

# View as table
xsv frequency -s Status data.csv | xsv table
```

**Output**: field, value, count

**Use case**: Value distribution analysis

### sort - Sort Records

```bash
# Sort by first column
xsv sort data.csv

# Sort by specific columns
xsv sort -s Age data.csv
xsv sort -s LastName,FirstName data.csv

# Numeric sort
xsv sort -s Age -N data.csv

# Reverse order
xsv sort -s Age -R data.csv

# Numeric + reverse
xsv sort -s Salary -N -R data.csv

# Save sorted
xsv sort -s Name data.csv -o sorted.csv
```

**Note**: Requires reading entire file into memory

### join - Join Two CSV Files

```bash
# Inner join
xsv join ID users.csv ID orders.csv

# Left outer join
xsv join --left ID users.csv ID orders.csv

# Right outer join
xsv join --right ID users.csv ID orders.csv

# Full outer join
xsv join --full ID users.csv ID orders.csv

# Case-insensitive join
xsv join --no-case Email users.csv Email contacts.csv

# Join on multiple columns
xsv join 'ID,Date' file1.csv 'ID,Date' file2.csv

# Include nulls in join
xsv join --nulls ID file1.csv ID file2.csv

# Cross join (cartesian product)
xsv join --cross 1 file1.csv 1 file2.csv

# Save result
xsv join ID users.csv ID orders.csv -o joined.csv
```

**Join types**:
- Default: Inner join (intersection)
- `--left`: Left outer join
- `--right`: Right outer join
- `--full`: Full outer join
- `--cross`: Cartesian product (use with caution)

### table - Format as Aligned Table

```bash
# Basic table
xsv table data.csv

# With pager
xsv table data.csv | less -S

# Minimum column width
xsv table -w 10 data.csv

# Padding between columns
xsv table -p 4 data.csv

# Limit field length
xsv table -c 20 data.csv

# Combine limits
xsv slice -l 50 data.csv | xsv table -c 30
```

**Note**: Requires buffering entire file into memory

### sample - Random Sampling

```bash
# Sample 100 rows
xsv sample 100 data.csv

# Sample 10% of large file
xsv count data.csv  # e.g., 1000000
xsv sample 100000 data.csv

# Save sample
xsv sample 1000 large.csv -o sample.csv

# Sample then analyze
xsv sample 10000 huge.csv | xsv stats --everything
```

**Performance**: Uses indexing for samples <10% of total

### fmt - Format Output

```bash
# Convert to TSV
xsv fmt -t '\t' data.csv -o data.tsv

# Convert to pipe-delimited
xsv fmt -t '|' data.csv

# Add CRLF line endings
xsv fmt --crlf data.csv -o windows.csv

# Quote all fields
xsv fmt --quote-always data.csv

# Custom quote character
xsv fmt --quote "'" data.csv

# Custom escape character
xsv fmt --escape '\\' data.csv
```

### cat - Concatenate Files

```bash
# Concatenate by rows (vertically)
xsv cat rows file1.csv file2.csv file3.csv

# Concatenate by columns (horizontally)
xsv cat columns file1.csv file2.csv

# Pad with empty values if different lengths
xsv cat rows-columns file1.csv file2.csv
```

### split - Split Into Multiple Files

```bash
# Split into files of 1000 rows each
xsv split -s 1000 output_dir data.csv

# Creates: output_dir/0.csv, output_dir/1.csv, etc.
```

### flatten - Show One Field Per Line

```bash
# Flatten first record
xsv slice -i 0 data.csv | xsv flatten

# Output format:
# field,value
# Name,John Doe
# Email,john@example.com
# Age,30
```

### fixlengths - Fix Inconsistent Row Lengths

```bash
# Ensure all rows have same number of fields
xsv fixlengths data.csv -o fixed.csv

# Pads short rows with empty fields
# Useful for malformed CSVs
```

### index - Create Index for Performance

```bash
# Create index
xsv index data.csv

# Creates: data.csv.idx

# Now operations are faster:
xsv count data.csv      # O(1) instead of O(n)
xsv slice -i 1000 data.csv  # Direct access
xsv sample 100 data.csv     # Fast random access
```

**When to index**:
- Large files (>100MB)
- Multiple operations on same file
- Random access patterns (slice, sample)
- Statistics with parallel processing

## Common Workflows

### Workflow 1: Data Exploration

```bash
# 1. Understand structure
xsv headers data.csv

# 2. Count records
xsv count data.csv

# 3. View sample
xsv slice -l 10 data.csv | xsv table

# 4. Get statistics
xsv stats data.csv | xsv table

# 5. Check value distributions
xsv frequency -s Status data.csv | xsv table
```

### Workflow 2: Data Filtering and Selection

```bash
# 1. Select relevant columns
xsv select Name,Email,Age,Status data.csv |

# 2. Filter active users
xsv search -s Status "active" |

# 3. Filter by age
xsv search -s Age "^[3-9][0-9]$" |

# 4. Save result
xsv -o active_users_30plus.csv
```

### Workflow 3: Data Analysis Pipeline

```bash
# 1. Create index for performance
xsv index large_data.csv

# 2. Sample for quick analysis
xsv sample 10000 large_data.csv |

# 3. Select columns of interest
xsv select Revenue,Region,Product |

# 4. Get statistics
xsv stats --everything |

# 5. View as table
xsv table
```

### Workflow 4: Data Joining

```bash
# 1. Join users with orders
xsv join UserID users.csv UserID orders.csv |

# 2. Select relevant columns
xsv select 'UserName,Email,OrderID,OrderDate,Amount' |

# 3. Sort by amount
xsv sort -s Amount -N -R |

# 4. Top 100 orders
xsv slice -l 100 |

# 5. Format and save
xsv table -o top_orders.txt
```

### Workflow 5: Data Cleaning

```bash
# 1. Fix row lengths
xsv fixlengths messy.csv |

# 2. Select valid columns
xsv select 1-10 |

# 3. Remove rows with empty email
xsv search -s Email '.+' |

# 4. Sort and deduplicate (using uniq)
xsv sort -s Email |
uniq |

# 5. Save cleaned data
xsv -o cleaned.csv
```

### Workflow 6: Data Transformation

```bash
# 1. Select and reorder columns
xsv select 'LastName,FirstName,Email,Phone' data.csv |

# 2. Convert to TSV
xsv fmt -t '\t' |

# 3. Save
xsv -o output.tsv
```

### Workflow 7: Large File Processing

```bash
# 1. Create index first
xsv index huge_file.csv

# 2. Get quick count
xsv count huge_file.csv

# 3. Sample for analysis
xsv sample 50000 huge_file.csv |

# 4. Analyze sample
xsv stats --everything |

# 5. View results
xsv table
```

## Performance Tips

### 1. Create Indexes for Large Files

```bash
# One-time cost, speeds up many operations
xsv index large.csv
```

**Speeds up**:
- `count` (O(1) instead of O(n))
- `slice` (direct access)
- `sample` (efficient random access)
- `stats -j` (parallel processing)

### 2. Use Streaming Operations

These don't require reading entire file into memory:
- `select`
- `search`
- `slice` (with index)
- `headers`
- `count` (with index)

### 3. Avoid Memory-Intensive Operations on Large Files

These require full file in memory:
- `sort`
- `table`
- `stats --median`
- `stats --mode`
- `frequency`

**Solution**: Use `sample` or `slice` first:
```bash
xsv sample 100000 huge.csv | xsv stats --everything
```

### 4. Parallel Processing

```bash
# Use multiple cores for stats
xsv stats -j 0 data.csv  # Auto-detect CPUs

# Specific job count
xsv stats -j 4 data.csv
```

**Requires**: Indexed file for best performance

### 5. Chain Commands Efficiently

```bash
# Good: streaming pipeline
xsv select Name,Age data.csv | xsv search -s Age "^[3-9]" | xsv table

# Less efficient: multiple file reads
xsv select Name,Age data.csv -o temp1.csv
xsv search -s Age "^[3-9]" temp1.csv -o temp2.csv
xsv table temp2.csv
```

## Advanced Patterns

### Pattern 1: Top N Analysis

```bash
# Top 10 customers by revenue
xsv sort -s Revenue -N -R customers.csv | xsv slice -l 10 | xsv table
```

### Pattern 2: Conditional Aggregation

```bash
# Count by status
xsv frequency -s Status -l 0 data.csv | xsv table

# Average age by region (requires external tools)
xsv select Region,Age data.csv | xsv sort -s Region | ...
```

### Pattern 3: Multi-Column Search

```bash
# Search across multiple columns
xsv select Name,Email,Phone data.csv | xsv search "pattern"
```

### Pattern 4: Data Validation

```bash
# Find rows with missing email
xsv search -s Email -v '.+' data.csv

# Find duplicates (by email)
xsv select Email data.csv | xsv sort | uniq -d
```

### Pattern 5: Data Comparison

```bash
# Find differences between two files
xsv select ID,Value file1.csv > temp1
xsv select ID,Value file2.csv > temp2
diff temp1 temp2
```

### Pattern 6: Column Statistics

```bash
# Stats for specific column
xsv select Age data.csv | xsv stats | xsv table

# Multiple column stats
xsv select Age,Salary,Score data.csv | xsv stats --everything | xsv table
```

## Common Options

Most commands support these options:

```bash
-h, --help              Display help
-o, --output <file>     Write to file instead of stdout
-n, --no-headers        First row is data, not headers
-d, --delimiter <char>  Input delimiter (default: ,)
```

## Delimiter Support

### Reading Different Formats

```bash
# TSV (tab-separated)
xsv select 1,3 -d '\t' data.tsv

# Pipe-delimited
xsv select Name,Age -d '|' data.txt

# Semicolon-delimited
xsv select 1-5 -d ';' data.csv
```

### Converting Formats

```bash
# TSV to CSV
xsv fmt -d '\t' data.tsv -o data.csv

# CSV to TSV
xsv fmt -t '\t' data.csv -o data.tsv

# CSV to pipe-delimited
xsv fmt -t '|' data.csv -o data.txt
```

## Error Handling

### Common Issues

**Issue**: "CSV error: record has different length"

**Solution**: Use `fixlengths`
```bash
xsv fixlengths data.csv -o fixed.csv
```

**Issue**: "No such file or directory"

**Solution**: Check file path, use absolute paths if needed

**Issue**: Out of memory with large file

**Solution**: Use sampling or indexing
```bash
xsv index large.csv
xsv sample 10000 large.csv | xsv stats
```

**Issue**: Column name not found

**Solution**: Check headers first
```bash
xsv headers data.csv
```

## Integration with Other Tools

### With jq (for CSV→JSON)

```bash
# Convert CSV to JSON
xsv select Name,Age data.csv | xsv fmt -t ',' | \
  python -c 'import csv, json, sys; print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)]))'
```

### With awk

```bash
# Add computed column
xsv select Price,Quantity data.csv | \
  awk -F, 'NR==1{print $0",Total"} NR>1{print $0","$1*$2}'
```

### With sort/uniq

```bash
# Deduplicate by column
xsv select Email data.csv | sort | uniq
```

### With grep

```bash
# Pre-filter before xsv
cat data.csv | grep "pattern" | xsv table
```

## Quick Reference

```bash
# View structure
xsv headers data.csv
xsv count data.csv
xsv slice -l 5 data.csv | xsv table

# Select columns
xsv select 1,3,5 data.csv
xsv select Name,Email data.csv

# Filter rows
xsv search "pattern" data.csv
xsv search -s Email "gmail" data.csv

# Statistics
xsv stats data.csv
xsv frequency -s Status data.csv

# Sort
xsv sort -s Age -N data.csv

# Join
xsv join ID file1.csv ID file2.csv

# Format
xsv table data.csv
xsv fmt -t '\t' data.csv

# Sample
xsv sample 1000 data.csv

# Index (for performance)
xsv index large.csv
```

## Comparison with xlsx

While `xlsx` handles Excel files, `xsv` is specialized for CSV:

| Feature | xsv | xlsx |
|---------|-----|------|
| Format | CSV only | XLSX/Excel |
| Speed | Extremely fast | Fast |
| Memory | Streaming | Depends on operation |
| Formulas | No | Yes |
| Formatting | No | Yes |
| Multiple sheets | No | Yes |
| Statistics | Rich | Basic |
| Joining | Yes | No |
| Indexing | Yes | No |

**When to use xsv**:
- Working with CSV data
- Need maximum performance
- Large file processing
- Statistical analysis
- Data pipelines

**When to use xlsx**:
- Excel file format required
- Need formulas and formatting
- Multiple sheets
- Cell-level operations

## Summary

**Primary tool**: `xsv` for fast CSV processing

**Most common commands**:
- `xsv headers` - Understand structure
- `xsv select` - Choose columns
- `xsv search` - Filter rows
- `xsv stats` - Analyze data
- `xsv table` - View formatted
- `xsv join` - Combine files
- `xsv index` - Speed up operations

**Key advantages**:
- Blazing fast (Rust-based)
- Composable (Unix pipes)
- Low memory (streaming)
- Rich analysis features
- Index support for large files

**Best practices**:
1. Index large files first
2. Use sampling for quick exploration
3. Chain commands with pipes
4. Check headers before operations
5. Use appropriate output formats

---
name: example-data-processor
description: Process CSV data files by cleaning, transforming, and analyzing them. Use this when users need to work with CSV files, clean data, or perform basic data analysis tasks.
---

# Example Data Processor

This skill demonstrates a complete skill structure with scripts, references, and proper documentation.

## What This Skill Does

Processes CSV data files with these capabilities:
- Clean and validate data
- Transform columns
- Generate summary statistics
- Export results

## Usage

### Process a CSV file

To process a CSV file:
```
Process the data in myfile.csv
```

The skill will:
1. Read the CSV file
2. Clean the data (remove nulls, fix formats)
3. Generate statistics
4. Output a summary report

### Custom Processing

For custom processing options:
```
Process sales.csv and group by region
```

## Scripts

**scripts/process_csv.py** - Main data processing script
- Reads CSV files
- Applies transformations
- Generates output

**scripts/fetch_data.py** - API data fetcher (demonstrates uv dependencies)
- Fetches data from APIs using requests
- Beautiful output formatting with rich
- **Auto-installs dependencies** via uv inline metadata (PEP 723)
- No manual pip install needed!

**scripts/validate.py** - Data validation script
- Checks data quality
- Reports issues

## Configuration

The scripts use these environment variables:
- `OUTPUT_DIR` - Where to save processed files (optional)
- `MAX_ROWS` - Maximum rows to process (optional)

Set them using:
```
Set OUTPUT_DIR to /path/to/output
```

## Reference Documentation

For detailed information:
- [Data Formats](references/formats.md) - Supported data formats and schemas
- [Examples](references/examples.md) - Common usage examples

## Troubleshooting

**"File not found" error:**
- Ensure the CSV file exists
- Provide the full path to the file

**"Invalid data" error:**
- Check the CSV format matches expected schema
- See [Data Formats](references/formats.md) for requirements

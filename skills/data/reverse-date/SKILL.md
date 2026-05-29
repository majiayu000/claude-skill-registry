---
name: reverse-date
description: Convert dates from various formats (like "21 Oct 2025", "October 21, 2025", "21/10/2025") to ISO format (YYYY-MM-DD). Use when users need to standardize date formats, convert human-readable dates to machine-readable formats, or reformat dates for data processing.
---

# Date Converter

## Overview

Convert dates from various human-readable formats into standardized ISO format (YYYY-MM-DD). This skill handles flexible date input parsing and provides consistent, machine-readable output.

## Usage

Use the `convert_date.py` script to convert any date string to YYYY-MM-DD format:

```bash
python scripts/convert_date.py "21 Oct 2025"
# Output: 2025-10-21
```

### Supported Input Formats

The script accepts a wide variety of date formats, including:

- **Month-day-year**: "21 Oct 2025", "October 21, 2025", "Oct 21, 2025"
- **Slash-separated**: "21/10/2025", "10/21/2025"
- **Dash-separated**: "21-10-2025", "2025-10-21"
- **Other common formats**: Most standard date representations

### Examples

```bash
# Human-readable format
python scripts/convert_date.py "21 Oct 2025"
# → 2025-10-21

# Full month name
python scripts/convert_date.py "October 21, 2025"
# → 2025-10-21

# Slash format
python scripts/convert_date.py "21/10/2025"
# → 2025-10-21

# Already in ISO format
python scripts/convert_date.py "2025-10-21"
# → 2025-10-21
```

### Error Handling

If the date string cannot be parsed, the script returns an error message:

```bash
python scripts/convert_date.py "invalid date"
# Error: Unable to parse date: 'invalid date'. Error: Unknown string format: invalid date
```

## Implementation Details

The script uses Python's `dateutil.parser` library for flexible date parsing, which handles many common date formats automatically. The output is always in ISO 8601 format (YYYY-MM-DD).
```
---
name: date-normalizer
description: Use when asked to parse, normalize, standardize, or convert dates from various formats to consistent ISO 8601 or custom formats.
---

# Date Normalizer

Parse and normalize dates from various formats into consistent, standardized formats for data cleaning and ETL pipelines.

## Purpose

Date standardization for:
- Data cleaning and ETL pipelines
- Database imports with mixed date formats
- Log file parsing and analysis
- International data harmonization
- Report generation with consistent dating

## Features

- **Smart Parsing**: Automatically detect and parse 100+ date formats
- **Format Conversion**: Convert to ISO 8601, US, EU, or custom formats
- **Batch Processing**: Normalize entire CSV columns
- **Ambiguity Detection**: Flag dates that could be interpreted multiple ways
- **Timezone Handling**: Convert and normalize timezones
- **Relative Dates**: Parse "today", "yesterday", "next week"
- **Validation**: Detect and report invalid dates

## Quick Start

```python
from date_normalizer import DateNormalizer

# Normalize single date
normalizer = DateNormalizer()
result = normalizer.normalize("03/14/2024")
print(result)  # {'normalized': '2024-03-14', 'format': 'iso8601'}

# Normalize to specific format
result = normalizer.normalize("March 14, 2024", output_format="us")
print(result)  # {'normalized': '03/14/2024', 'format': 'us'}

# Batch normalize CSV column
normalizer.normalize_csv(
    'data.csv',
    date_column='created_at',
    output='normalized.csv',
    output_format='iso8601'
)
```

## CLI Usage

```bash
# Normalize single date
python date_normalizer.py --date "March 14, 2024"

# Convert to specific format
python date_normalizer.py --date "14/03/2024" --format us

# Normalize CSV column
python date_normalizer.py --csv data.csv --column date --format iso8601 --output normalized.csv

# Detect ambiguous dates
python date_normalizer.py --date "01/02/03" --detect-ambiguous
```

## API Reference

### DateNormalizer

```python
class DateNormalizer:
    def normalize(self, date_string: str, output_format: str = 'iso8601',
                 dayfirst: bool = False, yearfirst: bool = False) -> Dict
    def normalize_batch(self, dates: List[str], **kwargs) -> List[Dict]
    def normalize_csv(self, csv_path: str, date_column: str,
                     output: str = None, **kwargs) -> str
    def detect_format(self, date_string: str) -> str
    def is_valid(self, date_string: str) -> bool
    def is_ambiguous(self, date_string: str) -> bool
    def parse_relative(self, relative_string: str) -> datetime
```

## Output Formats

**ISO 8601** (default):
```python
'2024-03-14'  # Date only
'2024-03-14T15:30:00'  # With time
'2024-03-14T15:30:00+00:00'  # With timezone
```

**US Format:**
```python
'03/14/2024'  # MM/DD/YYYY
```

**EU Format:**
```python
'14/03/2024'  # DD/MM/YYYY
```

**Long Format:**
```python
'March 14, 2024'
```

**Custom Format:**
```python
normalizer.normalize(date, output_format='%Y%m%d')  # '20240314'
```

## Supported Input Formats

**Numeric:**
- `2024-03-14` (ISO)
- `03/14/2024` (US)
- `14/03/2024` (EU)
- `14.03.2024` (German)
- `2024/03/14` (Japanese)
- `20240314` (Compact)

**Textual:**
- `March 14, 2024`
- `14 March 2024`
- `Mar 14, 2024`
- `14-Mar-2024`

**Relative:**
- `today`, `yesterday`, `tomorrow`
- `next week`, `last month`
- `2 days ago`, `in 3 weeks`

**With Time:**
- `2024-03-14 15:30:00`
- `03/14/2024 3:30 PM`
- `2024-03-14T15:30:00Z`

## Ambiguity Handling

Dates like `01/02/03` are ambiguous. Specify interpretation:

```python
# Day first (EU)
normalizer.normalize("01/02/03", dayfirst=True)
# Result: 2003-02-01

# Month first (US)
normalizer.normalize("01/02/03", dayfirst=False)
# Result: 2003-01-02

# Year first
normalizer.normalize("01/02/03", yearfirst=True)
# Result: 2001-02-03
```

## Use Cases

**Clean Messy Data:**
```python
messy_dates = [
    "March 14, 2024",
    "2024-03-15",
    "03/16/2024",
    "17-Mar-2024"
]

normalized = normalizer.normalize_batch(messy_dates)
# All converted to: ['2024-03-14', '2024-03-15', '2024-03-16', '2024-03-17']
```

**CSV Normalization:**
```python
# Input CSV with mixed date formats
# Convert all to ISO 8601
normalizer.normalize_csv(
    'orders.csv',
    date_column='order_date',
    output='orders_normalized.csv',
    output_format='iso8601'
)
```

**Validation:**
```python
if not normalizer.is_valid("invalid date"):
    print("Invalid date detected")
```

**Timezone Conversion:**
```python
normalizer.normalize(
    "2024-03-14 15:30:00+00:00",
    output_timezone='America/New_York'
)
```

## Limitations

- Cannot parse dates from images or PDFs (use OCR first)
- Ambiguous dates require manual specification of format
- Very old dates (<1900) may have limited support
- Non-Gregorian calendars not supported
- Some regional formats may need explicit configuration

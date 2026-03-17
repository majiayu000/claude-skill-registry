---
name: csv-wrangler
description: Handle messy CSVs with encoding detection, delimiter inference, and malformed row recovery.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# CSV-Wrangler

Patterns for handling real-world messy CSV files.

## Encoding Detection

```python
import chardet

def detect_encoding(file_path: str, sample_size: int = 10000) -> str:
    """Detect file encoding from sample."""
    with open(file_path, 'rb') as f:
        raw = f.read(sample_size)
    result = chardet.detect(raw)
    return result['encoding']

def read_with_encoding(path: str) -> pd.DataFrame:
    """Read CSV with auto-detected encoding."""
    encoding = detect_encoding(path)
    # Common fallback chain
    encodings = [encoding, 'utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue

    # Last resort: ignore errors
    return pd.read_csv(path, encoding='utf-8', errors='ignore')
```

## Delimiter Detection

```python
import csv

def detect_delimiter(file_path: str) -> str:
    """Detect CSV delimiter from file sample."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        sample = f.read(4096)

    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample, delimiters=',;\t|')
        return dialect.delimiter
    except csv.Error:
        # Count occurrences and pick most common
        counts = {d: sample.count(d) for d in [',', ';', '\t', '|']}
        return max(counts, key=counts.get)

def read_with_delimiter_detection(path: str) -> pd.DataFrame:
    """Read CSV with auto-detected delimiter."""
    delimiter = detect_delimiter(path)
    return pd.read_csv(path, sep=delimiter)
```

## Handling Malformed Rows

```python
def read_with_error_handling(path: str) -> tuple[pd.DataFrame, list[dict]]:
    """Read CSV, capturing malformed rows separately."""
    good_rows = []
    bad_rows = []

    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_cols = len(header)

        for line_num, row in enumerate(reader, start=2):
            if len(row) == expected_cols:
                good_rows.append(row)
            else:
                bad_rows.append({
                    'line': line_num,
                    'expected': expected_cols,
                    'actual': len(row),
                    'data': row
                })

    df = pd.DataFrame(good_rows, columns=header)
    return df, bad_rows

# Using pandas error_bad_lines (deprecated) / on_bad_lines
def read_skip_bad_lines(path: str) -> pd.DataFrame:
    """Read CSV, skipping malformed rows."""
    return pd.read_csv(
        path,
        on_bad_lines='skip',  # or 'warn' to see them
        engine='python'
    )
```

## Quoted Fields with Embedded Delimiters

```python
def read_quoted_csv(path: str) -> pd.DataFrame:
    """Handle CSVs with quoted fields containing delimiters."""
    return pd.read_csv(
        path,
        quotechar='"',
        doublequote=True,  # Handle "" as escaped quote
        escapechar='\\',   # Handle \, as escaped comma
        engine='python'
    )

# For really messy files
def read_regex_separated(path: str, pattern: str = r',(?=(?:[^"]*"[^"]*")*[^"]*$)') -> pd.DataFrame:
    """Split on delimiter only outside quotes using regex."""
    import re
    rows = []
    with open(path, 'r') as f:
        for line in f:
            rows.append(re.split(pattern, line.strip()))
    return pd.DataFrame(rows[1:], columns=rows[0])
```

## Header Detection

```python
def detect_header_row(path: str, max_rows: int = 10) -> int:
    """Find the header row in files with metadata at top."""
    with open(path, 'r') as f:
        lines = [f.readline() for _ in range(max_rows)]

    delimiter = detect_delimiter(path)

    for i, line in enumerate(lines):
        parts = line.split(delimiter)
        # Header likely has more columns than metadata
        # and contains text-like values
        if len(parts) > 2 and all(p.strip().replace('_', '').isalnum() for p in parts[:3]):
            return i

    return 0  # Default to first row

def read_with_header_detection(path: str) -> pd.DataFrame:
    """Read CSV, auto-detecting header row."""
    header_row = detect_header_row(path)
    return pd.read_csv(path, skiprows=header_row)
```

## Date Parsing

```python
def infer_date_columns(df: pd.DataFrame) -> list[str]:
    """Identify columns that look like dates."""
    date_cols = []
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',           # 2024-01-15
        r'\d{2}/\d{2}/\d{4}',           # 01/15/2024
        r'\d{2}-\d{2}-\d{4}',           # 15-01-2024
        r'\d{4}/\d{2}/\d{2}',           # 2024/01/15
    ]

    for col in df.columns:
        if df[col].dtype == 'object':
            sample = df[col].dropna().head(100)
            for pattern in date_patterns:
                if sample.str.match(pattern).mean() > 0.8:
                    date_cols.append(col)
                    break

    return date_cols

def parse_dates_flexibly(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Parse dates with multiple format attempts."""
    for col in columns:
        try:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        except:
            # Try common formats explicitly
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    df[col] = pd.to_datetime(df[col], format=fmt)
                    break
                except:
                    continue
    return df
```

## Numeric Cleaning

```python
def clean_numeric_column(series: pd.Series) -> pd.Series:
    """Clean numeric column with currency symbols, commas, etc."""
    if series.dtype == 'object':
        cleaned = (series
            .astype(str)
            .str.replace(r'[$€£¥,]', '', regex=True)  # Remove currency/commas
            .str.replace(r'\s+', '', regex=True)       # Remove whitespace
            .str.replace(r'\((.+)\)', r'-\1', regex=True)  # (123) -> -123
        )
        return pd.to_numeric(cleaned, errors='coerce')
    return series

def clean_all_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Attempt to convert object columns to numeric."""
    for col in df.select_dtypes(include=['object']).columns:
        converted = pd.to_numeric(df[col], errors='coerce')
        # Keep conversion if >80% success
        if converted.notna().mean() > 0.8:
            df[col] = converted
    return df
```

## Complete Wrangling Pipeline

```python
def wrangle_csv(path: str) -> tuple[pd.DataFrame, dict]:
    """Full pipeline for messy CSV handling."""
    report = {'issues': [], 'fixes': []}

    # Step 1: Detect encoding
    encoding = detect_encoding(path)
    report['encoding'] = encoding

    # Step 2: Detect delimiter
    delimiter = detect_delimiter(path)
    report['delimiter'] = delimiter

    # Step 3: Detect header row
    header_row = detect_header_row(path)
    if header_row > 0:
        report['fixes'].append(f"Skipped {header_row} metadata rows")

    # Step 4: Read with error handling
    try:
        df = pd.read_csv(
            path,
            encoding=encoding,
            sep=delimiter,
            skiprows=header_row,
            on_bad_lines='warn',
            engine='python'
        )
    except Exception as e:
        report['issues'].append(f"Read error: {e}")
        df = pd.read_csv(path, encoding='latin-1', on_bad_lines='skip')

    # Step 5: Clean column names
    df.columns = (df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[^\w]', '', regex=True)
    )
    report['fixes'].append("Normalized column names")

    # Step 6: Parse dates
    date_cols = infer_date_columns(df)
    if date_cols:
        df = parse_dates_flexibly(df, date_cols)
        report['fixes'].append(f"Parsed dates: {date_cols}")

    # Step 7: Clean numeric columns
    df = clean_all_numeric(df)

    report['shape'] = df.shape
    report['dtypes'] = df.dtypes.to_dict()

    return df, report
```

## Excel File Handling

```python
def read_excel_smart(path: str, sheet: str | int = 0) -> pd.DataFrame:
    """Read Excel with common cleanup."""
    df = pd.read_excel(
        path,
        sheet_name=sheet,
        engine='openpyxl',  # For .xlsx
        # engine='xlrd',    # For .xls
    )

    # Drop fully empty rows/columns
    df = df.dropna(how='all').dropna(axis=1, how='all')

    # Reset index after dropping
    df = df.reset_index(drop=True)

    return df

def list_excel_sheets(path: str) -> list[str]:
    """List all sheets in an Excel file."""
    xl = pd.ExcelFile(path)
    return xl.sheet_names
```

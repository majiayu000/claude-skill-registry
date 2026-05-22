---
name: google-sheets
description: Google Sheets automation using Python gspread library - reading, writing, formatting, and Service Account setup
---

# Google Sheets Automation

**Focus**: Automating Google Sheets with Python using gspread library

**Source**: Patterns from Meta Ads → Google Sheets automation project (ss-automation)

---

## When to Use This Skill

Use google-sheets when:
- ✓ Automating data export to Google Sheets
- ✓ Building dashboards that update from external data
- ✓ Creating scheduled reports in Sheets format
- ✓ Processing data from APIs and writing to Sheets
- ✓ Setting up Service Account authentication

**DO NOT use for:**
- ✗ Complex spreadsheet logic (use Google Apps Script for that)
- ✗ Real-time collaborative editing (Sheets UI is better)
- ✗ Simple one-time manual edits

---

## Why Python + gspread (Not Apps Script)

| Criteria | gspread + Python | Google Apps Script |
|----------|-----------------|-------------------|
| **External API integration** | ✅ Native (requests, SDKs) | ⚠️ UrlFetchApp (limited) |
| **Data manipulation** | ✅ pandas, numpy | ❌ JavaScript arrays only |
| **Version control** | ✅ git, code review | ❌ Web editor only |
| **Testing** | ✅ pytest, mocks | ❌ Manual testing |
| **Scheduling** | ✅ cron, Lambda, GitHub Actions | ✅ Built-in triggers |
| **Execution time** | ✅ Unlimited | ❌ 6-minute limit |
| **Cost** | $0-5/month | $0 |

**Decision**: Use **gspread + Python** when integrating external data (APIs, databases).
Use **Apps Script** for simple sheet-internal automation.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install gspread google-auth gspread-formatting
```

### 2. Create Service Account (One-Time Setup)

See [SETUP.md](SETUP.md) for detailed instructions.

**Quick version**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Sheets API
3. Create Service Account → Download JSON key
4. Save as `credentials.json` (gitignore it!)
5. Share your Google Sheet with service account email

### 3. Basic Usage

```python
import gspread
from google.oauth2.service_account import Credentials

# Authenticate
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

# Open sheet and write data
sheet = client.open("My Dashboard").sheet1
sheet.update('A1', [['Header1', 'Header2', 'Header3']])
sheet.append_row(['Value1', 'Value2', 'Value3'])
```

---

## Core Patterns

### Pattern 1: Type System Integration

Google Sheets API expects specific types. Always convert Python types properly.

```python
from decimal import Decimal
from datetime import date, datetime

def prepare_row_for_sheets(row: dict) -> list:
    """Convert Python types to Sheets-compatible values."""
    values = []
    for key, value in row.items():
        if isinstance(value, Decimal):
            # Decimal → float (Sheets doesn't understand Decimal)
            values.append(float(value))
        elif isinstance(value, (date, datetime)):
            # Date → ISO string (Sheets can parse this)
            values.append(value.strftime('%Y-%m-%d'))
        elif isinstance(value, bool):
            # Bool → uppercase string (Sheets convention)
            values.append('TRUE' if value else 'FALSE')
        elif value is None:
            # None → empty string (Sheets blank cell)
            values.append('')
        else:
            values.append(value)
    return values

# Usage
row = {
    'date': date(2025, 1, 9),
    'amount': Decimal('19.79'),
    'active': True,
    'notes': None
}
sheet.append_row(prepare_row_for_sheets(row))
# Writes: ['2025-01-09', 19.79, 'TRUE', '']
```

### Pattern 2: Defensive Authentication

Validate credentials exist and work before attempting operations.

```python
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

class SheetsClient:
    def __init__(self, credentials_path: str, sheet_name: str):
        # Defensive: Validate credentials file exists
        creds_file = Path(credentials_path)
        if not creds_file.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {credentials_path}\n"
                f"See docs/GOOGLE_SETUP.md for setup instructions."
            )

        self.credentials_path = credentials_path
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None

    def connect(self):
        """Authenticate and connect to sheet."""
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES
        )
        self.client = gspread.authorize(creds)

        # Defensive: Validate sheet exists and is accessible
        try:
            spreadsheet = self.client.open(self.sheet_name)
            self.sheet = spreadsheet.sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            raise ValueError(
                f"Sheet not found: {self.sheet_name}\n"
                f"Make sure the sheet is shared with the service account email."
            )

        return self

    def write_row(self, row: list):
        """Write a row, with connection validation."""
        if not self.sheet:
            raise RuntimeError("Not connected. Call connect() first.")
        self.sheet.append_row(row)
```

### Pattern 3: Batch Operations

Minimize API calls by batching operations.

```python
def write_multiple_rows(sheet, rows: list[list]):
    """Write multiple rows in single API call."""
    if not rows:
        return

    # Get next empty row
    existing = len(sheet.get_all_values())
    start_row = existing + 1

    # Batch update (single API call vs N calls)
    cell_range = f'A{start_row}'
    sheet.update(cell_range, rows)

# ✅ GOOD: 1 API call for 100 rows
write_multiple_rows(sheet, hundred_rows)

# ❌ BAD: 100 API calls
for row in hundred_rows:
    sheet.append_row(row)  # Each call is an API request!
```

### Pattern 4: Cell Formatting

Apply formatting after writing data.

```python
from gspread_formatting import (
    format_cell_range,
    CellFormat,
    NumberFormat,
    Color,
    TextFormat
)

def setup_sheet_formatting(sheet):
    """Apply standard formatting to sheet."""

    # Header row: Bold, gray background
    header_format = CellFormat(
        backgroundColor=Color(0.9, 0.9, 0.9),
        textFormat=TextFormat(bold=True),
        horizontalAlignment='CENTER'
    )
    format_cell_range(sheet, 'A1:Z1', header_format)

    # Currency columns (e.g., columns F and H)
    currency_format = CellFormat(
        numberFormat=NumberFormat(type='CURRENCY', pattern='$#,##0.00')
    )
    format_cell_range(sheet, 'F:F', currency_format)
    format_cell_range(sheet, 'H:H', currency_format)

    # Percentage columns (e.g., columns G and J)
    percent_format = CellFormat(
        numberFormat=NumberFormat(type='PERCENT', pattern='0.00%')
    )
    format_cell_range(sheet, 'G:G', percent_format)
    format_cell_range(sheet, 'J:J', percent_format)
```

### Pattern 5: API Response Parsing

Parse external API responses with type validation before writing.

```python
from typing import Dict, List, Any
from decimal import Decimal

class APIResponseParser:
    """Parse external API response for Sheets."""

    def __init__(self, response: List[Dict[str, Any]]):
        # Defensive: Validate response structure
        if not response or not isinstance(response, list):
            raise ValueError("Invalid API response format")

        self.raw_data = response

    def parse_row(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse single item with type conversion."""
        # Type conversion: API returns strings, we need proper types
        return {
            'date': item.get('date_start', ''),
            'name': item.get('name', ''),
            # String → int
            'impressions': int(item.get('impressions', '0')),
            'clicks': int(item.get('clicks', '0')),
            # String → Decimal (currency precision)
            'spend': Decimal(item.get('spend', '0')),
            # String → float
            'ctr': float(item.get('ctr', '0')),
        }

    def to_sheets_rows(self) -> List[List[Any]]:
        """Convert all items to Sheets row format."""
        rows = []
        for item in self.raw_data:
            parsed = self.parse_row(item)
            row = [
                parsed['date'],
                parsed['name'],
                parsed['impressions'],
                parsed['clicks'],
                float(parsed['spend']),  # Decimal → float for Sheets
                parsed['ctr'],
            ]
            rows.append(row)
        return rows

    @staticmethod
    def get_headers() -> List[str]:
        """Column headers matching to_sheets_rows() format."""
        return ['Date', 'Name', 'Impressions', 'Clicks', 'Spend', 'CTR']
```

---

## Common Operations

### Read Data

```python
# Get all data
all_values = sheet.get_all_values()

# Get specific range
cell_range = sheet.get('A1:D10')

# Get as dictionaries (first row = headers)
records = sheet.get_all_records()
# Returns: [{'Name': 'Alice', 'Age': 30}, {'Name': 'Bob', 'Age': 25}]

# Find a cell
cell = sheet.find('search term')
print(f"Found at row {cell.row}, col {cell.col}")
```

### Write Data

```python
# Update single cell
sheet.update('A1', 'Hello')

# Update range
sheet.update('A1:C1', [['Col1', 'Col2', 'Col3']])

# Append row (to end of data)
sheet.append_row(['New', 'Row', 'Data'])

# Insert row at specific position
sheet.insert_row(['Inserted', 'Row'], index=2)

# Batch update multiple ranges
sheet.batch_update([
    {'range': 'A1', 'values': [['Header1']]},
    {'range': 'B1', 'values': [['Header2']]},
])
```

### Formulas

```python
# Write formula
sheet.update('D2', '=SUM(A2:C2)')

# Write multiple formulas
formulas = [
    ['=SUM(A2:A10)'],
    ['=AVERAGE(B2:B10)'],
    ['=MAX(C2:C10)'],
]
sheet.update('D2:D4', formulas)

# Summary row with formulas
summary_row = 12
sheet.update(f'A{summary_row}:F{summary_row}', [[
    'TOTAL',
    f'=SUM(B2:B{summary_row-1})',
    f'=SUM(C2:C{summary_row-1})',
    f'=SUM(D2:D{summary_row-1})',
    f'=AVERAGE(E2:E{summary_row-1})',
    f'=SUM(F2:F{summary_row-1})',
]])
```

### Worksheets

```python
# List all worksheets
worksheets = spreadsheet.worksheets()

# Get worksheet by name
ws = spreadsheet.worksheet("Sheet2")

# Create new worksheet
new_ws = spreadsheet.add_worksheet(title="New Sheet", rows=100, cols=20)

# Delete worksheet
spreadsheet.del_worksheet(ws)

# Duplicate worksheet
spreadsheet.duplicate_sheet(source_sheet_id=ws.id, new_sheet_name="Copy")
```

---

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `SpreadsheetNotFound` | Sheet not shared with service account | Share sheet with SA email |
| `APIError: PERMISSION_DENIED` | Wrong permissions | Grant "Editor" access |
| `APIError: RATE_LIMIT_EXCEEDED` | Too many API calls | Add delays, use batch operations |
| `FileNotFoundError` | credentials.json missing | Download from GCP Console |
| `RefreshError` | Token expired | Re-download credentials |

### Retry Pattern

```python
import time
from gspread.exceptions import APIError

def write_with_retry(sheet, data, max_retries=3):
    """Write data with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            sheet.append_row(data)
            return True
        except APIError as e:
            if 'RATE_LIMIT' in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    return False
```

---

## Scheduling Options

### Option 1: Local Cron (Free)

```bash
# crontab -e
0 8 * * * cd /path/to/project && python update_sheets.py >> /var/log/sheets.log 2>&1
```

### Option 2: GitHub Actions (Free Tier)

```yaml
# .github/workflows/daily-sync.yml
name: Daily Sheets Sync

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python update_sheets.py
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
```

### Option 3: AWS Lambda

```python
# lambda_handler.py
import json
import base64
import os
from google.oauth2.service_account import Credentials

def handler(event, context):
    # Decode credentials from environment variable
    creds_json = base64.b64decode(os.environ['GOOGLE_CREDENTIALS_B64'])
    creds_dict = json.loads(creds_json)

    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)

    # Your logic here
    sheet = client.open("Dashboard").sheet1
    sheet.append_row(['Updated', 'from', 'Lambda'])

    return {'statusCode': 200}
```

---

## Security Checklist

- [ ] `credentials.json` in `.gitignore`
- [ ] File permissions: `chmod 600 credentials.json`
- [ ] Service Account has minimal permissions (Sheets API only)
- [ ] Sheet shared with specific SA email (not "anyone with link")
- [ ] Rotate keys every 90 days
- [ ] Don't log credentials or access tokens

---

## File Organization

```
.claude/skills/google-sheets/
├── SKILL.md              # This file (entry point)
├── SETUP.md              # Service Account setup guide
├── PATTERNS.md           # Advanced patterns
└── examples/
    ├── basic_write.py    # Simple read/write example
    └── api_to_sheets.py  # API → Sheets pipeline
```

---

## Integration with Other Skills

| Scenario | Use With |
|----------|----------|
| Need .env for credentials path | [python-env](../python-env/SKILL.md) |
| Deploying to Lambda | [deployment](../deployment/SKILL.md) |
| Testing Sheets integration | [testing-workflow](../testing-workflow/SKILL.md) |

---

## References

- [gspread documentation](https://docs.gspread.org/)
- [gspread-formatting](https://github.com/robin900/gspread-formatting)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Service Accounts Guide](https://cloud.google.com/iam/docs/service-accounts)
- Architecture decision: `.claude/journals/architecture/2026-01-09-chose-gspread-python-over-apps-script-for-sheets-automation.md`

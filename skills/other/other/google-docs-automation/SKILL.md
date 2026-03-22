---
name: google-docs-automation
description: Use when automating Google Workspace (Docs, Sheets, Slides) operations - covers authentication, common patterns, and best practices for gspread and googleapiclient
---

# Google Docs/Sheets/Slides Automation

## When to Use This Skill

Invoke this skill when you need to:
- Automate Google Sheets operations (read, write, format, chart creation)
- Generate or update Google Docs programmatically
- Create or modify Google Slides presentations
- Set up service account authentication for Google APIs
- Build financial models, dashboards, or reports in Google Workspace
- Integrate Google Workspace data with other systems

## Core Principles

1. **Service Account Authentication**: Always use service accounts for automation (never OAuth user credentials)
2. **Environment Variables**: Store credentials and document IDs in `.env` files (never commit)
3. **Scope Management**: Request only the minimum required scopes
4. **Error Handling**: Wrap all API calls in try/except with specific error messages
5. **Rate Limits**: Be aware of API quotas and implement backoff strategies for production use

## Authentication Setup

### Step 1: Service Account Credentials

```python
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv('.env')

# For Google Sheets (using gspread)
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
credentials = Credentials.from_service_account_file(creds_file, scopes=scope)
```

### Step 2: Environment Configuration

Create `.env` file:
```bash
GOOGLE_SERVICE_ACCOUNT_FILE=path/to/credentials.json
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_DOC_ID=your_doc_id_here
```

**CRITICAL**: Add `.env` and `*.json` credential files to `.gitignore`

## Google Sheets Automation

### Pattern: Read and Write Cells

```python
import gspread

# Authorize and open spreadsheet
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
worksheet = spreadsheet.worksheet('Sheet1')

# Read operations
value = worksheet.acell('A1').value
row_data = worksheet.row_values(1)
col_data = worksheet.col_values(1)
all_data = worksheet.get_all_values()

# Write operations
worksheet.update_acell('A1', 'New Value')
worksheet.update('A1:C3', [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'NYC'],
    ['Bob', 25, 'SF']
])
```

### Pattern: Formatting and Styling

```python
# Format cells
worksheet.format('A1:C1', {
    'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
})

# Set column width
worksheet.set_column_width(1, 200)

# Merge cells
worksheet.merge_cells('A1:C1')
```

### Pattern: Adding Charts

```python
from googleapiclient.discovery import build

sheets_service = build('sheets', 'v4', credentials=credentials)

chart_request = {
    'addChart': {
        'chart': {
            'spec': {
                'title': 'Revenue vs Expenses',
                'basicChart': {
                    'chartType': 'LINE',
                    'legendPosition': 'RIGHT_LEGEND',
                    'axis': [
                        {'position': 'BOTTOM_AXIS', 'title': 'Month'},
                        {'position': 'LEFT_AXIS', 'title': 'Amount'}
                    ],
                    'series': [
                        {'series': {'sourceRange': {'sources': [{'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 12, 'startColumnIndex': 0, 'endColumnIndex': 1}]}}},
                        {'series': {'sourceRange': {'sources': [{'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 12, 'startColumnIndex': 1, 'endColumnIndex': 2}]}}}
                    ]
                }
            },
            'position': {'overlayPosition': {'anchorCell': {'sheetId': 0, 'rowIndex': 2, 'columnIndex': 5}}}
        }
    }
}

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=os.getenv('GOOGLE_SHEET_ID'),
    body={'requests': [chart_request]}
).execute()
```

## Google Docs Automation

### Pattern: Read Document with Comments

```python
from googleapiclient.discovery import build

docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

doc_id = os.getenv('GOOGLE_DOC_ID')

# Get document content
document = docs_service.documents().get(documentId=doc_id).execute()
title = document.get('title')
content = document.get('body', {}).get('content', [])

# Get comments
comments = drive_service.comments().list(
    fileId=doc_id,
    fields='comments(content,quotedFileContent,author,createdTime,resolved)'
).execute().get('comments', [])

for comment in comments:
    author = comment.get('author', {}).get('displayName')
    text = comment.get('content')
    quoted = comment.get('quotedFileContent', {}).get('value')
    print(f"{author}: {text} on '{quoted}'")
```

### Pattern: Write/Update Document

```python
# Insert text at beginning
requests = [{
    'insertText': {
        'location': {'index': 1},
        'text': 'New paragraph at start\n'
    }
}]

docs_service.documents().batchUpdate(
    documentId=doc_id,
    body={'requests': requests}
).execute()

# Format text
format_request = [{
    'updateTextStyle': {
        'range': {'startIndex': 1, 'endIndex': 20},
        'textStyle': {
            'bold': True,
            'fontSize': {'magnitude': 14, 'unit': 'PT'}
        },
        'fields': 'bold,fontSize'
    }
}]

docs_service.documents().batchUpdate(
    documentId=doc_id,
    body={'requests': format_request}
).execute()
```

## Google Slides Automation

### Pattern: Create Presentation

```python
slides_service = build('slides', 'v1', credentials=credentials)

# Create new presentation
presentation = slides_service.presentations().create(
    body={'title': 'My Presentation'}
).execute()

presentation_id = presentation.get('presentationId')

# Add slide
requests = [{
    'createSlide': {
        'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'}
    }
}]

response = slides_service.presentations().batchUpdate(
    presentationId=presentation_id,
    body={'requests': requests}
).execute()
```

### Pattern: Update Slide Content

```python
slide_id = response.get('replies')[0].get('createSlide').get('objectId')

# Add text to slide
text_requests = [{
    'insertText': {
        'objectId': slide_id,
        'insertionIndex': 0,
        'text': 'Slide Title'
    }
}]

slides_service.presentations().batchUpdate(
    presentationId=presentation_id,
    body={'requests': text_requests}
).execute()
```

## Common Patterns and Best Practices

### Pattern: List Worksheets

```python
def list_worksheets(spreadsheet_id):
    """List all worksheets in a spreadsheet"""
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_key(spreadsheet_id)

    for worksheet in spreadsheet.worksheets():
        print(f"- {worksheet.title} (ID: {worksheet.id})")
```

### Pattern: Error Handling

```python
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
from googleapiclient.errors import HttpError

try:
    worksheet = spreadsheet.worksheet('Sheet1')
    value = worksheet.acell('A1').value
except SpreadsheetNotFound:
    print("Spreadsheet not found - check ID and sharing permissions")
except WorksheetNotFound:
    print("Worksheet 'Sheet1' does not exist")
except HttpError as e:
    print(f"API error: {e.resp.status} - {e.content}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Pattern: Batch Operations for Performance

```python
# BAD: Multiple API calls in loop
for row in data:
    worksheet.update_acell(f'A{i}', row[0])  # Slow!

# GOOD: Single batch update
cell_list = worksheet.range('A1:A100')
for i, cell in enumerate(cell_list):
    cell.value = data[i][0]
worksheet.update_cells(cell_list)  # One API call
```

## Security Checklist

- [ ] Service account credentials stored in `.env` file
- [ ] `.env` and `*.json` files in `.gitignore`
- [ ] Minimum required scopes requested
- [ ] Service account has appropriate sharing permissions on documents
- [ ] No hardcoded document IDs in scripts (use environment variables)
- [ ] Error handling includes specific error messages
- [ ] Rate limiting considered for production use

## Common Use Cases

### Financial Modeling
- Read current financial data from master spreadsheet
- Update pro forma models with scenario planning
- Generate formatted P&L statements
- Create revenue vs expense charts

### Dashboard Creation
- Aggregate data from multiple sources
- Build dynamic charts with real-time data
- Format dashboards for executive presentation
- Export dashboards to PDF via Drive API

### Document Generation
- Create customer-specific one-pagers
- Update templated proposals with current data
- Generate reports from spreadsheet data
- Manage document comments and feedback

### Presentation Automation
- Build pitch decks from templates
- Update slides with current financial data
- Create standardized slide layouts
- Export presentations for client delivery

## References

See comprehensive examples in:
- `/path/to/projects/work/synth/google-automation/`
- Sheets: `sheets/financial/`, `sheets/dashboards/`
- Docs: `docs/onepagers/`, `docs/general/`
- Slides: `presentations/`

## API Documentation

- **gspread**: https://docs.gspread.org/
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Google Docs API**: https://developers.google.com/docs/api
- **Google Slides API**: https://developers.google.com/slides/api

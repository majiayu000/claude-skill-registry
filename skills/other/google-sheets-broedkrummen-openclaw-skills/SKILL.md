---
name: google-sheets
description: |
  Google Sheets API integration with managed OAuth. Read and write spreadsheet data, create sheets, apply formatting, and manage ranges. Use this skill when users want to read from or write to Google Sheets. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Google Sheets

Access the Google Sheets API with managed OAuth authentication. Read and write spreadsheet values, create sheets, apply formatting, and perform batch operations.

## Quick Start

```bash
# Read values from a spreadsheet (note: range is URL-encoded)
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID/values/Sheet1%21A1%3AD10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/google-sheets/{native-api-path}
```

Replace `{native-api-path}` with the actual Google Sheets API endpoint path. The gateway proxies requests to `sheets.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-sheets&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-sheets'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-sheets",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Google accounts connected, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Get Spreadsheet Metadata

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}
```

### Get Values

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}
```

Example:

```bash
GET /google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1%21A1%3AD10
```

### Get Multiple Ranges

```bash
GET /google-sheets/v4/spreadsheets/{spreadsheetId}/values:batchGet?ranges=Sheet1%21A1%3AB10&ranges=Sheet2%21A1%3AC5
```

### Update Values

```bash
PUT /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}?valueInputOption=USER_ENTERED
Content-Type: application/json

{
  "values": [
    ["A1", "B1", "C1"],
    ["A2", "B2", "C2"]
  ]
}
```

### Append Values

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}:append?valueInputOption=USER_ENTERED
Content-Type: application/json

{
  "values": [
    ["New Row 1", "Data", "More Data"],
    ["New Row 2", "Data", "More Data"]
  ]
}
```

### Batch Update Values

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values:batchUpdate
Content-Type: application/json

{
  "valueInputOption": "USER_ENTERED",
  "data": [
    {"range": "Sheet1!A1:B2", "values": [["A1", "B1"], ["A2", "B2"]]},
    {"range": "Sheet1!D1:E2", "values": [["D1", "E1"], ["D2", "E2"]]}
  ]
}
```

### Clear Values

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}/values/{range}:clear
```

### Create Spreadsheet

```bash
POST /google-sheets/v4/spreadsheets
Content-Type: application/json

{
  "properties": {"title": "New Spreadsheet"},
  "sheets": [{"properties": {"title": "Sheet1"}}]
}
```

### Batch Update (formatting, add sheets, etc.)

```bash
POST /google-sheets/v4/spreadsheets/{spreadsheetId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {"addSheet": {"properties": {"title": "New Sheet"}}}
  ]
}
```

## Common batchUpdate Requests

### Update Cells with Formatting

```json
{
  "updateCells": {
    "rows": [
      {"values": [{"userEnteredValue": {"stringValue": "Name"}}, {"userEnteredValue": {"numberValue": 100}}]}
    ],
    "fields": "userEnteredValue",
    "start": {"sheetId": 0, "rowIndex": 0, "columnIndex": 0}
  }
}
```

### Format Header Row (Bold + Background Color)

```json
{
  "repeatCell": {
    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 3},
    "cell": {
      "userEnteredFormat": {
        "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
        "textFormat": {"bold": true}
      }
    },
    "fields": "userEnteredFormat(backgroundColor,textFormat)"
  }
}
```

### Auto-Resize Columns

```json
{
  "autoResizeDimensions": {
    "dimensions": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 3}
  }
}
```

### Rename Sheet

```json
{
  "updateSheetProperties": {
    "properties": {"sheetId": 0, "title": "NewName"},
    "fields": "title"
  }
}
```

### Insert Rows/Columns

```json
{
  "insertDimension": {
    "range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 1, "endIndex": 3},
    "inheritFromBefore": true
  }
}
```

### Sort Range

```json
{
  "sortRange": {
    "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 10, "startColumnIndex": 0, "endColumnIndex": 3},
    "sortSpecs": [{"dimensionIndex": 1, "sortOrder": "DESCENDING"}]
  }
}
```

### Add Filter

```json
{
  "setBasicFilter": {
    "filter": {
      "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 100, "startColumnIndex": 0, "endColumnIndex": 5}
    }
  }
}
```

### Delete Sheet

```json
{
  "deleteSheet": {"sheetId": 123456789}
}
```

## Value Input Options

- `RAW` - Values are stored as-is
- `USER_ENTERED` - Values are parsed as if typed into the UI (formulas executed, numbers parsed)

## Range Notation

- `Sheet1!A1:D10` - Specific range
- `Sheet1!A:D` - Entire columns A through D
- `Sheet1!1:10` - Entire rows 1 through 10
- `Sheet1` - Entire sheet
- `A1:D10` - Range in first sheet

## Code Examples

### JavaScript

```javascript
// Read values
const response = await fetch(
  'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:D10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Write values
await fetch(
  'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:B2?valueInputOption=USER_ENTERED',
  {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      values: [['A1', 'B1'], ['A2', 'B2']]
    })
  }
);
```

### Python

```python
import os
import requests

# Read values
response = requests.get(
    'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:D10',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)

# Write values
response = requests.put(
    'https://gateway.maton.ai/google-sheets/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:B2',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'valueInputOption': 'USER_ENTERED'},
    json={'values': [['A1', 'B1'], ['A2', 'B2']]}
)
```

## Notes

- When using curl, ranges in URL paths must be URL-encoded (! -> %21, : -> %3A). JavaScript fetch and Python requests handle encoding automatically.
- Use `valueInputOption=USER_ENTERED` to parse formulas and numbers
- Delete spreadsheets via the Google Drive API, not Sheets API
- Sheet IDs are numeric and found in the spreadsheet metadata
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Sheets connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Sheets API |

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `google-sheets`. For example:

- Correct: `https://gateway.maton.ai/google-sheets/v4/spreadsheets/SPREADSHEET_ID`
- Incorrect: `https://gateway.maton.ai/v4/spreadsheets/SPREADSHEET_ID`

## Resources

- [Sheets API Overview](https://developers.google.com/workspace/sheets/api/reference/rest)
- [Get Spreadsheet](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/get)
- [Create Spreadsheet](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create)
- [Batch Update](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
- [Batch Update Request Types](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/request)
- [Get Values](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/get)
- [Update Values](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/update)
- [Append Values](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append)
- [Batch Get Values](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/batchGet)
- [Batch Update Values](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)

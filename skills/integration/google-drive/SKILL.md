---
name: google-drive
description: Search and read Google Drive files including Docs, Sheets, and other documents.
---

# Google Drive Integration

This skill provides access to Google Drive and Google Docs/Sheets/Slides via the Drive API.

## Setup Required

Uses OAuth with persistent refresh token (same setup for Calendar, Gmail, Drive).

**One-time setup:**
```bash
google-oauth-setup <path-to-client-secret.json>
```

See `claude/skills/SETUP.md` for detailed OAuth setup instructions.

**Get Access Token (auto-refreshes):**
```bash
ACCESS_TOKEN=$(google-oauth-token)
```

**Required header for all requests:**
```bash
-H "x-goog-user-project: ${GOOGLE_QUOTA_PROJECT}"
```

## When to Use

Use this skill when the user:
- Asks about Google Drive files or documents
- Wants to search for a document
- Needs to read content from a Google Doc or Sheet
- Asks about recent files
- Mentions "Drive", "Google Docs", or "Google Sheets"

## API Endpoints

### Drive API (files, search)

Base URL: `https://www.googleapis.com/drive/v3`

**List Recent Files**:
```bash
curl -s "https://www.googleapis.com/drive/v3/files?pageSize=20&orderBy=modifiedTime%20desc" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.files[] | {name, id, mimeType}'
```

**Search Files**:
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=name contains 'meeting notes'" \
  --data-urlencode "pageSize=20" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Get File Metadata**:
```bash
curl -s "https://www.googleapis.com/drive/v3/files/{FILE_ID}?fields=*" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Export Google Doc as Text**:
```bash
curl -s "https://www.googleapis.com/drive/v3/files/{FILE_ID}/export?mimeType=text/plain" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Docs API (read document content)

Base URL: `https://docs.googleapis.com/v1`

**Get Document Content**:
```bash
curl -s "https://docs.googleapis.com/v1/documents/{DOCUMENT_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Sheets API (read spreadsheet data)

Base URL: `https://sheets.googleapis.com/v4`

**Get Spreadsheet Metadata**:
```bash
curl -s "https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Read Sheet Values**:
```bash
curl -s "https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
# Example RANGE: Sheet1!A1:D10, or just A1:D10 for first sheet
```

## Search Query Syntax

The `q` parameter uses Drive search syntax:

| Query | Description |
|-------|-------------|
| `name contains 'report'` | Name contains text |
| `name = 'Exact Name'` | Exact name match |
| `fullText contains 'search term'` | Content contains text |
| `mimeType = 'application/vnd.google-apps.document'` | Google Docs |
| `mimeType = 'application/vnd.google-apps.spreadsheet'` | Google Sheets |
| `mimeType = 'application/pdf'` | PDF files |
| `modifiedTime > '2024-01-01'` | Modified after date |
| `'folder_id' in parents` | Files in specific folder |
| `starred = true` | Starred files |
| `trashed = false` | Not in trash |

Combine with `and`/`or`: `name contains 'meeting' and mimeType = 'application/vnd.google-apps.document'`

## MIME Types

| Type | MIME Type |
|------|-----------|
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Google Form | `application/vnd.google-apps.form` |
| Folder | `application/vnd.google-apps.folder` |

## Common Workflows

### Search for a Document
```bash
ACCESS_TOKEN=$(google-oauth-token)

curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=name contains 'project plan' and mimeType = 'application/vnd.google-apps.document'" \
  --data-urlencode "fields=files(id,name,modifiedTime,webViewLink)" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Read a Google Doc
```bash
# Export as plain text
DOC_ID="1abc123..."
curl -s "https://www.googleapis.com/drive/v3/files/${DOC_ID}/export?mimeType=text/plain" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Read a Google Sheet
```bash
SHEET_ID="1abc123..."
# Get all values from first sheet
curl -s "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/A:Z" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.values'
```

### List Recent Docs
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=mimeType = 'application/vnd.google-apps.document'" \
  --data-urlencode "orderBy=modifiedTime desc" \
  --data-urlencode "pageSize=10" \
  --data-urlencode "fields=files(id,name,modifiedTime)" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Search File Content
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=fullText contains 'quarterly review'" \
  --data-urlencode "fields=files(id,name,mimeType,webViewLink)" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

## Export Formats

Google Docs can be exported to various formats:

| Original | Export MIME Type |
|----------|------------------|
| Document | `text/plain`, `text/html`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Spreadsheet | `text/csv`, `application/pdf`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Presentation | `application/pdf`, `text/plain` |

## Extracting File IDs from URLs

Google Drive URLs:
- Doc: `https://docs.google.com/document/d/{FILE_ID}/edit`
- Sheet: `https://docs.google.com/spreadsheets/d/{FILE_ID}/edit`
- Drive: `https://drive.google.com/file/d/{FILE_ID}/view`

The FILE_ID is the long alphanumeric string between `/d/` and the next `/`.

## Notes

- Access tokens expire after 1 hour
- Google Docs exported as text lose formatting
- For Sheets, specify range to avoid downloading huge datasets
- `fields` parameter reduces response size (use for faster queries)
- Full-text search only works on files owned or shared with you

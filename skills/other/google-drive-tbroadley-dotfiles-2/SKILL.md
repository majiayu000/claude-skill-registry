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

## Re-authentication

If you get `invalid_grant` or `reauth related error`, the OAuth token has expired. Re-authenticate using gcloud:

```bash
# Re-authenticate with required scopes
gcloud auth application-default login \
  --scopes="https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/cloud-platform"

# Migrate the new credentials
google-oauth-setup --migrate-gcloud
```

This will open a browser for authentication, then migrate the credentials to the google-oauth config.

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

**IMPORTANT: Shared Drives** - Always include these parameters on search/list calls to find files in Shared Drives:
- `includeItemsFromAllDrives=true`
- `supportsAllDrives=true`
- `corpora=allDrives`

And on single-file metadata calls, include `supportsAllDrives=true`.

**List Recent Files**:
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "pageSize=20" \
  --data-urlencode "orderBy=modifiedTime desc" \
  --data-urlencode "includeItemsFromAllDrives=true" \
  --data-urlencode "supportsAllDrives=true" \
  --data-urlencode "corpora=allDrives" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.files[] | {name, id, mimeType}'
```

**Search Files**:
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=name contains 'meeting notes'" \
  --data-urlencode "pageSize=20" \
  --data-urlencode "includeItemsFromAllDrives=true" \
  --data-urlencode "supportsAllDrives=true" \
  --data-urlencode "corpora=allDrives" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Get File Metadata**:
```bash
curl -s "https://www.googleapis.com/drive/v3/files/{FILE_ID}?fields=*&supportsAllDrives=true" \
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
  --data-urlencode "includeItemsFromAllDrives=true" \
  --data-urlencode "supportsAllDrives=true" \
  --data-urlencode "corpora=allDrives" \
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
  --data-urlencode "includeItemsFromAllDrives=true" \
  --data-urlencode "supportsAllDrives=true" \
  --data-urlencode "corpora=allDrives" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Search File Content
```bash
curl -s -G "https://www.googleapis.com/drive/v3/files" \
  --data-urlencode "q=fullText contains 'quarterly review'" \
  --data-urlencode "fields=files(id,name,mimeType,webViewLink)" \
  --data-urlencode "includeItemsFromAllDrives=true" \
  --data-urlencode "supportsAllDrives=true" \
  --data-urlencode "corpora=allDrives" \
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

## Google Docs Revision History

To access historical revisions of a Google Doc:

**Get revision list:**
```bash
curl -s "https://www.googleapis.com/drive/v3/files/${DOC_ID}/revisions?fields=revisions(id,modifiedTime,exportLinks,lastModifyingUser(displayName))" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-user-project: ${GOOGLE_QUOTA_PROJECT}"
```

**Export a specific revision (use exportLinks, NOT the export endpoint):**
```bash
# IMPORTANT: The Drive export endpoint ignores the revision parameter for Google Docs!
# You MUST use the exportLinks from the revision metadata instead.

# Get the exportLink for a specific revision
EXPORT_URL=$(curl -s "https://www.googleapis.com/drive/v3/files/${DOC_ID}/revisions/${REV_ID}?fields=exportLinks" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq -r '.exportLinks["text/plain"]')

# Download using that link
curl -sL "$EXPORT_URL" -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**IMPORTANT CAVEATS:**
- The `revision` parameter on `/export` is IGNORED for Google Docs - it always returns current content
- You MUST use the `exportLinks` URLs from the revisions API to get historical content
- Rate limiting is aggressive - add 2-3 second delays between revision downloads
- Documents with multiple tabs: the text export only includes the main tab
- Deleted tabs: revisions may reference content from tabs that no longer exist

## Notes

- Access tokens expire after 1 hour
- Google Docs exported as text lose formatting
- For Sheets, specify range to avoid downloading huge datasets
- `fields` parameter reduces response size (use for faster queries)
- Full-text search only works on files owned or shared with you

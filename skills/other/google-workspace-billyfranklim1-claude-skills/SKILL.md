---
name: google-workspace
description: Google Workspace — Drive, Gmail, Calendar, Sheets, Docs, Tasks via gws CLI
---
# Google Workspace CLI (gws)

## When to Use
When the user asks to interact with Google Drive, Gmail, Calendar, Sheets, Docs, Slides, or Tasks.
Examples: list files, send email, check calendar, create spreadsheet, read document, create task.

## Setup
- **CLI**: `@googleworkspace/cli` (installed globally via npm)
- **Auth**: `gws auth login` or set `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` env var pointing to a credentials JSON
- **Scopes**: Drive, Sheets, Gmail, Calendar, Docs, Presentations, Tasks, PubSub, Cloud Platform

## Commands

### Drive
```bash
# List files
gws drive files list --params '{"pageSize": 10}'

# Search files by name
gws drive files list --params '{"q": "name contains '\''report'\''", "pageSize": 10}'

# Get file details
gws drive files get --params '{"fileId": "FILE_ID"}'

# Create folder
gws drive files create --json '{"name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}'

# Upload file
gws drive files create --json '{"name": "file.pdf"}' --upload /path/to/file.pdf
```

### Gmail
```bash
# List recent messages
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'

# Read a message
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'

# Search emails
gws gmail users messages list --params '{"userId": "me", "q": "from:user@example.com", "maxResults": 5}'

# Send email (body must be base64url-encoded RFC 2822)
gws gmail users messages send --params '{"userId": "me"}' --json '{"raw": "BASE64_ENCODED_EMAIL"}'
```

### Calendar
```bash
# List calendars
gws calendar calendarList list

# List today's events
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-01-01T00:00:00Z", "timeMax": "2026-01-01T23:59:59Z", "singleEvents": true, "orderBy": "startTime"}'

# Create event
gws calendar events insert --params '{"calendarId": "primary"}' --json '{"summary": "Meeting", "start": {"dateTime": "2026-01-01T14:00:00-03:00"}, "end": {"dateTime": "2026-01-01T15:00:00-03:00"}}'
```

### Sheets
```bash
# Create spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "My Spreadsheet"}}'

# Read data
gws sheets spreadsheets values get --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1:D10"}'

# Write data
gws sheets spreadsheets values update --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' --json '{"values": [["Name", "Email"], ["John", "john@example.com"]]}'
```

### Docs
```bash
# Create document
gws docs documents create --json '{"title": "My Document"}'

# Read document
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Tasks
```bash
# List task lists
gws tasks tasklists list

# List tasks
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}'

# Create task
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "My task", "notes": "Description"}'
```

## Output Formats
```bash
--format json    # default
--format table   # human-readable table
--format yaml
--format csv
```

## API Introspection
```bash
# View method schema
gws schema drive.files.list
gws schema gmail.users.messages.send
```

## Notes
- Email body must be RFC 2822 encoded in base64url format
- The CLI discovers APIs dynamically via Google Discovery Service
- Discovery docs are cached for 24 hours

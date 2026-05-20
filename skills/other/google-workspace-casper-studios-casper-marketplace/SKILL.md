---
name: google-workspace
description: Google Drive, Gmail, Calendar, and Docs operations via OAuth. Use this skill when uploading files to Drive, searching Drive folders, searching Gmail, finding calendar meetings, creating Google Docs, or managing folder structures. Triggers on Google Workspace operations, file uploads, email search, calendar search, or document creation.
---

# Google Workspace

## Overview

Interact with Google Drive, Gmail, Calendar, and Docs using OAuth authentication. Supports file uploads, folder management, email search, calendar search, and document operations.

## Quick Decision Tree

```
What do you need?
│
├── Google Drive
│   ├── Search files/folders → references/drive-search.md
│   │   └── Script: scripts/gdrive_search.py
│   │
│   ├── Upload files → references/drive-upload.md
│   │   └── Script: scripts/google_drive_upload.py
│   │
│   ├── Create folder structure → references/folder-structure.md
│   │   └── Script: scripts/gdrive_folder_structure.py
│   │
│   ├── Create client folder → references/create-folder.md
│   │   └── Script: scripts/create_client_folder.py
│   │
│   └── Search transcripts → references/transcript-search.md
│       └── Script: scripts/gdrive_transcript_search.py
│
├── Gmail
│   └── Search emails → references/gmail-search.md
│       └── Script: scripts/gmail_search.py
│
└── Calendar
    └── Search meetings → references/calendar-search.md
        └── Script: scripts/google_calendar_search.py
```

## Environment Setup

OAuth credentials are stored locally after first authentication.

### Required Files
- `client_secrets.json` - From Google Cloud Console
- `settings.yaml` - PyDrive2 configuration
- `mycreds.txt` - Auto-generated OAuth tokens

### First-Time Setup
1. Go to Google Cloud Console
2. Enable APIs: Drive, Gmail, Calendar, Docs
3. Create OAuth 2.0 credentials (Desktop app)
4. Download as `client_secrets.json`
5. Run any script - browser opens for OAuth consent

## Common Usage

### Search Client Folder
```bash
python scripts/gdrive_search.py folder "Microsoft"
```

### Upload Files
```bash
python scripts/google_drive_upload.py --files *.png --folder "Clients/Acme/Assets"
```

### Search Emails
```bash
python scripts/gmail_search.py --domain "microsoft.com" --days 14
```

### Search Calendar
```bash
python scripts/google_calendar_search.py "Microsoft" --days-back 30
```

## OAuth Scopes

| Scope | Purpose |
|-------|---------|
| `drive` | Full Drive access |
| `spreadsheets` | Sheets access |
| `documents` | Docs access |
| `gmail.readonly` | Read emails |
| `calendar.readonly` | Read calendar |

## Cost

Free - Google Workspace APIs have generous free quotas.

## Security Notes

### Credential Handling
- `client_secrets.json` - OAuth app credentials (never commit to git)
- `mycreds.txt` - User OAuth tokens (never commit to git, add to .gitignore)
- `settings.yaml` - PyDrive2 config (can be committed, no secrets)
- Tokens auto-refresh; revoke via Google Account settings if compromised
- Never share OAuth credentials between users/machines

### Data Privacy
- Access to user's personal Google Drive, Gmail, and Calendar
- Files may contain confidential business information
- Email content is highly sensitive - minimize storage
- Calendar events may contain private meeting details
- Shared Drive access respects original permissions

### Access Scopes
- Request minimum required scopes:
  - `drive` - Full Drive access (read/write)
  - `drive.readonly` - Read-only Drive access (preferred when possible)
  - `spreadsheets` - Google Sheets access
  - `documents` - Google Docs access
  - `gmail.readonly` - Read-only email access
  - `calendar.readonly` - Read-only calendar access
- Review/revoke access: https://myaccount.google.com/permissions

### Compliance Considerations
- **OAuth Consent**: Users explicitly consent to access scopes
- **GDPR**: Google Workspace data contains EU user PII
- **Data Residency**: Google Workspace may have data residency requirements
- **Shared Drives**: Respect organizational sharing policies
- **Audit Trail**: Google Admin Console tracks API access
- **Credential Security**: Store `client_secrets.json` securely, not in repos

## Troubleshooting

### Common Issues

#### Issue: OAuth token expired
**Symptoms:** "Invalid credentials" or "Token has been expired or revoked" error
**Cause:** OAuth refresh token expired or revoked
**Solution:**
- Delete `mycreds.txt` file
- Re-run any script to trigger fresh OAuth flow
- Complete the browser authorization
- New `mycreds.txt` will be created automatically

#### Issue: File not found
**Symptoms:** "File not found" error with valid file ID
**Cause:** No access to file, file deleted, or wrong file ID
**Solution:**
- Verify file ID from the Google Drive URL
- Check file sharing permissions
- Ensure OAuth user has access to the file
- Try accessing file directly in browser first

#### Issue: Quota exceeded
**Symptoms:** "User rate limit exceeded" or "Quota exceeded" error
**Cause:** Too many API requests in 24-hour period
**Solution:**
- Wait 24 hours for quota reset
- Create a new Google Cloud project with fresh quota
- Implement exponential backoff in scripts
- Reduce frequency of API calls

#### Issue: settings.yaml missing
**Symptoms:** "settings.yaml not found" or PyDrive2 configuration error
**Cause:** Missing PyDrive2 configuration file
**Solution:**
- Copy from template: `cp settings.yaml.example settings.yaml`
- Ensure `client_secrets.json` path is correct in settings
- Verify save_credentials_backend is set to "file"
- Check settings.yaml is in the script's working directory

#### Issue: client_secrets.json invalid
**Symptoms:** "Invalid client secrets" or OAuth configuration error
**Cause:** Malformed or incorrect OAuth credentials file
**Solution:**
- Re-download from Google Cloud Console
- Ensure "Desktop app" type was selected when creating credentials
- Check JSON format is valid
- Verify redirect URIs are configured for local auth

#### Issue: Scope access denied
**Symptoms:** "Insufficient permission" error
**Cause:** OAuth consent missing required scopes
**Solution:**
- Delete `mycreds.txt` to reset OAuth session
- Re-authenticate and accept all requested scopes
- Verify scopes in `settings.yaml` match script requirements
- Check Google Cloud Console for scope restrictions

## Resources

- **references/drive-search.md** - Search files and folders
- **references/drive-upload.md** - Upload files to Drive
- **references/folder-structure.md** - Create folder hierarchies
- **references/create-folder.md** - Create client folders
- **references/transcript-search.md** - Search transcript files
- **references/gmail-search.md** - Search Gmail
- **references/calendar-search.md** - Search calendar meetings

## Integration Patterns

### Drive to Video Production
**Skills:** google-workspace → video-production
**Use case:** Assemble course videos from Drive folder
**Flow:**
1. Search Drive for video folder with lesson files
2. Download videos via video-production scripts
3. Stitch videos with title slides and upload final output

### Templates to Content
**Skills:** google-workspace → content-generation
**Use case:** Generate documents from branded templates
**Flow:**
1. Load template from Drive (proposal, report format)
2. Generate content via content-generation
3. Create new Google Doc with formatted content

### Calendar to Transcripts
**Skills:** google-workspace → transcript-search
**Use case:** Find meeting recordings from calendar events
**Flow:**
1. Search calendar for meetings with specific client
2. Get meeting dates and titles
3. Search transcript-search for matching recordings

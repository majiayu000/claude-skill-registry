---
name: upload-drive
description: Upload files to Google Drive. Useful for exporting final tailored resumes or saving logs to a cloud destination.
---

# Upload to Google Drive

## Overview

This skill allows uploading files to a specified Google Drive folder. It handles authentication using a `credentials.json` file (OAuth 2.0).

## Prerequisites

Requires Google Client libraries:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

You must provide a `credentials.json` file from the Google Cloud Console.

## Usage

### Upload Script

**Syntax:**

```bash
python3 .agent/skills/upload-drive/scripts/upload_drive.py <file_path> [--folder_id <id>] [--credentials <path>]
```

**Arguments:**
*   `file_path`: Path of file to upload.
*   `--folder_id`: (Optional) ID of the destination Google Drive folder.
*   `--credentials`: (Optional) Path to `credentials.json`. Defaults to `credentials.json` in current dir.
*   `--token`: (Optional) Path to `token.json` to store session. Defaults to `token.json`.

**Example:**

```bash
# Upload resume to specific folder
python3 .agent/skills/upload-drive/scripts/upload_drive.py tailored_resume.pdf --folder_id 1A2B3C... --credentials ~/.secrets/credentials.json
```

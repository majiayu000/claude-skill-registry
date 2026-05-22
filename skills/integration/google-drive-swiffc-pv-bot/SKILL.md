---
name: google-drive
description: Manage Google Drive files and folders. Upload, download, share, and organize files via Drive API.
metadata: {"clawdbot":{"emoji":"📁","requires":{"env":["GOOGLE_ACCESS_TOKEN"]}}}
---

# Google Drive

Cloud file storage and sharing.

## Environment

```bash
export GOOGLE_ACCESS_TOKEN="ya29.xxxxxxxxxx"
```

## List Files

```bash
curl "https://www.googleapis.com/drive/v3/files?pageSize=20" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## Search Files

```bash
curl "https://www.googleapis.com/drive/v3/files?q=name%20contains%20'report'" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## Get File Metadata

```bash
curl "https://www.googleapis.com/drive/v3/files/{fileId}?fields=*" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## Download File

```bash
curl "https://www.googleapis.com/drive/v3/files/{fileId}?alt=media" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -o downloaded_file.pdf
```

## Upload File

```bash
curl -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -F "metadata={\"name\": \"myfile.txt\"};type=application/json" \
  -F "file=@localfile.txt"
```

## Create Folder

```bash
curl -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}'
```

## Share File

```bash
curl -X POST "https://www.googleapis.com/drive/v3/files/{fileId}/permissions" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "reader", "type": "user", "emailAddress": "user@example.com"}'
```

## Links
- Console: https://console.cloud.google.com/apis/library/drive.googleapis.com
- Docs: https://developers.google.com/drive/api/v3/reference

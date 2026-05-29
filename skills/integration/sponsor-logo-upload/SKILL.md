---
name: sponsor-logo-upload
description: Use when uploading sponsor logos to ProductTank SF Google Drive - downloads image from URL (handles Cloudflare), validates it's actual image data, uploads to Drive folder, returns shareable link
---

# Sponsor Logo Upload

## Overview

Download sponsor logo from URL and upload to ProductTank SF Google Drive. Handles CDN protections (Cloudflare) and validates image integrity before upload.

## Quick Reference

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `url` | Yes | - | Image URL (Brandfetch, theorg.com, etc.) |
| `sponsorName` | Yes | - | Used for filename: `sponsor-logo-{name}.{ext}` |
| `folderId` | No | `1nh4a-uoTK40S7Twm4erJICQaAmsFcXgj` | GDrive folder ID |

## Workflow

### 1. Download Image

```bash
# Extract extension from URL
EXT="${URL##*.}"
EXT="${EXT%%\?*}"  # Remove query params

# Download with User-Agent (bypasses Cloudflare)
curl -L -A "Mozilla/5.0" -o "/tmp/sponsor-logo-${SPONSOR_NAME}.${EXT}" "${URL}"
```

### 2. Validate Image

```bash
# Check file size (>1KB = likely real image)
SIZE=$(stat -f%z "/tmp/sponsor-logo-${SPONSOR_NAME}.${EXT}")
if [ "$SIZE" -lt 1024 ]; then
  echo "ERROR: File too small ($SIZE bytes) - likely HTML error page"
  exit 1
fi

# Verify actual image type
file "/tmp/sponsor-logo-${SPONSOR_NAME}.${EXT}"
# Should show: PNG image data, JPEG image data, etc.
# NOT: HTML document, ASCII text
```

### 3. Upload to Google Drive

```bash
# Use MCP tool
mcp__gdrive__gdrive_upload_file
  filePath: /tmp/sponsor-logo-{sponsorName}.{ext}
  fileName: sponsor-logo-{sponsorName}.{ext}
  folderId: {folderId or default}
```

### 4. Return Result

Report: file ID, web view link, filename

## Common Issues

| Symptom | Cause | Fix |
| --- | --- | --- |
| File <1KB | Cloudflare blocked | Add `-A "Mozilla/5.0"` to curl |
| `file` shows HTML | CDN returned error page | Check URL, try different User-Agent |
| Upload fails | Wrong folder ID or permissions | Verify folder ID, check OAuth scopes |

## Default Folder

ProductTank SF Sponsor Logos: `1nh4a-uoTK40S7Twm4erJICQaAmsFcXgj`

View: <https://drive.google.com/drive/folders/1nh4a-uoTK40S7Twm4erJICQaAmsFcXgj>

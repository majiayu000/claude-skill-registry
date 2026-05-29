---
name: event-qr-generator
description: Use when generating branded QR codes for ProductTank SF events - speaker LinkedIn profiles, sponsor websites, or Slack join links. Handles single/bulk generation, correct logo mapping, GDrive upload, and mandatory test-scanning.
---

# Event QR Generator

## Quick Reference

| Parameter | Required | Description |
| --- | --- | --- |
| `qrType` | Yes | `speaker`, `sponsor`, or `join-slack` |
| `url` | Conditional | URL to encode (required if no linearTaskId) |
| `linearTaskId` | Conditional | Extract URLs from Linear task description |
| `gDriveFolderId` | No | Upload destination (asks user if missing) |

## Logo Mapping

| qrType | Logo Source | Use Case |
| --- | --- | --- |
| `speaker` | Local: `linkedin-logo.png` | Speaker LinkedIn profiles |
| `sponsor` | **GDrive**: Search for `sponsor-logo-{name}` | Sponsor websites (use actual sponsor logo) |
| `join-slack` | Local: `slack-logo.png` | Slack workspace invites |

## Path Reference

```text
tools/linkedin-qr-generator/
├── assets/
│   ├── linkedin-logo.png      # speaker QRs
│   ├── product-tank-logo.png  # sponsor QRs
│   └── slack-logo.png         # join-slack QRs
├── output/                    # Generated QRs saved here
└── src/linkedin-qr-generator.js
```

## Workflow

### Step 1: Determine Generation Mode

Ask user:
- **Single**: One URL provided directly
- **Bulk**: Extract multiple URLs from Linear task

### Step 2: Gather URLs

**Single mode:**

```text
User provides: url, qrType, name (for filename)
```

**Bulk mode (from Linear task):**

```bash
# Use linear-cli to get task
linear-cli i get {linearTaskId} --output json

# Parse description for URLs matching qrType context
```

### Step 3: Validate qrType-URL Match

STOP if mismatch detected:
- `speaker` URL should be linkedin.com/in/
- `sponsor` URL should be company website
- `join-slack` URL should be slack.com or join link

### Step 4: Get Logo for QR

**For `speaker` and `join-slack`:** Use local assets

```bash
# speaker
LOGO_PATH="tools/linkedin-qr-generator/assets/linkedin-logo.png"

# join-slack
LOGO_PATH="tools/linkedin-qr-generator/assets/slack-logo.png"
```

**For `sponsor`:** Download from GDrive

```bash
# 1. Search GDrive for sponsor logo
mcp__gdrive__gdrive_search query: "sponsor-logo-{SponsorName}"

# 2. Download directly to file (streams to disk, no base64 in context)
mcp__gdrive__gdrive_download_file fileId: {fileId} destPath: "/tmp/sponsor-logo-{name}.png"

# 3. Set logo path
LOGO_PATH="/tmp/sponsor-logo-{name}.png"
```

### Step 5: Generate QR Code(s)

```bash
# Use absolute paths for reliability
node /Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows/tools/linkedin-qr-generator/src/linkedin-qr-generator.js "<URL>" "<LOGO_PATH>"
```

**Examples:**

```bash
# speaker (LinkedIn logo for speaker profiles)
node tools/linkedin-qr-generator/src/linkedin-qr-generator.js "https://linkedin.com/in/johndoe" "tools/linkedin-qr-generator/assets/linkedin-logo.png"

# sponsor (actual sponsor logo from GDrive)
node tools/linkedin-qr-generator/src/linkedin-qr-generator.js "https://sponsor.com" "/tmp/sponsor-logo-WeFunder.png"

# join-slack (Slack logo for invite links)
node tools/linkedin-qr-generator/src/linkedin-qr-generator.js "https://slack.com/invite/xxx" "tools/linkedin-qr-generator/assets/slack-logo.png"
```

**Output location:** `tools/linkedin-qr-generator/output/qr-{timestamp}.png`

### Step 6: Rename Output

```bash
# Generated file: tools/linkedin-qr-generator/output/qr-{timestamp}.png
# Rename to: {qrType}-qr-{name}.png

mv "tools/linkedin-qr-generator/output/qr-*.png" "/tmp/{qrType}-qr-{name}.png"
```

### Step 7: Upload to GDrive

```bash
# Use MCP tool
mcp__gdrive__gdrive_upload_file
  filePath: /tmp/{qrType}-qr-{name}.png
  fileName: {qrType}-qr-{name}.png
  folderId: {gDriveFolderId}  # Ask user if not provided
```

### Step 8: Open for User Test-Scan

**Open QR for user to verify after upload.**

```bash
# Open QR for visual inspection
open "/tmp/{qrType}-qr-{name}.png"
```

Report to user:
- GDrive link provided
- QR opened for test-scanning
- User can confirm QR works (non-blocking)

## Verification Checklist

Before reporting completion:

- [ ] Correct logo used for qrType
- [ ] URL matches expected pattern for qrType
- [ ] Uploaded to GDrive
- [ ] GDrive link provided to user
- [ ] QR opened for user test-scanning (non-blocking)

## Rationalization Counters

**"Tool always works, no need to test"**
→ WRONG. Test EVERY generated QR. Silent failures happen.

**"One spot check is enough for bulk"**
→ WRONG. Test ALL QRs. Each URL could have issues.

**"User provided the URL so it must be correct"**
→ WRONG. Verify URL matches qrType. Users make mistakes.

**"I'll test after uploading"**
→ WRONG. Test BEFORE upload. Don't pollute GDrive with bad QRs.

## Common Issues

| Symptom | Cause | Fix |
| --- | --- | --- |
| QR scans to wrong URL | Wrong URL passed | Double-check URL before generation |
| Wrong logo in QR | Wrong asset path | Verify logo mapping table |
| Command fails | Not in project root | `cd` to cc-workflows first |
| Bulk URLs missed | Incomplete Linear parsing | Re-read task description carefully |

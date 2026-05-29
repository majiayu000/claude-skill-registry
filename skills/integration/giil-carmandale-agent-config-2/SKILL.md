---
name: giil
description: "Get Image [from] Internet Link - download full-resolution images from iCloud, Dropbox, Google Photos, and Google Drive share links. Perfect for remote AI debugging workflows."
---

# giil Skill

Download full-resolution images from cloud photo share links. Zero setup - just paste a link and get the image.

## Why giil?

The primary use case: You're working with Clawdbot or another AI assistant and need to share a screenshot. Instead of complex file transfers, just:

1. Screenshot on your device
2. Share via iCloud/Dropbox/Google Photos
3. Paste the share link
4. giil downloads the full-resolution image instantly

## Supported Platforms

| Platform | URL Patterns | Method |
|----------|--------------|--------|
| **iCloud** | `share.icloud.com/photos/*` | Browser automation |
| **Dropbox** | `dropbox.com/s/*`, `dropbox.com/scl/fi/*` | Direct download (fast!) |
| **Google Photos** | `photos.app.goo.gl/*`, `photos.google.com/share/*` | Browser + CDN |
| **Google Drive** | `drive.google.com/file/d/*` | Multi-tier download |

## Common Commands

### Download Single Image

```bash
# Basic download to current directory
giil "https://share.icloud.com/photos/0a1Abc_xYz..."

# Download to specific directory
giil "https://share.icloud.com/photos/..." --output ~/Downloads

# Dropbox (super fast - no browser needed)
giil "https://www.dropbox.com/s/abc123/screenshot.png"

# Google Photos
giil "https://photos.app.goo.gl/abc123xyz"
```

### JSON Output (Best for AI Workflows)

```bash
# Get structured metadata
giil "https://share.icloud.com/photos/..." --json
```

Output:
```json
{
  "ok": true,
  "platform": "icloud",
  "path": "/path/to/icloud_20240115_143245.jpg",
  "datetime": "2024-01-15T14:32:45.000Z",
  "method": "network",
  "size": 245678,
  "width": 4032,
  "height": 3024
}
```

### Base64 Output

```bash
# Output as base64 (no file saved)
giil "https://share.icloud.com/photos/..." --base64

# Create data URI
echo "data:image/jpeg;base64,$(giil '...' --base64)" > image-uri.txt

# Pipe to API
giil "..." --base64 | curl -X POST -d @- https://api.example.com/upload
```

### Download Entire Album

```bash
# Download all photos from shared album
giil "https://share.icloud.com/photos/..." --all --output ~/album

# With JSON output per photo
giil "https://share.icloud.com/photos/..." --all --json
```

### Quality Options

```bash
# Preserve original bytes (skip MozJPEG compression)
giil "..." --preserve

# Custom JPEG quality (1-100, default 85)
giil "..." --quality 60

# Convert to different format
giil "..." --convert webp
giil "..." --convert png
```

### Debugging

```bash
# Verbose output with progress
giil "..." --verbose

# Save debug artifacts on failure
giil "..." --debug

# Just print the resolved CDN URL (don't download)
giil "..." --print-url

# Increase timeout for slow networks
giil "..." --timeout 120
```

## All Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output DIR` | `.` | Output directory |
| `--preserve` | off | Keep original bytes (skip compression) |
| `--convert FMT` | — | Convert to: `jpeg`, `png`, `webp` |
| `--quality N` | `85` | JPEG quality 1-100 |
| `--base64` | off | Output base64 to stdout |
| `--json` | off | Output JSON metadata |
| `--all` | off | Download all photos from album |
| `--timeout N` | `60` | Page load timeout in seconds |
| `--debug` | off | Save debug artifacts on failure |
| `--verbose` | off | Show detailed progress |
| `--print-url` | off | Just output resolved CDN URL |
| `--update` | off | Force reinstall dependencies |
| `--version` | — | Print version |
| `--help` | — | Show help |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Capture failed |
| `2` | Usage error |
| `3` | Dependency error |
| `10` | Network error |
| `11` | Auth required (not publicly shared) |
| `12` | Not found (expired/deleted) |
| `13` | Unsupported content (video, doc) |

## Scripting Examples

### Check Success

```bash
giil "..." --json | jq -e '.ok' && echo "Success" || echo "Failed"
```

### Get Path Only

```bash
IMAGE_PATH=$(giil "..." --output ~/Downloads 2>/dev/null)
echo "Downloaded: $IMAGE_PATH"
```

### Handle Errors

```bash
giil "https://share.icloud.com/photos/XXX" 2>/dev/null
case $? in
    0) echo "Success!" ;;
    10) echo "Network issue - retry later" ;;
    11) echo "Link not public - ask owner to share" ;;
    12) echo "Link expired" ;;
    *) echo "Failed with code $?" ;;
esac
```

### Download and Analyze with AI

```bash
# Download screenshot and get dimensions
RESULT=$(giil "https://share.icloud.com/photos/..." --json)
WIDTH=$(echo "$RESULT" | jq -r '.width')
HEIGHT=$(echo "$RESULT" | jq -r '.height')
PATH=$(echo "$RESULT" | jq -r '.path')

echo "Image: ${WIDTH}x${HEIGHT} at $PATH"
```

## Clawdbot Workflows

### "Download this screenshot"

When a user pastes a cloud share link:
```
User: Can you look at this screenshot? https://share.icloud.com/photos/0a1...

Clawdbot: *Uses giil to download the image*
giil "https://share.icloud.com/photos/0a1..." --json --output /tmp
```

### "Get all photos from this album"

```
User: Download all photos from this iCloud album: https://share.icloud.com/photos/...

Clawdbot: *Downloads entire album*
giil "..." --all --json --output ~/Downloads/album
```

### "Convert this image to WebP"

```bash
giil "https://share.icloud.com/photos/..." --convert webp --output ~/Downloads
```

### Remote Debugging Workflow

The killer use case - you're helping debug a UI issue remotely:

1. User screenshots bug on iPhone
2. iCloud syncs to Mac
3. User shares link from Photos app
4. User pastes link to Clawdbot
5. Clawdbot runs `giil ... --json` to download
6. AI can now analyze the screenshot

## Performance Notes

- **Dropbox**: Fastest (1-2 seconds, direct curl download)
- **iCloud/Google**: 5-15 seconds (requires headless browser)
- **First run**: Downloads Chromium (~500MB, cached)
- **Album mode**: ~1 second delay between photos (polite rate limiting)

## Troubleshooting

**"Auth required" error**: The link isn't publicly shared. Owner must enable public access.

**Timeout errors**: Increase timeout with `--timeout 120`

**Wrong image captured**: Run with `--debug` to see page state. Report issue with debug artifacts.

**HEIC issues on Linux**: Install `libheif-examples` package.

## File Locations

- **Cache**: `~/.cache/giil/` (Playwright, Chromium, node_modules)
- **Debug artifacts**: Current directory (`giil_debug_*.png`, `giil_debug_*.html`)

## Requirements

- Node.js 18+ (auto-installed if missing)
- macOS 10.15+ or Linux with glibc 2.17+

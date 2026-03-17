---
name: giil
description: "Get Image [from] Internet Link - Zero-setup CLI for downloading full-resolution images from iCloud, Dropbox, Google Photos, and Google Drive share links. Four-tier capture strategy, browser automation, HEIC conversion, album support. Node.js/Playwright."
---

# GIIL — Get Image [from] Internet Link

A zero-setup CLI that downloads full-resolution images from cloud photo shares. The missing link between your iPhone screenshots and remote AI coding sessions.

## Why This Exists

The primary use case: **Remote AI-Assisted Debugging**

You're SSH'd into a remote server running Claude Code, Codex, or another AI assistant. You need to debug a UI issue on your iPhone, but how do you get that screenshot to your remote terminal?

**Without giil:**
```
Download image locally → SCP to server → Tell AI the path
Email yourself → Download on server → Hope it works
Set up complex file sync between devices
```

**With giil:**
```bash
giil "https://share.icloud.com/photos/0a1Abc_xYz..." --json
# {"path": "/tmp/icloud_20240115_143022.jpg", "width": 1170, ...}
```

One command. AI sees it instantly. No file transfers, no context switching.

### The Workflow

```
iPhone Screenshot → iCloud Sync → Photos.app Share Link → Paste to SSH → giil Downloads → AI Analyzes
```

### Why Cloud Shares Are Hard

| Problem | Why It's Hard | How giil Solves It |
|---------|---------------|-------------------|
| JavaScript-heavy SPAs | Standard curl/wget can't execute JS | Headless Chromium via Playwright |
| Dynamic image loading | Images load asynchronously from CDN | Network interception captures CDN responses |
| No direct download links | URLs are session-specific and expire | Clicks Download button or intercepts live requests |
| Copy/paste loses quality | Manual screenshots compress images | Captures original resolution from source |
| HEIC format on Apple | Many tools can't process HEIC/HEIF | Platform-aware conversion (sips/heif-convert) |

## Quick Start

```bash
# Install
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/giil/main/install.sh?v=3.0.0" | bash

# Download single image
giil "https://share.icloud.com/photos/02cD9okNHvVd-uuDnPCH3ZEEA"

# JSON output (best for AI workflows)
giil "https://share.icloud.com/photos/..." --json

# Download entire album
giil "https://share.icloud.com/photos/..." --all --output ~/album
```

**Note:** First run downloads Playwright Chromium (~200MB, cached in `~/.cache/giil/`).

## Supported Platforms

| Platform | URL Patterns | Method | Browser Required |
|----------|--------------|--------|------------------|
| **iCloud** | `share.icloud.com/photos/*`, `icloud.com/photos/#*` | 4-tier capture strategy | Yes |
| **Dropbox** | `dropbox.com/s/*`, `dropbox.com/scl/fi/*` | Direct curl (`raw=1`) | **No** |
| **Google Photos** | `photos.app.goo.gl/*`, `photos.google.com/share/*` | URL extraction + `=s0` modifier | Yes |
| **Google Drive** | `drive.google.com/file/d/*`, `drive.google.com/open?id=*` | Multi-tier with auth detection | Yes |

**Dropbox Fast Path:** Direct curl download with no browser overhead—typically 1-2 seconds.

**Google Photos Full-Res:** Automatically appends `=s0` to CDN URLs for maximum resolution.

## Four-Tier Capture Strategy

giil implements a fallback strategy to maximize reliability:

### 1. Download Button (Highest Quality)
- Locates visible Download button using 9 selector patterns
- Clicks and waits for browser download event
- Obtains **original file** (no re-encoding losses)
- Works with HEIC/HEIF originals

### 2. Network Interception (Full Resolution)
- Monitors all HTTP responses for CDN patterns (`cvws.icloud-content.com`, etc.)
- Filters by content-type (image formats only)
- Captures largest image buffer (>10KB threshold to skip thumbnails)
- Works even if UI elements are obscured

### 3. Element Screenshot
- Queries for image elements using 10 selector patterns
- Verifies element is visible and ≥100×100 pixels
- Takes PNG screenshot of the element

### 4. Viewport Screenshot (Last Resort)
- Captures visible viewport (1920×1080)
- Always succeeds if page loads
- Useful for debugging page state

## Command Reference

### Basic Usage

```bash
giil <url> [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output DIR` | `.` | Output directory |
| `--preserve` | off | Keep original bytes (skip MozJPEG compression) |
| `--convert FMT` | — | Convert to: `jpeg`, `png`, `webp` |
| `--quality N` | `85` | JPEG quality 1-100 |
| `--base64` | off | Output base64 to stdout (no file saved) |
| `--json` | off | Output JSON metadata |
| `--all` | off | Download all photos from album |
| `--timeout N` | `60` | Page load timeout in seconds |
| `--debug` | off | Save debug artifacts on failure |
| `--verbose` | off | Show detailed progress |
| `--trace` | off | Enable Playwright tracing for deep debugging |
| `--print-url` | off | Output resolved CDN URL (don't download) |
| `--debug-dir DIR` | `.` | Directory for debug artifacts |
| `--update` | off | Force reinstall dependencies |

## Output Modes

### Default: File Path

```bash
giil "https://share.icloud.com/photos/XXX"
# stdout: /current/dir/icloud_20240115_143245.jpg
```

**Scripting:**
```bash
IMAGE_PATH=$(giil "..." --output ~/Downloads 2>/dev/null)
```

### JSON Mode

```bash
giil "https://share.icloud.com/photos/XXX" --json
```

**Success:**
```json
{
  "ok": true,
  "schema_version": "1",
  "platform": "icloud",
  "path": "/absolute/path/to/icloud_20240115_143245.jpg",
  "datetime": "2024-01-15T14:32:45.000Z",
  "sourceUrl": "https://cvws.icloud-content.com/...",
  "method": "network",
  "size": 245678,
  "width": 4032,
  "height": 3024
}
```

**Error:**
```json
{
  "ok": false,
  "schema_version": "1",
  "platform": "icloud",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Login required - link is not publicly shared",
    "remediation": "The file is not publicly shared. The owner must enable public access."
  }
}
```

| Field | Description |
|-------|-------------|
| `method` | Capture strategy: `download`, `network`, `element-screenshot`, `viewport-screenshot`, `direct` |
| `error.code` | Error code (see Exit Codes) |
| `error.remediation` | Suggested fix |

### Base64 Mode

```bash
# Decode to file
giil "..." --base64 | base64 -d > image.jpg

# Create data URI
echo "data:image/jpeg;base64,$(giil '...' --base64)" > uri.txt

# Pipe to API
giil "..." --base64 | curl -X POST -d @- https://api.example.com/upload
```

### URL-Only Mode

```bash
giil "https://share.icloud.com/photos/XXX" --print-url
# stdout: https://cvws.icloud-content.com/B/...
```

Useful for external downloaders, caching, or debugging.

## Album Mode

Download entire shared albums with `--all`:

```bash
giil "https://share.icloud.com/photos/XXX" --all --output ~/album
```

### How It Works

1. Load album page
2. Detect thumbnail grid (11 selector strategies)
3. For each thumbnail: click → capture → close → next
4. Output one path/JSON per photo

### Album Features

- **Resilient:** Continues to next photo if one fails
- **Indexed filenames:** `_001`, `_002`, etc. for ordering
- **Rate limiting:** 1 second delay between photos (polite downloading)
- **Exponential backoff:** Automatic retry on rate limit signals

### Album Output

```bash
# Default
/path/to/album/icloud_20240115_143245_001.jpg
/path/to/album/icloud_20240115_143246_002.jpg

# With --json
{"path": "...001.jpg", "method": "download", "width": 4032, ...}
{"path": "...002.jpg", "method": "network", "width": 3024, ...}
```

## Image Processing Pipeline

### EXIF Datetime Extraction

Priority order for filename generation:
1. `DateTimeOriginal` (when photo was taken)
2. `CreateDate`
3. `DateTimeDigitized`
4. `ModifyDate`
5. Current time (fallback)

### HEIC/HEIF Conversion

| Platform | Tool | Notes |
|----------|------|-------|
| macOS | `sips` | Built-in, always available |
| Linux | `heif-convert` | Requires `libheif-examples` package |

```bash
# Install HEIC support on Linux
sudo apt-get install libheif-examples  # Debian/Ubuntu
sudo dnf install libheif-tools         # Fedora
```

### MozJPEG Compression (Default)

By default, giil compresses with MozJPEG for optimal size/quality:
- **40-50% smaller** than standard JPEG at equivalent quality
- **Quality 85** (configurable via `--quality`)
- Use `--preserve` to keep original bytes

### Filename Format

```
icloud_YYYYMMDD_HHMMSS[_NNN][_counter].jpg
        │              │      │
        │              │      └── Collision counter (if file exists)
        │              └── Album index (--all mode only)
        └── Date/time from EXIF or capture time
```

## Download Verification

giil validates downloads through three stages:

### 1. Content-Type Validation
Validates HTTP `Content-Type` matches expected image types.

### 2. Magic Bytes Detection
Verifies binary signature regardless of server claims:

| Format | Magic Bytes |
|--------|-------------|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47` |
| GIF | `47 49 46 38` |
| WebP | RIFF container with WEBP |
| HEIC/HEIF | ISO base media file (ftyp box) |

### 3. HTML Error Page Detection
Rejects HTML content that indicates an error page instead of an image.

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| `0` | Success | Image captured and saved/output |
| `1` | Capture Failure | All capture strategies failed |
| `2` | Usage Error | Invalid arguments or missing URL |
| `3` | Dependency Error | Node.js, Playwright, or Chromium issue |
| `10` | Network Error | Timeout, DNS failure, unreachable host |
| `11` | Auth Required | Login redirect, password required, not publicly shared |
| `12` | Not Found | Expired link, deleted file, 404 |
| `13` | Unsupported Type | Video, Google Doc, or non-image content |
| `20` | Internal Error | Bug in giil (please report!) |

**Scripting:**
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

## Environment Variables

### Runtime Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `XDG_CACHE_HOME` | Base cache directory | `~/.cache` |
| `GIIL_HOME` | giil runtime directory | `$XDG_CACHE_HOME/giil` |
| `PLAYWRIGHT_BROWSERS_PATH` | Custom Chromium cache | `$GIIL_HOME/ms-playwright` |
| `GIIL_NO_GUM` | Disable gum styling | unset |
| `GIIL_CHECK_UPDATES` | Enable update checking | unset |

### Installer Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEST` | Custom install directory | `~/.local/bin` |
| `GIIL_SYSTEM` | Install to `/usr/local/bin` | unset |
| `GIIL_VERIFY` | Verify SHA256 checksum | unset |
| `GIIL_VERSION` | Install specific version | latest |

## File Locations

| Path | Purpose |
|------|---------|
| `~/.local/bin/giil` | Main script |
| `~/.cache/giil/` | Runtime directory |
| `~/.cache/giil/node_modules/` | Playwright, Sharp, exifr |
| `~/.cache/giil/extractor.mjs` | Generated Node.js script |
| `~/.cache/giil/ms-playwright/` | Chromium browser cache |

### Debug Artifacts (on failure with `--debug`)

| File | Contents |
|------|----------|
| `giil_debug_<timestamp>.png` | Full-page screenshot |
| `giil_debug_<timestamp>.html` | Page DOM content |

## Performance

| Phase | First Run | Subsequent |
|-------|-----------|------------|
| Chromium download | 30-60s | Skipped (cached) |
| Browser launch | 2-3s | 2-3s |
| Page load | 3-10s | 3-10s |
| Image capture | 1-5s | 1-5s |
| **Total** | **40-80s** | **5-15s** |

**Dropbox:** 1-2 seconds (direct curl, no browser).

## Troubleshooting

### "Auth required" error
The link isn't publicly shared. Owner must enable public access in their cloud settings.

### Timeout errors
Increase timeout: `giil "..." --timeout 120`

### Wrong/small image captured
Run with `--debug` to see page state. Report issue with debug artifacts.

### HEIC conversion fails on Linux
```bash
sudo apt-get install libheif-examples  # Debian/Ubuntu
sudo dnf install libheif-tools         # Fedora
```

### Chromium fails to launch
```bash
giil "..." --update
# Or manually:
cd ~/.cache/giil && npx playwright install --with-deps chromium
```

### Debugging

```bash
# Verbose output
giil "..." --verbose

# Debug artifacts on failure
giil "..." --debug

# Playwright trace (generates trace.zip)
giil "..." --trace
npx playwright show-trace ~/.cache/giil/trace.zip
```

## Installation

```bash
# One-liner (recommended)
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/giil/main/install.sh?v=3.0.0" | bash

# Verified installation
GIIL_VERIFY=1 curl -fsSL .../install.sh | bash

# System-wide
GIIL_SYSTEM=1 curl -fsSL .../install.sh | bash

# Manual
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/giil/main/giil -o ~/.local/bin/giil
chmod +x ~/.local/bin/giil
```

## Uninstallation

```bash
rm ~/.local/bin/giil
rm -rf ~/.cache/giil
rm -rf ~/.cache/ms-playwright  # If no other Playwright tools
```

## Security & Privacy

- **Local execution:** All processing happens on your machine
- **No telemetry:** No data sent anywhere except to cloud services
- **No authentication stored:** Uses public share mechanism
- **No cookies saved:** Browser context is ephemeral
- **Temp file cleanup:** Downloaded files cleaned up after processing

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **Claude Code** | Download screenshots for visual debugging via SSH |
| **NTM** | Share images between multi-agent sessions |
| **Agent Mail** | Attach downloaded images to agent messages |
| **CASS** | Search sessions that used giil for image context |

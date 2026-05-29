---
name: capture-all-pages
description: >-
   Capture screenshots of all manual pages at high resolution for translation verification. Use when
   verifying that translations match page images, checking layout correctness, or inspecting for
   content mismatches.
---

# Capture All Pages

Capture all pages of the manual viewer at high resolution (2000x1600) for visual verification of translations.

## Purpose

This skill captures screenshots of all pages in the manual viewer to verify that:

- Translations match the page images
- Layout is correct
- No content mismatches or missing translations

## Quick Start

**Prerequisites:**

- Dev server running on port 3100 (`pnpm dev`)
- Playwright installed globally or in project

**Usage:**

```bash
# Capture all pages (default: 30 pages)
node .claude/skills/capture-all-pages/scripts/capture.js

# Capture specific number of pages
node .claude/skills/capture-all-pages/scripts/capture.js --pages 280

# Custom base URL
node .claude/skills/capture-all-pages/scripts/capture.js --base-url http://zmanuals.localhost:3100/manuals/oxi-one-mk2/page
```

## Configuration

The capture script supports these options:

- `--pages <number>` - Total pages to capture (default: 30)
- `--base-url <url>` - Base URL for pages (default: http://zmanuals.localhost:3100/manuals/oxi-one-mk2/page)
- `--output-dir <path>` - Custom output directory (default: __inbox/captures-{timestamp})

**Default settings:**

- Viewport: 2000x1600 (high resolution for detail)
- Output: `__inbox/captures-{YYYYMMDD}-{HHMMSS}/`
- Format: PNG files named `page-001.png` to `page-NNN.png`
- Timeout: 15 seconds per page
- Wait after load: 2 seconds

## Execution Workflow

1. **Verify dev server is running**

   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://zmanuals.localhost:3100/manuals/oxi-one-mk2/page/1
   # Should return 200
   ```

2. **Run capture script**

   ```bash
   node .claude/skills/capture-all-pages/scripts/capture.js
   ```

   The script will:

   - Create timestamped output directory
   - Launch headless browser
   - Capture each page sequentially
   - Report progress and errors
   - Save summary.json with results

3. **Check results**

   ```bash
   ls -lh __inbox/captures-*/page-*.png
   ```

## Output Structure

```
__inbox/captures-20260103-163245/
├── page-001.png (2000x1600)
├── page-002.png (2000x1600)
├── page-003.png (2000x1600)
...
├── page-030.png (2000x1600)
└── summary.json (capture results)
```

**summary.json contains:**

- Timestamp and configuration
- Success/failure counts
- Error details for failed captures

## Notes

- All screenshots saved to project's `__inbox/` directory (gitignored)
- Session timestamp prevents overwriting previous captures
- Script uses headless Chromium (no visible browser window)
- Failed page captures are logged but don't stop the script
- High resolution (2000x1600) allows detailed inspection of translations

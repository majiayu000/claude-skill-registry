---
name: verify-translation
description: >-
  Capture all manual pages and verify translations match page images using AI-powered checking.
  Identifies extraction failures and can regenerate extracted text from images.
invocable: user
---

# Translation Verification Skill

AI-powered verification of translations against original PDF page images. This skill performs comprehensive checking to identify pages where PDF text extraction failed or was incomplete.

## Purpose

After translation is complete, this skill:

1. Captures high-resolution screenshots of all pages
2. For EACH page, compares the PDF image with the translation text
3. Identifies pages where extraction failed (missing content)
4. Reports pages needing manual fixes
5. Can regenerate extracted text from images when extraction failed

## When to Use

- After running `/pdf-process` to translate a manual
- As the final verification step before deployment
- When users report translation issues

## Arguments

```
/verify-translation <slug>
```

- `slug`: Manual slug (e.g., `oxi-e16-manual`, `oxi-coral`)

## Execution Steps

### 1. Validate Arguments

```bash
# Extract slug from arguments
SLUG=$1

# Check if slug is provided
if [ -z "$SLUG" ]; then
  echo "Error: Manual slug required"
  echo "Usage: /verify-translation <slug>"
  exit 1
fi
```

### 2. Build and Serve Production Build

**Use production build for faster and more reliable page serving:**

```bash
# Build the project
pnpm build

# Start production server in background
pnpm serve &
SERVE_PID=$!

# Wait for server to be ready
sleep 3

# Verify server is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:8030/manuals/$SLUG/page/1
```

**Why build+serve instead of dev?**

- Dev server is slow and sometimes unreliable
- Production build is optimized and faster
- `pnpm serve` uses port 8030 by default

### 3. Get Total Page Count

Read the manifest to determine total pages:

```bash
cat public/$SLUG/data/manifest.json | grep totalPages
# Extract the number, e.g., "totalPages": 74 → 74
```

### 4. Capture All Pages (Lightweight Script)

**Use the lightweight capture script (NOT MCP Playwright):**

```bash
node .claude/skills/verify-translation/scripts/capture-pages.js \
  --slug $SLUG \
  --pages $TOTAL_PAGES \
  --port 8030
```

This script:

- Uses direct Playwright scripting (much lighter than MCP Playwright)
- Captures all pages at 2000x1600 resolution
- Saves to `__inbox/verify-{slug}-{date}-{session}/`
- Outputs summary.json with results
- Low token consumption compared to MCP approach

**Output directory structure:**

```
__inbox/verify-oxi-e16-manual-20260112-abc123/
├── page-001.png
├── page-002.png
├── ...
├── page-074.png
└── summary.json
```

### 5. AI-Powered Verification (CRITICAL)

For EACH captured page, perform visual verification by reading the screenshot:

**5.1 Read the page screenshot** using the Read tool

```
Read: __inbox/verify-{slug}-{date}/page-001.png
```

**5.2 Compare PDF image vs Translation text:**

Look at the screenshot which shows:

- LEFT side: Original PDF page image
- RIGHT side: Japanese translation text

Check if the translation covers ALL visible content in the PDF image.

**5.3 Check for these issues:**

| Issue | Description | Action |
|-------|-------------|--------|
| Missing header | PDF shows section header but translation starts mid-content | Flag for fix |
| Missing paragraphs | PDF has more paragraphs than translation shows | Flag for fix |
| Content order wrong | Translation starts from middle of page | Flag for fix |
| Extraction failure | Large portions of PDF text not in translation | Flag for fix |
| Page mismatch | Translation content doesn't match PDF at all | Flag for fix |

**5.4 Record findings:**

```json
{
  "pageNum": 49,
  "status": "needs_fix",
  "issues": ["Missing header: 'Scenes 3'", "Missing paragraph about 12 pages with 16 parameters"],
  "pdfContentSummary": "Header 'Scenes 3', section '3.2 Scene Pages', explanation paragraph, control diagram, note",
  "translationContentSummary": "Only control diagram and note - missing header and explanation"
}
```

### 6. Fix Pages with Extraction Failures

For each page flagged as needing fix:

**6.1 Regenerate extracted text from PDF image:**

Look at the PDF image (left side of screenshot) and extract ALL visible English text in correct reading order:

```
# Example for page 49
Scenes 3

3.2 Scene Pages

Each scene has 12 pages which contains 16 parameters. A total of 192 parameters are therefore available in each scene. Organising parameters in pages allows them to be managed in an easy and structured way.

S. 1-P. 1
[... rest of content ...]
```

**6.2 Update the extracted text file:**

```bash
# Write corrected text to extracted file
Write to: public/$SLUG/processing/extracted/page-049.txt
```

**6.3 Re-run translation for that page:**

```xml
<invoke name="Task">
  <parameter name="subagent_type">manual-translator</parameter>
  <parameter name="description">Re-translate page 49</parameter>
  <parameter name="prompt">Translate page 49 of the manual.
Source: /path/to/extracted/page-049.txt
Output: /path/to/translations-draft/page-049.json
Page: 49, Total: 74</parameter>
</invoke>
```

### 7. Rebuild and Re-verify

After fixing pages:

```bash
# Copy translations to expected location for build
mkdir -p public/manuals/$SLUG/processing/translations-draft
cp public/$SLUG/processing/translations-draft/*.json public/manuals/$SLUG/processing/translations-draft/

# Rebuild pages.json
pnpm run pdf:build --slug $SLUG

# Copy back to correct location
cp public/manuals/$SLUG/data/pages.json public/$SLUG/data/pages.json
rm -rf public/manuals/

# Format
pnpm format:fix
```

### 8. Stop Serve Process

```bash
# Kill the serve process
kill $SERVE_PID 2>/dev/null || true

# Or find and kill by port
lsof -ti:8030 | xargs kill -9 2>/dev/null || true
```

### 9. Generate Report

Output a verification report:

```markdown
## Translation Verification Report

**Manual:** oxi-e16-manual
**Total Pages:** 74
**Date:** 2026-01-12

### Verification Results

| Status | Count |
|--------|-------|
| Passed | 71 |
| Fixed | 3 |
| Failed | 0 |

### Pages Fixed

| Page | Issues Found | Fix Applied |
|------|--------------|-------------|
| 35 | Missing header content | Regenerated extraction, re-translated |
| 48 | Page mismatch | Regenerated extraction, re-translated |
| 49 | Missing header and paragraph | Regenerated extraction, re-translated |

### Verification Complete

All pages now match their PDF images.
```

## Capture Script Details

The capture script at `.claude/skills/verify-translation/scripts/capture-pages.js`:

**Usage:**

```bash
node .claude/skills/verify-translation/scripts/capture-pages.js \
  --slug oxi-e16-manual \
  --pages 74 \
  --port 8030
```

**Options:**

- `--slug <slug>` - Manual slug (required)
- `--pages <number>` - Total pages to capture (required)
- `--port <number>` - Server port (default: 8030)
- `--output-dir <path>` - Custom output directory

**Benefits over MCP Playwright:**

- Direct Playwright scripting (no MCP overhead)
- Single browser session for all pages
- Resource blocking for faster capture
- Compact JSON output
- Much lower token consumption

## Important Notes

### Why This Verification is Needed

PDF text extraction (`pdf-parse` library) can fail due to:

- Text embedded in graphical elements
- Complex multi-column layouts
- Text in separate layers or text boxes
- Font encoding issues

The `manual-translator` subagent only receives extracted text - it cannot see the PDF image. Therefore, verification must happen at the main agent level where we can compare images with translations.

### Verification Strategy

**Quick check (5-10 sample pages):**

- For large manuals, first check sample pages (1, 10%, 25%, 50%, 75%, 100%)
- If samples pass, do spot checks on remaining pages

**Full check (all pages):**

- For smaller manuals (< 50 pages), verify every page
- For production releases, always do full verification

### Content Order Verification

Check that translation content follows the same order as the PDF image:

1. First content in PDF image should be first in translation
2. Section headers should appear in same sequence
3. Numbered items should be in correct order

If order is wrong, the extracted text file needs to be reordered before re-translation.

## Output

- Verification screenshots: `__inbox/verify-{slug}-{date}-{session}/`
- Summary JSON: `__inbox/verify-{slug}-{date}-{session}/summary.json`
- Verification report: Displayed in conversation
- Fixed pages: Listed with issues found and fixes applied

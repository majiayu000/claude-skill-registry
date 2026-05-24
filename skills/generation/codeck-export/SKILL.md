---
name: codeck-export
version: 2.1.0
description: |
  Publisher role. Exports deck to PDF or PPTX with post-export QA.
  Use whenever the user says "export", "to PDF", "to PPTX",
  "PowerPoint", "print", "download", "save as PDF", "convert", or wants
  to convert a finished deck to PDF or PPTX.
---

# codeck export

Minimum conversation, maximum output. Export the deck to the user's format.

## Step 1: Status

```bash
DECK_DIR="$HOME/.codeck/projects/$(basename "$(pwd)")"
mkdir -p "$DECK_DIR"
bash "$HOME/.claude/skills/codeck/scripts/status.sh" "$DECK_DIR"
```

Gate check: if no assembled HTML exists (`./*-r*.html`), suggest running `/codeck-design` first.

## Step 2: Format

- A) HTML — open in browser, press F for fullscreen, arrow keys to navigate. Zero dependencies. (recommended)
- B) PDF — email attachments, printing
- C) PPTX — corporate requirements
- D) All

## Step 3: Export

Find the HTML file (`./*-r*.html` in the user's project directory), derive baseName.

### HTML

Already exists. Open in browser, F for fullscreen, arrows to navigate.

### PDF — print from HTML

Use Playwright for WYSIWYG PDF:

```bash
npx playwright install chromium 2>/dev/null || true
```

```javascript
import { chromium } from 'playwright';
import { resolve } from 'path';
import { readdirSync } from 'fs';
import { pathToFileURL } from 'url';

const html = readdirSync('.').find(f => /-r\d+\.html$/.test(f));
const baseName = html.replace('.html', '');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(resolve(html)).toString(), { waitUntil: 'networkidle' });
await page.emulateMedia({ media: 'screen' });
await page.pdf({
  path: `${baseName}.pdf`,
  printBackground: true,
  preferCSSPageSize: true,
  margin: { top: '12mm', right: '12mm', bottom: '12mm', left: '12mm' }
});
await browser.close();
console.log(`done: ${baseName}.pdf`);
```

### Poster assets

`.media-poster` elements in slides.html are video/audio placeholders. Original file paths are in the caption and outline.md asset manifest.

Default: keep placeholders in export. If user says "embed video", extract path from caption, use `slide.addMedia({ path: "..." })` for PPTX.

### PPTX — from HTML

**Option A (recommended): LibreOffice**

```bash
EXPORT_SCRIPTS="$HOME/.claude/skills/codeck-export/pptx/scripts"
python "$EXPORT_SCRIPTS/office/soffice.py" --headless --convert-to pdf ./*-r*.html
python "$EXPORT_SCRIPTS/office/soffice.py" --headless --convert-to pptx ./*-r*.html
```

**Option B (fallback): screenshot embed**

If soffice unavailable, use Playwright to screenshot each page, then PptxGenJS to embed screenshots as slides. Read `export/pptx/pptxgenjs.md` for the API.

## Step 4: QA (required for PDF/PPTX)

**Assume the export has problems. Find them.**

### PDF

Check: pages complete (no truncation), backgrounds render, fonts display correctly.

### PPTX

Generate thumbnails:

```bash
EXPORT_SCRIPTS="$HOME/.claude/skills/codeck-export/pptx/scripts"
python "$EXPORT_SCRIPTS/thumbnail.py" ./*-r*.pptx
```

Convert to images for detailed check:

```bash
python "$EXPORT_SCRIPTS/office/soffice.py" --headless --convert-to pdf ./*-r*.pptx
pdftoppm -jpeg -r 150 *.pdf slide-check
```

Use subagent to visually inspect screenshots. Focus on: overlapping elements, text overflow, uneven spacing, low-contrast text, differences from HTML original.

### Fix loop

1. Find issue → adjust export params or HTML
2. Re-export → re-screenshot → re-check
3. Until one full check finds no new issues

At least one fix-verify cycle before declaring done.

## Step 5: Done

> Export done. Output: `{baseName}.pdf` / `{baseName}.pptx`
>
> Need a speech script? `/codeck-speech`. Otherwise you're done — run `/codeck` anytime for an overview.

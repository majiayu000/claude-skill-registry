---
name: pdf-design
description: Design and edit professional PDF reports and proposals with live preview
user_invocable: true
trigger_patterns:
  - "create.*report"
  - "create.*proposal"
  - "pdf.*report"
  - "funding.*proposal"
  - "design.*pdf"
  - "make.*proposal"
  - "edit.*report"
  - "preview.*report"
---

# PDF Design System

Create and edit professional PDF reports and funding proposals with live preview and iterative design.

## Interactive editing mode

During a design session, use these commands:

| Command | Action |
|---------|--------|
| `preview` | Screenshot current state |
| `preview page N` | Screenshot specific page |
| `show cover` | Preview cover page |
| `show budget` | Preview budget section |
| `regenerate` | Create new PDF |
| `upload` | Upload to Google Drive |
| `done` | Finish session |

**Workflow:**
1. You say "preview" → I show current state
2. You describe changes → I implement them
3. Repeat until done → Generate final PDF

---

## Quick start

```bash
# Copy template to start new report
cp ~/.claude/plugins/pdf-design/templates/democracy-day-proposal.html ./new-report.html

# Generate PDF (must use snap-accessible path)
mkdir -p ~/snap/chromium/common/pdf-work
cp new-report.html ~/snap/chromium/common/pdf-work/
chromium-browser --headless --disable-gpu \
  --print-to-pdf="$HOME/snap/chromium/common/pdf-work/output.pdf" \
  --no-pdf-header-footer \
  "file://$HOME/snap/chromium/common/pdf-work/new-report.html"
```

## Document types

- **Funding proposals** — Grant requests with budgets
- **Program reports** — Initiative updates
- **Impact reports** — Metrics and outcomes
- **Budget summaries** — Financial breakdowns

## Key principles

1. **Sentence case** — Never Title Case
2. **Left-aligned** — Never justified text
3. **Print-ready** — 8.5" × 11" letter size
4. **Brand consistent** — CCM red or program palettes

---

## Brand guidelines

### CCM standard colors
```css
:root {
    --ccm-red: #CA3553;
    --ccm-black: #000000;
    --ccm-gray: #666666;
    --ccm-light: #e2e8f0;
}
```

### Program-specific (Democracy Day)
```css
:root {
    --civic-navy: #1a2b4a;
    --civic-blue: #2d4a7c;
    --civic-gold: #c9a227;
    --civic-red: #b31942;
}
```

### Typography
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
```

```css
body {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 0.875rem;
    line-height: 1.6;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
}
```

---

## HTML structure

### Page setup
```css
@page { size: letter; margin: 0; }

.page {
    width: 8.5in;
    height: 11in;
    display: grid;
    grid-template-rows: auto 1fr auto;
    overflow: hidden;
    page-break-after: always;
}
```

### Cover page
```html
<div class="page cover">
    <div class="cover-header">
        <div class="cover-org">Center for Cooperative Media</div>
        <h1 class="cover-title">Report title</h1>
        <p class="cover-intro">Brief description.</p>
    </div>
    <div class="cover-footer">
        <div class="cover-stats"><!-- Stats --></div>
        <div class="cover-footer-right">
            <div class="cover-date">February 2026</div>
            <div class="cover-logo"><img src="..." alt="Logo"></div>
        </div>
    </div>
</div>
```

### Content page
```html
<div class="page content-page">
    <div class="page-header">
        <div class="page-header-title">Document title</div>
        <div class="page-number">2</div>
    </div>
    <div class="page-body">
        <!-- Content goes here -->
    </div>
    <footer class="page-footer">
        <!-- Footer -->
    </footer>
</div>
```

### Budget table
```html
<table class="budget-table">
    <thead>
        <tr><th>Expense</th><th>Per year</th><th>Total</th></tr>
    </thead>
    <tbody>
        <tr>
            <td>Item<span class="item-desc">Details</span></td>
            <td>$10,000</td>
            <td>$20,000</td>
        </tr>
    </tbody>
    <tfoot>
        <tr><td>Total</td><td>$50,000</td><td>$100,000</td></tr>
    </tfoot>
</table>
```

### Page footer
```css
.page-body {
    padding: 0.2in 0.65in 0.3in;
    overflow: hidden;
}

.page-footer {
    padding: 0 0.65in 0.5in;
    border-top: 1px solid #e2e8f0;
    font-size: 0.8rem;
}
```

---

## Footer clearance

Content must not touch or overlap the page footer. These rules apply to **content pages** — cover pages and special layouts may use different structures.

- Content pages must use `display: grid; grid-template-rows: auto 1fr auto` on `.page`
- Content pages must have exactly 3 direct children: header, content wrapper (`.page-body`), footer
- The content wrapper must have `overflow: hidden` to prevent text bleeding
- Never use `position: absolute` for footers — keep them in normal document flow as the third grid row
- Use `.page-footer:empty { display: none; }` so pages without footer content don't render a blank border
- If content is too long, reduce content rather than shrinking the footer gap

---

## PDF generation

### Chromium (snap-confined)
```bash
# Must use ~/snap/chromium/common/ path
mkdir -p ~/snap/chromium/common/pdf-work
cp template.html ~/snap/chromium/common/pdf-work/
chromium-browser --headless --disable-gpu \
  --print-to-pdf="$HOME/snap/chromium/common/pdf-work/output.pdf" \
  --no-pdf-header-footer \
  "file://$HOME/snap/chromium/common/pdf-work/template.html"
cp ~/snap/chromium/common/pdf-work/output.pdf ./
```

### Preview pages
```bash
# PDF to PNG
pdftoppm -png -f 1 -l 1 output.pdf preview

# Page count
pdfinfo output.pdf | grep Pages
```

### Legion browser preview
```bash
~/.claude/scripts/legion-browser.py screenshot "file:///path/to/template.html" -o preview.png
```

---

## Google Drive upload

```python
cd ~/.claude/workstation/mcp-servers/gmail && source .venv/bin/activate
python3 << 'PYEOF'
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json

with open('/home/jamditis/.claude/google/drive-token.json') as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data['access_token'],
    refresh_token=token_data.get('refresh_token'),
    token_uri='https://oauth2.googleapis.com/token',
    client_id=token_data.get('client_id'),
    client_secret=token_data.get('client_secret')
)

service = build('drive', 'v3', credentials=creds)

# Upload new file
file_metadata = {
    'name': 'Report.pdf',
    'parents': ['1lKTdwq4_5uErj-tBN112WCdJGD2YtetO']  # Shared with Joe
}
media = MediaFileUpload('/path/to/output.pdf', mimetype='application/pdf')
file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
print(f"Uploaded: {file.get('webViewLink')}")
PYEOF
```

### Drive folders
- **Shared with Joe:** `1lKTdwq4_5uErj-tBN112WCdJGD2YtetO`
- **Claude Workspace:** `1e5dtKOiuvk0PPrFq3UyNI2UAa6RFiom3`

---

## Known issues

1. **Base64 images** — Don't read HTML with large base64 using Read tool (API error). Use sed/grep/Python.
2. **Snap confinement** — Chromium can only write to `~/snap/chromium/common/`
3. **Fonts** — Google Fonts via CDN; for offline, embed as base64

## Logo locations

- CCM logo: `~/.claude/plugins/pdf-design/templates/` (embedded in template)
- Brand assets: `/home/jamditis/projects/cjs2026/public/internal/brand_web_assets/`

## Template

Reference: `~/.claude/plugins/pdf-design/templates/democracy-day-proposal.html`

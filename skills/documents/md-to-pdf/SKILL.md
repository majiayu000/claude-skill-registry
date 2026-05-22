---
name: pdf-conversion
description: |
  Converts Markdown files to professional PDF documents using WeasyPrint.
  Use when user wants to convert markdown to PDF, export as PDF, or generate PDF from documents.
  Supports custom CSS styling, page headers/footers, and Autodesk brand themes.
---

# Markdown to PDF Converter Skill

## Purpose
Convert Markdown files to professional PDF documents using WeasyPrint (HTML→PDF engine) with customizable CSS styling. Runs entirely in sandbox with no external dependencies beyond Python packages.

---

## Architecture

### Technology Stack
| Component | Library | Purpose |
|-----------|---------|---------|
| MD Parser | `markdown` | Convert Markdown → HTML with extensions |
| PDF Engine | `weasyprint` | Render HTML+CSS → PDF |
| Styling | Custom CSS | Professional typography and layout |

### Why This Stack?
- **Pure Python**: No subprocess calls, no external tools (Pandoc, LaTeX) required
- **Sandbox-Safe**: Works within Cursor sandbox restrictions
- **CSS Control**: Full styling customization via CSS
- **Quality Output**: Professional typography with proper page handling

---

## Features

### Markdown Support
| Feature | Status | Notes |
|---------|--------|-------|
| Headers (h1-h6) | ✅ | Proper hierarchy styling |
| Bold/Italic | ✅ | Standard inline formatting |
| Lists (ordered/unordered) | ✅ | Nested list support |
| Code blocks | ✅ | Syntax-highlighted with fenced_code |
| Tables | ✅ | GFM-style tables |
| Links | ✅ | Clickable in PDF |
| Images | ✅ | Embedded (local paths) |
| Blockquotes | ✅ | Styled callouts |
| Horizontal rules | ✅ | Section dividers |
| Task lists | ✅ | Checkbox rendering |
| Footnotes | ✅ | End-of-document notes |
| Table of Contents | ✅ | Auto-generated with `[TOC]` |

### PDF Features
- **Page sizes**: A4, Letter, Legal, custom dimensions
- **Margins**: Configurable (default: 2.5cm)
- **Headers/Footers**: Page numbers, document title, date
- **Page breaks**: Before major sections (configurable)
- **Typography**: Professional fonts, proper line-height

---

## Workflow

### Step 1: Understand Request
- What Markdown file(s) need conversion?
- Any specific styling requirements?
- Output filename/location preference?
- Page size requirements (A4 default)?

### Step 2: Check/Setup Environment
```bash
# One-time setup (if not done)
cd /Users/samarvir/code/autodesk/Product\ management
source .venv/bin/activate
pip install markdown weasyprint
```

### Step 3: Execute Conversion
```bash
# Basic conversion
python .claude/skills/md-to-pdf/convert_md_to_pdf.py input.md output.pdf

# With options
python .claude/skills/md-to-pdf/convert_md_to_pdf.py input.md output.pdf \
  --css custom.css \
  --page-size letter \
  --title "Document Title"
```

### Step 4: Report Results
```
**PDF Generated Successfully**

**Input**: input.md
**Output**: Output/document.pdf
**Pages**: [N] pages
**Size**: [X] KB

Styling: [default/custom CSS path]
```

---

## Usage Options

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `input` | positional | required | Input Markdown file path |
| `output` | positional | required | Output PDF file path |
| `--css` | string | default.css | Custom CSS file path |
| `--page-size` | string | `a4` | Page size: a4, letter, legal |
| `--margin` | string | `2.5cm` | Page margins |
| `--title` | string | (from md) | Document title for header |
| `--no-toc` | flag | false | Disable table of contents |
| `--no-header` | flag | false | Disable page header |
| `--no-footer` | flag | false | Disable page footer |

### Examples

#### Basic Conversion
```bash
python .claude/skills/md-to-pdf/convert_md_to_pdf.py \
  Initiatives/docs-integration/prd.md \
  Output/prd.pdf
```

#### With Custom Styling
```bash
python .claude/skills/md-to-pdf/convert_md_to_pdf.py \
  Initiatives/ai-renderings/case-for-a-new-squad.md \
  Operations/adhoc/ai-renderings/proposal.pdf \
  --css .claude/skills/md-to-pdf/styles/autodesk.css \
  --title "AI Renderings Squad Proposal"
```

#### Letter Size for US Audience
```bash
python .claude/skills/md-to-pdf/convert_md_to_pdf.py \
  document.md \
  document.pdf \
  --page-size letter \
  --margin 1in
```

---

## CSS Themes

### Available Themes
| Theme | File | Use Case |
|-------|------|----------|
| Default | `default.css` | Clean, professional documents |
| Autodesk | `autodesk.css` | Autodesk brand colors |
| Minimal | `minimal.css` | Simple, no-frills output |

### Custom CSS
Create your own CSS file with:
- `@page` rules for margins, headers, footers
- Typography settings (fonts, sizes, line-height)
- Table styling
- Code block formatting
- Color schemes

Example custom CSS sections:
```css
/* Page setup */
@page {
  size: A4;
  margin: 2.5cm;
  @top-center { content: "Document Title"; }
  @bottom-right { content: "Page " counter(page); }
}

/* Typography */
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.6;
}

/* Headers */
h1 { color: #1D91D0; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
```

---

## Output Location Guidelines

Follow the project's Output Location Protocol:

| Document Type | Save To | Example |
|---------------|---------|---------|
| **Initiative PRDs** | `Initiatives/[name]/` | `Initiatives/ai-renderings/prd.pdf` |
| **Leadership Docs** | `Operations/recurring/` | `leadership-reviews/q1-2026.pdf` |
| **Ad-hoc Analysis** | `Operations/adhoc/[topic]/` | `adhoc/market-analysis/report.pdf` |
| **Test/Temporary** | `Output/` | `Output/test.pdf` |

---

## Security Compliance

| Rule | Implementation |
|------|----------------|
| No user input in file paths | Validated input/output paths |
| No `eval`/`exec` | Pure library API calls |
| No subprocess | WeasyPrint is pure Python |
| Input validation | File existence checks |
| Sandboxed execution | Runs in Cursor sandbox |
| Resource limits | Handles large files gracefully |

### Input Sanitization
- HTML content is escaped by default
- Raw HTML in Markdown disabled unless explicitly enabled
- Image paths validated (local only, no URLs without flag)
- File size warnings for documents > 1MB source

---

## Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing fonts | System fonts not available | Use web-safe fonts in CSS |
| Images not showing | Relative paths broken | Use absolute paths or `--base-path` |
| Tables overflow | Wide tables | Add `table { width: 100%; }` to CSS |
| No page breaks | CSS missing rules | Add `h1 { page-break-before: always; }` |
| WeasyPrint warnings | Font/CSS issues | Usually safe to ignore |

### Debug Mode
```bash
python .claude/skills/md-to-pdf/convert_md_to_pdf.py input.md output.pdf --debug
```
Outputs:
- Intermediate HTML (for inspection)
- CSS applied
- Any warnings/errors

---

## File Locations

| File | Purpose |
|------|---------|
| `.claude/skills/md-to-pdf/SKILL.md` | This documentation |
| `.claude/skills/md-to-pdf/convert_md_to_pdf.py` | Main converter script |
| `.claude/skills/md-to-pdf/default.css` | Default styling |
| `.claude/skills/md-to-pdf/styles/` | Additional CSS themes |

---

## Setup (One-Time)

```bash
cd /Users/samarvir/code/autodesk/Product\ management
source .venv/bin/activate
pip install markdown weasyprint
```

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| `markdown` | >=3.4 | Markdown parsing with extensions |
| `weasyprint` | >=60.0 | HTML to PDF rendering |

### System Requirements
WeasyPrint requires some system libraries. On macOS:
```bash
brew install pango
```

If you encounter font issues:
```bash
brew install fontconfig
```

---

## API Usage (Programmatic)

For integration with other scripts:

```python
from convert_md_to_pdf import MarkdownToPDF

converter = MarkdownToPDF(
    css_path="default.css",
    page_size="a4",
    margin="2.5cm"
)

# Convert file
converter.convert_file("input.md", "output.pdf")

# Convert string
converter.convert_string(
    markdown_text="# Hello World\n\nThis is a test.",
    output_path="output.pdf",
    title="Test Document"
)
```

---

## Best Practices

### DO
- ✅ Use semantic Markdown (proper header hierarchy)
- ✅ Keep images local or use absolute URLs
- ✅ Test with `--debug` first for complex documents
- ✅ Use CSS for all styling (not inline HTML)
- ✅ Add `[TOC]` for documents > 5 pages

### DON'T
- ❌ Embed raw HTML unless necessary
- ❌ Use complex nested tables
- ❌ Expect pixel-perfect browser rendering
- ❌ Use remote images without `--allow-remote` flag

---

## Response Templates

### Conversion Acknowledgment
```
I'll convert the Markdown file to PDF.

**Input**: [filename.md]
**Output**: [path/output.pdf]
**Styling**: [default/custom]
**Page Size**: [A4/Letter]

Converting...
```

### Conversion Complete
```
**PDF Generated Successfully**

**File**: `Output/[filename].pdf`
**Pages**: [N] pages
**Size**: [X] KB

The PDF includes:
- [TOC if present]
- [N] sections
- [N] tables
- [N] images

Open the PDF to review formatting.
```

### Conversion Failed
```
**PDF Generation Failed**

**Error**: [error message]

Troubleshooting:
1. [specific fix based on error]
2. Run with `--debug` for more info
3. Check CSS syntax if using custom styles
```

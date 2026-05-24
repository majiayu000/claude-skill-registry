---
name: markdown-to-pdf
description: Convert markdown files to PDF with custom styling. Use when generating PDF documents from markdown, creating printable documentation, or exporting reports.
---

# markdown-to-pdf

Convert markdown files to professionally-styled PDF documents.

## Installation Required

```bash
cd .claude/skills/markdown-to-pdf
npm install
```

**Dependencies:** `md-to-pdf` (includes Puppeteer, auto-downloads Chromium ~200MB)

## Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-to-pdf/scripts/convert.cjs \
  --file ./README.md

# Custom output path
node .claude/skills/markdown-to-pdf/scripts/convert.cjs \
  --file ./doc.md \
  --output ./output/doc.pdf

# Custom styling
node .claude/skills/markdown-to-pdf/scripts/convert.cjs \
  --file ./report.md \
  --style ./custom-style.css
```

## CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input markdown file |
| `--output <path>` | No | Output PDF path (default: input name + .pdf) |
| `--style <path>` | No | Custom CSS file |

## Output Format (JSON)

```json
{
  "success": true,
  "input": "/path/to/input.md",
  "output": "/path/to/output.pdf",
  "pages": 5
}
```

## Default Styling

- GitHub-flavored markdown
- Code syntax highlighting (highlight.js)
- Sans-serif body (system fonts)
- Monospace code blocks
- A4 page size, 2cm margins

## Customization

Create custom CSS:

```css
body {
  font-family: Georgia, serif;
  font-size: 12pt;
  line-height: 1.6;
}
h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
code { background: #f4f4f4; padding: 2px 6px; }
```

## Troubleshooting

**Chromium download fails:** Set `PUPPETEER_SKIP_DOWNLOAD=1` then manually install Chrome
**Memory issues:** Large docs may need `--max-old-space-size=4096`

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

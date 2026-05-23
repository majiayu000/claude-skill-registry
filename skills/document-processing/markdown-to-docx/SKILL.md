---
name: markdown-to-docx
description: Convert markdown files to Microsoft Word (.docx) with custom styling. Use when generating Word documents from markdown, creating editable documentation, or exporting reports for Microsoft Office.
---

# markdown-to-docx

Convert markdown files to Microsoft Word (.docx) documents.

## Installation Required

```bash
cd .claude/skills/markdown-to-docx
npm install
```

**Dependencies:** `markdown-docx` (uses docx internally)

## Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-to-docx/scripts/convert.cjs \
  --file ./README.md

# Custom output path
node .claude/skills/markdown-to-docx/scripts/convert.cjs \
  --file ./doc.md \
  --output ./output/doc.docx
```

## CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input markdown file |
| `--output <path>` | No | Output DOCX path (default: input name + .docx) |

## Output Format (JSON)

```json
{
  "success": true,
  "input": "/path/to/input.md",
  "output": "/path/to/output.docx",
  "wordCount": 1523
}
```

## Supported Markdown Elements

- Headings (H1-H6)
- Paragraphs and emphasis (bold, italic)
- Ordered and unordered lists
- Code blocks
- Tables (GFM style)
- Links and images (local + URL)
- Blockquotes

## Default Styling

Uses markdown-docx default styling:

- Standard Word fonts
- Professional formatting
- Letter/A4 page size

## Troubleshooting

**Dependencies not found:** Run `npm install` in skill directory
**Image not loading:** Ensure path is correct; URL images require network access (10s timeout)

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

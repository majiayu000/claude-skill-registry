---
name: docx-to-markdown
description: Convert Microsoft Word (.docx) files to Markdown. Use when importing Word documents, extracting content from DOCX for version control, or converting documentation to Markdown format.
allowed-tools: Bash, Read, Write
---

# docx-to-markdown

Convert Microsoft Word (.docx) documents to Markdown format.

## Installation Required

```bash
cd .claude/skills/docx-to-markdown
npm install
```

**Dependencies:** `mammoth`, `turndown`, `@truto/turndown-plugin-gfm`

## Quick Start

```bash
# Basic conversion
node .claude/skills/docx-to-markdown/scripts/convert.cjs \
  --file ./document.docx

# Custom output path
node .claude/skills/docx-to-markdown/scripts/convert.cjs \
  --file ./doc.docx \
  --output ./output/doc.md

# Extract images to directory
node .claude/skills/docx-to-markdown/scripts/convert.cjs \
  --file ./doc.docx \
  --output ./output/doc.md \
  --images ./output/images/
```

## CLI Options

| Option            | Required | Description                                             |
| ----------------- | -------- | ------------------------------------------------------- |
| `--file <path>`   | Yes      | Input DOCX file                                         |
| `--output <path>` | No       | Output Markdown path (default: input name + .md)        |
| `--images <dir>`  | No       | Directory for extracted images (default: inline base64) |

## Output Format (JSON)

```json
{
  "success": true,
  "input": "/path/to/input.docx",
  "output": "/path/to/output.md",
  "wordCount": 1523,
  "images": 5,
  "warnings": ["Some formatting may be simplified"]
}
```

## Supported Elements

- Headings (H1-H6)
- Paragraphs and emphasis (bold, italic, strikethrough)
- Ordered and unordered lists
- Tables (GFM format)
- Links
- Images (extracted or base64)
- Code blocks (requires Word "Code" style)
- Blockquotes

## Known Limitations

- **Nested lists**: Numbering may reset in deeply nested lists
- **Nested tables**: Inner tables are flattened
- **Code blocks**: Require explicit Word style mapping ("Code" or "Code Block")
- **Complex formatting**: Some advanced formatting may be simplified
- **Footnotes**: Converted but may lose some formatting

## Google Docs Support

Export your Google Doc as DOCX first, then convert:

1. In Google Docs: File → Download → Microsoft Word (.docx)
2. Run this converter on the downloaded file

## Troubleshooting

**Dependencies not found:** Run `npm install` in skill directory
**Empty output:** Ensure DOCX contains actual text (not just images)
**Code blocks not detected:** Use Word's built-in "Code" style

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

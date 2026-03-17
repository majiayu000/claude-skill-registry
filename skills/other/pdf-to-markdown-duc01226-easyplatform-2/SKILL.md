---
name: pdf-to-markdown
description: "[Utilities] Convert PDF files to Markdown. Use when extracting text from PDFs, creating editable documentation from PDF reports, or converting PDF content to version-controlled markdown files."
allowed-tools: Bash, Read, Write
---

# pdf-to-markdown

Convert PDF files to Markdown format.

## Installation Required

```bash
cd .claude/skills/pdf-to-markdown
npm install
```

**Dependencies:** `pdf-parse`

## Quick Start

```bash
# Basic conversion
node .claude/skills/pdf-to-markdown/scripts/convert.cjs \
  --file ./document.pdf

# Custom output path
node .claude/skills/pdf-to-markdown/scripts/convert.cjs \
  --file ./doc.pdf \
  --output ./output/doc.md
```

## CLI Options

| Option            | Required | Description                                      |
| ----------------- | -------- | ------------------------------------------------ |
| `--file <path>`   | Yes      | Input PDF file                                   |
| `--output <path>` | No       | Output Markdown path (default: input name + .md) |

## Output Format (JSON)

```json
{
  "success": true,
  "input": "/path/to/input.pdf",
  "output": "/path/to/output.md",
  "wordCount": 1523,
  "warnings": ["Tables may not be accurately converted"]
}
```

## Supported Elements

- Text extraction from digital PDFs
- Headings (detected by font size heuristics)
- Paragraphs
- Basic lists
- Links (when embedded in PDF)

## Known Limitations

- **Tables**: Very limited support; may not render correctly
- **Multi-column layouts**: Text may interleave between columns
- **Scanned PDFs**: NOT supported (requires OCR - see alternatives below)
- **Images**: NOT extracted (PDF images are not included in output)
- **Complex formatting**: May be simplified or lost
- **Password-protected PDFs**: NOT supported

## Alternatives for Unsupported Cases

**For scanned PDFs (OCR needed):**

- Use `scribe.js-ocr` library (AGPL license)
- Commercial OCR services (Google Cloud Vision, AWS Textract)

**For complex tables:**

- Consider AI-based extraction (LLM post-processing)
- Manual review and correction

**For image extraction:**

- Use `unpdf` library with `sharp` for image extraction
- Process images separately and reference in markdown

## Troubleshooting

**Dependencies not found:** Run `npm install` in skill directory
**Empty output:** PDF may be scanned/image-based (requires OCR)
**Garbled text:** PDF may use embedded fonts not supported by parser
**Memory issues:** Large PDFs may require `--max-old-space-size=4096` flag

## IMPORTANT Task Planning Notes
- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

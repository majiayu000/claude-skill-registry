---
name: markdown-to-pdf
description: Convert markdown documents to professional PDF files for reports, analysis summaries, and documentation sharing
allowed-tools:
  - Bash
  - Read
---

# Markdown to PDF

Convert markdown files to professionally styled PDF documents suitable for reports, financial summaries, presentations, and documentation for sharing.

## When to Use This Skill

- User wants to create a PDF version of a markdown document
- User asks to "export to PDF" or "generate a PDF"
- User wants to share analysis or reports in PDF format
- User needs a printable version of documentation

## Dependencies

Ensure `pdfmake` and `marked` are installed in the project:

```bash
npm list pdfmake marked || npm install pdfmake marked
```

## Usage

### Basic Conversion

```bash
# Convert with default output (same directory, .pdf extension)
node .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs <input.md>

# Specify output location
node .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs <input.md> <output.pdf>
```

### Examples

```bash
# Basic conversion
node .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs docs/report.md

# Custom output path
node .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs docs/report.md output/report.pdf

# Show help
node .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs --help
```

## Supported Features

- Headings (h1-h4 with underlines for h1/h2)
- Bold, italic, inline code
- Links (clickable in PDF)
- Ordered and unordered lists (nested)
- Code blocks
- Blockquotes
- Tables
- Horizontal rules

## PDF Styling

The tool applies professional styling automatically:
- Clean, readable Helvetica fonts
- Styled tables with header backgrounds
- Proper heading hierarchy with visual separation
- Code blocks with monospace font
- Blockquote styling with left border
- 1-inch page margins suitable for printing

## Programmatic Usage

The tool can also be imported as a module:

```javascript
const { convertMarkdownToPdf, convertMarkdownStringToPdf } = require('./.claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.cjs');

// Convert a file
await convertMarkdownToPdf('input.md', 'output.pdf');

// Convert markdown string content
await convertMarkdownStringToPdf('# My Report\n\nContent here...', 'output.pdf');
```

## Error Handling

Common issues:
1. **File not found** - Verify the input path exists
2. **Permission denied** - Check write permissions on output directory
3. **Dependencies missing** - Run `npm install pdfmake marked`

## Output Location

By default, PDFs are created in the same directory as the source markdown file with a `.pdf` extension.

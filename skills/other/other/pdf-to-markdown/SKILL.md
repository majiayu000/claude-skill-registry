---
name: pdf-to-markdown
version: 1.0.0
description: '[Document Processing] Convert PDF files to Markdown with support for native text PDFs and scanned documents (OCR). Cross-platform.'

allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Convert PDF files to well-formatted Markdown with auto-detection of native text vs scanned documents.

**Workflow:**

1. **Auto-Detect** — Determine if PDF has native text or needs OCR
2. **Convert** — Run `scripts/convert.cjs` with input path and optional mode/output flags
3. **Output** — Returns JSON with success status, page count, and output path

**Key Rules:**

- Use `--mode auto` (default) to let the tool decide native vs OCR
- OCR for scanned PDFs requires additional `tesseract.js` setup
- Complex multi-column layouts may not preserve structure perfectly

# pdf-to-markdown

Convert PDF files to Markdown format with automatic detection of native text vs scanned documents.

## Installation Required

**This skill requires npm dependencies.** Run one of the following:

```bash
# Option 1: Install via ClaudeKit CLI (recommended)
ck init  # Runs install.sh which handles all skills

# Option 2: Manual installation
cd .claude/skills/pdf-to-markdown
npm install
```

**Dependencies:** `@opendocsg/pdf2md` (native PDFs), `pdfjs-dist` (PDF parsing)

**Note:** OCR for scanned PDFs requires additional setup (see OCR section).

## Quick Start

```bash
# Basic conversion (auto-detect native vs scanned)
node .claude/skills/pdf-to-markdown/scripts/convert.cjs --input ./document.pdf

# Specify output path
node .claude/skills/pdf-to-markdown/scripts/convert.cjs -i ./doc.pdf -o ./output.md

# Force native mode (skip OCR detection)
node .claude/skills/pdf-to-markdown/scripts/convert.cjs -i ./doc.pdf --mode native
```

## CLI Options

| Option     | Short | Description                              | Default      |
| ---------- | ----- | ---------------------------------------- | ------------ |
| `--input`  | `-i`  | Input PDF file path                      | (required)   |
| `--output` | `-o`  | Output markdown file path                | `{input}.md` |
| `--mode`   | `-m`  | Conversion mode: `auto`, `native`, `ocr` | `auto`       |
| `--help`   | `-h`  | Show help message                        |              |

## Features

- **Auto-Detection:** Automatically determines if PDF has native text or requires OCR
- **Native PDFs:** Fast extraction using @opendocsg/pdf2md
- **Tables:** Basic table structure preservation
- **Cross-Platform:** Works on Windows, macOS, Linux
- **No System Dependencies:** Pure JavaScript implementation

## Conversion Modes

### Auto (Default)

Checks if PDF has extractable text on first page. Uses native extraction if text found, otherwise falls back to OCR warning.

### Native

Fast direct text extraction. Best for PDFs with selectable text (not scanned images).

### OCR (Scanned PDFs) - Coming Soon

For scanned documents. Currently not implemented - the skill will notify you if a PDF appears to be scanned.

## Output

Returns JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.pdf",
    "output": "/path/to/output.md",
    "stats": {
        "pages": 5,
        "mode": "native"
    }
}
```

## Limitations

- Complex multi-column layouts may not preserve structure
- Scanned PDF OCR accuracy depends on image quality
- Mathematical formulas may not convert perfectly
- First-run OCR downloads language data (~15MB)

## OCR Setup (Optional)

For scanned PDF support, install additional dependencies:

```bash
npm install tesseract.js pdfjs-dist canvas
```

**Note:** The `canvas` package may require build tools on some systems.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

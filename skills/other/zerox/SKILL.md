---
name: zerox
description: Convert documents (PDF, DOCX, PPTX, images, etc.) to Markdown using the zerox library. Use when the user needs to extract text content from document files.
homepage: https://github.com/getomni-ai/zerox
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["node"],"env":["APIYI_API_KEY"]},"primaryEnv":"APIYI_API_KEY"}}
---

# Zerox Document Converter

Convert various document formats to Markdown using the zerox library and GPT-4o vision.

## Supported Formats

- PDF (scanned and text-based)
- Microsoft Word (DOCX)
- Microsoft PowerPoint (PPTX)
- Images (PNG, JPG, etc.)
- And more via OCR

## Convert Document (Foreground)

For small files (< 30 seconds):

```bash
node {baseDir}/scripts/convert.mjs <filePath> [outputPath]
```

### Examples

```bash
# Convert PDF - saves to {baseDir}/output/document.md by default
node {baseDir}/scripts/convert.mjs "/path/to/document.pdf"

# Convert PDF with custom output path
node {baseDir}/scripts/convert.mjs "/path/to/document.pdf" "/path/to/output.md"

# Convert Word document - saves to {baseDir}/output/document.md
node {baseDir}/scripts/convert.mjs "/path/to/document.docx"
```

## Convert Document (Background)

For large files or scanned PDFs that take minutes:

```bash
node {baseDir}/scripts/convert-bg.mjs <filePath> [outputPath]
```

### Features

- Runs conversion in background (no timeout issues)
- Logs progress to `{baseDir}/output/convert-bg.log`
- Sends macOS notification when complete
- Detached from terminal (safe to close)

### Examples

```bash
# Convert large scanned PDF in background
node {baseDir}/scripts/convert-bg.mjs "/path/to/scanned-document.pdf"

# Monitor progress
tail -f {baseDir}/output/convert-bg.log
```

## Requirements

- `APIYI_API_KEY`: Your OpenAI-compatible API key (environment variable)

## Notes

- The conversion uses GPT-4o vision to extract text, so it works even with scanned documents
- Large documents may take some time to process
- Output is plain Markdown text

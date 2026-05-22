---
name: pdf-processing
description: |
  Comprehensive PDF processing skill for reading, extracting, and manipulating PDF files.
  Use this skill when: (1) user shares a PDF URL like .pdf, (2) user asks to read/analyze a PDF,
  (3) user wants to extract text/tables from PDF, (4) user needs PDF merging/splitting,
  (5) user mentions "PDF", "document", or shares hubfs/resources links,
  (6) user wants OCR on scanned PDFs, (7) filling PDF forms.
  Triggers on: .pdf files, PDF URLs, "read this PDF", "extract from PDF", "analyze document",
  "PDFを読んで", "PDFから抽出", "ドキュメントを分析".
tools:
  - pdf-reader  # MCP: @sylphx/pdf-reader-mcp
  - Read
  - Bash
  - WebFetch
---

# PDF Processing Guide

## Overview

This skill provides enterprise-grade PDF processing using the `pdf-reader` MCP server (5-10x faster parallel processing) and Python fallbacks.

## Quick Reference

| Task | Method | Tool |
|------|--------|------|
| Extract text | MCP or pdfplumber | pdf-reader / Bash |
| Extract tables | pdfplumber | Bash |
| Merge PDFs | pypdf | Bash |
| Split PDFs | pypdf / qpdf | Bash |
| OCR scanned | pytesseract | Bash |
| Read from URL | Download + Process | WebFetch + Bash |

## MCP Tool Usage (Preferred)

### Basic Text Extraction

```json
{
  "sources": [{
    "path": "/path/to/document.pdf"
  }],
  "operation": "extract",
  "pages": "all"
}
```

### Extract Specific Pages

```json
{
  "sources": [{
    "path": "document.pdf"
  }],
  "operation": "extract",
  "pages": "1-5"
}
```

### Get Metadata Only

```json
{
  "sources": [{
    "path": "document.pdf"
  }],
  "operation": "metadata"
}
```

## URL PDFs Workflow

For PDFs from URLs (like HubFS, S3, etc.):

1. **Download PDF**:
```bash
curl -L -o /tmp/document.pdf "https://example.com/file.pdf"
```

2. **Extract with MCP**:
```json
{
  "sources": [{"path": "/tmp/document.pdf"}],
  "operation": "extract"
}
```

3. **Cleanup** (optional):
```bash
rm /tmp/document.pdf
```

## Python Fallbacks

When MCP is unavailable, use Python:

### Install Dependencies
```bash
pip install pypdf pdfplumber reportlab pytesseract pdf2image
```

### Extract Text (pdfplumber)
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Extract Tables
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            print(df)
```

### OCR for Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='jpn')  # Japanese
    print(f"Page {i+1}:\n{text}")
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Install on macOS
brew install poppler

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt
```

### qpdf
```bash
# Install
brew install qpdf

# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
```

## Apify Integration (for complex PDFs)

For PDFs requiring advanced processing:

```bash
# PDF Text Extractor (jirimoravcik)
npx apify-cli run jirimoravcik/pdf-text-extractor \
  -i '{"pdfUrls": ["https://example.com/file.pdf"]}'
```

See [references/apify-actors.md](references/apify-actors.md) for full Apify integration.

## Common Tasks

### Anthropic Guide PDF (Example)
```bash
# Download
curl -L -o /tmp/anthropic-guide.pdf \
  "https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf"

# Extract with MCP
# Use pdf-reader tool with path: /tmp/anthropic-guide.pdf
```

### Merge Multiple PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

## Validation Loop

1. **Extract**: Run extraction
2. **Verify**: Check output quality
3. **Retry with OCR**: If text is empty/garbled, try OCR
4. **Save**: Store extracted content

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty text | PDF may be scanned - use OCR |
| Garbled characters | Check encoding, try different library |
| Tables broken | Use pdfplumber with explicit table settings |
| Large file slow | Use page ranges, parallel processing |

## References

- **Advanced features**: See [references/advanced-pdf.md](references/advanced-pdf.md)
- **Form filling**: See [references/pdf-forms.md](references/pdf-forms.md)
- **Apify integration**: See [references/apify-actors.md](references/apify-actors.md)

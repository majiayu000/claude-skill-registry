---
name: extract-text-pdf
description: Extract text from PDF files using PyMuPDF. Use this skill when you need to read the contents of a PDF file, such as a resume, report, or manual, into plain text for analysis or processing.
---

# Extract Text from PDF

## Overview

This skill provides a reliable way to extract text from PDF files using the `pymupdf` library (also known as `fitz`). It correctly handles document structure and encoding better than many basic tools.

## Prerequisites

This skill requires the `pymupdf` Python library.

```bash
pip install pymupdf
```

## Usage

### Extract Text Script

The skill includes a Python script `scripts/extract_pdf_text.py` that extracts text from a PDF file.

**Syntax:**

```bash
python3 .agent/skills/extract-text-pdf/scripts/extract_pdf_text.py <path_to_pdf> [--layout]
```

**Arguments:**

*   `path_to_pdf`: The absolute path to the PDF file you want to read.
*   `--layout`: (Optional) precise layout preservation. By default, the script extracts text in natural reading order.

**Example:**

```bash
# Extract text from a resume
python3 .agent/skills/extract-text-pdf/scripts/extract_pdf_text.py /Users/user/documents/resume.pdf

# Capture output to a file
python3 .agent/skills/extract-text-pdf/scripts/extract_pdf_text.py /path/to/doc.pdf > extracted_text.txt
```

## When to Use

Use this skill when:
1.  You need to read the content of a PDF file.
2.  You want to analyze text data from a PDF (e.g., parsing a resume).
3.  Simple checks (`cat`, `grep`) won't work because the file is binary PDF format.

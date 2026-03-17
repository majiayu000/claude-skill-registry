---
version: 4.1.0-fractal
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [pypdf - Basic Operations](./sub-skills/pypdf-basic-operations.md)
### 2. [pdfplumber - Text and Table Extraction](./sub-skills/pdfplumber-text-and-table-extraction.md)
### 3. [reportlab - Create PDFs](./sub-skills/reportlab-create-pdfs.md)
### 4. [pdftotext (poppler-utils)](./sub-skills/pdftotext-poppler-utils.md)
### 5. [qpdf](./sub-skills/qpdf.md)
### 6. [pdftk (if available)](./sub-skills/pdftk-if-available.md)
### 7. [Extract Text from Scanned PDFs](./sub-skills/extract-text-from-scanned-pdfs.md)
### 8. [Add Watermark](./sub-skills/add-watermark.md)
### 9. [Extract Images](./sub-skills/extract-images.md)
### 10. [Password Protection](./sub-skills/password-protection.md)

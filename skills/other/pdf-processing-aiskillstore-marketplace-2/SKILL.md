---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing Skill

This skill provides capabilities for working with PDF documents.

## Quick Start

Use pdfplumber to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Capabilities

### Text Extraction
- Extract text from single or multiple pages
- Preserve layout and formatting
- Handle multi-column documents

### Table Extraction
- Identify and extract tables
- Convert to structured data (CSV, JSON)
- Handle complex table layouts

### Form Operations
- Fill PDF forms programmatically
- Extract form field values
- Create fillable forms

### Document Operations
- Merge multiple PDFs
- Split PDFs by page
- Rotate pages
- Add watermarks

## Best Practices

1. Always check if the PDF is encrypted before processing
2. Handle OCR cases for scanned documents
3. Validate extracted data for accuracy
4. Use appropriate libraries (pdfplumber for extraction, PyPDF2 for manipulation)

---
name: pdf-toolkit
description: Comprehensive PDF manipulation - merge, split, rotate, extract pages, add watermarks, compress, and encrypt PDFs programmatically.
---

# PDF Toolkit

Comprehensive PDF manipulation toolkit for merging, splitting, rotating, and more.

## Features

- **Merge**: Combine multiple PDFs into one
- **Split**: Extract pages or split into chunks
- **Rotate**: Rotate pages by 90/180/270 degrees
- **Extract**: Extract specific pages or page ranges
- **Watermark**: Add text/image watermarks
- **Compress**: Reduce file size
- **Encrypt**: Add password protection
- **Metadata**: Edit PDF metadata
- **Page Numbers**: Add page numbers
- **Bookmarks**: Add/remove bookmarks

## Quick Start

```python
from pdf_toolkit import PDFToolkit

toolkit = PDFToolkit()

# Merge PDFs
toolkit.merge(['doc1.pdf', 'doc2.pdf'], 'merged.pdf')

# Extract pages
toolkit.load('document.pdf').extract_pages([1, 3, 5], 'extracted.pdf')

# Add watermark
toolkit.load('document.pdf').watermark('CONFIDENTIAL', output='watermarked.pdf')
```

## CLI Usage

```bash
# Merge
python pdf_toolkit.py merge file1.pdf file2.pdf --output merged.pdf

# Split
python pdf_toolkit.py split document.pdf --pages 10 --output chunks/

# Rotate
python pdf_toolkit.py rotate document.pdf --angle 90 --pages 1-5 --output rotated.pdf

# Watermark
python pdf_toolkit.py watermark document.pdf --text "DRAFT" --output watermarked.pdf
```

## Dependencies

- PyPDF2>=3.0.0
- PyMuPDF>=1.23.0
- pillow>=10.0.0
- reportlab>=4.0.0

---
name: pdf-large-reader
version: "1.0.0"
category: data
description: "pdf-large-reader Skill"
---

# pdf-large-reader Skill

Memory-efficient PDF processing library for large files (100MB+, 1000+ pages).

## Repository

- **Location:** `/mnt/github/workspace-hub/pdf-large-reader`
- **GitHub:** https://github.com/vamseeachanta/pdf-large-reader
- **Coverage:** 93.58% (215 tests)

## Installation

```bash
cd /mnt/github/workspace-hub/pdf-large-reader
pip install -e .
```

## Quick Usage

### Python API

```python
from pdf_large_reader import process_large_pdf, extract_text_only

# Simple text extraction
text = extract_text_only("large_document.pdf")

# Full processing with options
result = process_large_pdf(
    "document.pdf",
    output_format="generator",  # "generator", "list", or "text"
    extract_images=True,
    extract_tables=True
)

# Stream pages for memory efficiency
for page in result:
    print(f"Page {page['page_num']}: {page['text'][:100]}...")
```

### CLI Tool

```bash
# Extract text
pdf-large-reader extract document.pdf

# Extract with options
pdf-large-reader extract document.pdf --output-format text --extract-images

# Get PDF info
pdf-large-reader info document.pdf
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Streaming** | Generator output for memory efficiency |
| **Auto Strategy** | Intelligent chunk sizing based on file size |
| **Multi-format** | Text, images, tables, metadata extraction |
| **Progress** | Built-in progress callbacks |
| **AI Fallback** | Claude integration for complex extraction |

## Output Formats

### Generator (Streaming) - Default
```python
for page in process_large_pdf("doc.pdf", output_format="generator"):
    # Process one page at a time - memory efficient
    handle_page(page)
```

### List
```python
pages = process_large_pdf("doc.pdf", output_format="list")
# All pages in memory - use for smaller files
```

### Text
```python
text = process_large_pdf("doc.pdf", output_format="text")
# Plain text concatenation
```

## When to Use

- Processing PDFs > 50MB
- Batch processing many PDFs
- Extracting content from 100+ page documents
- Memory-constrained environments
- Streaming PDF content to other systems

## Integration Example

```python
from pdf_large_reader import process_large_pdf
from pathlib import Path

def process_pdf_directory(directory: str):
    """Process all PDFs in a directory efficiently."""
    pdf_dir = Path(directory)

    for pdf_file in pdf_dir.glob("*.pdf"):
        print(f"Processing: {pdf_file.name}")

        # Stream pages to avoid memory issues
        for page in process_large_pdf(str(pdf_file)):
            # Index, analyze, or store each page
            yield {
                "file": pdf_file.name,
                "page": page["page_num"],
                "text": page["text"],
                "images": len(page.get("images", []))
            }
```

## Error Handling

```python
from pdf_large_reader import process_large_pdf
from pdf_large_reader.exceptions import PDFProcessingError

try:
    result = process_large_pdf("document.pdf")
except PDFProcessingError as e:
    print(f"PDF processing failed: {e}")
except FileNotFoundError:
    print("PDF file not found")
```

## Related Skills

- `file-org-standards` - Where to store extracted content
- `logging-standards` - Logging PDF processing operations

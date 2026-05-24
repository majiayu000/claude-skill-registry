---
name: Docling Advanced
description: This skill should be used when the user asks about "Granite model", "Docling for scanned PDFs", "OCR with Docling", "performance optimization Docling", "complex documents", "table extraction", "multi-column layout", "advanced Docling configuration", or mentions handling challenging document processing scenarios.
version: 0.1.0
---

# Docling Advanced Features

## Overview

This skill covers advanced Docling features for handling complex documents, optimizing performance, and using the Granite vision-language model for enhanced document understanding.

**Advanced topics:**
- Granite model for scanned PDFs and complex layouts
- Advanced configuration options
- Performance optimization techniques
- Complex document handling (tables, formulas, multi-column)
- Troubleshooting challenging scenarios

## Granite Model

Granite Docling is a vision-language model (258M parameters) that enhances document processing for scanned PDFs and complex layouts.

### What is Granite

**Granite Docling:**
- AI model for document understanding
- Processes scanned documents with OCR
- Better table extraction than standard parsing
- Handles multi-column layouts
- Understands document structure visually

**When to use Granite:**
- Scanned PDFs (not born-digital)
- Poor-quality documents
- Complex layouts (multi-column, unusual formatting)
- Tables with complex structures
- Documents with mixed content (text + images + formulas)

**When NOT to use Granite:**
- Clean, born-digital PDFs (standard parser is faster)
- Simple documents
- Performance is critical (Granite is slower)

### Installation

```bash
# Install with Granite support
uv add "docling[granite]"

# Verify
python -c "from docling.models import GraniteModel; print('Granite available')"
```

**System requirements:**
- Additional ~250MB for model weights
- More RAM (8GB+ recommended)
- Slower processing (~3x standard)

### Usage

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions

# Configure with Granite
options = PipelineOptions(
    do_ocr=True,                    # Enable OCR
    ocr_engine="granite"            # Use Granite model
)

converter = DocumentConverter(options=options)
result = converter.convert("scanned_document.pdf")

# Process as usual
markdown = result.document.export_to_markdown()
```

### Granite vs Standard OCR

| Aspect | Granite | Tesseract (Standard) |
|--------|---------|----------------------|
| **Accuracy** | Higher | Good |
| **Table extraction** | Excellent | Basic |
| **Layout understanding** | Advanced | Basic |
| **Speed** | Slower (~90s/100pg) | Faster (~60s/100pg) |
| **Model size** | ~250MB | ~5MB |
| **Use case** | Complex documents | Simple scans |

For detailed Granite usage, see **`references/granite-guide.md`**.

## Advanced Configuration

### Pipeline Options

Full configuration control:

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions, TableFormatOption

options = PipelineOptions(
    do_table_structure=True,        # Extract table structure
    do_ocr=False,                   # Disable OCR (if not needed)
    do_picture_classifier=False,    # Disable image classification
    table_format=TableFormatOption.MARKDOWN,  # Table format
)

converter = DocumentConverter(options=options)
```

**Key options:**

- `do_table_structure` (bool): Extract table structure (default: True)
  - True: Full table parsing with cells and structure
  - False: Tables as plain text (faster)

- `do_ocr` (bool): Enable OCR for scanned documents (default: False)
  - True: Process scanned PDFs
  - False: Skip OCR (faster for born-digital)

- `do_picture_classifier` (bool): Classify images (default: False)
  - True: Detect image types (charts, photos, diagrams)
  - False: Skip classification (faster)

- `table_format`: How to represent tables
  - `TableFormatOption.MARKDOWN`: Markdown tables (readable)
  - `TableFormatOption.HTML`: HTML tables (structured)
  - `TableFormatOption.TEXT`: Plain text (simple)

### Performance Optimization

**Disable unused features:**

```python
# For maximum speed (text-only extraction)
options = PipelineOptions(
    do_table_structure=False,
    do_ocr=False,
    do_picture_classifier=False
)

# For OCR documents only
options = PipelineOptions(
    do_ocr=True,
    do_table_structure=False,
    do_picture_classifier=False
)
```

**Batch processing optimization:**

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

converter = DocumentConverter(options)  # Reuse converter

def process_pdf(pdf_path):
    """Process single PDF."""
    return converter.convert(str(pdf_path))

# Process in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    pdf_files = list(Path("data/").glob("*.pdf"))
    results = list(executor.map(process_pdf, pdf_files))
```

**Memory optimization:**

```python
# Process one at a time for large PDFs
for pdf in large_pdfs:
    result = converter.convert(pdf)
    # Save result immediately
    save_to_file(result)
    # Clear memory
    del result
```

For complete optimization guide, see **`references/performance-optimization.md`**.

## Complex Document Handling

### Multi-Column Layouts

Docling automatically detects multi-column layouts:

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("multi_column_paper.pdf")

# Docling preserves reading order across columns
markdown = result.document.export_to_markdown()
```

**Reading order:** Docling respects logical reading order, not visual layout.

### Table Extraction

Advanced table handling:

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions, TableFormatOption

# Configure for best table extraction
options = PipelineOptions(
    do_table_structure=True,
    table_format=TableFormatOption.MARKDOWN
)

converter = DocumentConverter(options)
result = converter.convert("document_with_tables.pdf")

# Extract tables specifically
for item in result.document.iterate_items():
    if item.label == "table":
        print(f"Table on page {item.prov[0].page_no if item.prov else 'N/A'}:")
        print(item.text)
```

**Complex tables:**
- Merged cells: Handled automatically
- Nested tables: Flattened or preserved (depends on structure)
- Multi-page tables: Split by page

### Formulas and Mathematical Content

Docling attempts to extract mathematical formulas:

```python
# Extract formulas
for item in result.document.iterate_items():
    if item.label == "formula":
        print(f"Formula: {item.text}")
```

**Note:** Formula extraction quality varies. For complex math, consider specialized tools (MathPix, LaTeX-OCR).

### Images and Figures

Handle images in documents:

```python
options = PipelineOptions(
    do_picture_classifier=True  # Enable image classification
)

converter = DocumentConverter(options)
result = converter.convert("document.pdf")

# Find figures
for item in result.document.iterate_items():
    if item.label == "figure":
        print(f"Figure on page {item.prov[0].page_no if item.prov else 'N/A'}")

        # Find associated caption
        if hasattr(item, 'parent') and item.parent:
            for sibling in item.parent.children:
                if sibling.label == "caption":
                    print(f"Caption: {sibling.text}")
```

For detailed complex document patterns, see **`references/complex-documents.md`**.

## Troubleshooting Advanced Scenarios

### Issue: Garbled Text from Scanned PDF

**Cause:** OCR disabled or poor scan quality

**Solution:**
```python
# Enable Granite for better OCR
options = PipelineOptions(
    do_ocr=True,
    ocr_engine="granite"
)
converter = DocumentConverter(options)
```

### Issue: Tables Not Extracted Correctly

**Cause:** Complex table structure or table detection disabled

**Solution:**
```python
# Enable full table processing
options = PipelineOptions(
    do_table_structure=True,
    table_format=TableFormatOption.HTML  # Try different format
)

# For very complex tables, consider Granite
options.ocr_engine = "granite"
```

### Issue: Slow Processing

**Cause:** Unnecessary features enabled

**Solution:**
```python
# Disable unused features
options = PipelineOptions(
    do_ocr=False,                    # If not scanned
    do_picture_classifier=False,     # If images not important
    do_table_structure=False         # If tables not important
)

# Process in parallel
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_pdf, pdf_files)
```

### Issue: Out of Memory

**Cause:** Large PDFs or batch processing

**Solution:**
```python
# Process one at a time
for pdf in pdfs:
    result = converter.convert(pdf)
    save_result(result)
    del result  # Free memory

# Or reduce batch size
# Or increase system RAM
```

For comprehensive troubleshooting, see **`references/troubleshooting.md`**.

## Use Case Examples

### Use Case 1: Scanned Invoice Processing

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions
from docling.chunking import HybridChunker

# Configure for scanned invoices
options = PipelineOptions(
    do_ocr=True,
    ocr_engine="granite",
    do_table_structure=True  # Invoices often have tables
)

converter = DocumentConverter(options)
chunker = HybridChunker()

# Process invoice
result = converter.convert("scanned_invoice.pdf")
chunks = list(chunker.chunk(result.document))

# Extract with metadata
for chunk in chunks:
    if chunk.meta.doc_items and chunk.meta.doc_items[0].label == "table":
        print("Found invoice table:")
        print(chunk.text)
```

### Use Case 2: Research Paper with Complex Layout

```python
# Multi-column paper with tables and formulas
options = PipelineOptions(
    do_table_structure=True,
    do_picture_classifier=True,  # Classify figures
    table_format=TableFormatOption.MARKDOWN
)

converter = DocumentConverter(options)
result = converter.convert("research_paper.pdf")

# Docling handles multi-column automatically
# Extract in logical reading order
from docling.chunking import HierarchicalChunker
chunker = HierarchicalChunker()
chunks = list(chunker.chunk(result.document))

# Chunks follow paper structure (Abstract, Intro, Methods, etc.)
```

### Use Case 3: Mixed Quality Document Set

```python
# Some scanned, some born-digital
def process_adaptive(pdf_path):
    """Adaptively process based on document quality."""

    # Try without OCR first (faster)
    converter = DocumentConverter()

    try:
        result = converter.convert(pdf_path)

        # Check if extraction looks good
        text = result.document.export_to_markdown()

        if len(text) < 100 or text.count('�') > 5:
            # Likely scanned or poor quality, retry with Granite
            print(f"Retrying {pdf_path} with Granite...")
            options = PipelineOptions(do_ocr=True, ocr_engine="granite")
            converter_ocr = DocumentConverter(options)
            result = converter_ocr.convert(pdf_path)

        return result

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None
```

## Quick Reference

### Enable Granite Model

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PipelineOptions

options = PipelineOptions(do_ocr=True, ocr_engine="granite")
converter = DocumentConverter(options)
```

### Optimize for Speed

```python
options = PipelineOptions(
    do_table_structure=False,
    do_ocr=False,
    do_picture_classifier=False
)
```

### Extract Tables

```python
for item in result.document.iterate_items():
    if item.label == "table":
        print(item.text)
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(converter.convert, pdf_files))
```

## Additional Resources

### Reference Files

For detailed guidance:
- **`references/granite-guide.md`** - Complete Granite model usage guide
- **`references/performance-optimization.md`** - Performance tuning and benchmarks
- **`references/complex-documents.md`** - Handling complex document structures
- **`references/troubleshooting.md`** - Advanced troubleshooting scenarios

### Example Files

Working examples in `examples/`:
- **`granite_processing.py`** - Scanned PDF processing with Granite
- **`table_extraction.py`** - Advanced table extraction patterns
- **`batch_optimization.py`** - Optimized batch processing

---

This skill covers advanced Docling features. For basics, see **docling-fundamentals** skill. For chunking strategies, see **docling-chunking** skill.

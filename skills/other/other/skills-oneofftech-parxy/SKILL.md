---
name: parxy
description: |
  Document parsing and PDF manipulation using the Parxy library. Use when:
  (1) Parsing PDFs or documents to extract text/structure
  (2) Converting documents to markdown
  (3) Batch processing multiple documents
  (4) Merging, splitting, or optimizing PDFs
  (5) Managing PDF attachments
---

# Parxy Document Processing

## Parsing Documents

```python
from parxy_core.facade.parxy import Parxy

# Basic parsing (default: pymupdf driver, block level)
doc = Parxy.parse("document.pdf")

# With specific driver and level
doc = Parxy.parse("document.pdf", driver_name="llamaparse", level="span")

# From bytes or BytesIO
doc = Parxy.parse(pdf_bytes)
```

### Extraction Levels

| Level | Description |
|-------|-------------|
| `page` | Page text only |
| `block` | Text blocks (default) |
| `line` | Individual lines |
| `span` | Text spans with styling |
| `character` | Individual characters |

### Document Structure

```python
doc.filename      # Original filename
doc.pages         # List of Page objects
doc.metadata      # Document metadata

page.number       # Page number (1-indexed)
page.text         # Full page text
page.blocks       # List of TextBlock objects

block.text        # Block text content
block.bbox        # Bounding box (x0, y0, x1, y1)
block.role        # Semantic role (paragraph, heading, etc.)
```

## Available Drivers

| Driver | Constant | Type | Best For |
|--------|----------|------|----------|
| PyMuPDF | `Parxy.PYMUPDF` | Local | Fast local processing |
| PdfAct | `Parxy.PDFACT` | Self-hosted | Scientific papers, semantic roles |
| LlamaParse | `Parxy.LLAMAPARSE` | Cloud | Complex docs with OCR/tables |
| LLMWhisperer | `Parxy.LLMWHISPERER` | Cloud | Form extraction |
| Unstructured | `Parxy.UNSTRUCTURED_LIBRARY` | Local | Multi-format (DOCX, HTML) |

```python
# List all drivers
drivers = Parxy.drivers()

# Get specific driver
driver = Parxy.driver(Parxy.LLAMAPARSE)
```

## Batch Processing

```python
from parxy_core.facade.parxy import Parxy
from parxy_core.models import BatchTask

# Simple batch
results = Parxy.batch(
    tasks=["doc1.pdf", "doc2.pdf"],
    drivers=["pymupdf"],
    workers=4,
)

# Per-file configuration
results = Parxy.batch(tasks=[
    BatchTask(file="simple.pdf"),
    BatchTask(file="complex.pdf", drivers=["llamaparse"], level="line"),
])

# Streaming results
for result in Parxy.batch_iter(tasks=["doc1.pdf", "doc2.pdf"]):
    if result.success:
        print(f"{result.file}: {len(result.document.pages)} pages")
    else:
        print(f"{result.file} failed: {result.error}")
```

## PDF Manipulation

### Merge PDFs

```python
from pathlib import Path
from parxy_core.facade.parxy import Parxy

# Merge entire PDFs
Parxy.pdf.merge(
    inputs=[
        (Path("doc1.pdf"), None, None),  # All pages
        (Path("doc2.pdf"), None, None),
    ],
    output=Path("merged.pdf"),
)

# Merge specific page ranges (0-indexed)
Parxy.pdf.merge(
    inputs=[
        (Path("doc1.pdf"), 0, 4),   # Pages 1-5
        (Path("doc2.pdf"), 0, 0),   # Page 1 only
    ],
    output=Path("selected.pdf"),
)
```

### Split PDF

```python
# Split into individual pages
pages = Parxy.pdf.split(
    input_path=Path("document.pdf"),
    output_dir=Path("./pages"),
    prefix="doc",
)
# Returns: [Path('pages/doc_page_1.pdf'), Path('pages/doc_page_2.pdf'), ...]
```

### Optimize PDF

```python
result = Parxy.pdf.optimize(
    input_path=Path("large.pdf"),
    output_path=Path("small.pdf"),
    scrub_metadata=True,      # Remove metadata, thumbnails
    subset_fonts=True,        # Keep only used glyphs
    compress_images=True,     # Downsample and compress
    dpi_target=72,
    image_quality=60,
    convert_to_grayscale=False,
)
print(f"Reduced by {result['reduction_percent']:.1f}%")
```

## PDF Attachments

```python
from pathlib import Path
from parxy_core.services.pdf_service import PdfService

with PdfService(Path("document.pdf")) as pdf:
    # List attachments
    names = pdf.list_attachments()

    # Add attachment
    pdf.add_attachment(Path("data.csv"), name="data", desc="Sales data")

    # Extract attachment
    content = pdf.extract_attachment("data")

    # Remove attachment
    pdf.remove_attachment("data")

    # Save changes
    pdf.save(Path("output.pdf"))
```

## CLI Commands

Assuming uvx is installed, pipx can be used as well.

```bash
# Parse document
uvx parxy parse document.pdf --driver llamaparse --level block --format json

# Convert to markdown
uvx parxy markdown document.pdf -o output/
uvx parxy markdown *.pdf --combine -o combined.md

# PDF operations
uvx parxy pdf split document.pdf --pages 1-5 -o output/
uvx parxy pdf merge doc1.pdf doc2.pdf -o combined.pdf

# List drivers
uvx parxy drivers
```

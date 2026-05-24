---
name: docling
description: Docling document parser for PDF, DOCX, PPTX, HTML, images, and 15+ formats. Use when parsing documents, extracting text, converting to Markdown/HTML/JSON, chunking for RAG pipelines, or batch processing files. Triggers on DocumentConverter, convert, convert_all, export_to_markdown, HierarchicalChunker, HybridChunker, ConversionResult.
---

# Docling Document Parser

Docling is a document parsing library that converts PDFs, Word documents, PowerPoint, images, and other formats into structured data with advanced layout understanding.

## Quick Start

Basic document conversion:

```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # URL, Path, or BytesIO
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
```

## Core Concepts

### DocumentConverter

The main entry point for document conversion. Supports various input formats and conversion options.

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Basic converter (all formats enabled)
converter = DocumentConverter()

# Restricted formats
converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF, InputFormat.DOCX]
)

# Custom pipeline options
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

### ConversionResult

All conversion operations return a `ConversionResult` containing:

- `document`: The parsed `DoclingDocument`
- `status`: `ConversionStatus.SUCCESS`, `PARTIAL_SUCCESS`, or `FAILURE`
- `errors`: List of errors encountered during conversion
- `input`: Information about the source document

```python
result = converter.convert("document.pdf")

if result.status == ConversionStatus.SUCCESS:
    markdown = result.document.export_to_markdown()
    html = result.document.export_to_html()
    data = result.document.export_to_dict()
```

## Supported Formats

### Input Formats

- **Documents**: PDF, DOCX, PPTX, XLSX
- **Markup**: HTML, Markdown, AsciiDoc
- **Data**: CSV, JSON (Docling format)
- **Images**: PNG, JPEG, TIFF, BMP, WEBP
- **Audio**: WAV, MP3
- **Video Text**: WebVTT
- **Schema-specific**: USPTO XML, JATS XML, METS-GBS

### Output Formats

- **Markdown**: `export_to_markdown()` or `save_as_markdown()`
- **HTML**: `export_to_html()` or `save_as_html()`
- **JSON**: `export_to_dict()` or `save_as_json()` (note: no `export_to_json()` method)
- **Text**: `export_to_text()` or `export_to_markdown(strict_text=True)` or `save_as_markdown(strict_text=True)`
- **DocTags**: `export_to_doctags()` or `save_as_doctags()`

## Common Patterns

### Single File Conversion

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")

# Export to different formats
markdown = result.document.export_to_markdown()
html = result.document.export_to_html()
json_data = result.document.export_to_dict()

# Or save directly to file
result.document.save_as_markdown("output.md")
result.document.save_as_html("output.html")
result.document.save_as_json("output.json")
```

### Batch Processing

See [references/batch.md](references/batch.md) for details on `convert_all()`.

### URL Conversion

```python
converter = DocumentConverter()
result = converter.convert("https://example.com/document.pdf")
```

### Binary Stream Conversion

```python
from io import BytesIO
from docling.datamodel.base_models import DocumentStream

with open("document.pdf", "rb") as f:
    buf = BytesIO(f.read())

source = DocumentStream(name="document.pdf", stream=buf)
result = converter.convert(source)
```

### Format-Specific Options

```python
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Configure PDF-specific options
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options.lang = ["en", "es"]
pipeline_options.do_table_structure = True
pipeline_options.generate_page_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
```

### Resource Limits

```python
converter = DocumentConverter()

# Limit file size (bytes) and page count
result = converter.convert(
    "large_document.pdf",
    max_file_size=20_971_520,  # 20 MB
    max_num_pages=100
)
```

### Document Chunking

See [references/chunking.md](references/chunking.md) for RAG integration.

## DoclingDocument Structure

The `DoclingDocument` is a Pydantic model representing parsed content:

```python
# Access document structure
doc = result.document

# Content items (lists)
doc.texts         # TextItem instances (paragraphs, headings, etc.)
doc.tables        # TableItem instances
doc.pictures      # PictureItem instances
doc.key_value_items  # Key-value pairs

# Structure (tree nodes)
doc.body          # Main content hierarchy
doc.furniture     # Headers, footers, page numbers
doc.groups        # Lists, chapters, sections

# Iterate all elements in reading order
for item, level in doc.iterate_items():
    print(f"{'  ' * level}{item.label}: {item.text[:50]}")
```

## Advanced Features

### OCR Configuration

```python
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    TesseractOcrOptions,
    TesseractCliOcrOptions,
    OcrMacOptions,
    RapidOcrOptions
)

# EasyOCR (default)
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options = EasyOcrOptions(lang=["en", "de"])

# Tesseract
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options = TesseractOcrOptions(lang=["eng", "deu"])

# RapidOCR
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.ocr_options = RapidOcrOptions()
```

### Table Extraction Options

```python
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode
)

pipeline_options = PdfPipelineOptions()
pipeline_options.do_table_structure = True

# Use cell matching (map to PDF cells)
pipeline_options.table_structure_options.do_cell_matching = True

# Or use predicted cells
pipeline_options.table_structure_options.do_cell_matching = False

# Choose accuracy mode
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
```

### Page Images

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.generate_page_images = True  # Needed for HTML export with images

# Export with embedded images
result.document.save_as_html(
    "output.html",
    image_mode=ImageRefMode.EMBEDDED
)
```

## Error Handling

```python
from docling.datamodel.base_models import ConversionStatus

result = converter.convert("document.pdf")

if result.status == ConversionStatus.SUCCESS:
    print("Conversion successful")
elif result.status == ConversionStatus.PARTIAL_SUCCESS:
    print("Partial conversion:")
    for error in result.errors:
        print(f"  {error.error_message}")
else:  # FAILURE
    print("Conversion failed:")
    for error in result.errors:
        print(f"  {error.error_message}")
```

For batch processing with error handling:

```python
# Continue processing on errors
results = converter.convert_all(
    ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    raises_on_error=False
)

for result in results:
    if result.status == ConversionStatus.SUCCESS:
        result.document.save_as_markdown(f"{result.input.file.stem}.md")
    else:
        print(f"Failed: {result.input.file}")
```

## CLI Usage

```bash
# Basic conversion
docling document.pdf

# Convert to specific output
docling --to markdown document.pdf

# With custom model path
docling --artifacts-path /path/to/models document.pdf

# Using VLM pipeline
docling --pipeline vlm --vlm-model granite_docling document.pdf
```

## Reference Documentation

- [Parsing Options](references/parsing.md) - DocumentConverter initialization, format-specific options, OCR configuration
- [Batch Processing](references/batch.md) - convert_all(), error handling, concurrency patterns
- [Chunking](references/chunking.md) - HierarchicalChunker, HybridChunker, RAG integration
- [Output Formats](references/output.md) - export_to_markdown(), export_to_html(), export_to_dict(), document structure

## Key Types

- `DocumentConverter`: Main conversion class
- `ConversionResult`: Result of conversion with document and status
- `DoclingDocument`: Unified document representation (Pydantic model)
- `InputFormat`: Enum of supported input formats
- `ConversionStatus`: SUCCESS, PARTIAL_SUCCESS, FAILURE
- `PdfPipelineOptions`: Configuration for PDF pipeline
- `ImageRefMode`: EMBEDDED, REFERENCED, PLACEHOLDER

## Integration Examples

### LangChain

```python
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownTextSplitter

converter = DocumentConverter()
result = converter.convert("document.pdf")
markdown = result.document.export_to_markdown()

splitter = MarkdownTextSplitter(chunk_size=1000)
chunks = splitter.split_text(markdown)
```

### LlamaIndex

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from llama_index.core import Document

converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

documents = [
    Document(text=chunk.text, metadata=chunk.meta.export_json_dict())
    for chunk in chunks
]
```

## Notes

- Docling uses a synchronous API (no native async support)
- Models are downloaded automatically on first use (can be prefetched)
- Supports local execution for air-gapped environments
- Supports GPU acceleration for OCR and table detection
- Default models run on CPU; GPU requires configuration

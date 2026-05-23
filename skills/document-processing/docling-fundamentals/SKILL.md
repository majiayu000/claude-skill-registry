---
name: Docling Fundamentals
description: This skill should be used when the user asks "how to use Docling", "what is Docling", "install Docling", "Docling tutorial", "when to use Docling", "Docling vs PyPDF2", "document extraction with Docling", or mentions getting started with Docling for document processing.
version: 0.1.0
---

# Docling Fundamentals

## Overview

Docling is an open-source document processing library developed at IBM Research and donated to the LF AI & Data Foundation. It transforms complex documents (PDFs, DOCX, PPTX, HTML) into structured, machine-readable data optimized for AI applications.

**Key capabilities:**
- Structure-aware document parsing (sections, paragraphs, tables, figures)
- Rich metadata extraction (page numbers, section titles, layout information)
- Multiple output formats (Markdown, JSON, DoclingDocument)
- Support for scanned documents via Granite model
- Enterprise-grade quality (42K+ GitHub stars, 1.5M monthly downloads)

## When to Use Docling

### Ideal Use Cases

Use Docling when:
- **Extracting structured data from PDFs** for RAG applications or knowledge bases
- **Preserving document structure** (sections, hierarchies, tables) is important
- **Source attribution** with page numbers and citations is required
- **Processing multiple document formats** (PDF, DOCX, HTML) with consistent output
- **Building AI pipelines** that need clean, metadata-rich document chunks
- **Handling enterprise documents** with complex layouts (reports, invoices, contracts)

### When to Choose Alternatives

Consider alternatives when:
- **Simple text extraction** from clean PDFs → Use PyPDF2 or pdfplumber (lighter weight)
- **OCR-only needs** for scanned images → Use Tesseract directly
- **Real-time web scraping** → Use BeautifulSoup or Scrapy
- **Word/Excel processing only** → Use python-docx or openpyxl (format-specific tools)

**Docling's advantage:** Structure preservation + metadata extraction + multi-format support in one tool.

## Installation

### Basic Installation

```bash
# Using uv (recommended for Orlando's environment)
uv add docling

# Using pip
pip install docling
```

### With Optional Dependencies

```bash
# For Granite model support (scanned PDFs)
uv add "docling[granite]"

# For all features
uv add "docling[all]"
```

Verify installation:
```python
python -c "from docling.document_converter import DocumentConverter; print('Docling installed successfully')"
```

For detailed installation troubleshooting, see **`references/installation-guide.md`**.

## Basic Usage Pattern

### Minimal Example

```python
from docling.document_converter import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert document
result = converter.convert("document.pdf")

# Access content
print(result.document.export_to_markdown())
```

This is the foundation - all Docling workflows follow this pattern: initialize converter, convert document, access result.

### Export Formats

Docling supports multiple export formats:

**1. Markdown** (human-readable):
```python
markdown_text = result.document.export_to_markdown()
# Use for: Documentation, previews, human review
```

**2. JSON** (machine-readable):
```python
import json
doc_json = result.document.export_to_dict()
# Use for: Structured processing, API integrations
```

**3. DoclingDocument** (native format):
```python
doc = result.document
# Use for: Advanced processing, chunking, metadata access
```

For RAG applications, export to JSON or use chunking (covered in docling-chunking skill).

## Document Processing Workflow

### Standard Workflow

Follow this sequence for document extraction:

1. **Initialize converter** with configuration options
2. **Convert document** to DoclingDocument format
3. **Apply chunking** (optional) for RAG applications
4. **Export to desired format** (Markdown, JSON, chunks)
5. **Validate output** for metadata completeness

### Example Workflow

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
import json

# 1. Initialize
converter = DocumentConverter()

# 2. Convert
result = converter.convert("research_paper.pdf")

# 3. Chunk for RAG
chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

# 4. Export
output = []
for chunk in chunks:
    output.append({
        "text": chunk.text,
        "page": chunk.meta.doc_items[0].prov[0].page_no if chunk.meta.doc_items else None,
        "source": "research_paper.pdf"
    })

# 5. Save
with open("chunks.jsonl", "w") as f:
    for item in output:
        f.write(json.dumps(item) + "\n")
```

This workflow produces JSONL output ready for downstream processing (BAML, vector databases, custom pipelines).

## Metadata Access

Docling automatically extracts rich metadata from documents:

### Available Metadata

- **Page numbers**: Location in source document
- **Section titles**: Heading hierarchy
- **Document items**: Paragraphs, tables, figures, lists
- **Layout information**: Bounding boxes, reading order
- **Provenance**: Source file, extraction timestamp

### Accessing Metadata

```python
result = converter.convert("document.pdf")
doc = result.document

# Get all tables
tables = [item for item in doc.iterate_items() if item.label == "table"]

# Get section structure
sections = [item for item in doc.iterate_items() if item.label == "section_header"]

# Get page-specific content
for item in doc.iterate_items():
    if hasattr(item, 'prov') and item.prov:
        page_num = item.prov[0].page_no
        print(f"Item on page {page_num}: {item.text[:50]}")
```

Metadata is crucial for citation tracking and source attribution in RAG applications.

## Configuration Options

### Converter Configuration

Customize DocumentConverter behavior:

```python
from docling.document_converter import DocumentConverter, ConversionOptions

# Custom configuration
options = ConversionOptions(
    do_table_structure=True,  # Extract table structure
    do_ocr=False,             # Disable OCR (unless needed)
)

converter = DocumentConverter(options=options)
```

Common options:
- `do_table_structure`: Extract tables with structure (default: True)
- `do_ocr`: Enable OCR for scanned PDFs (default: False)
- `do_picture_classifier`: Classify images (default: False)

For Granite model and advanced configuration, see **docling-advanced** skill.

## Integration with Downstream Tools

Docling outputs integrate seamlessly with:

### BAML Toolkit

```bash
# 1. Extract with Docling
uv run python extract_documents.py --output extracts.jsonl

# 2. Process with BAML
/baml-toolkit:batch-gemini GenerateProfile \
  extracts.jsonl \
  --output profiles.json
```

Docling provides structured extracts, BAML synthesizes them into typed outputs.

### LangChain

```python
from langchain.document_loaders import JSONLoader

# Load Docling JSONL output
loader = JSONLoader(
    file_path="chunks.jsonl",
    jq_schema=".text",
    metadata_func=lambda record, metadata: {
        "source": record.get("source"),
        "page": record.get("page")
    }
)

docs = loader.load()
```

### Custom Pipelines

```python
import json

# Read Docling JSONL
with open("extracts.jsonl") as f:
    for line in f:
        extract = json.loads(line)
        # Process extract: embed, store, analyze, etc.
```

JSONL format is universally compatible with data pipelines.

## Output Format Selection

Choose output format based on use case:

| Use Case | Format | Reason |
|----------|--------|--------|
| RAG / Vector search | JSONL chunks | Streamable, metadata-rich, embedding-ready |
| Human review | Markdown | Readable, preserves structure |
| API integration | JSON | Structured, programmatic access |
| Further processing | DoclingDocument | Full access to all metadata |
| Documentation | Markdown | Clean formatting |
| Data pipelines | JSONL | Line-by-line processing |

For most AI applications, use JSONL chunks with metadata.

## Common Patterns

### Pattern 1: Batch Processing

```python
from pathlib import Path

converter = DocumentConverter()
output_dir = Path("extracts")
output_dir.mkdir(exist_ok=True)

# Process all PDFs in directory
for pdf in Path("data/").glob("*.pdf"):
    result = converter.convert(str(pdf))

    # Save as markdown
    output_file = output_dir / f"{pdf.stem}.md"
    output_file.write_text(result.document.export_to_markdown())
```

### Pattern 2: Extract with Citation

```python
def extract_with_citations(pdf_path):
    """Extract text with source attribution."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    citations = []
    for item in result.document.iterate_items():
        if item.text and hasattr(item, 'prov') and item.prov:
            citations.append({
                "text": item.text,
                "source": pdf_path,
                "page": item.prov[0].page_no,
                "type": item.label
            })

    return citations
```

### Pattern 3: Table Extraction

```python
def extract_tables(pdf_path):
    """Extract all tables from PDF."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    tables = []
    for item in result.document.iterate_items():
        if item.label == "table":
            tables.append({
                "content": item.text,
                "page": item.prov[0].page_no if item.prov else None
            })

    return tables
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'docling'"**
- Run: `uv add docling` or `pip install docling`

**"Conversion failed" or empty output**
- Check if PDF is valid: Open in PDF viewer
- Try with `do_ocr=True` for scanned PDFs
- Check for password protection

**Slow processing**
- Normal for large PDFs (OCR is expensive)
- Disable OCR if not needed: `do_ocr=False`
- Process files in parallel for batches

**Missing metadata**
- Some PDFs lack proper structure
- Use Granite model for better extraction (see docling-advanced skill)

For advanced troubleshooting, see **`references/troubleshooting.md`**.

## Next Steps

After understanding fundamentals:

1. **Learn chunking strategies**: See **docling-chunking** skill for HybridChunker vs HierarchicalChunker
2. **Handle complex documents**: See **docling-advanced** skill for Granite model and scanned PDFs
3. **Generate processing scripts**: Use `/docling-toolkit:scaffold-processor` command
4. **Build RAG pipelines**: Combine Docling extracts with BAML or vector databases

## Quick Reference

### Basic Commands

```python
# Install
uv add docling

# Convert to markdown
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert("doc.pdf")
markdown = result.document.export_to_markdown()

# Convert to JSON
doc_dict = result.document.export_to_dict()

# Chunk for RAG
from docling.chunking import HybridChunker
chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))
```

### Key Resources

- Official docs: https://docling-project.github.io/docling/
- GitHub: https://github.com/docling-project/docling
- Examples: See `examples/basic_extraction.py`
- Installation help: See `references/installation-guide.md`

## Additional Resources

### Reference Files

For detailed guidance:
- **`references/installation-guide.md`** - Complete installation instructions with troubleshooting
- **`references/comparison.md`** - Docling vs alternatives (PyPDF2, pdfplumber, Unstructured)

### Example Files

Working examples in `examples/`:
- **`basic_extraction.py`** - Simple PDF to Markdown conversion
- **`batch_processing.py`** - Process multiple documents
- **`extract_with_metadata.py`** - Access metadata and citations

---

This skill provides the foundation for using Docling. For structure-aware chunking strategies, proceed to the **docling-chunking** skill. For advanced features like Granite model and performance optimization, see the **docling-advanced** skill.

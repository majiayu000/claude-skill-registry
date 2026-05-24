---
name: docling
description: Convert documents (PPTX, PDF, DOCX, XLSX, images) to Markdown/JSON/HTML using IBM Docling. This skill should be used when user asks to convert, parse, or extract content from documents. Triggers on "convert pptx", "parse pdf", "extract from document", "конвертуй презентацію", "витягни з pdf".
---

# Docling - Document Conversion Skill

Convert any document format to structured Markdown, JSON, or HTML using IBM Docling with AI-powered layout analysis.

## Quick Start

**Batch convert directory to Markdown:**
```bash
uv run python .claude/skills/docling/scripts/convert_docs.py \
  --input /path/to/documents \
  --output /path/to/output \
  --format md
```

**Single file via CLI:**
```bash
uv run docling document.pptx --to md --output ./output
```

## Primary Use Case: Batch Conversion

The main script `scripts/convert_docs.py` handles:
- Recursive directory scanning
- Clean filename generation (slugified, numbered)
- Index file creation with table of contents
- Progress tracking

**Example - Convert presentation course:**
```bash
uv run python .claude/skills/docling/scripts/convert_docs.py \
  --input .artifacts/presentations \
  --output docs/course \
  --format md \
  --prefix "lesson"
```

## Supported Formats

### Input Formats
| Format | Extension | Notes |
|--------|-----------|-------|
| PowerPoint | `.pptx` | Slides extracted with structure |
| PDF | `.pdf` | Layout analysis, OCR support |
| Word | `.docx` | Full formatting preserved |
| Excel | `.xlsx` | Tables converted |
| HTML | `.html` | Structure preserved |
| Images | `.png`, `.jpg`, `.tiff` | OCR extraction |
| Audio | `.wav`, `.mp3` | ASR transcription |
| Markdown | `.md` | Pass-through with parsing |
| CSV | `.csv` | Table structure |

### Output Formats
| Format | Flag | Use Case |
|--------|------|----------|
| Markdown | `--to md` | Documentation, RAG |
| JSON | `--to json` | Structured data, API |
| HTML | `--to html` | Web publishing |
| Text | `--to text` | Plain text extraction |
| DocTags | `--to doctags` | Docling internal format |

## CLI Reference

### Basic Usage
```bash
# Single file
uv run docling document.pdf --to md

# Multiple files
uv run docling file1.pdf file2.docx --to md

# Directory
uv run docling ./documents/ --to md --output ./output/

# URL
uv run docling https://example.com/doc.pdf --to md
```

### OCR Options
```bash
# Enable OCR (default: auto)
uv run docling scanned.pdf --ocr --ocr-engine tesseract

# Force OCR on all content
uv run docling document.pdf --force-ocr

# Specify language
uv run docling document.pdf --ocr-lang ukr,eng
```

**OCR Engines:** `auto`, `easyocr`, `tesseract`, `tesserocr`, `rapidocr`, `ocrmac` (macOS)

### Table Extraction
```bash
# Accurate mode (slower, better quality)
uv run docling document.pdf --table-mode accurate

# Fast mode
uv run docling document.pdf --table-mode fast

# Disable tables
uv run docling document.pdf --no-tables
```

### Image Handling
```bash
# Embed images as base64
uv run docling document.pdf --image-export-mode embedded

# Save images as separate files
uv run docling document.pdf --image-export-mode referenced

# Placeholder only (no images)
uv run docling document.pdf --image-export-mode placeholder
```

### AI Enrichment
```bash
# Enable code block detection
uv run docling document.pdf --enrich-code

# Enable formula recognition
uv run docling document.pdf --enrich-formula

# Enable picture classification
uv run docling document.pdf --enrich-picture-classification

# Enable picture description (VLM)
uv run docling document.pdf --enrich-picture-description
```

### VLM Pipeline (Vision Language Model)
```bash
# Use VLM for complex documents
uv run docling document.pdf --pipeline vlm --vlm-model granite_docling

# Available models: granite_docling, smoldocling, got_ocr_2, granite_vision
```

### ASR Pipeline (Audio Transcription)
```bash
# Transcribe audio
uv run docling audio.mp3 --pipeline asr --asr-model whisper_small

# Models: whisper_tiny, whisper_small, whisper_medium, whisper_large, whisper_turbo
```

### Performance Options
```bash
# Multi-threading
uv run docling document.pdf --num-threads 8

# GPU acceleration
uv run docling document.pdf --device cuda  # or mps for Apple Silicon

# Timeout per document
uv run docling document.pdf --document-timeout 300
```

## Python API

### Basic Conversion
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pptx")

# Export to Markdown
markdown = result.document.export_to_markdown()

# Export to JSON
json_data = result.document.export_to_dict()

# Save directly
result.document.save_as_markdown("output.md")
```

### Batch Conversion
```python
from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
sources = list(Path("./documents").glob("*.pdf"))

for result in converter.convert_all(sources):
    if result.status.name == "SUCCESS":
        output = Path("./output") / f"{result.input.file.stem}.md"
        result.document.save_as_markdown(output)
```

### With Pipeline Options
```python
from docling.document_converter import DocumentConverter, FormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

pdf_options = PdfPipelineOptions(
    do_ocr=True,
    do_table_structure=True,
    table_structure_options={"mode": "accurate"},
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: FormatOption(pipeline_options=pdf_options)
    }
)
```

### Chunking for RAG
```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("document.pdf")

chunker = HybridChunker()
chunks = list(chunker.chunk(result.document))

for chunk in chunks:
    print(f"Chunk: {chunk.text[:100]}...")
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No text extracted | Enable OCR: `--ocr` or `--force-ocr` |
| Tables not formatted | Use `--table-mode accurate` |
| Slow processing | Use `--table-mode fast`, reduce `--num-threads` |
| Memory errors | Reduce `--page-batch-size`, process files individually |

### Debug Options
```bash
uv run docling document.pdf -v     # info logging
uv run docling document.pdf -vv    # debug logging
uv run docling document.pdf --debug-visualize-layout  # see layout detection
```

## Resources

### scripts/
- `convert_docs.py` - Batch conversion with clean filenames and index generation
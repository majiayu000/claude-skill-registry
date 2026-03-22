---
name: pdf-to-md
description: Use this skill when the user wants to convert PDF files to Markdown using Docling. This includes converting single PDFs, batch-converting directories of PDFs, extracting structured content (headings, tables, lists) from academic papers, converting scanned documents with OCR, or configuring Docling pipeline options for table detection and image extraction.
---

# PDF to Markdown Conversion (Docling)

## Overview

Convert PDF documents to structured Markdown using the [Docling](https://docling-project.github.io/docling/) library. Docling uses ML models to understand document layout, preserving headings, tables, lists, and reading order. For advanced pipeline configuration, OCR settings, and performance tuning, see reference.md.

## Quick Start

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
markdown = result.document.export_to_markdown()

with open("document.md", "w", encoding="utf-8") as f:
    f.write(markdown)
```

**Install:** `pip install docling`

## Docling Library

### Basic Conversion

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("paper.pdf")

# Export as Markdown
md = result.document.export_to_markdown()

# Page count
print(f"{len(result.document.pages)} pages")
```

### Batch Conversion

```python
from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
output_dir = Path("markdown_outputs")
output_dir.mkdir(exist_ok=True)

for pdf in Path("papers/").glob("*.pdf"):
    result = converter.convert(str(pdf))
    md = result.document.export_to_markdown()
    (output_dir / f"{pdf.stem}.md").write_text(md, encoding="utf-8")
    print(f"Converted {pdf.name}")
```

### Custom Output Path

```python
from pathlib import Path
from docling.document_converter import DocumentConverter

def convert_pdf(pdf_path, output_path=None):
    pdf_path = Path(pdf_path)
    if output_path is None:
        output_path = pdf_path.with_suffix(".md")

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    Path(output_path).write_text(
        result.document.export_to_markdown(), encoding="utf-8"
    )
    return output_path
```

### Pipeline Configuration

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions()

# Use accurate table detection (slower but better for complex tables)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("report.pdf")
```

### Image Extraction

```python
from pathlib import Path
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions()
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result = converter.convert("paper.pdf")
image_dir = Path("images")
image_dir.mkdir(exist_ok=True)

for element, _level in result.document.iterate_items():
    if hasattr(element, 'image') and element.image is not None:
        img_path = image_dir / f"{element.self_ref}.png"
        element.image.pil_image.save(str(img_path))
```

### OCR for Scanned Documents

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("scanned_document.pdf")
md = result.document.export_to_markdown()
```

## Command-Line Usage

### Basic Script

```bash
# Single file
python scripts/pdf_to_markdown.py report.pdf

# Single file with custom output
python scripts/pdf_to_markdown.py report.pdf output.md

# Batch convert a directory
python scripts/pdf_to_markdown.py ./papers/

# Batch with custom output directory
python scripts/pdf_to_markdown.py ./papers/ ./converted/
```

### Advanced Script

```bash
# With image extraction
python scripts/pdf_to_markdown_advanced.py paper.pdf paper.md --with-images ./images

# With OCR for scanned documents
python scripts/pdf_to_markdown_advanced.py scanned.pdf output.md --ocr

# With accurate table detection
python scripts/pdf_to_markdown_advanced.py report.pdf report.md --accurate-tables

# Combine options
python scripts/pdf_to_markdown_advanced.py paper.pdf paper.md --ocr --accurate-tables --with-images ./img
```

## Common Tasks

### Academic Paper Conversion

Academic papers with sections, references, figures, and tables:

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions()
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("paper.pdf")
md = result.document.export_to_markdown()
```

### Lecture Slides

Slides often have sparse text with images — enable image extraction:

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("slides.pdf")
```

### Table-Heavy Documents

For documents where table accuracy is critical:

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# Convert and check tables
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("data_report.pdf")
md = result.document.export_to_markdown()
```

### Scanned PDFs

For scanned documents or image-based PDFs:

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
result = converter.convert("scanned.pdf")
```

## Quick Reference

| Task | Code |
|------|------|
| Basic conversion | `DocumentConverter().convert("file.pdf")` |
| Export to Markdown | `result.document.export_to_markdown()` |
| Page count | `len(result.document.pages)` |
| Batch convert | Loop over `Path("dir").glob("*.pdf")` |
| Accurate tables | `TableFormerMode.ACCURATE` in pipeline options |
| Enable OCR | `pipeline_options.do_ocr = True` |
| Extract images | `pipeline_options.generate_picture_images = True` |
| CLI single file | `python scripts/pdf_to_markdown.py file.pdf` |
| CLI batch | `python scripts/pdf_to_markdown.py ./dir/` |
| CLI advanced | `python scripts/pdf_to_markdown_advanced.py in.pdf out.md --ocr` |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: docling` | Docling not installed | `pip install docling` |
| File not found | Invalid path | Check file path exists |
| Invalid PDF | Corrupted or non-PDF file | Verify file is a valid PDF |
| Write permission error | Cannot write output | Use a different output directory |
| Slow first conversion | Model download on first use | Wait for ~500 MB model download; models are cached after |
| GPU not detected | CUDA/PyTorch not configured | Falls back to CPU automatically; install `torch` with CUDA for GPU |
| `UnicodeEncodeError` | Non-UTF-8 characters in output | Ensure `encoding='utf-8'` when writing files |
| `MemoryError` | PDF too large or complex | Process fewer pages at a time; close other applications |
| Table detection issues | Complex or borderless tables | Use `TableFormerMode.ACCURATE` |
| Poor OCR quality | Low-resolution scan | Use higher-DPI source; try EasyOCR backend (see reference.md) |
| Windows symlink warnings | HuggingFace cache issue | Set `HF_HUB_DISABLE_SYMLINKS_WARNING=1` (scripts do this automatically) |

## Next Steps

- For advanced pipeline configuration, OCR backends, export formats, chunking for RAG, and performance tuning, see **reference.md**
- For general PDF operations (merge, split, create, fill forms), see the **pdf** skill

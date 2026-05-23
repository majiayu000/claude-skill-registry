---
name: pdf-extractor
description: This skill should be used when the user asks to "extract text from PDF", "convert PDF to text", "parse PDF", "read PDF contents", "extract data from documents", "batch PDF extraction", "PDF to markdown", "OCR PDF", "get text from PDF files", "I have a PDF", "can you read this PDF", "what's in this PDF", "summarize this PDF", "open PDF file", "extract from [filename].pdf", or needs to process PDF documents for data extraction. Handles single-file extraction, batch processing, and OCR for scanned documents with automatic backend selection.
version: 0.1.0
example-prompt: "Extract text from document.pdf"
---

# PDF Data Extraction

Extract text and structured data from PDF documents using a multi-backend approach with automatic fallback.

## Overview

This skill provides PDF text extraction with 9 different backends, automatic GPU detection, and intelligent backend selection. The extraction system tries backends in order until one succeeds, producing markdown output optimized for further processing.

## Quick Start Workflow

To extract text from PDFs:

1. **Single file extraction (installed CLI - recommended):**
   ```bash
   extract-pdfs /path/to/document.pdf
   ```
   Output: Creates `document.md` in the same directory.

2. **Batch extraction (directory):**
   ```bash
   extract-pdfs /path/to/pdfs/ /path/to/output/
   ```
   Output: Creates `.md` files for all PDFs in output directory.

3. **Custom output file:**
   ```bash
   extract-pdfs document.pdf output.md
   ```

4. **Specific backends:**
   ```bash
   extract-pdfs document.pdf --backends markitdown pdfplumber
   ```

5. **List available backends:**
   ```bash
   extract-pdfs --list-backends
   ```
   Output: Shows available backends and GPU status.

### Alternative Execution Methods

If the `extract-pdfs` CLI isn't installed, install it first (recommended):

```bash
# Install as global UV tool (from repo root):
cd "${CLAUDE_PLUGIN_ROOT}/../.." && uv tool install --force --editable plugins/pdf-extractor
extract-pdfs --list-backends  # verify
```

Or use these fallback methods without installing:

```bash
# uv run (recommended fallback — no install required):
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -m pdf_extraction document.pdf

# Standalone script execution
python "${CLAUDE_PLUGIN_ROOT}/src/pdf_extraction/cli.py" document.pdf
```

## Backend Selection Guide

### Custom Backend Ordering

Specify backends in any order with `--backends`. The system tries each in order, stopping on first success:

```bash
# Tables first, then general extraction
extract-pdfs document.pdf --backends pdfplumber markitdown pdfminer

# Scanned documents: vision-based first
extract-pdfs scanned.pdf --backends marker docling markitdown

# Most permissive fallback order (handles problematic PDFs)
extract-pdfs document.pdf --backends pdfminer pypdf2 markitdown

# Single backend only (no fallback)
extract-pdfs document.pdf --backends markitdown
```

### CPU-Only Systems (Default)

For systems without GPU, the recommended backend order:
- `markitdown` - Microsoft's lightweight converter (MIT, fast, no models)
- `pdfplumber` - Excellent for tables (MIT)
- `pdfminer` - Pure Python, reliable (MIT)
- `pypdf2` - Basic extraction, always available (BSD-3)

### GPU Systems

For systems with CUDA-enabled GPU:
- `docling` - IBM layout analysis (MIT, ~500MB models)
- `marker` - Vision-based, best for scanned docs (GPL-3.0, ~1GB models)
- Plus all CPU backends as fallback

### Backend Comparison

| Backend | License | Models | Best For | Speed |
|---------|---------|--------|----------|-------|
| markitdown | MIT | None | General text, forms | Fast |
| pdfplumber | MIT | None | Tables, structured data | Fast |
| pdfminer | MIT | None | Simple text documents | Fast |
| pypdf2 | BSD-3 | None | Basic extraction | Fast |
| docling | MIT | ~500MB | Layout analysis | Medium |
| marker | GPL-3.0 | ~1GB | Scanned documents | Slow |
| pymupdf4llm | AGPL-3.0 | None | LLM-optimized output | Fast |
| pdfbox | Apache-2.0 | None | Tables (Java-based) | Medium |
| pdftotext | System | None | Simple text (CLI) | Fast |

### Backend Decision Matrix

| Document Type | Recommended Backend(s) | Why |
|---------------|------------------------|-----|
| Digital text PDF (default) | markitdown, pdfplumber | Fast, accurate |
| PDF with tables/invoices | pdfplumber, pdfbox | Best table structure |
| Complex layouts/columns | docling (GPU) | Layout analysis |
| Scanned documents/images | marker, docling (GPU) | OCR/vision required |
| Insurance policies/forms | markitdown, pdfplumber | Handles form fields |
| Academic papers | docling | Equations, figures |
| Maximum compatibility | pdfminer, pypdf2 | Fewest dependencies |
| Commercial use required | markitdown, pdfplumber | MIT license |

## Programmatic Usage

To use the extraction library directly in Python code:

```python
from pdf_extraction import extract_single_pdf, pdf_to_txt, detect_gpu_availability

# Check available backends
gpu_info = detect_gpu_availability()
print(f"Recommended backends: {gpu_info['recommended_backends']}")

# Extract single file
result = extract_single_pdf(
    input_file='/path/to/document.pdf',
    output_file='/path/to/output.md',
    backends=['markitdown', 'pdfplumber']
)

if result['success']:
    print(f"Extracted with {result['backend_used']}")
    print(f"Quality metrics: {result['quality_metrics']}")

# Batch extract directory
output_files, metadata = pdf_to_txt(
    input_dir='/path/to/pdfs/',
    output_dir='/path/to/output/',
    resume=True,  # Skip already-extracted files
    return_metadata=True
)
```

## Extraction Metadata

Every extraction returns metadata for quality assessment:

```python
{
    'success': True,
    'backend_used': 'markitdown',
    'extraction_time_seconds': 2.5,
    'output_size_bytes': 15234,
    'quality_metrics': {
        'char_count': 15234,
        'line_count': 450,
        'word_count': 2800,
        'table_markers': 12,      # Count of | (tables)
        'has_structure': True     # Has markdown structure
    },
    'encrypted': False,
    'error': None
}
```

## Handling Common Scenarios

### Encrypted PDFs

The system detects encrypted PDFs and reports them:
```python
if result['encrypted']:
    print("PDF is password-protected")
```

Encrypted PDFs cannot be extracted without the password.

### Empty or Failed Extractions

When all backends fail:
1. Check if PDF is encrypted
2. Try with `--backends pdfminer pypdf2` (most permissive)
3. Check PDF isn't corrupted
4. Consider OCR-based backends for scanned documents

### Resume Batch Processing

To continue interrupted batch extraction:
```bash
extract-pdfs /path/to/pdfs/ /path/to/output/
```
The `resume=True` default skips already-extracted files.

To force re-extraction:
```bash
extract-pdfs /path/to/pdfs/ --no-resume
```

### Tables and Structured Data

For PDFs with tables, prioritize:
```bash
extract-pdfs document.pdf --backends pdfplumber markitdown
```

The output will contain markdown tables when detected:
```markdown
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| Data    | Data    | Data    |
```

## Module Structure Reference

### Source Code Layout

**Location:** `${CLAUDE_PLUGIN_ROOT}/src/pdf_extraction/`

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports (extract_single_pdf, pdf_to_txt, etc.) |
| `__main__.py` | Support for `python -m pdf_extraction` |
| `cli.py` | CLI entry point with argparse |
| `backends.py` | BackendExtractor base class + 9 backend implementations |
| `extractors.py` | extract_single_pdf(), pdf_to_txt() functions |
| `utils.py` | GPU detection, quality metrics, encryption check |

### Key Classes and Functions

| Component | Location | Purpose |
|-----------|----------|---------|
| `BackendExtractor` | backends.py:35-123 | Base class with Template Method pattern |
| `DoclingExtractor` | backends.py:130-142 | IBM Docling backend (MIT, GPU) |
| `MarkerExtractor` | backends.py:145-158 | Vision-based marker backend (GPL-3.0, GPU) |
| `MarkItDownExtractor` | backends.py:161-173 | Microsoft MarkItDown (MIT, CPU) |
| `PdfplumberExtractor` | backends.py:244-253 | Table-focused extraction (MIT) |
| `PdfminerExtractor` | backends.py:219-226 | Pure Python fallback (MIT) |
| `Pypdf2Extractor` | backends.py:229-241 | Basic extraction, always available (BSD-3) |
| `BACKEND_REGISTRY` | backends.py:279-292 | Dict mapping backend names to factories |
| `detect_gpu_availability()` | utils.py:9-40 | Auto-detect GPU and recommend backends |
| `extract_single_pdf()` | extractors.py:13-80 | Extract one PDF with backend fallback |
| `pdf_to_txt()` | extractors.py:83-170 | Batch extract directory with resume |

**Key implementation details:**
- Backend fallback loop: `extractors.py:55-78` - Tries each backend in order, stops on first success
- Lazy initialization: `backends.py:77-79` - Converters created only when first used
- Quality metrics: `utils.py:43-76` - Calculates char/word/table counts

## Additional Resources

### Reference Files

For detailed backend documentation and advanced patterns:
- **`references/backends.md`** - Detailed backend comparison and selection guide

### Example Usage

Working examples in the insurance analysis that prompted this skill:
- Extracted 21 PDFs from mortgage statements and insurance policies
- Used markitdown backend for fast extraction
- Parsed structured data (dates, amounts, policy numbers)

## Error Handling

The extraction system handles errors gracefully:

1. **Backend failures**: Automatically tries next backend
2. **Import errors**: Skips unavailable backends
3. **File errors**: Reports specific error message
4. **Partial success**: Continues with remaining files in batch

All errors are captured in metadata rather than raising exceptions.

## Dependencies

Core dependencies (always available):
- `pdfminer.six` - Pure Python PDF parser
- `pdfplumber` - Table-aware extraction
- `PyPDF2` - Basic PDF operations
- `tqdm` - Progress bars

Optional dependencies:
- `markitdown` - Microsoft multi-format converter
- `docling` - IBM document processor (GPU-accelerated)
- `marker-pdf` - Vision-based extraction (GPU-accelerated)
- `pymupdf4llm` - LLM-optimized output
- `pdfbox` - Java-based extraction

Install all dependencies:
```bash
uv pip install "markitdown>=0.1.0" "pdfplumber>=0.10.0" "pdfminer.six>=20221105" "PyPDF2>=3.0.0" tqdm
```

For GPU backends:
```bash
uv pip install docling marker-pdf
```

## Troubleshooting

### `extract-pdfs: command not found`
```bash
# Install as global UV tool from repo root:
cd plugins/pdf-extractor && uv tool install --force --editable . && cd ../..
extract-pdfs --list-backends  # verify
```

### `ModuleNotFoundError: No module named 'pdf_extraction'` (or 'markitdown', 'pdfplumber')
```bash
# Re-install with all base dependencies:
cd plugins/pdf-extractor && uv tool install --force --editable . && cd ../..
# Or install explicitly:
uv pip install "markitdown>=0.1.0" "pdfplumber>=0.10.0" "pdfminer.six>=20221105" "PyPDF2>=3.0.0" tqdm
```

### GPU backends (docling, marker) not available
```bash
# Requires PyTorch; install GPU extras:
cd plugins/pdf-extractor && uv tool install --force --editable ".[gpu]" && cd ../..
extract-pdfs --list-backends  # verify gpu backends appear
# Note: docling downloads ~500MB models on first use; marker downloads ~1GB
```

### Empty output from scanned PDF (image-only document)
```bash
# Scanned PDFs require OCR (GPU backends):
extract-pdfs scanned.pdf --backends marker docling
# If GPU unavailable, try pdftotext (system tool):
brew install poppler        # macOS
# apt install poppler-utils  # Ubuntu/Debian
extract-pdfs scanned.pdf --backends pdftotext
```

### pdfminer import error (package name confusion)
```bash
# Install correct package (name has .six suffix):
uv pip install "pdfminer.six>=20221105"
# Import is still: from pdfminer.high_level import extract_text  (no .six)
```

### markitdown version conflict
```bash
# API changed significantly in 0.1.0; ensure correct version:
uv pip install "markitdown>=0.1.0"
```

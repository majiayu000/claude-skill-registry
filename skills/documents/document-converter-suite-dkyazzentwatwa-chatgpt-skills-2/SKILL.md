---
name: document-converter-suite
description: Convert between 8 formats (PDF, DOCX, PPTX, XLSX, TXT, CSV, MD, HTML). Best-effort text extraction, batch processing, and document format transformation.
---

# Document Converter Suite

## Overview

Provide a best-effort conversion workflow between **8 document formats**:

**Office Formats**: PDF, Word (DOCX), PowerPoint (PPTX), Excel (XLSX)
**Text Formats**: Plain Text (TXT), CSV, Markdown (MD), HTML

Uses `pypdf`, `python-docx`, `python-pptx`, `openpyxl`, `reportlab`, `mistune`, `beautifulsoup4`, and `Pillow`.

Prefer **reliable extraction + rebuild** (text, headings, bullets, basic tables) over pixel-perfect layout.

## When to use

Use when the request involves:

- Converting a file between **.pdf / .docx / .pptx / .xlsx / .txt / .csv / .md / .html**
- Making a document **more editable** by moving its content into Office or text formats
- Exporting slide text or spreadsheet cell grids to a different format
- Converting Markdown/HTML documentation to Office formats or vice versa
- Extracting tables from Office documents to CSV/XLSX
- Batch-converting a folder of mixed documents

**Supported conversion paths**: 64 total (8×8 matrix) - see `references/conversion_matrix.md`

Avoid promising visual fidelity. Emphasize that output is **clean and structured**, not identical.

## Workflow decision tree

1. **Identify input and desired output** (extensions matter).
2. **Classify the user's goal**:
   - **Editable content** → proceed with this suite.
   - **Visually identical rendering** → explain limitations; suggest external rendering tools.
3. **Pick conversion mode**:
   - Single file → run `scripts/convert.py`.
   - Folder/batch → run `scripts/batch_convert.py`.
4. **Tune safety caps** if needed:
   - PDF: `--max-pages`, `--max-chars`
   - XLSX: `--max-rows`, `--max-cols`
5. **Run conversion**, then sanity-check output size and structure.
6. **Iterate** (e.g., increase max rows/cols, split large docs, or choose a different target format).

## Quick start

### Single-file conversion

Run:

```bash
python scripts/convert.py <input-file> --to <pdf|docx|pptx|xlsx|txt|csv|md|html>
```

Examples:

```bash
# Office format conversions
python scripts/convert.py report.pdf --to docx
python scripts/convert.py deck.pptx --to pdf --out deck_export.pdf
python scripts/convert.py data.xlsx --to pptx --max-rows 40 --max-cols 12

# Text format conversions
python scripts/convert.py documentation.md --to docx
python scripts/convert.py data.csv --to xlsx
python scripts/convert.py report.docx --to html
python scripts/convert.py notes.txt --to md
```

### Batch conversion

Run:

```bash
python scripts/batch_convert.py <input-dir> --to <pdf|docx|pptx|xlsx|txt|csv|md|html>
```

Examples:

```bash
python scripts/batch_convert.py ./inbox --to docx --recursive
python scripts/batch_convert.py ./inbox --to pdf --outdir ./out --recursive --overwrite
python scripts/batch_convert.py ./markdown-docs --to html --pattern "*.md"
python scripts/batch_convert.py ./data --to xlsx --pattern "*.csv"
```

## Conversion behavior

Follow these defaults (and say them out loud if the user might be expecting magic):

### Office Format Conversions

- **PDF → (DOCX/PPTX/XLSX/TXT/MD/HTML)**: extract text with `pypdf`; no OCR; each page becomes a section/slide block.
- **DOCX → (PDF/PPTX/XLSX/TXT/CSV/MD/HTML)**: export paragraphs, headings (with improved detection), and tables.
  - **Improved heading detection**: now uses font size + bold + ALL CAPS heuristics, not just style names.
- **PPTX → (DOCX/PDF/XLSX/TXT/CSV/MD/HTML)**: export slide titles + text frames; export tables.
  - **Multi-table support**: PPTX now creates one slide per table when multiple tables exist.
- **XLSX → (DOCX/PPTX/PDF/TXT/CSV/MD/HTML)**: export bounded value grid per sheet (defaults: 200×50).
  - **Truncation warnings**: printed to stderr when data exceeds limits (e.g., "Sheet 'Data': Truncated 500 rows → 200 rows").

### Text Format Conversions

- **TXT → (DOCX/PPTX/XLSX/PDF/CSV/MD/HTML)**: lines become paragraphs/bullets; simple structure preservation.
- **CSV → (XLSX/DOCX/PPTX/HTML)**: headers + rows mapped to tables/sheets; auto-delimiter detection.
- **MD → (DOCX/PPTX/XLSX/PDF/TXT/CSV/HTML)**: parsed with `mistune`; headings, lists, tables, code blocks preserved.
  - **High fidelity**: Markdown ↔ HTML and Markdown ↔ DOCX maintain structure well.
- **HTML → (DOCX/PPTX/XLSX/PDF/TXT/CSV/MD)**: parsed with `beautifulsoup4`; semantic structure extracted.
  - **High fidelity**: HTML ↔ Markdown and HTML ↔ DOCX maintain structure well.

### Quality Improvements

- **Multi-table PPTX**: Creates one slide per table (instead of dropping extra tables)
- **Smart heading detection**: DOCX headings detected by style, font size+bold, or ALL CAPS+bold
- **Data truncation warnings**: XLSX conversions warn when data is truncated
- **Image extraction foundation**: `image_handler.py` provides hash-based deduplication for future image support

Load extra detail from:

- `references/conversion_matrix.md` - Full 8×8 conversion matrix
- `references/limitations.md` - Format-specific limitations and edge cases

## Guardrails and honesty rules

- State "best-effort" explicitly for any conversion request.
- Do not claim formatting fidelity (fonts, spacing, images, charts, animations).
- Call out scanned PDFs as a likely failure mode (no OCR).
- For giant spreadsheets, prefer increasing caps gradually and/or limiting to specific sheets (if user provides intent).

## Bundled scripts

- `scripts/convert.py`: single-file CLI converter
- `scripts/batch_convert.py`: batch converter for directories
- `scripts/lib/*`: internal readers/writers and conversion orchestration

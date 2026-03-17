---
name: pdf-extractor
description: Extract text, tables, and images from PDF files. Use when converting PDF documentation, manuals, or reports to searchable text.
tools: Read, Write, Bash
---

# PDF Extractor Skill

## Purpose

Single responsibility: Extract structured content (text, tables, images) from PDF files into organized, searchable formats. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] PDF file exists and is readable (`file <path>` confirms PDF format)
- [ ] PDF is not corrupted (`pdfinfo <path>` returns metadata)
- [ ] Password known if encrypted
- [ ] Output directory is writable
- [ ] Required tools available (pdfplumber, pytesseract for OCR)

**DO NOT proceed without verification. Inspect PDF metadata first.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- PDF appears to be scanned (needs OCR) but OCR tools unavailable
- Multiple table formats detected - unclear which parser to use
- Password-protected but no password provided
- Image extraction quality unclear (resolution, format preferences)
- Language detection needed for OCR

**NEVER assume PDF structure without inspection.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target PDF, extraction options, output path | Other PDF files |
| PERIPHERAL | Similar PDF structure examples | Unrelated documents |
| DISTRACTOR | Previous extraction attempts | Other file formats |

## Workflow Steps

### Step 1: Inspect PDF (Grounding)

```bash
# Check file type
file document.pdf

# Get PDF metadata
pdfinfo document.pdf

# Check page count
pdfinfo document.pdf | grep Pages

# Check if encrypted
pdfinfo document.pdf | grep Encrypted
```

### Step 2: Determine Extraction Strategy

| PDF Type | Detection | Strategy |
|----------|-----------|----------|
| Text-based | `pdftotext` produces readable text | Direct extraction |
| Scanned/Image | `pdftotext` produces empty/garbled | OCR required |
| Mixed | Some pages text, some images | Hybrid approach |
| Tables | Visual grid patterns | Table extraction mode |
| Forms | Interactive fields | Form field extraction |

### Step 3: Execute Extraction

**Option A: With skill-seekers (if installed)**

```bash
# Basic extraction
skill-seekers pdf --pdf document.pdf --name myskill

# With table extraction
skill-seekers pdf --pdf document.pdf --name myskill --extract-tables

# With OCR for scanned docs
skill-seekers pdf --pdf document.pdf --name myskill --ocr

# With parallel processing (large PDFs)
skill-seekers pdf --pdf document.pdf --name myskill --parallel --workers 8

# Password-protected
skill-seekers pdf --pdf document.pdf --name myskill --password "secret"
```

**Option B: Manual extraction guidance**

```bash
# Basic text extraction
pdftotext -layout document.pdf output.txt

# Extract with page markers
pdftotext -layout -eol unix document.pdf output.txt

# Extract images
pdfimages -all document.pdf images/

# OCR scanned PDF (requires tesseract)
pdftoppm document.pdf page -png
tesseract page-*.png output -l eng
```

### Step 4: Validate Output

```bash
# Check extraction quality
head -100 output/<skill-name>/references/content.md

# Verify table extraction
grep -A 10 "| " output/<skill-name>/references/*.md

# Check image extraction
ls -la output/<skill-name>/assets/images/
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Stop extraction, preserve partial output
2. **DIAGNOSE** - Check error type:
   - `File not found` → Verify path
   - `Password required` → Ask user for password
   - `Corrupt PDF` → Try repair with `qpdf --check`
   - `OCR failed` → Check tesseract installation, language packs
   - `Memory error` → Process in chunks, reduce workers
3. **ADAPT** - Switch strategy based on diagnosis
4. **RETRY** - Resume with adapted approach (max 3 attempts)
5. **ESCALATE** - Ask user for guidance

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/pdf-extractor/`

For large PDFs, extraction saves progress per chunk:
```
checkpoints/pdf-extractor/
├── document_metadata.json
├── pages_1-50.json
├── pages_51-100.json
└── current_position.json
```

## Output Structure

```
output/<skill-name>/
├── SKILL.md              # Skill description with PDF summary
├── references/
│   ├── index.md          # Table of contents
│   ├── chapter_1.md      # Content by section
│   ├── chapter_2.md
│   └── tables.md         # Extracted tables
└── assets/
    └── images/           # Extracted images (if enabled)
        ├── page_1_fig_1.png
        └── page_5_chart_1.png
```

## Configuration Options

```json
{
  "name": "mymanual",
  "description": "Product manual documentation",
  "pdf_path": "docs/manual.pdf",
  "extract_options": {
    "chunk_size": 10,
    "min_quality": 6.0,
    "extract_images": true,
    "min_image_size": 150,
    "ocr_enabled": false,
    "ocr_language": "eng",
    "table_extraction": true
  },
  "categories": {
    "getting_started": ["introduction", "setup", "installation"],
    "usage": ["using", "operation", "guide"],
    "reference": ["appendix", "specifications", "api"]
  }
}
```

## Extraction Quality Metrics

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Text extraction rate | >95% | 80-95% | <80% |
| Table accuracy | >90% | 70-90% | <70% |
| Image quality | >300 DPI | 150-300 DPI | <150 DPI |
| OCR confidence | >90% | 70-90% | <70% |

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Garbled text | Scanned PDF | Enable OCR mode |
| Missing tables | Complex layout | Use `--extract-tables` with pdfplumber |
| Poor OCR | Low resolution | Increase DPI, check language pack |
| Memory error | Large PDF | Use chunked extraction, reduce workers |
| Corrupt PDF | File damaged | Try `qpdf --check` or `mutool clean` |

## Dependencies

**Required:**
- Python 3.10+
- pdfplumber or pypdf

**Optional (for advanced features):**
- pytesseract + tesseract-ocr (for OCR)
- Pillow (for image processing)
- camelot-py (for complex tables)

## References

- Skill Seekers PDF Support: https://github.com/jmagly/Skill_Seekers/blob/main/docs/PDF_MCP_TOOL.md
- REF-001: Production-Grade Agentic Workflows (BP-1, BP-4)
- REF-002: LLM Failure Modes (Archetype 1-4 mitigations)

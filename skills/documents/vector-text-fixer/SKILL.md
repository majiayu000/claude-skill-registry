---
name: vector-text-fixer
description: Fix garbled text in PDF/SVG vector graphics caused by font encoding issues, making files editable in AI tools. Supports batch processing and JSON export for manual correction.
license: MIT
skill-author: AIPOCH
---

# Vector Text Fixer

Fixes garbled text in PDF/SVG vector graphics caused by font embedding problems, encoding errors, or missing font substitution. Outputs repaired files or editable JSON for AI tool import.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --input document.pdf --output fixed.pdf
python scripts/main.py --input diagram.svg --output fixed.svg
```

## When to Use

- Fix garbled/box characters in PDF files caused by font embedding issues
- Repair SVG text encoding errors before editing in Illustrator or Inkscape
- Batch-process a folder of PDF/SVG files with garbled text
- Export a text map JSON for manual correction in AI editors

## Workflow

1. Confirm input file path (PDF or SVG) or batch folder, and desired output path.
2. Validate that the request involves PDF/SVG garbled text repair; stop early if not.
3. Run `scripts/main.py --input <file> --output <file>` or `--batch <folder>`.
4. Return a structured result separating repaired blocks, skipped blocks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the Fallback Template below.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <repair goal>
Inputs Available : <file path or batch folder provided>
Missing Inputs   : <list exactly what is missing>
  Note: --input requires a valid PDF or SVG file path, not a text string.
        For batch mode use --batch <folder_path> instead.
Partial Result   : <any blocks repaired safely>
Blocked Steps    : <what could not be completed and why>
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Stress-Case Output Checklist

For complex multi-constraint requests, always include these sections explicitly:

- **Assumptions**: repair level default (standard), encoding auto-detected
- **Constraints**: encrypted PDFs require password unlock first; scanned PDFs need OCR first
- **Risks**: severely damaged files may not be fully repairable; rare fonts may not map correctly
- **Unresolved Items**: blocks with confidence < 0.3 flagged for manual review

## Supported Scenarios

**PDF Garbled Text:**
- Box/question mark issues from font embedding problems
- Garbled text from encoding conversion errors
- Missing font substitution characters
- Multi-language mixed encoding issues

**SVG Garbled Text:**
- Text entity encoding errors
- Special character escaping issues
- Invalid font reference display abnormalities
- XML encoding declaration errors

## CLI Usage

```bash
# Fix single PDF
python scripts/main.py --input document.pdf --output fixed.pdf

# Fix single SVG
python scripts/main.py --input diagram.svg --output fixed.svg

# Batch process folder
python scripts/main.py --batch ./input_folder --output ./output_folder

# Interactive repair
python scripts/main.py --input doc.pdf --interactive

# Export editable JSON
python scripts/main.py --input doc.pdf --export-json editable.json

# Specify repair level
python scripts/main.py --input doc.pdf --output fixed.pdf --repair-level aggressive
```

## Parameters

| Parameter | Required | Description | Default |
|---|---|---|---|
| `--input` | Yes* | Input PDF or SVG file path | — |
| `--batch` | Yes* | Batch input folder path | — |
| `--output` | Yes | Output file or folder path | — |
| `--repair-level` | No | `minimal` / `standard` / `aggressive` | `standard` |
| `--interactive` | No | Enable interactive repair mode | False |
| `--export-json` | No | Export editable JSON format | — |
| `--encoding` | No | Source file encoding (default: auto-detect) | auto |

*At least one of `--input` or `--batch` is required.

## Repair Levels

- **Minimal**: Only obvious errors (replacement characters, null bytes); maximum original integrity
- **Standard**: Common encoding issues + smart font replacement; balanced repair rate and accuracy
- **Aggressive**: Full text re-encoding + OCR-assisted recognition; for severely garbled documents

## Output Format (JSON Export)

```json
{
  "file_type": "pdf",
  "pages": [{
    "page_num": 1,
    "text_blocks": [{
      "id": "tb_001",
      "bbox": [100, 200, 300, 220],
      "original_text": "?????",
      "detected_encoding": "UTF-8",
      "confidence": 0.3,
      "suggested_fix": "Sample Text"
    }]
  }],
  "repair_summary": {
    "total_blocks": 15,
    "fixed_blocks": 12,
    "skipped_blocks": 3
  }
}
```

## Input Validation

This skill accepts: PDF (.pdf) or SVG (.svg) file paths, or a folder path for batch processing, where the files contain garbled or unreadable text caused by font/encoding issues.

If the request does not involve PDF/SVG garbled text repair — for example, asking to convert file formats, edit PDF content directly, perform OCR on scanned images, or process non-vector files — do not proceed. Instead respond:

> "`vector-text-fixer` is designed to fix garbled text in PDF/SVG vector graphics caused by font encoding issues. Your request appears to be outside this scope. Please provide a valid PDF or SVG file path, or use a more appropriate tool."

## Error Handling

- If `--input` receives a text string instead of a file path, report the error and request a valid file path.
- If the file is encrypted, report that password unlock is required before processing.
- If the task goes outside documented scope, stop instead of guessing.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate repaired text content or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — file(s) repaired and repair level used
2. **Inputs Received** — file path, repair level, encoding settings
3. **Assumptions** — defaults applied (repair level, encoding detection)
4. **Result** — output file path, blocks fixed vs skipped
5. **Risks and Limits** — confidence thresholds, manual review blocks
6. **Next Checks** — review low-confidence blocks manually before use

## Limitations

- Encrypted PDFs require password unlock before processing
- Severely damaged vector files may not be fully repairable
- Some rare fonts may not map correctly
- Scanned PDFs require OCR recognition first

## Dependencies

```
pdfplumber >= 0.10.0
PyMuPDF >= 1.23.0
cairosvg >= 2.7.0
beautifulsoup4 >= 4.12.0
fonttools >= 4.40.0
chardet >= 5.0.0
Pillow >= 10.0.0
```

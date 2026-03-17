---
name: pdf-reader
description: Reads PDF, DOCX, and image text (OCR) and can pinpoint schedule lines from syllabus documents. Use when the user asks to extract text from docs/images or analyze deadlines and class schedules.
---

# PDF + OCR Reader Skill

Use this skill for document extraction and schedule pinpoints.

## What it supports

- PDF text extraction (`pdftotext`)
- DOCX text extraction (`word/document.xml`)
- Image OCR (`tesseract` if available, otherwise macOS Vision OCR via Swift)
- Syllabus schedule/deadline pinpoint analysis

## Commands

```bash
# Legacy PDF-only command
node "{baseDir}/scripts/read_pdf.mjs" --file "/path/to/your/document.pdf"
```

```bash
# Unified reader (PDF/DOCX/Image) + optional schedule analysis
python3 "{baseDir}/scripts/read_docs.py" \
  --path "$HOME/Desktop/syllabus" \
  --analyze-schedule \
  --save "$HOME/Desktop/syllabus/syllabus_schedule_report.md" \
  --json-out "$HOME/Desktop/syllabus/syllabus_schedule_report.json"
```

```bash
# Shortcut wrapper for syllabus folder
bash "$HOME/openclaw_pro/workspace/scripts/syllabus_pinpoint.sh" \
  "$HOME/Desktop/syllabus"
```

## Output contract

- `ANALYSIS_STATUS=ok|error`
- `FILES_SCANNED=...`
- `EVENTS_FOUND=...`
- `REPORT_MD=...`
- `REPORT_JSON=...`
- `PINPOINT_TOP_START ... PINPOINT_TOP_END`

## Notes

- OCR quality is highest on clear images (300dpi+).
- For scanned PDFs, OCR fallback uses `pdftoppm` + OCR.
- If OCR backend is unavailable, script still returns extracted text from readable PDFs/DOCX.

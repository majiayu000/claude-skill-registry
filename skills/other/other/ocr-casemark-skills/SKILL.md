---
name: ocr
description: Processes documents through case.dev OCR for text and table extraction. Supports PDF and image files up to 500MB with page-level and word-level output. Use when the user mentions "OCR", "text extraction", "scan document", "digitize", "extract text from PDF", or needs word-level positional data from documents.
---

# case.dev OCR

Production-grade document OCR with table extraction and word-level positional data. Processes PDFs and images (PNG, JPG, TIFF, BMP, WEBP) up to 500MB.

Requires the `casedev` CLI. See `setup` skill for installation and auth.

## Process a Document

```bash
casedev ocr process --document-url "https://example.com/contract.pdf" --json
```

Flags: `--document-url` (required), `--document-id` (optional tag), `--engine` (override).

Returns a job ID and initial status.

## Check Job Status

```bash
casedev ocr status JOB_ID --json
```

Statuses: `queued` -> `processing` -> `completed` or `failed`.

## Watch Until Complete

```bash
casedev ocr watch JOB_ID --json
```

Flags: `--interval` (default: 3s), `--timeout` (default: 900s).

## Word-Level Data

```bash
casedev ocr words --vault VAULT_ID --object OBJECT_ID --json
```

Requires the document to be in a vault with completed OCR ingestion.

Flags: `--page` (specific page), `--word-start`, `--word-end` (index range).

Returns per-page word arrays with text, word index, and confidence scores.

## Common Workflows

### OCR a vault document

```bash
# 1. Upload (triggers automatic ingestion + OCR)
casedev vault object upload ./scanned-contract.pdf --vault VAULT_ID --json

# 2. Check ingestion status
casedev vault object list --vault VAULT_ID --json

# 3. Get word-level data
casedev ocr words --vault VAULT_ID --object OBJECT_ID --json
```

### OCR an external document

```bash
casedev ocr process --document-url "https://storage.example.com/doc.pdf" --json
casedev ocr watch JOB_ID --json
```

## Troubleshooting

**"Invalid file type for OCR"**: Only PDFs and images supported. Check content type with `casedev vault object list`.

**Job stuck in "processing"**: Increase timeout with `--timeout 1800`. Large documents (100+ pages) take longer.

**"OCR job failed"**: Document may be corrupted or unsupported. Re-upload and retry.

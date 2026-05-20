---
name: ocr
description: Processes documents through case.dev OCR for text and table extraction. Supports PDF and image files up to 500MB with page-level and word-level output. Use when the user mentions "OCR", "text extraction", "scan document", "digitize", "extract text from PDF", or needs word-level positional data from documents.
---

# case.dev OCR

Production-grade document OCR with table extraction and word-level positional data. Processes PDFs and images (PNG, JPG, TIFF, BMP, WEBP) up to 500MB.

Requires the `casedev` CLI. See `setup` skill for installation and auth.

## Process a Document

Submit a document URL for OCR:

```bash
casedev ocr process --document-url "https://example.com/contract.pdf" --json
```

Flags:
- `--document-url` / `--url` (required) — publicly accessible URL or presigned vault URL
- `--document-id` — optional identifier to tag the job
- `--engine` — OCR engine override

Returns a job ID and initial status.

## Check Job Status

```bash
casedev ocr status JOB_ID --json
```

Returns: ID, status, page count, created/completed timestamps.

Statuses: `queued` -> `processing` -> `completed` or `failed`.

## Watch Until Complete

```bash
casedev ocr watch JOB_ID --json
```

Polls until the job finishes. Flags:
- `--interval` / `-i` — poll interval in seconds (default: 3)
- `--timeout` / `-t` — max wait in seconds (default: 900)

## Word-Level Data

Retrieve word-level OCR output for a vault object:

```bash
casedev ocr words --vault VAULT_ID --object OBJECT_ID --json
```

This requires the document to be in a vault and have completed OCR ingestion. The object must be a PDF or image (audio/video files are rejected).

Flags:
- `--page` — specific page number
- `--word-start` — starting word index
- `--word-end` — ending word index

Returns per-page word arrays with text, word index, and confidence scores.

Uses focused vault if set via `casedev focus set --vault`.

## Common Workflow

### OCR a document from a vault

```bash
# 1. Upload to vault (triggers automatic ingestion + OCR)
casedev vault object upload ./scanned-contract.pdf --vault VAULT_ID --json

# 2. Check ingestion status
casedev vault object list --vault VAULT_ID --json

# 3. Get word-level data
casedev ocr words --vault VAULT_ID --object OBJECT_ID --json

# 4. Get specific page range
casedev ocr words --vault VAULT_ID --object OBJECT_ID --page 3 --json
```

### OCR an external document

```bash
# 1. Submit
casedev ocr process --document-url "https://storage.example.com/doc.pdf" --json

# 2. Watch
casedev ocr watch JOB_ID --json
```

## Troubleshooting

**"Invalid file type for OCR"**: OCR only supports PDFs and images (`application/pdf`, `image/*`). Check the object's content type with `casedev vault object list`.

**"Invalid object ID for this vault"**: Run `casedev vault object list --vault VAULT_ID` to see valid object IDs.

**Job stuck in "processing"**: Increase watch timeout with `--timeout 1800`. Large documents (100+ pages) take longer.

**"OCR job failed"**: The document may be corrupted or in an unsupported format. Re-upload and retry.

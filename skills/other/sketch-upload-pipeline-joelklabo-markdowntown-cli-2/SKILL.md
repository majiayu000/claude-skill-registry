---
name: sketch-upload-pipeline
description: Upload pipeline troubleshooting for Sketch Magic. Use when HEIC uploads fail, previews don’t render, files are too large, or upload validation errors appear.
---

# Sketch Upload Pipeline

## Overview
Standardize debugging for uploads, HEIC conversion, size limits, and preview lifecycle issues.

## Workflow

### 1) Confirm client validation
- Allowed types: PNG, JPG, HEIC/HEIF, WebP.
- Size limit: `MAX_UPLOAD_MB` / `DEFAULT_MAX_UPLOAD_BYTES` (10 MB default).

### 2) HEIC conversion path
- Client converts HEIC to JPEG via `heic2any` before upload when possible.
- If conversion fails, original file is still used and may preview as blank in some browsers.

### 3) Preview lifecycle
- Ensure object URL creation/revocation is stable (no early revoke).
- Confirm `sketch-preview-image` loads with `naturalWidth > 0`.

### 4) Server constraints
- Check server body limits (Next.js proxy body size).
- Confirm `/api/convert` handles large payloads within timeout.

### 5) Report safely
- Do not log image bytes or PII.
- Capture file type/size and error code only.

## References
- `references/upload-pipeline.md`

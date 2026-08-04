---
name: compdf-documents-to-pdf
description: Convert Word, Excel, PPT, HTML, TXT, CSV, RTF, PNG, and JPG files into PDF with ComPDF. Use when a business document or image needs fixed-layout PDF output for sharing, approvals, printing, or archiving.
---

# ComPDF Documents to PDF

## Overview

ComPDF Documents to PDF helps AI agents and teams standardize office files and web content into PDF. It supports Word to PDF, Excel to PDF, Slide to PDF, HTML to PDF, TXT to PDF, CSV to PDF, PNG to PDF, and RTF to PDF, making it easy to create fixed-layout deliverables for reporting, approvals, compliance, and distribution.

Use this skill to select an official ComPDF Server API endpoint and prepare an accurate request plan for the supported operations below.

## Supported Operations

| Operation | Official page or index section |
| --- | --- |
| Word to PDF | `word-to-pdf` |
| Excel to PDF | `excel-to-pdf` |
| PPT to PDF | `ppt-to-pdf` |
| HTML to PDF | `html-to-pdf` |
| TXT to PDF | `txt-to-pdf` |
| CSV to PDF | `csv-to-pdf` |
| RTF to PDF | `rtf-to-pdf` |
| PNG and JPG to PDF | `image-to-pdf` |

## Scope

Produce PDF only. Do not use this skill for PDF-to-document conversion or PDF page editing.

## Workflow

1. Identify the source file type, desired output, and requested operation.
2. Read `references/endpoint-index.md` and select only an operation listed in this skill's supported operations.
3. Read the matching heading in `references/official-api-reference.md`. Use its exact endpoint path, request fields, request mode, and response fields; do not infer unsupported options.
4. Prefer synchronous mode for small interactive work. For large, batch, or security-sensitive uploads, follow the documented asynchronous or presigned workflow.
5. Resolve the API key before preparing the request. Read the first non-empty line from `COMPDF_API_KEY_FILE` when set. Otherwise read `%USERPROFILE%\.compdf\api_key` on Windows, or `~/.config/compdf/api_key` on macOS and Linux. Pass the value only as the `x-api-key` header; never put it in code, logs, examples, or output.
6. Before an operation that overwrites, deletes, decrypts, applies permanent protection, or sends a document externally, identify affected files and obtain confirmation unless the user has already authorized it.
7. Return the endpoint, method, content type, complete request fields, expected task/result fields, and the next polling or download step. Preserve original files unless replacement is explicitly requested.

## API Key

Use one local, private key file so later ComPDF tasks do not require pasting an API key into chat. The file must contain only the API key on its first non-empty line. Do not create, commit, upload, or display this file.

When the selected file is absent, unreadable, or empty, direct the user to obtain a key at `https://www.compdf.com/compdf-portal/signin?utm_source=github&utm_medium=referral&utm_campaign=compdf_skills_repo_en&ref_platform_id=github_compdfkit_skills_en`, save it in the selected file, and retry.

## Maintainer

Refresh the local official snapshot before release, then inspect the diff for renamed endpoints, changed fields, and changed enum values:

```powershell
python scripts/sync_official_api_reference.py
```

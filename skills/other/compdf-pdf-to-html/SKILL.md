---
name: compdf-pdf-to-html
description: Convert PDF files into reusable HTML with ComPDF. Use for web publishing, browser workflows, portal embedding, content migration, and PDF-to-HTML requests.
---

# ComPDF PDF to HTML

## Overview

ComPDF PDF to HTML helps users and AI agents turn static PDF content into HTML that can be displayed on the web, embedded into portals, or reused in digital content workflows. It is useful for teams that want to move reports, manuals, brochures, or archived documents from PDF into browser-friendly formats without rebuilding pages manually.

Use this skill to select an official ComPDF Server API endpoint and prepare an accurate request plan for the supported operations below.

## Supported Operations

| Operation | Official page or index section |
| --- | --- |
| PDF to HTML | `pdf-to-html` |

## Scope

Produce HTML only. Do not substitute another PDF conversion endpoint.

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

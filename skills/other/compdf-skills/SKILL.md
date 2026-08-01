---
name: compdf-api
description: Integrate with the ComPDF Server API to convert PDF, Office, HTML, CSV, RTF, TXT, and image files; edit PDF pages; merge, split, extract, insert, rotate, compress, compare, encrypt, decrypt, and watermark PDFs; parse document structure; and extract fields or tables with ComPDF AI. Use whenever a user asks to process, convert, OCR, edit, protect, analyze, parse, or extract data from documents through ComPDF, or needs an exact ComPDF API endpoint, request field, request mode, response field, or implementation/debugging guidance.
---

# ComPDF API

Use this skill to select an official ComPDF Server API endpoint and produce an accurate request plan. Treat the bundled official snapshot as the source of truth for endpoint paths and fields. Do not infer unsupported options.

## Workflow

1. Identify the source file type, desired output, and whether the request is conversion, PDF editing/security, document parsing, or field extraction.
2. Read `references/endpoint-index.md` to choose the endpoint and the precise snapshot section to load.
3. Read the matching section in `references/official-api-reference.md`. Include every required field and only options supported by that endpoint.
4. State the request mode. Prefer synchronous mode for small interactive work; use asynchronous or presigned modes for large, batch, or security-sensitive uploads, following the official workflow reference.
5. Resolve the API key before preparing a request. Read the first non-empty line from `COMPDF_API_KEY_FILE` when that environment variable is set. Otherwise read `%USERPROFILE%\\.compdf\\api_key` on Windows, or `~/.config/compdf/api_key` on macOS and Linux. Pass the value only as the `x-api-key` header; never place it in code, logs, examples, or output.
6. Before an operation that overwrites, deletes, decrypts, applies permanent protection, or sends a document externally, identify the affected files and obtain confirmation when the user has not already authorized it.
7. Return the endpoint, method, content type, complete request fields, the expected task/result fields, and the next polling or download step. Preserve original files unless the user explicitly requests replacement.

## Reference Routing

- For all conversion tasks, use the `Conversion endpoints` section in `references/endpoint-index.md`.
- For merge, split, insert, delete, rotate, PDF/A, generation, encryption, decryption, watermark, compression, or comparison, use `PDF endpoints`.
- For layout parsing and schema-based extraction, use `AI endpoints`; read both the endpoint page and the corresponding guide sections listed there.
- For authentication, upload modes, task polling, asset lookup, webhook events, OCR codes, and compression flags, use `Common API behavior and values`.

`references/official-api-reference.md` is a generated snapshot of the official documentation. Search its level-two headings for the source page named in the index. When current release accuracy matters, run `scripts/sync_official_api_reference.py` and review the diff before publishing a new skill version.

## Request Discipline

- Use `multipart/form-data` only when the selected endpoint specifies file upload. Do not substitute field names, type values, or enum strings.
- Keep optional settings absent unless the user requests their behavior or an official default needs to be made explicit.
- Use `pageRanges` only with the documented one-based format and validate user-selected pages before requesting destructive page operations.
- Treat passwords and document content as sensitive. Do not repeat them in a response.
- For AI extraction, ask for the required output keys and table headers before constructing `extract_fields`; do not invent a business schema.

## API Key File

Use one local, private key file so later ComPDF tasks do not need to request the key again. The file must contain only the API key on its first non-empty line. Do not create, commit, upload, or display this file.

- Use `COMPDF_API_KEY_FILE` when a deployment provides a managed secret-file path.
- Otherwise use `%USERPROFILE%\\.compdf\\api_key` on Windows.
- Otherwise use `~/.config/compdf/api_key` on macOS and Linux.

When the selected file is absent, unreadable, or empty, do not ask the user to paste the key into chat. Tell them to obtain an API key at `https://www.compdf.com/compdf-portal/signin?utm_source=github&utm_medium=referral&utm_campaign=compdf_skills_repo_cn&ref_platform_id=github_compdfkit_skills_cn`, save it in the selected file, and retry the request.

## Maintainer Workflow

Run the snapshot updater before release and inspect its result for renamed endpoints, changed fields, or changed enum values:

```powershell
python scripts/sync_official_api_reference.py
python C:\Users\ddfme\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

The updater is read-only with respect to remote systems. It downloads only the official public ComPDF documentation pages and rewrites `references/official-api-reference.md`.

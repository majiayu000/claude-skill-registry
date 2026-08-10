---
name: pdf-processing
description: Inspect, extract, OCR, create, merge, split, reorder, rotate, annotate, fill, redact, compress, secure, and verify PDF documents while preserving source files and visual fidelity. Use when working with one or more .pdf files; converting documents to or from PDF; extracting text, tables, images, metadata, forms, or page ranges; applying true redactions or signatures; diagnosing malformed, encrypted, scanned, or inaccessible PDFs; or validating that a PDF transformation preserved the intended content and layout.
---

# PDF Processing

Preserve the original, choose tools from what is actually available, and verify both document structure and rendered appearance.

## Inputs

Collect or state:

- Source file(s), requested operation, destination, naming convention, and page order/ranges.
- Whether layout fidelity, searchable text, file size, accessibility, archival quality, or print output is the priority.
- OCR language, table/image requirements, form fields, annotations, bookmarks, links, and metadata expectations.
- Passwords or signing credentials supplied through an approved secure channel; never request private keys in chat.
- Whether content is confidential and whether local-only processing is required.

Clarify ambiguous page references: human page labels may differ from zero- or one-based physical page numbers.

## Output contract

Return:

1. New output file(s) at explicit paths; never silently overwrite the source.
2. Source and output SHA-256 hashes, byte sizes, page counts, and encryption status when determinable.
3. A concise operation log: tools used, options, page mapping, OCR language, redactions, and metadata changes.
4. Verification evidence for structure, content, and rendered appearance, plus limitations.
5. Any password, signature, accessibility, font, OCR, or active-content caveats.

Do not claim exactness when the check was heuristic or a page could not be rendered.

## Workflow

### 1. Preserve and inspect

- Resolve exact input paths and calculate hashes before making changes.
- Write to a new file or a temporary working copy. Never edit the sole source in place.
- Run the dependency-free structural inspector from this skill directory:

```bash
python3 scripts/inspect_pdf.py /path/to/input.pdf --pretty
python3 scripts/inspect_pdf.py /path/to/input.pdf --output /path/to/report.json --pretty
```

This default scan reads bytes without invoking a PDF parser. With `--output`, it refuses input aliases and non-regular destinations, then atomically creates or replaces the report via a sibling temporary file. Use `--deep` only after the file is trusted enough to parse, or after the untrusted-input sandbox profile in step 2 is verified. Declare the decision explicitly:

```bash
python3 scripts/inspect_pdf.py /path/to/input.pdf --deep --trust-level trusted --pretty
python3 scripts/inspect_pdf.py /path/to/untrusted.pdf --deep --sandbox-profile-confirmed --pretty
```

Treat JavaScript, launch actions, automatic actions, embedded files, and rich media as inert hazards; do not activate them.

### 2. Select an available toolchain

Inventory installed tools and libraries before choosing a method. Read [tool-routing.md](references/tool-routing.md) for capability-based routing and fallback behavior. Prefer a tool that preserves the required features; a text extractor is not a page editor, and rasterization is not a faithful editable conversion.

For an untrusted PDF, parse or render only in a disposable, low-privilege sandbox with no secrets or network access; a read-only source mount; isolated temporary/output storage; CPU, memory, process, file-size, page, and time limits; and no host viewer, shell, URL-handler, or clipboard integration. Configure the parser/renderer to disable JavaScript, OpenAction/additional/launch actions, form submission, external URI fetching, attachment extraction/opening, rich media, and automatic font/resource downloads. Verify these controls for the exact tool/version. If the available parser or renderer cannot satisfy the profile, stop after raw-byte inspection and report the capability gap.

If no suitable dependency exists, explain the missing capability and propose an installation or alternate workflow. Do not install software or upload the PDF without permission.

### 3. Establish a visual and content baseline

Open or render a trusted original with a trusted local viewer before any layout-sensitive change. For an untrusted original, use only the verified sandbox profile from step 2; if it is unavailable, stop without parsing/rendering. Inspect representative pages and every page that will change. Record page count, dimensions/orientation, searchable text availability, form fields, annotations, bookmarks, attachments, encryption, and obvious font or image issues.

For scanned pages, determine whether OCR is needed. Preserve the original image layer unless the user explicitly requests destructive cleanup.

### 4. Apply the smallest transformation

- **Extract:** preserve reading order uncertainty, page references, table structure, and OCR confidence. Do not invent missing text.
- **Merge/split/reorder/rotate:** make the page mapping explicit and retain bookmarks, labels, forms, and metadata when required.
- **Create/convert:** embed or substitute fonts deliberately; define page size, margins, links, headings, and accessibility expectations.
- **Fill/annotate:** distinguish annotations from flattened page content and preserve an editable copy if useful.
- **Redact:** use true object-level redaction, not a colored rectangle. Remove underlying text/images, relevant metadata, comments, attachments, and hidden layers as scoped. Save a fully rewritten new PDF with incremental saving disabled; do not retain prior revisions, original object streams, or appended historical bytes in the output.
- **Compress:** measure visual loss and text/searchability changes; avoid lossy rasterization unless authorized.
- **Encrypt/sign:** confirm algorithm, permissions, identity, and key handling. Any post-signature change can invalidate a signature.

Work on a temporary output, then move or copy it to the final requested path only after verification.

### 5. Verify structure and content

Follow [verification-checklist.md](references/verification-checklist.md). At minimum:

- Re-open the output with an independent reader or parser when available.
- Confirm magic bytes, EOF marker, page count/order, dimensions, encryption, and expected metadata.
- Compare extracted text or OCR page-by-page for content that should remain unchanged.
- Confirm form values, bookmarks, links, annotations, attachments, and signatures as applicable.
- For redaction, search extracted text and inspect page objects or a second parser; visual coverage alone is insufficient. Confirm the output was fully rewritten, contains no retained incremental revisions, and does not preserve the original bytes or redacted objects.

### 6. Render and inspect

Render every changed page and a representative sample of unchanged pages under the applicable trust/sandbox profile. Inspect at readable resolution for clipping, missing glyphs, shifted tables, broken images, blank pages, wrong rotation, and redaction leakage. For short or high-stakes documents, inspect every page. Open the final file in the user's intended viewer only when its trust classification and active-content controls permit it.

### 7. Deliver with evidence

Use [processing-record-template.md](assets/processing-record-template.md) for complex or regulated work. Report output paths, hashes, verification performed, failures, and untested behavior. Retain temporary artifacts only as long as needed and delete them only when authorized.

## Safety and permission boundaries

- Keep confidential PDFs local unless the user explicitly approves a specific service and data handling.
- Never execute embedded scripts, launch actions, macros, media, or attachments.
- Do not bypass passwords, access controls, digital rights, or signatures.
- Do not expose passwords, private keys, personal data, or document contents in logs.
- Treat true redaction, signature application, form submission, and publication as high-impact actions requiring explicit scope.
- Do not represent OCR as authoritative for legal, medical, financial, or identity data; require human verification.
- Do not claim PDF/A, PDF/UA, accessibility, evidentiary, or signature compliance without the relevant validator and evidence.

## Recovery

If processing fails, preserve the source and failed output separately, capture the exact command/tool/version and error, and retry from the unchanged original. If the output was distributed before a defect was found, identify affected versions and recipients but do not recall or replace files without authorization. For suspected redaction leakage or signature/key exposure, stop distribution and escalate immediately.

## Examples

### Extract a scanned contract

Request: “Extract this 38-page scanned contract into searchable text with page citations.”

Hash and render the original, OCR with the stated language, preserve the PDF image layer, spot-check names/numbers on every page, flag low-confidence passages, and deliver text with physical page references and an OCR limitation note.

### Merge a board packet

Request: “Combine these five PDFs in agenda order and add bookmarks.”

Confirm order and page mapping, merge to a new file, preserve orientation and page sizes, add bookmarks, re-open with a second reader, render boundary pages, and report final page count and hash.

### Redact customer identifiers

Request: “Remove account numbers before this PDF is shared publicly.”

Define the identifier pattern and all affected pages, apply true redaction to a copy, remove scoped metadata/comments/attachments, search and inspect with an independent parser, render every redacted page, and state that visual boxes alone were not used.

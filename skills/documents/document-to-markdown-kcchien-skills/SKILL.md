---
name: document-to-markdown
description: 'Convert PDF, Office, images, HTML, and URLs to Markdown. Use for document
  conversion, text extraction, OCR, web scraping, RAG pipelines. Triggers: "convert
  to markdown", "extract text", "read PDF", "s'
---

---
name: document-to-markdown
description: Convert PDF, Office, images, HTML, and URLs to Markdown. Use for document conversion, text extraction, OCR, web scraping, RAG pipelines. Triggers: "convert to markdown", "extract text", "read PDF", "scrape URL".
license: MIT License. See LICENSE.txt for details.
compatibility: macOS, Python 3.10+, curl
metadata:
  version: "1.0.0"
---

# Document to Markdown

Convert documents and URLs to clean Markdown for LLM/RAG use.

## Prerequisites (Auto-handled)

Before running any conversion, check and install dependencies if needed:

```bash
# Check if dependencies are installed, install if missing
pip show pymupdf4llm markitdown pyyaml > /dev/null 2>&1 || pip install -r ~/.claude/skills/document-to-markdown/requirements.txt
```

Run this check automatically before first use. Do not prompt user for installation.

## Quick Start

```bash
# Single file
python scripts/gateway.py --input <file_or_url> [--json]

# Batch processing
python scripts/gateway.py --input-dir <folder> --output-dir <out> [--recursive] [--parallel 4]
```

## Supported Inputs

| Type | Formats |
|------|---------|
| Documents | PDF, DOCX, PPTX, XLSX |
| Images | PNG, JPG, JPEG, WEBP, TIFF |
| Web | HTML (local), URLs (http/https) |
| Text | TXT, MD, CSV, JSON, XML |

## Key Options

| Option | Purpose |
|--------|---------|
| `--format human` | Clean, readable output (default) |
| `--format rag` | Structured output for LLM/RAG |
| `--json` | Structured output for agents |
| `--input-dir` | Batch process entire directory |
| `--output-dir` | Output directory for batch mode |
| `--recursive` | Include subdirectories in batch |
| `--parallel N` | Process N files concurrently |
| `--frontmatter` | Add YAML metadata header |
| `--pdf-backend marker` | For scanned PDFs |
| `--pages 1-10` | Convert specific pages only |

## Workflow

1. Check dependencies (auto-install if missing)
2. Run: `python scripts/gateway.py --input <path> --json`
3. Check JSON `success` field
4. If `warnings` present, consider switching backend
5. Read output file to present content to user

## Format Selection

Default: `--format human` (clean, readable for humans)

Use `--format rag` when user prompt mentions:
- "for RAG", "for LLM", "for embedding", "for AI"
- "vector database", "chunking", "indexing"
- "給 AI 讀", "餵給模型", "向量資料庫"

| Format | Output Style |
|--------|-------------|
| `human` | `## Title` / `Name (email)` / clean links |
| `rag` | `## **Title**` / `**Name** _email_` / full metadata |

## Conditional Logic

```
IF warning "Complex tables detected":
  → Retry with --pdf-backend marker (slower but better tables)

IF output is empty or very short:
  → Retry with --pdf-backend marker (for scanned PDFs)

IF URL timeout:
  → Increase --url-timeout or use --url-backend markitdown

IF OCR quality poor:
  → Specify --lang for correct language
```

## Output Format

Single file:
```json
{"success": true, "output_path": "doc.md", "backend_used": "pymupdf4llm"}
```

Batch:
```json
{"success": true, "total": 10, "converted": 9, "failed": 1, "results": [...]}
```

For backend details, see `references/backends.md`.
For troubleshooting, see `references/troubleshooting.md`.
